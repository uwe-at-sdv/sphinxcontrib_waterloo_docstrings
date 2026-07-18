from __future__ import annotations
from typing import Any, Callable, List, cast

from sphinxcontrib.waterloo_docstrings.wtrl_protocol import (
	InlinerProtocol,
	SphinxAppProtocol
	)
from sphinxcontrib.waterloo_docstrings.wtrl_parse import (
	parse_inline
	)
from sphinxcontrib.waterloo_docstrings.wtrl_context import (
	context,
	make_context
	)
from sphinxcontrib.waterloo_docstrings.wtrl_state import (
	resolve_qualified_name
	)

import inspect,re
from docutils import nodes
import sdv.doc.waterloo.docitem as mod_docitem

def _signature_for(obj: object) -> inspect.Signature:
	return inspect.signature(cast(Callable[..., Any], obj))

def _maybe_drop_first_param(sig: inspect.Signature, *, drop: bool) -> inspect.Signature:
	if not drop:
		return sig
	params = list(sig.parameters.values())
	if not params:
		return sig
	first = params[0]
	if first.name in {"self", "cls", "mcls"}:
		return inspect.Signature(parameters=params[1:], return_annotation=sig.return_annotation)
	return sig

def format_type(tp: object) -> str:
	if tp is inspect._empty:
		return "Any"
	if isinstance(tp, type):
		return tp.__name__
	return str(tp)

def format_default(val: object) -> str:
	if val is inspect._empty:
		return ""
	return repr(val)

def render_head_of_callable(ctx: context, obj: object, display_scope: bool = True) -> List[nodes.line]:
	lines: List[nodes.line] = []
	objname = mod_docitem.get_obj_name(obj)
	objname_segments = objname.split(".")
# detect decorators
	decorator_lines = mod_docitem.get_obj_decorators(obj)
# detect async
	coroutine_marker = ""
	if inspect.iscoroutinefunction(obj) or inspect.isasyncgenfunction(obj):
		coroutine_marker = "async "
# find module
	mod = obj.__module__
# decorator
	decorator = nodes.line(classes=["wtrl-signature-decorator"])
	if decorator_lines:
		for decorator_line in decorator_lines:
			node_deco = nodes.line()
			node_deco += _tkn(ctx.add_role_attr, decorator_line)
			decorator.append(node_deco)
		lines.append(decorator)
# Header: Coroutine marker, module, class hierarchy and function name.
	header = nodes.line(classes=["wtrl-signature-head"])
# coroutine
	if coroutine_marker:
		header += _tkn(ctx.add_role_attr, coroutine_marker)
	if display_scope:
# module name
		header += _tkn(ctx.add_role_mod, mod_docitem.get_obj_name(mod))
		header += _tkn(ctx.add_role_op, ".")
# qualified function name: class segments
	for i_seg in range(len(objname_segments) - 1):
# Class and nested classes
		header += _tkn(ctx.add_role_type, objname_segments[i_seg])
		header += _tkn(ctx.add_role_op, ".")
# Unqualified function name.
	header += _tkn(ctx.add_role_func, objname_segments[-1])
	header += _tkn(ctx.add_role_op, "(")
	lines.append(header)
	return lines

def render_params_and_return_of_callable(ctx: context, obj: object,drop_self: bool = True) -> List[nodes.line]:
	lines: List[nodes.line] = []
	sig = _signature_for(obj)
	sig = _maybe_drop_first_param(sig, drop=drop_self)

# parameter lines
	for pname, p in sig.parameters.items():
# Important: build a style in order to shape indentation for parameters.
		line = nodes.line(classes=["wtrl-signature-param"])

		if p.kind == inspect.Parameter.VAR_POSITIONAL:
			line += _tkn(ctx.add_role_op, "*")
		elif p.kind == inspect.Parameter.VAR_KEYWORD:
			line += _tkn(ctx.add_role_op, "**")

		line += _tkn(ctx.add_role_var, pname)

		ann = format_type(p.annotation)
# Decomment in order to suppress ": Any" for unannotaated code.
# Better: use Annotations!
#		if ann != "Any":
		if 1:
			line += _tkn(ctx.add_role_op, ": ")
			line += _tkn(ctx.add_role_type, ann)

		dflt = format_default(p.default)
		if dflt:
			line += _tkn(ctx.add_role_op, " = ")
			line += _tkn(ctx.add_role_lit, dflt)

		lines.append(line)

 # closing line with return annotation
	closing = nodes.line(classes=["wtrl-signature-ret"])
	closing += _tkn(ctx.add_role_op, ")")
	closing += _tkn(ctx.add_role_op, " -> ")
	closing += _tkn(ctx.add_role_type, format_type(sig.return_annotation))
	lines.append(closing)
	return lines

