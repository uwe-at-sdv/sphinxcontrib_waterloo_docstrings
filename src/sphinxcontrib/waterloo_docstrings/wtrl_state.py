from __future__ import annotations
from typing import Any, List, cast

import importlib

from sphinxcontrib.waterloo_docstrings.wtrl_protocol import (
	InlinerProtocol,
	SphinxAppProtocol
	)
from sphinxcontrib.waterloo_docstrings.wtrl_parse import (
	parse_inline,
	)
from sphinxcontrib.waterloo_docstrings.wtrl_context import (
	context,
	make_context,
	_get_validated_doc_for_object
	)
from docutils import nodes
import sdv.doc.waterloo.docitem as mod_docitem
from sphinx.util import logging

logger = logging.getLogger(__name__)

#----- Globale variables --------------------------------------#
# These are fallback variables in case of testing from outside
# the Sphinx context. In normal usage the stacks are located
# in some appropriate place within Sphinx.
_global_current_module: List[str] = []
_global_current_class: List[str] = []
_global_current_scope: List[mod_docitem.Scope] = [mod_docitem.Scope.PUBLIC]

#----- Helpers ------------------------------------------------#
def _get_module_stack(env: Any | None) -> List[str]:
	attr = "_docitem_module_stack"
	if env is not None and hasattr(env, attr):
		return cast(List[str], getattr(env, attr))
	if env is not None and not hasattr(env, attr):
		setattr(env, attr, [])
		return cast(List[str], getattr(env, attr))
	return _global_current_module

def _get_class_stack(env: Any | None) -> List[str]:
	attr = "_docitem_class_stack"
	if env is not None and hasattr(env, attr):
		return cast(List[str], getattr(env, attr))
	if env is not None and not hasattr(env, attr):
		setattr(env, attr, [])
		return cast(List[str], getattr(env, attr))
	return _global_current_class

def _get_scope_stack(env: Any | None) -> List[mod_docitem.Scope]:
	attr = "_docitem_scope_stack"
	if env is not None and hasattr(env, attr):
		return cast(List[mod_docitem.Scope], getattr(env, attr))
	if env is not None and not hasattr(env, attr):
		setattr(env, attr, [mod_docitem.Scope.PUBLIC])
		return cast(List[mod_docitem.Scope], getattr(env, attr))
	return _global_current_scope

# Stack ops for current module
def push_current_module(qualified_module_name : str, env: Any | None = None) -> None:
	stack = _get_module_stack(env)
	stack.append(qualified_module_name)
def pop_current_module(env: Any | None = None) -> None:
	stack = _get_module_stack(env)
	del stack[-1]
def get_current_module(env: Any | None = None) -> str:
	return _get_module_stack(env)[-1]
def has_current_module(env: Any | None = None) -> bool:
	return len(_get_module_stack(env)) > 0

# Stack ops for current class
def push_current_class(qualified_class_name : str, env: Any | None = None) -> None:
	stack = _get_class_stack(env)
	stack.append(qualified_class_name)
def pop_current_class(env: Any | None = None) -> None:
	stack = _get_class_stack(env)
	del stack[-1]
def get_current_class(env: Any | None = None) -> str:
	return _get_class_stack(env)[-1]
def has_current_class(env: Any | None = None) -> bool:
	return len(_get_class_stack(env)) > 0

# Stack ops for current scope.
def push_current_scope(scope_tag : str, env: Any | None = None) -> None:
	if scope_tag not in mod_docitem.SCOPE_TAG_MAP:
		raise RuntimeError(f"Unknown scope '{scope_tag}'. Expected one of {list(mod_docitem.SCOPE_TAG_MAP.keys())}.")
	scope = mod_docitem.SCOPE_TAG_MAP[scope_tag]
	stack = _get_scope_stack(env)
	stack.append(scope)

def pop_current_scope(env: Any | None = None) -> None:
	stack = _get_scope_stack(env)
	if not stack:
		raise RuntimeError("Cannot pop current scope: stack is empty.")
	del stack[-1]

def get_current_scope(env: Any | None = None) -> mod_docitem.Scope:
	return _get_scope_stack(env)[-1]

