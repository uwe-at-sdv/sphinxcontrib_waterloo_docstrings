from __future__ import annotations
from typing import Any, Callable, List, cast

from sphinxcontrib.waterloo_docstrings.wtrl_protocol import (
	SphinxAppProtocol
	)

import importlib
from docutils import nodes
import sdv.doc.waterloo.docitem as mod_docitem

from sphinxcontrib.waterloo_docstrings.wtrl_roles import (
	context_roles
	)

def import_by_path(path: str) -> Any:
	if "." in path:
		mod, _, attr = path.rpartition(".")
	else:
		mod, attr = "conf", path
	return getattr(importlib.import_module(mod), attr)

# Not in use
def build_prolog_method_overview(ctx: context,class_name : str) -> List[nodes.Node]:
	return [cast(nodes.Node,nodes.rubric(text="Public methods of class :wtrl_type:`" + class_name + "`"))]

def build_prolog_method_block(ctx: context,parent : nodes.Element | None,class_obj: type[object],meth_obj : Callable[..., Any]) -> List[nodes.Node]:
# Render the signature directly (multiline variant) instead of parsing a directive string.
# Use fully-qualified name so resolution works even for nested classes.
#	qname = mod_docitem.get_obj_fully_qualified_name(meth_obj)
#	return render_signature_tokens_multiline(ctx, qname, drop_self=True, display_scope=True)
	return []

class context(context_roles):
	"""
	Preamble:
		profile:
			class
		normative_sections:
			Contract, Factory, Public_methods
		scope:
			extension
	Contract:
		general:
			|Must| provide the shared rendering state used by Waterloo Sphinx node builders.
			|Must| store the Docutils/Sphinx inline parser callback used to turn resolved Waterloo markup into nodes.
			|Must| store the source line number used for diagnostics and inline parsing.
			|Must| provide slots for the active Sphinx environment and configuration object.
			|Must| provide a cache for validated Waterloo docstrings used by scope-aware link rendering.
			|Must| provide a tracer for diagnostics emitted while resolving or rendering Waterloo content.
			|Must| provide configurable prolog hook callables for method overview and method block rendering.
			|Must| provide access to Waterloo role helper functions through |class|`context_roles`.
			|Must| provide a method for applying hook configuration from a simple dictionary.
		constructor:
			|Must| accept a callable for parsing inline text into a list of |class|`nodes.Node` objects.
			|Must| accept a line number for error reporting.
			|Must| initialize |attr|`env` and |attr|`config` as unset placeholders.
			|Must| initialize default prolog hook callables.
			|Must| initialize an empty validated-docstring cache and a fresh tracer.
	Factory:
		make_context:
			|Must| create a |class|`context` instance from a Sphinx application object, an inline parser callable, and a line number.
	Public_methods:
		__init__
	Notes:
		Context population:
			Call |func|`make_context` instead of instantiating this class directly when Sphinx environment and configuration access are needed.
		Last reviewed:
			2026-07-23
		Todo:
			Methods like |func|`build_prolog_method_overview` and |func|`build_prolog_method_block` need to be reviewed.
	"""
	def __init__(self,parse_inline : Callable[[nodes.Element, int, str], List[nodes.Node]],lineno: int) -> None:
		r"""
		Preamble:
			profile:
				method
			normative_sections:
				Contract, Parameters, Returns, Raises
			scope:
				extension
		Contract:
			general:
				|Must| initialize the context with the given inline parser and line number.
				|Must| initialize the Sphinx environment |var|`env` and configuration |var|`config` placeholders as unset.
				|Must| initialize the validated-docstring cache |var|`wtrl_validated_doc_cache` and tracer |var|`tr`.
		Parameters:
			parse_inline:
				A callable that takes a |class|`nodes.Element` parent, an integer line number, and a string of inline text, and returns a list of |class|`nodes.Node` objects.
			lineno:
				An integer line number within the source file.
		Returns:
			|None|
		Raises:
		"""
		super().__init__()
		self.parse = parse_inline
		self.i_line = lineno