def render_signature_tokens_inline(ctx: context, func_qname: str, *, drop_self: bool = True, display_scope: bool = False) -> List[nodes.Node]:
	obj, modname, head_name, tail = resolve_qualified_name(ctx, func_qname)

	display_mod = ".".join([modname] + tail[:-1])
	display_name = head_name

# detect decorators
	decorator_lines = mod_docitem.get_obj_decorators(obj)
# detect async
	coroutine_marker = ""
	if inspect.iscoroutinefunction(obj) or inspect.isasyncgenfunction(obj):
		coroutine_marker = "async "

	sig = _signature_for(obj)
	sig = _maybe_drop_first_param(sig, drop=drop_self)

	def _tkn(role_fn: Callable[[str], str], text: str) -> List[nodes.Node]:
		markup = role_fn(text)
		m = re.match(r":([A-Za-z0-9_]+):`(.+)`", markup)
		if m:
			role_name, body = m.group(1), m.group(2)
			return [nodes.inline(body, body, classes=[role_name])]
		return [nodes.inline(markup, markup)]

	tokens: List[nodes.Node] = []

# decorators - does not look good in practice because it's inline.
# Better use the block representation.
	if decorator_lines:
		for decorator_line in decorator_lines:
			tokens.extend(_tkn(ctx.add_role_attr, decorator_line + " "))
# coroutine
	if coroutine_marker:
		tokens.extend(_tkn(ctx.add_role_attr, coroutine_marker))

	if display_scope:
		tokens.extend(_tkn(ctx.add_role_func, display_mod))
		tokens.extend(_tkn(ctx.add_role_op, "."))
	tokens.extend(_tkn(ctx.add_role_func, display_name))
	tokens.extend(_tkn(ctx.add_role_op, "("))

	first = True
	for pname, p in sig.parameters.items():
		if not first:
			tokens.extend(_tkn(ctx.add_role_op, ", "))
		first = False

		if p.kind == inspect.Parameter.VAR_POSITIONAL:
			tokens.extend(_tkn(ctx.add_role_op, "*"))
		elif p.kind == inspect.Parameter.VAR_KEYWORD:
			tokens.extend(_tkn(ctx.add_role_op, "**"))

		tokens.extend(_tkn(ctx.add_role_var, pname))

		ann = format_type(p.annotation)
		if ann != "Any":
			tokens.extend(_tkn(ctx.add_role_op, ": "))
			tokens.extend(_tkn(ctx.add_role_type, ann))

		dflt = format_default(p.default)
		if dflt:
			tokens.extend(_tkn(ctx.add_role_op, " = "))
			tokens.extend(_tkn(ctx.add_role_lit, dflt))

	tokens.extend(_tkn(ctx.add_role_op, ")"))
	tokens.extend(_tkn(ctx.add_role_op, " -> "))
	tokens.extend(_tkn(ctx.add_role_type, format_type(sig.return_annotation)))
	return tokens

def _tkn(role_fn: Callable[[str], str], text: str) -> List[nodes.Node]:
	markup = role_fn(text)
	m = re.match(r":([A-Za-z0-9_]+):`(.+)`", markup)
	if m:
		role_name, body = m.group(1), m.group(2)
		return [nodes.inline(body, body, classes=[role_name])]
	return [nodes.inline(markup, markup)]

# Multiline variant: one parameter per line, hanging indent.
def render_signature_tokens_multiline(ctx: context, func_qname: str, *, drop_self: bool = True, display_scope: bool = True) -> List[nodes.Node]:
	obj, modname, head_name, tail = resolve_qualified_name(ctx, func_qname)

	display_mod = ".".join([modname] + tail[:-1])
	display_name = head_name

# detect decorators
	decorator_lines = mod_docitem.get_obj_decorators(obj)

# detect async
	coroutine_marker = ""
	if inspect.iscoroutinefunction(obj) or inspect.isasyncgenfunction(obj):
		coroutine_marker = "async "

	lines: List[nodes.line] = []
	# header line
	header = nodes.line(classes=["wtrl-signature-head"])
# decorator
	decorator = nodes.line(classes=["wtrl-signature-decorator"])
	if decorator_lines:
		for decorator_line in decorator_lines:
			node_deco = nodes.line()
			node_deco += _tkn(ctx.add_role_attr, decorator_line)
			decorator.append(node_deco)
# coroutine
	if coroutine_marker:
		header += _tkn(ctx.add_role_attr, coroutine_marker)
# [qualified] function name
	if display_scope:
		header += _tkn(ctx.add_role_func, display_mod)
		header += _tkn(ctx.add_role_op, ".")
	header += _tkn(ctx.add_role_func, display_name)
	header += _tkn(ctx.add_role_op, "(")

# Prepend decorators if there are any, one per line as in the source code.
	if(decorator_lines):
		lines.append(decorator)

	lines.append(header)

	lines += render_params_and_return_of_callable(ctx,obj,drop_self)
	
	# Wrap in a line_block so that Docutils renders each line separately
	line_block = nodes.line_block(classes=["wtrl-signature", "wtrl-signature-multiline"])
	for ln in lines:
		line_block += ln
	return [line_block]