def has_current_scope(env: Any | None = None) -> bool:
	return len(_get_scope_stack(env)) > 0

def get_current_scope_set(env: Any | None = None) -> mod_docitem.Scopes:
	"""
	Convert the current Sphinx rendering scope into a Waterloo scope set.

	The Sphinx layer currently maintains a single active scope on a stack,
	while the core visibility API expects a set of scopes. This helper
	provides the bridge for scope-aware rendering decisions.
	"""
	if not has_current_scope(env):
		return set([mod_docitem.Scope.PUBLIC])
	return set([get_current_scope(env)])

def is_target_obj_visible_in_current_scope(ctx: context, obj: object) -> bool:
	doc = _get_validated_doc_for_object(ctx, obj)
	if doc is None:
#		return False
# We must return True here. A target should not be greyed out
# just because of a missing docstring. It may remain unlinked
	# but it is not out of scope.
		return True
	return cast(bool, doc.is_visible(get_current_scope_set(ctx.env)))

def _make_context_admonition(inliner: InlinerProtocol, lineno: int, title: str, msg: str, classes: list[str]) -> nodes.admonition:
	node_adm = nodes.admonition(classes=["admonition", *classes])
	node_adm += nodes.title(text=title)
	node_par = nodes.paragraph()
	node_par.extend(parse_inline(inliner, node_par, lineno, msg))
	node_adm += node_par
	return node_adm

def wtrl_build_push_current_module_nodes(app: SphinxAppProtocol | Any, inliner: InlinerProtocol, lineno: int, qname: str) -> list[nodes.Node]:
	"""
	Preamble:
		profile:
			function
		normative_sections:
			Contract, Parameters, Returns, Raises, See_also
	Contract:
		general:
			|Must| push the qualified module name in |var|`text` to the module stack, which makes it the new current module.
			|Must| resolve |var|`qname`.
			|Must| build a list of Docutils nodes which represent a message about the changed state in the document.
			|May| write a log message to |file|`stdout`.
	Description:
		Implementation of directive |attr|`.. wtrl_push_current_module::`.
	Parameters:
		app:
			The Sphinx application instance that carries configuration and environment state.
		inliner:
			The Docutils inliner used to parse inline markup into nodes.
		lineno:
			Line number in the source document.
		qname:
			The qualified module name to push onto the stack.
	Returns:
		The list of generated |type|`docutils.nodes.Node` describing the resulting default module state.
	Raises:
		RuntimeError:
			|Must| raise if |var|`qname` does not resolve to a module.
		BaseException:
			|May| propagate exceptions from |func|`resolve_qualified_name`.
			|May| propagate exceptions from within Sphinx or Docutils.
	See_also:
		wtrl_build_pop_current_module_nodes,wtrl_build_push_current_class_nodes, wtrl_build_push_current_scope_nodes
	Notes:
		Last reviewed:
			2026-07-16
	"""
	ctx = make_context(app, lambda parent, ln, txt: parse_inline(inliner, parent, ln, txt), lineno)
	tr = ctx.tr
	with mod_docitem.traced_section(tr, qname):
		mod_obj, _, _, _ = resolve_qualified_name(ctx, qname)
		if not mod_docitem.is_obj_module(mod_obj):
			raise RuntimeError(f"{qname} does not resolve to a module.")
		if app.config and app.config.wtrl_verbose_state_change:
			logger.info(f"Waterloo: pushing current module '{qname}'")
		push_current_module(qname, env=ctx.env)
		msg = f"Classes and functions below this point implicitly belong to package/module {ctx.add_role_mod(qname)}. "
		if app.config.wtrl_verbose_state_change:
			return [_make_context_admonition(inliner, lineno, "Waterloo module context", msg, ["wtrl-current-module-message", "wtrl-current-module-push"])]
		else:
			return []

