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
			Contract
	Contract:
		general:
			|Must| be able to hold data from both the Sphinx environment and the user-defined configuration in |file|`conf.py`.
			|Must| provide a method which allows configuration by means of a simple, documented data structure.
			|Must| provide access to role decorator functions which map plain text to decorated text (through base class).
		constructor:
			Internal class, TBD later, complicated sphinx stuff.
	"""
	def __init__(self,parse_inline : Callable[[nodes.Element, int, str], List[nodes.Node]],lineno: int) -> None:
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