def wtrl_build_method_signature_nodes(app: SphinxAppProtocol | Any, inliner: InlinerProtocol, lineno: int, qname: str) -> list[nodes.Node]:
	"""
Preamble:
	profile:
		function
	normative_sections:
		Contract, Parameters, Returns, Raises, See_also
	scope:
		core
Contract:
	general:
		|Must| create a list of |type|`docutil`-nodes representing the method signature as inline text.
Parameters:
	app:
		The Sphinx application instance that carries configuration and environment state.
	inliner:
		The Docutils inliner used to parse inline markup into nodes.
	lineno:
		Line number in the source document.
	qname:
		Qualified name of method to render.
Returns:
	The list of generated |type|`docutils.nodes.Node` describing the method signature.
Raises:
	BaseException:
		|May| propagate exceptions from |type|`docutils`.
See_also:
	wtrl_build_function_signature_nodes, wtrl_build_method_signature_block_nodes
Notes:
	Last reviewed:
		2026-07-16
	"""
	ctx = make_context(app, lambda parent, ln, txt: parse_inline(inliner, parent, ln, txt), lineno)
	return render_signature_tokens_inline(ctx, qname)

def wtrl_build_function_signature_nodes(app: SphinxAppProtocol | Any, inliner: InlinerProtocol, lineno: int, qname: str) -> list[nodes.Node]:
	"""
Preamble:
	profile:
		function
	normative_sections:
		Contract, Parameters, Returns, Raises, See_also
	scope:
		core
Contract:
	general:
		|Must| create a list of |type|`docutil`-nodes representing the function signature as inline text.
Parameters:
	app:
		The Sphinx application instance that carries configuration and environment state.
	inliner:
		The Docutils inliner used to parse inline markup into nodes.
	lineno:
		Line number in the source document.
	qname:
		Qualified name of function to render.
Returns:
	The list of generated |type|`docutils.nodes.Node` describing the function signature.
Raises:
	BaseException:
		|May| propagate exceptions from |type|`docutils`.
See_also:
	wtrl_build_method_signature_nodes, wtrl_build_function_signature_block_nodes
Notes:
	Last reviewed:
		2026-07-16
	"""
	ctx = make_context(app, lambda parent, ln, txt: parse_inline(inliner, parent, ln, txt), lineno)
	return render_signature_tokens_inline(ctx, qname, drop_self=False)

def wtrl_build_method_signature_block_nodes(app: SphinxAppProtocol | Any, inliner: InlinerProtocol, lineno: int, qname: str) -> list[nodes.Node]:
	"""
Preamble:
	profile:
		function
	normative_sections:
		Contract, Parameters, Returns, Raises, See_also
	scope:
		core
Contract:
	general:
		|Must| create a list of |type|`docutil`-nodes representing the method signature as paragraph with one parameter per line.
Parameters:
	app:
		The Sphinx application instance that carries configuration and environment state.
	inliner:
		The Docutils inliner used to parse inline markup into nodes.
	lineno:
		Line number in the source document.
	qname:
		Qualified name of method to render.
Returns:
	The list of generated |type|`docutils.nodes.Node` describing the method signature.
Raises:
	BaseException:
		|May| propagate exceptions from |type|`docutils`.
See_also:
	wtrl_build_method_signature_nodes, wtrl_build_function_signature_block_nodes
Notes:
	Last reviewed:
		2026-07-16
	"""
	ctx = make_context(app, lambda parent, ln, txt: parse_inline(inliner, parent, ln, txt), lineno)
	return render_signature_tokens_multiline(ctx, qname)

def wtrl_build_function_signature_block_nodes(app: SphinxAppProtocol | Any, inliner: InlinerProtocol, lineno: int, qname: str) -> list[nodes.Node]:
	"""
Preamble:
	profile:
		function
	normative_sections:
		Contract, Parameters, Returns, Raises, See_also
	scope:
		core
Contract:
	general:
		|Must| create a list of |type|`docutil`-nodes representing the function signature as paragraph with one parameter per line.
Parameters:
	app:
		The Sphinx application instance that carries configuration and environment state.
	inliner:
		The Docutils inliner used to parse inline markup into nodes.
	lineno:
		Line number in the source document.
	qname:
		Qualified name of function to render.
Returns:
	The list of generated |type|`docutils.nodes.Node` describing the function signature.
Raises:
	BaseException:
		|May| propagate exceptions from |type|`docutils`.
See_also:
	wtrl_build_method_signature_block_nodes, wtrl_build_function_signature_nodes
Notes:
	Last reviewed:
		2026-07-16
	"""
	ctx = make_context(app, lambda parent, ln, txt: parse_inline(inliner, parent, ln, txt), lineno)
	return render_signature_tokens_multiline(ctx, qname, drop_self=False)