def wtrl_build_push_current_class_nodes(app: SphinxAppProtocol | Any, inliner: InlinerProtocol, lineno: int, qname: str) -> list[nodes.Node]:
	"""
	Preamble:
		profile:
			function
		normative_sections:
			Contract, Parameters, Returns, Raises, See_also
	Contract:
		general:
			|Must| push the qualified class name in |var|`text` to the class stack, which makes it the new current class.
			|Must| resolve |var|`qname`.
			|Must| build a list of Docutils nodes which represent a message about the changed state in the document.
			|May| write a log message to |file|`stdout`.
	Description:
		Implementation of directive |attr|`.. wtrl_push_current_class::`.
	Parameters:
		app:
			The Sphinx application instance that carries configuration and environment state.
		inliner:
			The Docutils inliner used to parse inline markup into nodes.
		lineno:
			Line number in the source document.
		qname:
			The qualified class name to push onto the stack.
	Returns:
		The list of generated |type|`docutils.nodes.Node` describing the resulting default module state.
	Raises:
		RuntimeError:
			|Must| raise if |var|`qname` does not resolve to a class.
		BaseException:
			|May| propagate exceptions from |func|`resolve_qualified_name`.
			|May| propagate exceptions from within Sphinx or Docutils.
	See_also:
		wtrl_build_pop_current_class_nodes, wtrl_build_push_current_module_nodes, wtrl_build_push_current_scope_nodes
	Notes:
		Last reviewed:
			2026-07-16
	"""
	ctx = make_context(app, lambda parent, ln, txt: parse_inline(inliner, parent, ln, txt), lineno)
	tr = ctx.tr
	with mod_docitem.traced_section(tr, qname):
		cls_obj, _, _, _ = resolve_qualified_name(ctx, qname)
		if not mod_docitem.is_obj_class(cls_obj):
			raise RuntimeError(f"{qname} does not resolve to a class.")
		if app.config and app.config.wtrl_verbose_state_change:
			logger.info(f"Waterloo: pushing current class '{qname}'")
		push_current_class(qname, env=ctx.env)
		msg = f"Methods below this point implicitly belong to class {ctx.add_role_class(qname)}."
		if app.config.wtrl_verbose_state_change:
			return [_make_context_admonition(inliner, lineno, "Waterloo class context", msg, ["wtrl-current-class-message", "wtrl-current-class-push"])]
		else:
			return []

def wtrl_build_push_current_scope_nodes(app: SphinxAppProtocol | Any, inliner: InlinerProtocol, lineno: int, scope_tag: str) -> list[nodes.Node]:
	"""
	Preamble:
		profile:
			function
		normative_sections:
			Contract, Parameters, Returns, Raises, See_also
	Contract:
		general:
			|Must| push the scope identifier in |var|`scope_tag` to the scope stack, which makes it the new current scope.
			|Must| build a list of Docutils nodes which represent a message about the changed state in the document.
			|May| write a log message to |file|`stdout`.
	Description:
		Implementation of directive |attr|`.. wtrl_push_current_scope::`.
	Parameters:
		app:
			The Sphinx application instance that carries configuration and environment state.
		inliner:
			The Docutils inliner used to parse inline markup into nodes.
		lineno:
			Line number in the source document.
		scope_tag:
			The scope identifier to push onto the stack.
	Returns:
		The list of generated |type|`docutils.nodes.Node` describing the resulting default scope state.
	Raises:
		RuntimeError:
			|Must| raise if |var|`scope_tag` is unknown.
		BaseException:
			|May| propagate exceptions from within Sphinx or Docutils.
	See_also:
		wtrl_build_pop_current_scope_nodes, wtrl_build_push_current_module_nodes, wtrl_build_push_current_class_nodes
	Notes:
		Last reviewed:
			2026-07-16
	"""
	ctx = make_context(app, lambda parent, ln, txt: parse_inline(inliner, parent, ln, txt), lineno)
	tr = ctx.tr
	with mod_docitem.traced_section(tr, scope_tag):
		if app.config and app.config.wtrl_verbose_state_change:
			logger.info(f"Waterloo: pushing current scope '{scope_tag}'")
		push_current_scope(scope_tag, env=ctx.env)
		msg = f"Scope below this point is set to {ctx.add_role_var(scope_tag)}."
		if app.config.wtrl_verbose_state_change:
			return [_make_context_admonition(inliner, lineno, "Waterloo scope context", msg, ["wtrl-current-scope-message", "wtrl-current-scope-push"])]
		else:
			return []