# See make_context. We extract env and config from the SphinxApp instance.
		self.env: Any = None
		self.config: Any = None
		self.wtrl_validated_doc_cache: dict[int, mod_docitem.docitem_docstring_base | None] = {}


		self.build_prolog_method_overview : Callable[[context,str],List[nodes.Node]] = build_prolog_method_overview
		self.build_prolog_method_block : Callable[[context,nodes.Element | None,type[object],Callable[...,Any]],List[nodes.Node]] = build_prolog_method_block
		self.tr = mod_docitem.tracer()

	def set_build_prolog_method_overview(self,c : Callable[[context,str],List[nodes.Node]]) -> None:
		self.build_prolog_method_overview = c
	def set_build_prolog_method_block(self,c : Callable[[context,nodes.Element | None,object,object],List[nodes.Node]]) -> None:
		self.build_prolog_method_block = c
	def apply_config(self, cfg: dict[str,str]) -> None:
		if "prolog_method_overview" in cfg:
			self.set_build_prolog_method_overview(import_by_path(cfg["prolog_method_overview"]))
		if "prolog_method_block" in cfg:
			self.set_build_prolog_method_block(import_by_path(cfg["prolog_method_block"]))

def make_context(app: SphinxAppProtocol | Any, parse_inline: Callable[[nodes.Element, int, str], List[nodes.Node]], lineno: int) -> context:
	r"""
	Preamble:
		profile:
			function
		normative_sections:
			Contract, Parameters, Returns, Raises
		scope:
			extension
	Contract:
		general:
			|Must| create a |class|`context` instance from a Sphinx application object, an inline parser callable, and a line number.
			|Must| extract the Sphinx environment and configuration from the application object and store them in the context.
			|Must| look for a |var|`docitem_context_configurator` dictionary in the application object or the Sphinx environment.
			|Must| apply the configurator to the context if it is found.
	Parameters:
		app:
			A Sphinx application object.
		parse_inline:
			A callable that takes a |class|`nodes.Element` parent, an integer line number, and a string of inline text, and returns a list of |class|`nodes.Node` objects.
		lineno:
			An integer line number within the source file.
	Returns:
		A |class|`context` instance with the Sphinx environment, configuration, and optional configurator applied.
	Raises:
	Notes:
		Last reviewed:
			2026-07-23
		Purpose:
			This factory function provides a convenient way to create a fully initialized
			rendering context with Sphinx environment and configuration details extracted
			from the application object. It also searches for and applies optional context
			configurators, allowing extensible customization of rendering behavior without
			modifying the context initialization logic directly.
			|
			Called whenever rendering content into the final document (e.g., HTML) at a
			specific source location (|var|`lineno`).
	"""
	ctx = context(parse_inline, lineno)
	ctx.env = getattr(app, "env", None)
	ctx.config = getattr(app, "config", None)
	configurator = getattr(app, "docitem_context_configurator", None)
	if configurator is None:
		configurator = getattr(app.env, "docitem_context_configurator", None)
	if configurator:
		assert isinstance(configurator, dict)
		ctx.apply_config(configurator)
	return ctx

# Not sure if this function should be here. Pro:
# Is tightly connected to the cache managed by the context.
# Required by wtrl_state.py.
def _get_validated_doc_for_object(
	ctx: context,
	obj: object,
) -> mod_docitem.docitem_docstring_base | None:
	"""
	Best-effort lookup of a validated Waterloo docstring tree for an object.

	Link rendering uses this to decide whether a resolved Waterloo object is
	visible under the current Sphinx scope. Failures are treated as
	non-linkable targets and handled by the caller via plain text fallback.
	"""
	cache = ctx.wtrl_validated_doc_cache
	key = id(obj)
	if key in cache:
		cached = cache[key]
		return cached if isinstance(cached, mod_docitem.docitem_docstring_base) else None
	obj_doc = mod_docitem.get_obj_docstring(obj)
	if not isinstance(obj_doc, str) or not obj_doc.strip():
# Objects without a Waterloo docstring cannot contribute scope metadata.
# We treat them as scope-agnostic, so that documented constants and
# similar values remain linkable without spurious warnings.
		cache[key] = None
		return None
	try:
		doc = mod_docitem.validate_docstring(ctx.tr, obj,top=None, session=mod_docitem.DocSession())
	except Exception:
		cache[key] = None
		return None
	cache[key] = doc
	return doc