def wtrl_build_pop_current_module_nodes(app: SphinxAppProtocol | Any, inliner: InlinerProtocol, lineno: int, qname: str) -> list[nodes.Node]:
	"""
	Preamble:
		profile:
			function
		normative_sections:
			Contract, Parameters, Returns, Raises, See_also
	Contract:
		general:
			|Must| compare the qualified module name in |var|`qname` to the top of the module stack and raise an exception in case of mismatch.
			|Must| resolve |var|`qname` against the current module/class context.
			|Must| pop one element from the module stack.
			|Must| build a list of Docutils nodes which represent a message about the changed state in the document.
			|May| write a log message to |file|`stdout`.
	Description:
		Implementation of directive |attr|`.. wtrl_pop_current_module::`.
	Parameters:
		app:
			The Sphinx application instance that carries configuration and environment state.
		inliner:
			The Docutils inliner used to parse inline markup into nodes.
		lineno:
			Line number in the source document.
		qname:
			The qualified module name to compare and pop from the stack.
	Returns:
		The list of generated |type|`docutils.nodes.Node` describing the resulting default module state.
	Raises:
		RuntimeError:
			|Must| raise on the attempt to access an element from an empty stack.
			|Must| raise if the qualified name on top of the stack does not match |var|`qname`.
			|Must| raise if |var|`qname` does not resolve to a module.
		BaseException:
			|May| propagate exceptions from |func|`resolve_qualified_name`.
			|May| propagate exceptions from within Sphinx or Docutils.
	See_also:
		wtrl_build_push_current_module_nodes, wtrl_build_pop_current_class_nodes, wtrl_build_pop_current_scope_nodes
	Notes:
		Last reviewed:
			2026-07-16
	"""
	ctx = make_context(app, lambda parent, ln, txt: parse_inline(inliner, parent, ln, txt), lineno)
	tr = ctx.tr
	with mod_docitem.traced_section(tr, qname):
		mod_obj, _, _, _ = resolve_qualified_name(ctx, qname)
		if not mod_docitem.is_obj_module(mod_obj):
			raise RuntimeError(f"{qname} does not resolve to a module.")
		text_top = get_current_module(ctx.env)
		if text_top != qname:
			raise RuntimeError(f"module stack push/pop mismatch, expected {text_top} got {qname}.")
		if app.config and app.config.wtrl_verbose_state_change:
			logger.info(f"Waterloo: popping current module '{qname}'")
		pop_current_module(ctx.env)
		if has_current_module(ctx.env):
			new_top = get_current_module(ctx.env)
			msg = f"Default module qualifier {ctx.add_role_mod(text_top)} ends here. New default: {ctx.add_role_mod(new_top)}. "
		else:
			msg = f"Default module qualifier {ctx.add_role_mod(text_top)} ends here. No default module active. "
		if app.config.wtrl_verbose_state_change:
			return [_make_context_admonition(inliner, lineno, "Waterloo module context", msg, ["wtrl-current-module-message", "wtrl-current-module-pop"])]
		else:
			return []

def wtrl_build_pop_current_class_nodes(app: SphinxAppProtocol | Any, inliner: InlinerProtocol, lineno: int, qname: str) -> list[nodes.Node]:
	"""
	Preamble:
		profile:
			function
		normative_sections:
			Contract, Parameters, Returns, Raises, See_also
	Contract:
		general:
			|Must| compare the qualified class name in |var|`qname` to the top of the class stack and raise an exception in case of mismatch.
			|Must| resolve |var|`qname` against the current module/class context.
			|Must| pop one element from the class stack.
			|Must| build a list of Docutils nodes which represent a message about the changed state in the document.
			|May| write a log message to |file|`stdout`.
	Description:
		Implementation of directive |attr|`.. wtrl_pop_current_class::`.
	Parameters:
		app:
			The Sphinx application instance that carries configuration and environment state.
		inliner:
			The Docutils inliner used to parse inline markup into nodes.
		lineno:
			Line number in the source document.
		qname:
			The qualified class name to compare and pop from the stack.
	Returns:
		The list of generated |type|`docutils.nodes.Node` describing the resulting default class state.
	Raises:
		RuntimeError:
			|Must| raise on the attempt to access an element from an empty stack.
			|Must| raise if the qualified name on top of the stack does not match |var|`qname`.
			|Must| raise if |var|`qname` does not resolve to a class.
		BaseException:
			|May| propagate exceptions from |func|`resolve_qualified_name`.
			|May| propagate exceptions from within Sphinx or Docutils.
	See_also:
		wtrl_build_push_current_class_nodes, wtrl_build_pop_current_module_nodes, wtrl_build_pop_current_scope_nodes
	Notes:
		Last reviewed:
			2026-07-16
	"""
	ctx = make_context(app, lambda parent, ln, txt: parse_inline(inliner, parent, ln, txt), lineno)
	tr = ctx.tr
	with mod_docitem.traced_section(tr, qname):
		cls_obj, _, _, _ = resolve_qualified_name(ctx, qname)
		if not mod_docitem.is_obj_class(cls_obj):
			raise RuntimeError(f"{qname} does not resolve to a class.")
		text_top = get_current_class(ctx.env)
		if text_top != qname:
			raise RuntimeError(f"class stack push/pop mismatch, expected {text_top} got {qname}.")
		if app.config and app.config.wtrl_verbose_state_change:
			logger.info(f"Waterloo: popping current class '{qname}'")
		pop_current_class(ctx.env)
		if has_current_class(ctx.env):
			new_top = get_current_class(ctx.env)
			msg = f"Default class qualifier {ctx.add_role_var(text_top)} ends here. New default: {ctx.add_role_class(new_top)}. "
		else:
			msg = f"Default class qualifier {ctx.add_role_var(text_top)} ends here. No default class active. "
		if app.config.wtrl_verbose_state_change:
			return [_make_context_admonition(inliner, lineno, "Waterloo class context", msg, ["wtrl-current-class-message", "wtrl-current-class-pop"])]
		else:
			return []

def wtrl_build_pop_current_scope_nodes(app: SphinxAppProtocol | Any, inliner: InlinerProtocol, lineno: int, scope_tag: str) -> list[nodes.Node]:
	"""
	Preamble:
		profile:
			function
		normative_sections:
			Contract, Parameters, Returns, Raises, See_also
	Contract:
		general:
			|Must| compare the scope identifier name in |var|`qname` to the top of the scope stack and raise an exception in case of mismatch.
			|Must| pop one element from the scope stack.
			|Must| build a list of Docutils nodes which represent a message about the changed state in the document.
			|May| write a log message to |file|`stdout`.
	Description:
		Implementation of directive |attr|`.. wtrl_pop_current_scope::`.
	Parameters:
		app:
			The Sphinx application instance that carries configuration and environment state.
		inliner:
			The Docutils inliner used to parse inline markup into nodes.
		lineno:
			Line number in the source document.
		scope_tag:
			The scope identifier to compare and pop from the stack.
	Returns:
		The list of generated |type|`docutils.nodes.Node` describing the resulting default scope state.
	Raises:
		RuntimeError:
			|Must| raise on the attempt to access an element from an empty stack.
			|Must| raise if the scope identifier on top of the stack does not match |var|`scope_tag`.
			|Must| raise if |var|`scope_tag` is unknown or mismatches the stack top.
		BaseException:
			|May| propagate exceptions from within Sphinx or Docutils.
	Notes:
		Last reviewed:
			2026-07-16
	See_also:
		wtrl_build_push_current_scope_nodes, wtrl_build_pop_current_module_nodes, wtrl_build_pop_current_class_nodes
	"""
	ctx = make_context(app, lambda parent, ln, txt: parse_inline(inliner,parent,ln,txt), lineno)
	tr = ctx.tr
	with mod_docitem.traced_section(tr, scope_tag):
		if not has_current_scope(ctx.env):
			raise RuntimeError("Cannot pop current scope: stack is empty.")
		text_top_scope = get_current_scope(ctx.env)
		if scope_tag not in mod_docitem.SCOPE_TAG_MAP:
			raise RuntimeError(f"Unknown scope '{scope_tag}'. Expected one of {list(mod_docitem.SCOPE_TAG_MAP.keys())}.")
		if text_top_scope !=  mod_docitem.SCOPE_TAG_MAP[scope_tag]:
			raise RuntimeError(f"scope stack push/pop mismatch, expected {text_top_scope} got {scope_tag}.")
		if app.config and app.config.wtrl_verbose_state_change:
			logger.info(f"Waterloo: popping current scope '{scope_tag}'")
		pop_current_scope(env=ctx.env)
		if has_current_scope(ctx.env):
			new_scope = get_current_scope(ctx.env)
			msg = f"Scope qualifier {ctx.add_role_var(scope_tag)} ends here. New current scope: {ctx.add_role_var(mod_docitem.Scope(new_scope).name.lower())}. "
		else:
			msg = f"Scope qualifier {ctx.add_role_var(scope_tag)} ends here. No current scope active. "
		if app.config.wtrl_verbose_state_change:
			return [_make_context_admonition(inliner, lineno, "Waterloo scope context", msg, ["wtrl-current-scope-message", "wtrl-current-scope-pop"])]
		else:
			return []

def resolve_qualified_name(ctx: context | None, qname: str) -> tuple[object, str, str, list[str]]:
	"""
	Preamble:
		profile:
			function
		normative_sections:
			Contract, Parameters, Returns, Raises
	Contract:
		general:
			|Must| resolve the qualified name |var|`qname` using current module/class context in |var|`ctx` when present.
			|Must| try to import the resolved object as criterion that resolution succeeded (see section |label|`Raises`)
			|Must| try fully qualified forms in this order: current module + current class + |var|`qname`, current module + |var|`qname`, then |var|`qname` as given.
	Parameters:
		ctx:
			The context which provides current module and current class.
		qname:
			The qualified name to resolve.
	Returns:
		|Must| return a tuple |type|`(obj, module_name, head_name, tail_parts)` where
		|var|`obj` is the resolved object, |var|`module_name` is the imported module name,
		|var|`head_name` is the last attribute component, and |var|`tail_parts`
		is the attribute chain after the module components.
	Raises:
		ImportError:
			|Must| raise if the module of the qualified name cannot be resolved.
		ValueError:
			|Must| raise if no attribute is specified after a resolved module name.
		BaseException:
			|Must| propagate exceptions from the module import.
	"""
	env = ctx.env if ctx is not None else None
	def _resolve_absolute(abs_qname: str) -> tuple[object, str, str, list[str]]:
		parts = abs_qname.split(".")
		mod = None
		modname = None
		split_at = None
		for i in range(len(parts), 0, -1):
			cand = ".".join(parts[:i])
			try:
				mod = importlib.import_module(cand)
				modname = cand
				split_at = i
				break
			except ImportError:
				continue
		if mod is None:
			raise ImportError(f"Could not import any module prefix from: {abs_qname} (2)")
		tail = parts[split_at:]
		if not tail:
			head_name = parts[-1]
			assert modname is not None
			return mod, modname, head_name, []
		obj = mod
		for p in tail:
			try:
				obj = getattr(obj, p)
			except AttributeError as exc:
				raise ImportError(f"{cand} has no attribute {p}") from exc
		head_name = tail[-1]
		assert modname is not None
		return obj, modname, head_name, tail

	candidates = []
	cur_mod = get_current_module(env) if has_current_module(env) else None
	cur_cls = get_current_class(env) if has_current_class(env) else None
	if cur_mod and cur_cls:
		candidates.append(f"{cur_mod}.{cur_cls}.{qname}")
	if cur_mod:
		candidates.append(f"{cur_mod}.{qname}")
	candidates.append(qname)
	seen = set()
	for cand in candidates:
		if cand in seen:
			continue
		seen.add(cand)
		try:
			return _resolve_absolute(cand)
		except ImportError:
			continue
	raise ImportError(f"Could not resolve qualified name '{qname}' with module/class context {cur_mod}/{cur_cls}.")
