from __future__ import annotations
from typing import Any, Callable, Dict, Iterable, List, Sequence, Tuple, cast

import re,warnings,inspect

from docutils import nodes
from sphinx.util import logging
from sphinx.util import console
from sphinx.util.nodes import make_refnode
import sdv.doc.waterloo.docitem as mod_docitem

from sphinxcontrib.waterloo_docstrings.wtrl_protocol import (
	InlinerProtocol,
	SphinxAppProtocol
	)
from sphinxcontrib.waterloo_docstrings.wtrl_parse import (
	parse_inline
	)
from sphinxcontrib.waterloo_docstrings.wtrl_context import (
	context,
	make_context,
	)
from sphinxcontrib.waterloo_docstrings.wtrl_state import (
	is_target_obj_visible_in_current_scope,
	get_current_scope_set,
	resolve_qualified_name,
	)
from sphinxcontrib.waterloo_docstrings.wtrl_markup import (
	resolve_markup
	)
from sphinxcontrib.waterloo_docstrings.wtrl_signature import (
	render_head_of_callable,
	render_params_and_return_of_callable
	)

logger = logging.getLogger(__name__)

def _emit_runtime_diagnostics(app: SphinxAppProtocol | Any, qname: str, lineno: int, msg: str) -> list[nodes.Node]:
	header = f"while building autodoc directive for `{qname}`:"
	log_msg = f"{header}\n{msg}"
	logger.error(log_msg, location=(app.env.docname, lineno))

	if not app.config.wtrl_diagnostics_admonitions_enabled:
		return []

	error_box = nodes.error("Waterloo directive diagnostics")

	qname_para = nodes.paragraph()
	qname_para.append(nodes.inline(text="Object: ", classes=["wtrl_label"]))
	qname_para.append(nodes.inline(text=qname))
	error_box.append(qname_para)

	msg_para = nodes.paragraph()
	msg_para.append(nodes.inline(text="Summary: ", classes=["wtrl_label"]))
	msg_para.append(nodes.inline(text=msg))
	error_box.append(msg_para)

	return [error_box]

def _emit_tracer_diagnostics(tr: mod_docitem.tracer, app: SphinxAppProtocol | Any, qname: str, lineno: int) -> list[nodes.Node]:
	generated_nodes: list[nodes.Node] = []
	try:
		print(tr.build_json(tr.Severity.INFO))
	except Exception as e:
		print(e)
	if tr.has_errors():
		header = f"while parsing object `{qname}`:"
		details = str(tr)
		if app.config.wtrl_diagnostics_logging_enabled:
			if app.config.wtrl_diagnostics_color_enabled:
				# If colours are used, we render the tracer in our own colors.
				log_msg = f"{header}\n{details}"
				logger.error(log_msg, location=(app.env.docname, lineno), color="reset")
			else:
				# Othewise we strip the colors.
				log_msg = f"{header}\n{tr.strip_ansi_escape_sequences(details)}"
				logger.error(log_msg, location=(app.env.docname, lineno))

#		clean_details = tr.strip_ansi_escape_sequences(str(tr))
#		error_box = nodes.error(f"Waterloo Error: {header}")
#		literal_block = nodes.literal_block(clean_details, clean_details)
#		error_box.append(literal_block)
#		return [error_box]

		json_data = tr.build_json(tr.Severity.INFO)
		errors = json_data.get("__WTRL_ERROR__", [])

		if not errors:
			return []

		for err in errors:
			rule_id = err.get("rule-id", "UNKNOWN-RULE")
			origin = err.get("origin", "general")
			msg = err.get("msg", "")
			hint = err.get("hint", "")

			# 1. Titel im Konstruktor uebergeben, damit das Theme die Box richtig baut
			error_box = nodes.error(f"Waterlint Diagnostics")

			# RuleID
			msg_para = nodes.paragraph()
			msg_para.append(nodes.inline(text="RuleID: ", classes=["wtrl_label"]))
			msg_para.append(nodes.inline(text=f"{rule_id}"))
			error_box.append(msg_para)

			# Origin
			msg_para = nodes.paragraph()
			msg_para.append(nodes.inline(text="Origin: ", classes=["wtrl_label"]))
			msg_para.append(nodes.inline(text=f"{origin}"))
			error_box.append(msg_para)

			# Summary
			msg_para = nodes.paragraph()
			msg_para.append(nodes.inline(text="Summary: ", classes=["wtrl_label"]))
			msg_para.append(nodes.inline(text=f"{msg}"))
			error_box.append(msg_para)

			# 2. Container als generischen 'container' (wird zu <div> statt <p>),
			# da er Block-Elemente wie literal_block aufnehmen soll
			node_content = nodes.container()
            
			if "found" in err or "expected" in err:
				for key in ["found", "expected"]:
					if key in err and err[key]:
						content_text = "\n".join(err[key]).replace("\t", "    ")

						# Das Label packen wir in einen eigenen Absatz, damit es vor dem Block steht
						label_para = nodes.paragraph()
						label_para.append(nodes.inline(text=key.capitalize() + ":", classes=["wtrl_label"]))
						node_content.append(label_para)
						
						# Jetzt steht der literal_block (Block-Element) sauber ausserhalb des Absatzes
						node_lit = nodes.literal_block(content_text, content_text)
						node_content.append(node_lit)
						
			if hint:
				# Sauber getrennter Absatz fuer den Hint
				hint_para = nodes.paragraph()
				hint_para.append(nodes.inline(text="Hint: ", classes=["wtrl_label"]))
				node_content.append(hint_para)
				
				# Der Hint als eigener Codeblock (Block-Element)
				hint_lit = nodes.literal_block(hint, hint)
				node_content.append(hint_lit)

			# Wir haengen den Container in die Error-Box
			error_box.append(node_content)
			generated_nodes.append(error_box)

	# The nodes we return here become part of the document,
	# so the returned list depends on the configuration.
	if app.config.wtrl_diagnostics_admonitions_enabled:
		return generated_nodes
	else:
		return []

def _register_anchor(ctx: context, obj: object, anchor: str) -> None:
	"""
	Register a local anchor for later cross-reference resolution.

	The registry lives on the Sphinx environment and maps fully qualified object
	names to tuples ``(docname, anchor_id)``.
	"""
	env = getattr(ctx, "env", None)
	if env is None:
		return
	docname = getattr(env, "docname", None)
	if not isinstance(docname, str) or not docname:
		return
	obj_fqn = mod_docitem.get_obj_fully_qualified_name(obj)
	if not isinstance(obj_fqn, str) or not obj_fqn:
		return
	index = getattr(env, "wtrl_anchor_index", None)
	if not isinstance(index, dict):
		index = {}
		setattr(env, "wtrl_anchor_index", index)
	index[obj_fqn] = (docname, anchor)


def _build_internal_ref(ctx: context, target_obj: object, link_text: str, css_class: str) -> nodes.reference:
	"""
	Create an internal reference node for a resolved target object.

	If Sphinx environment/builder context and anchor registry are available,
	use ``make_refnode`` (supports cross-document links). Otherwise fall back
	to a local ``refid`` reference.
	"""
	target_anchor = mod_docitem.build_anchor(target_obj)
	node_child = nodes.inline(link_text, link_text)
	env = getattr(ctx, "env", None)
	builder = getattr(getattr(env, "app", None), "builder", None)
	from_docname = getattr(env, "docname", None)
	index = getattr(env, "wtrl_anchor_index", None)
	target_fqn = mod_docitem.get_obj_fully_qualified_name(target_obj)

	if (
		builder is not None
		and isinstance(from_docname, str)
		and from_docname
		and isinstance(index, dict)
	):
		target_docname: str = from_docname
		target_id: str = target_anchor
		loc = index.get(target_fqn)
		if (
			isinstance(loc, tuple)
			and len(loc) == 2
			and isinstance(loc[0], str)
			and isinstance(loc[1], str)
		):
			target_docname, target_id = loc
		node_ref = cast(nodes.reference, make_refnode(
			builder,
			from_docname,
			target_docname,
			target_id,
			node_child,
			title=target_fqn,
		))
	else:
		node_ref = nodes.reference(link_text, link_text, refid=target_anchor)

	node_ref["classes"].append(css_class)
	return node_ref

def _is_doc_visible_in_current_scope(ctx: context, doc: mod_docitem.docitem_docstring_base) -> bool:
	"""
	Return whether the documented object is visible under the current
	Sphinx rendering scope.
	"""
	return cast(bool, doc.is_visible(get_current_scope_set(ctx.env)))

def build_sphinx_nodes(ctx : context,obj: object,doc: mod_docitem.docitem_docstring_base) -> List[nodes.Node]:
	"""
	Preamble:
		profile:
			function
		normative_sections:
			Contract, Parameters, Returns, Raises
		scope:
			extension
	Contract:
		general:
			|Must| convert a parsed Waterloo docstring into docutils nodes for Sphinx output.
			|Must| honor the current Waterloo scope before rendering the documented object.
			|Must| return an empty node list if the documented object is outside the current scope and scope-filter placeholders are disabled.
			|Must| render a note-style placeholder if the documented object is outside the current scope and scope-filter placeholders are enabled.
			|Must| assign a deterministic anchor id to the documentation box.
			|Must| register the anchor id for cross-document Waterloo references.
			|Must| render the docstring as a two-column documentation box with section labels on the left and rendered section content on the right.
			|Must| add a signature row for callable objects.
			|Must| preserve section-specific structure, for example executable-contract bullet lists, free-form paragraphs, grouped definitions, and public-object lists.
			|Must| resolve selected reference-like entries as internal links where targets can be resolved.
			|Must| mark resolvable but scope-filtered reference targets as out-of-scope entries.
			|Must| keep unresolved reference entries visible as role-rendered fallback text.
			|Must| emit runtime warnings for unresolved entries in sections where linkability is expected.
			|Must_not| raise hard validation errors for unresolved references; semantic enforcement belongs to the validator.
	Parameters:
		ctx:
			Rendering context providing Sphinx state, configuration, inline parsing, and Waterloo role helpers.
		obj:
			The documented Python object.
		doc:
			Parsed Waterloo docstring tree for |var|`obj`.
	Returns:
		List of |type|`docutils.nodes.Node` representing the rendered documentation box or scope-filter placeholder.
	Raises:
		NotImplementedError:
			|May| raise if the docstring contains a section shape that is not supported by this renderer.
		RuntimeError:
			|May| raise if unexpected section structure is encountered.
		ValueError:
			|May| raise if free-form itemization starts with an invalid nested list structure.
		RuntimeWarning:
			|May| emit warnings for unresolved link targets (for example in |label|`Public_*`, |label|`Derived_from`, or normative |label|`See_also`).
	Notes:
		Usage:
			This function is typically not called directly. It is called
			by the various |func|`autodoc` functions.
		Scope filtering:
			Scope filtering is handled before the documentation box is built.
			When placeholders are enabled, skipped objects remain visible in the rendered document as lightweight notes.
		Linking:
			Internal links are created using anchor ids from |func|`build_anchor` and the Sphinx environment's Waterloo anchor index.
			Built-in exceptions in section |label|`Raises` are intentionally rendered as plain text without internal links.
		Last reviewed:
			2026-07-23
	"""
	if not _is_doc_visible_in_current_scope(ctx, doc):
		if not ctx.config.wtrl_scope_filtered_object_placeholders_enabled:
			return []

		obj_name = mod_docitem.get_obj_name(obj)
		if mod_docitem.is_obj_module(obj):
			obj_name_markup = ":wtrl_mod:"
		elif mod_docitem.is_obj_class(obj):
			obj_name_markup = ":wtrl_class:"
		elif mod_docitem.is_obj_function(obj):
			obj_name_markup = ":wtrl_func:"
		else:
			obj_name_markup = ":wtrl_var:"

		node_note = nodes.note(classes=["wtrl_scope_filtered_object"])
		node_paragraph = nodes.paragraph()
		object_scopes = doc.scopes()
		object_scopes_str = ", ".join(map(lambda s: f":wtrl_value:`{mod_docitem.scope_to_string.get(int(s), 'unknown')}`", object_scopes))
		current_scopes = get_current_scope_set(ctx.env)
		current_scopes_str = ", ".join(map(lambda s: f":wtrl_value:`{mod_docitem.scope_to_string.get(int(s), 'unknown')}`", current_scopes))
		node_paragraph.extend(ctx.parse(
			node_paragraph,
			0,
			f"Scope filter: skipped {obj_name_markup}`{obj_name}` (object: {object_scopes_str}; active: {current_scopes_str}).",
			))
		node_note += node_paragraph
		return [node_note]
	def parse_text(parent: nodes.Element, text: str) -> List[nodes.Node]:
		return ctx.parse(parent, 0, resolve_markup(text, ctx))

	def is_normative_section(section_label: str) -> bool:
		try:
			node_preamble = cast(Any, doc_items["Preamble"])
			if not node_preamble.has_item("normative_sections"):
				return False
			node_norm = node_preamble.item("normative_sections")
			return section_label in {str(x) for x in node_norm.items()}
		except Exception:
			return False

	def render_linked_factory_entry(parent: nodes.paragraph,entry: str,objname: str,css_class: str,role_fn: Callable[[str], str]) -> None:
		try:
			target_obj, _, _, _ = resolve_qualified_name(ctx, entry)
		except Exception as exc:
			try:
				target_obj, _, _, _ = resolve_qualified_name(ctx, objname + "." + entry)
			except Exception as exc:
				warnings.warn(f"Factory entry '{entry}' cannot be resolved for linking: {exc}",RuntimeWarning)
				parent.extend(ctx.parse(parent,0,role_fn(entry)))
				return
		if not is_target_obj_visible_in_current_scope(ctx, target_obj):
			render_out_of_scope_entry(parent, entry, role_fn)
			return
		parent += _build_internal_ref(ctx, target_obj, entry, css_class)

	def render_linked_base_entry(parent: nodes.paragraph,entry: str,objname: str,css_class: str,role_fn: Callable[[str], str]) -> None:
		return render_linked_factory_entry(parent,entry,objname,css_class,role_fn)

# Not all parameters are used but we leave them in for future compatibility.
	def render_plain_entry(
		parent: nodes.paragraph,
		entry: str,
		css_class: str,
		role_fn: Callable[[str], str],
		warn_label: str,
	) -> None:
		parent.extend(ctx.parse(parent,0,role_fn(entry)))

	def render_out_of_scope_entry(parent: nodes.Element, entry: str, role_fn: Callable[[str], str]) -> None:
		def _mark(node: nodes.Node) -> None:
			if isinstance(node, nodes.literal):
				classes = node.get("classes", [])
				if "wtrl_out_of_scope" not in classes:
					classes.append("wtrl_out_of_scope")
					node["classes"] = classes
			if isinstance(node, nodes.Element):
				for child in node.children:
					_mark(child)

		nodes_out = ctx.parse(parent, 0, role_fn(entry))
		for node_any in nodes_out:
			_mark(node_any)
			parent += node_any

	def render_linked_public_entry(
		parent: nodes.paragraph,
		entry: str,
		resolver_prefix: str,
		css_class: str,
		role_fn: Callable[[str], str],
		warn_label: str,
	) -> None:
		try:
			target_obj, _, _, _ = resolve_qualified_name(ctx, resolver_prefix + "." + entry)
			if not is_target_obj_visible_in_current_scope(ctx, target_obj):
				render_out_of_scope_entry(parent, entry, role_fn)
				return
			parent += _build_internal_ref(ctx, target_obj, entry, css_class)
		except Exception as exc:
			warnings.warn(f"{warn_label} resolver_prefix '{resolver_prefix}': entry '{entry}' cannot be resolved for linking: {exc}",RuntimeWarning)
			parent.extend(ctx.parse(parent,0,role_fn(entry)))

	def render_linked_public_entries(
		parent: nodes.paragraph,
		entries: Sequence[str],
		resolver_prefix: str,
		css_class: str,
		role_fn: Callable[[str], str],
		warn_label: str,
	) -> None:
		for i_item, content in enumerate(entries):
			content_s = str(content)
			if i_item > 0:
				parent += nodes.Text(", ")
			render_linked_public_entry(parent,content_s,resolver_prefix,css_class,role_fn,warn_label)

	def render_linked_derived_from_entries(
		parent: nodes.paragraph,
		entries: Sequence[str],
		css_class: str,
		role_fn: Callable[[str], str],
	) -> None:
		base_by_name: Dict[str, object] = {}
		if mod_docitem.is_obj_class(obj):
			for b in cast(tuple[type[Any], ...], getattr(obj, "__bases__", ())):
				base_by_name[mod_docitem.get_obj_name(b)] = b
				base_by_name[mod_docitem.get_obj_fully_qualified_name(b)] = b
				nm = getattr(b, "__name__", None)
				if isinstance(nm, str):
					base_by_name[nm] = b
				qn = getattr(b, "__qualname__", None)
				if isinstance(qn, str):
					base_by_name[qn] = b
		for i_item, content in enumerate(entries):
			content_s = str(content)
			if i_item > 0:
				parent += nodes.Text(", ")
			base_obj = base_by_name.get(content_s)
			if base_obj is not None:
				if is_target_obj_visible_in_current_scope(ctx, base_obj):
					parent += _build_internal_ref(ctx, base_obj, content_s, css_class)
				else:
					render_out_of_scope_entry(parent, content_s, role_fn)
			else:
				warnings.warn(f"Derived_from entry '{content_s}' is not a direct base class of '{objname}'.",RuntimeWarning)
				parent.extend(ctx.parse(parent,0,role_fn(content_s)))

	def render_linked_see_also_entries(
		parent: nodes.paragraph,
		entries: Sequence[str],
		is_normative: bool,
		resolver_prefix: str | None,
	) -> None:
		obj_module_prefix = resolver_prefix
		obj_qualname = getattr(obj, "__qualname__", "")
		obj_class_prefix = None
		if isinstance(obj_qualname, str) and "." in obj_qualname and not mod_docitem.is_obj_module(obj):
			obj_class_prefix = f"{obj_module_prefix}.{obj_qualname.rsplit('.', 1)[0]}" if obj_module_prefix else None
		for i_item, content in enumerate(entries):
			content_s = str(content)
			if i_item > 0:
				parent += nodes.Text(", ")
			target_obj: object | None = None
			last_exc: Exception | None = None
			for cand in (
				content_s,
				f"{obj_module_prefix}.{content_s}" if obj_module_prefix else None,
				f"{obj_class_prefix}.{content_s}" if obj_class_prefix else None,
			):
				if cand is None:
					continue
				try:
					target_obj, _, _, _ = resolve_qualified_name(ctx, cand)
					last_exc = None
					break
				except Exception as exc:
					last_exc = exc
					target_obj = None
			if target_obj is not None and is_target_obj_visible_in_current_scope(ctx, target_obj):
				if mod_docitem.is_obj_module(target_obj):
					parent += _build_internal_ref(ctx, target_obj, content_s, "wtrl_mod")
				elif mod_docitem.is_obj_class(target_obj):
					parent += _build_internal_ref(ctx, target_obj, content_s, "wtrl_class")
				elif mod_docitem.is_obj_function(target_obj):
					parent += _build_internal_ref(ctx, target_obj, content_s, "wtrl_func")
				else:
					parent += _build_internal_ref(ctx, target_obj, content_s, "wtrl_var")
			elif target_obj is not None:
				# Role var as fallback.
				render_out_of_scope_entry(parent, content_s, ctx.add_role_var)
			else:
				warn_exc: Exception = last_exc if last_exc is not None else ImportError(f"Could not resolve qualified name '{content_s}' with module/class context None/None.")
				if is_normative:
					warnings.warn(f"See_also entry '{content_s}' cannot be resolved for linking: {warn_exc}",RuntimeWarning)
				# Role var as fallback.
				parent.extend(ctx.parse(parent,0,ctx.add_role_var(content_s)))

# Contract.*
	RE_DOC_BULLET_LIST = re.compile(r"^[-+*#]\s")
	def build_bullet_list_from_subsection_items(items: Iterable[str]) -> nodes.bullet_list:
		node_bullet_list = nodes.bullet_list()
		for content in items:
			node_list_item = nodes.list_item()
			node_paragraph = nodes.paragraph()
			node_paragraph.extend(parse_text(node_paragraph, content))
			node_list_item += node_paragraph
			node_bullet_list += node_list_item
		return node_bullet_list

# Definitions, Terminology, Description, Returns, Notes,
	def build_paragraphs_from_items(items: Sequence[str]) -> List[nodes.paragraph]:
		def gen_list(symbol: str) -> nodes.Element:
			node_any_list: nodes.Element
			if symbol == "#":
				node_any_list = nodes.enumerated_list()
				node_any_list['enumtype'] = 'arabic'
				node_any_list['prefix'] = ''
				node_any_list['suffix'] = '.'
				node_any_list['start'] = 1
			else:
				node_any_list = nodes.bullet_list()
			return node_any_list

		restart = True
# Here we collect the paragraph nodes to be returned.
		out: List[nodes.paragraph] = []
# This is the current object we append content to. Whenever we
# find a paragraph token "|" we push this to `out` and create
# a new one. After the loop the current paragraph is appended
# to `out`.
		node_paragraph = nodes.paragraph()

		i_item = 0
		while i_item < len(items):
			content = items[i_item]
			if content == "|":
				out.append(node_paragraph)
				node_paragraph = nodes.paragraph()
				restart = True
			else:
# We experimentally allow bullet lists triggered by a sequence of leading "* ", "+ ", or "- ".
# in the content lines. If we find such a pattern, we build a bullet list from
# all consecutive lines matching the pattern.
				n_lines = 0
				while i_item + n_lines < len(items) and RE_DOC_BULLET_LIST.match(items[i_item + n_lines]):
					n_lines += 1
					if i_item + n_lines >= len(items):
						break
# Originally at least two items are required for safe pattern recognition,
# but the normative rules are getting too complex in that case, so let's
# simplify this:
				if n_lines >= 1:
# For nested itemizations we need a stack.
					node_stack: List[nodes.Element] = []
					symb_stack: List[str] = []
					last_item_stack: List[nodes.list_item | None] = []

					for content in items[i_item:i_item + n_lines]:
						symbol = content[0]
# Drop bullet marker and space.
						text = content[2:]

						if not symb_stack:
							node_stack.append(gen_list(symbol))
							symb_stack.append(symbol)
							last_item_stack.append(None)
# Is this symbol different and new? -> Increase itemization level
						elif symbol != symb_stack[-1]:
							if symbol not in symb_stack:
# The new nested list must be attached to the previous item
								parent_item = last_item_stack[-1]
								if parent_item is None:
									raise ValueError(
									f"Cannot start nested list with symbol {symbol!r} "
									"without a previous list item."
									)
								symb_stack.append(symbol)
# Create (nested) bullet list and make it the current one.
								node_any_list = gen_list(symbol)
								parent_item += node_any_list
# Make nested list the current one
								node_stack.append(node_any_list)
								last_item_stack.append(None)
# Is this symbol different but old? -> Decrease itemization level
							else:
								while symb_stack[-1] != symbol:
									symb_stack.pop()
									node_stack.pop()
									last_item_stack.pop()
# Same symbol as before? -> Keep itemization level
						else:
							pass
# Always: create a new item on the current level
						node_list_item = nodes.list_item()
# Create paragraph for content.
						node_item_paragraph = nodes.paragraph()
						node_item_paragraph.extend(parse_text(node_list_item, text))
						node_list_item += node_item_paragraph
# Append item to current bullet list
						node_stack[-1] += node_list_item
# Remember last item on this level
						last_item_stack[-1] = node_list_item

					node_paragraph += node_stack[0]
					i_item += n_lines
					continue
# The normal stuff
				node_paragraph.extend(parse_text(node_paragraph, ("" if restart else " ") + content))
				restart = False
			i_item += 1
		out.append(node_paragraph)
		return out

	def append_term_paragraphs(node_parent: nodes.Element, term_nodes: Sequence[nodes.Node], items: Sequence[str]) -> None:
		node_term = nodes.paragraph(classes=["wtrl-dfn-term"])
		node_term.extend(term_nodes)
		node_parent += node_term
		for paragraph in build_paragraphs_from_items(items):
			paragraph["classes"].append("wtrl-dfn-content")
			node_parent += paragraph

	objname = mod_docitem.get_obj_name(obj)
	objname_q = mod_docitem.get_obj_fully_qualified_name(obj)
	anchor = mod_docitem.build_anchor(obj)

	if ctx.config and ctx.config.wtrl_current_object_logging_enabled:
		logger.info(f"Waterloo: now processing '{objname_q}'")


# Required for inter-page references.
	_register_anchor(ctx, obj, anchor)

# Build table
	node_table = nodes.table(classes=["wtrl-box"])
	node_table["ids"] = [anchor]
	node_tgroup = nodes.tgroup(cols=2)
	node_tgroup += nodes.colspec(colwidth=18)
	node_tgroup += nodes.colspec(colwidth=82)
	node_tbody = nodes.tbody()
	node_tgroup += node_tbody

	doc_items = cast(dict[str, Any], doc.items())
	profile = cast(str, cast(Any, doc_items["Preamble"]).items()["profile"].items()[0])
	node_thead = nodes.thead(classes=["wtrl-box-head-" + profile])
	node_hrow = nodes.row()
	node1_entry = nodes.entry()
	node1_entry += nodes.inline(text="«" + profile.capitalize() + "»",classes=["wtrl-obj-kind"])
	node2_entry = nodes.entry()
	node2_entry += nodes.paragraph(text=objname,classes=["wtrl-obj-qid"])
	node_hrow += node1_entry
	node_hrow += node2_entry
	node_thead += node_hrow
	node_tgroup += node_thead

	node_table += node_tgroup

# The purpose of this segment is to render the function or method signature
# inside the documentation box (instead of adding it overneath by hand).
# This is closer to the LoIO principle (Locality of Information Output),
# and it's easier for the user because rendering a function requires only
# a single directive.
	if mod_docitem.is_obj_function(obj):
# We achieve this by adding a (pseudo) section.
# Create a table row:
		node_row = nodes.row(classes=["wtrl-section"])
# Left column
		node_entry = nodes.entry()
		node_paragraph = nodes.paragraph()
		node_paragraph.extend(ctx.parse(node_paragraph,0,ctx.add_role_label("Signature")))
		node_entry += node_paragraph
		node_row += node_entry
# Right column
		node_entry = nodes.entry()
# Callable module, classes, head in multicolor.
		node_entry += render_head_of_callable(ctx,obj)
# drop_self=True only removes self,cls,mcls, so most likely we can leave as True. Not 100% sure though.
		node_entry += render_params_and_return_of_callable(ctx,obj,drop_self = True)
		node_row += node_entry
# Add table row to table body.
		node_tbody += node_row

	for label,item_section in doc_items.items():
# New table row per section
		node_row = nodes.row(classes=["wtrl-section"])

		node_entry = nodes.entry()
		node_paragraph = nodes.paragraph()
# Sectionlabels don't have underscores for human readable output.
		node_paragraph.extend(ctx.parse(node_paragraph,0,ctx.add_role_label(cast(Any, item_section).label().replace("_"," "))))
		node_entry += node_paragraph
		node_row += node_entry

		node_entry = nodes.entry()
		if label in ("Preamble","Contract"):
			for label1,item_subsection in cast(dict[str, Any], cast(Any, item_section).items()).items():
				if label1 == "profile":
					continue
# Human-readable substring label
				label1_hr = label1
				if label1 in ("normative_sections",):
					label1_hr = label1.replace("_"," ")

				node1_paragraph = nodes.paragraph()
				node1_paragraph.extend(ctx.parse(node1_paragraph,0,ctx.add_role_label(label1_hr)))
				if label1 in ("normative_sections","traits","status","scope"):
					node2_bullet_list = nodes.bullet_list()
					node2_list_item = nodes.list_item()
					node2_paragraph = nodes.paragraph()
					sub_items = list(cast(Iterable[str], cast(Any, item_subsection).items()))
					if len(sub_items) > 0:
						if label1 in ("normative_sections",):
							node2_paragraph.extend(ctx.parse(node2_paragraph,0,", ".join([ctx.add_role_label(content.replace("_"," ")) for content in sub_items])))
						elif label1 in ("traits","status","scope"):
							node2_paragraph.extend(ctx.parse(node2_paragraph,0,", ".join([ctx.add_role_value(content) for content in sub_items])))
					else:
						node2_paragraph.extend(ctx.parse(node1_paragraph,0,"|empty|"))
					node2_list_item += node2_paragraph
					node2_bullet_list += node2_list_item
				elif label1 in ("base",):
					node2_bullet_list = nodes.bullet_list()
					node2_list_item = nodes.list_item()
					node2_paragraph = nodes.paragraph()
					sub_items = list(cast(Iterable[str], cast(Any, item_subsection).items()))
# Always one entry.
					render_linked_base_entry(node2_paragraph,sub_items[0],objname,"wtrl_func",ctx.add_role_func)
#					node2_paragraph.extend(ctx.parse(node2_paragraph,0,ctx.add_role_func(sub_items[0])))

					node2_list_item += node2_paragraph
					node2_bullet_list += node2_list_item
				elif label1 in ("general","constructor","requires","ensures","invariants",):
					node2_bullet_list = build_bullet_list_from_subsection_items(item_subsection.items())
				else:
					raise NotImplementedError("dude",label1)
				node_entry += node1_paragraph
				node_entry += node2_bullet_list

		elif label in ("Definitions","Terminology"):
			if label == "Definitions":
				obj_definitions = cast(mod_docitem.docitem_definitions,item_section)
				if obj_definitions.inherited():
# We would like to link to the module doc.
					direct_module = mod_docitem.get_obj_direct_module(obj)
# Label "<Inherited terms>"
					if direct_module:
						node_inh = _build_internal_ref(
							ctx,
							direct_module,
							"<Terms inherited from module>",
							"wtrl_label",
						)
						term_nodes: List[nodes.Node] = [node_inh]
					else:
						node_label = nodes.inline()
						node_label.extend(ctx.parse(node_label, 0, ctx.add_role_label("<Terms inherited from module>")))
						term_nodes = [node_label]
					append_term_paragraphs(
						node_entry,
						term_nodes,
						[", ".join([ctx.add_role_dfn(inh) for inh in obj_definitions.inherited()])],
					)

				seen: Dict[Any,List[str]] = {}
# Collect terms having the same content (we have a DAG, not a tree!)
				for term, item_subsection in item_section.items().items():
					if item_subsection in seen:
						seen[item_subsection].append(term)
						continue
					seen[item_subsection] = [term]
# Now render
				for item_subsection,terms in seen.items():
					if not terms:
						continue
# Term
					node_term = nodes.inline()
					if len(terms) > 1:
						node_term.extend(ctx.parse(node_term, 0, ctx.add_role_dfn(terms[0] + " [" + ", ".join(terms[1:]) + "]")))
					else:
						node_term.extend(ctx.parse(node_term, 0, ctx.add_role_dfn(terms[0])))
# Content
					append_term_paragraphs(node_entry, [node_term], item_subsection.items())
			else:
				for term, item_subsection in item_section.items().items():
# Term
					node_term = nodes.inline()
					node_term.extend(ctx.parse(node_term, 0, ctx.add_role_dfn(term)))
# Content
					append_term_paragraphs(node_entry, [node_term], item_subsection.items())
# Both a freeform. "Description" is non-normative. "Returns" is normative,
# yet we msut provide tools  like itemization and enumeration in order to
# resolve the inner structure of the returned object, therefore freeform.
		elif label in ("Description", "Returns"):
# Content
			for paragraph in build_paragraphs_from_items(item_section.items()):
				node_entry += paragraph
		elif label in ("Notes",):
			for term, item_subsection in item_section.items().items():
# Rubric, allows classes=['',...]
				rub = nodes.rubric(classes=['wtrl-note-title'])
				rub.extend(ctx.parse(rub, 0, term))
				node_entry += rub
# Content
				for paragraph in build_paragraphs_from_items(item_subsection.items()):
					paragraph["classes"].append("wtrl-freeform-paragraph-content")
					node_entry += paragraph
# Factory: List of function names, each with a line-by-line executable contract.
		elif label in ("Factory"):
			if len(item_section.items()) == 0:
				node_entry.extend(parse_text(node1_paragraph,"|empty|"))
			else:
# The table cell is an alternating sequence of paragraphs and bulletlists.
				for label1, item_subsection in item_section.items().items():
# Wrap factory label in a paragraph
					node_label_paragraph = nodes.paragraph()
					render_linked_factory_entry(node_label_paragraph,label1,objname,"wtrl_func",ctx.add_role_func)
					node_entry += node_label_paragraph
# Iterate over logical lines in the exception class' content and add each bullet list as sibling node.
					node_entry += build_bullet_list_from_subsection_items(item_subsection.items())

# New in 0.1.1: Parameters and Class/Method/Function_overview are rendered as freeform, like Public_...
# The reason for parameters is that we must have tools like itemization and enumeration
# in order to resolve the inner structure of single parameters.
# The reason for Class/Method/Function_overview is that it makes little sense
# to enforce a line-by-line executable conract style for non-normative sections.
# From an aesthetic point of view we get rid of many bullets of non-items.
		elif label in ("Public_constants", "Public_variables", "Public_types", "Parameters", "Class_overview", "Method_overview", "Function_overview"):
			for label1, item_subsection in item_section.items().items():
# First paragraph of the entry group: clickable constant/variable label.
				node_label_paragraph = nodes.paragraph()
# Add a clickable label. Pass "Public_constants"/"Public_variables"/"Public_types" as label for warnings.
				if label in ("Public_constants", "Public_variables"):
					render_linked_public_entry(node_label_paragraph,label1,objname_q,"wtrl_var",ctx.add_role_var,label)
				elif label in ("Public_types",):
					render_linked_public_entry(node_label_paragraph,label1,objname_q,"wtrl_type",ctx.add_role_type,label)
# Add a label with semantic role |var|.
				elif label in ("Parameters",):
					render_plain_entry(node_label_paragraph,label1,"wtrl_var",ctx.add_role_var,label)
				elif label in ("Class_overview",):
					render_plain_entry(node_label_paragraph,label1,"wtrl_class",ctx.add_role_class,label)
				elif label in ("Method_overview",):
					render_plain_entry(node_label_paragraph,label1,"wtrl_func",ctx.add_role_func,label)
				elif label in ("Function_overview",):
					render_plain_entry(node_label_paragraph,label1,"wtrl_func",ctx.add_role_func,label)
				node_entry += node_label_paragraph
# Iterate over logical lines in the public constant's/variable's content and add each paragraph as sibling node.
				for paragraph in build_paragraphs_from_items(item_subsection.items()):
					paragraph["classes"].append("wtrl-freeform-paragraph-content")
					node_entry += paragraph

		elif label in ("Raises"):
# For section "Raises" we enforce the line-by-line style and interpret the content as an executable contract.
			if len(item_section.items()) == 0:
				node_entry.extend(parse_text(node1_paragraph,"|empty|"))
			else:
				for label1, item_subsection in item_section.items().items():
					node_label_paragraph = nodes.paragraph()
					render_plain_entry(node_label_paragraph,label1,"wtrl_class",ctx.add_role_class,"Raises")
					node_entry += node_label_paragraph
# Iterate over logical lines in the exception class' content and add each bullet list as sibling node.
					node_entry += build_bullet_list_from_subsection_items(item_subsection.items())
		elif label in ("Derived_from"):
			node1_paragraph = nodes.paragraph()
			render_linked_derived_from_entries(
				node1_paragraph,
				cast(Sequence[str], item_section.items()),
				"wtrl_type",
				ctx.add_role_type,
			)
			node_entry += node1_paragraph
		elif label in ("See_also",):
			node1_paragraph = nodes.paragraph()
			render_linked_see_also_entries(
				node1_paragraph,
				cast(Sequence[str], item_section.items()),
				is_normative_section("See_also"),
				mod_docitem.get_obj_name(obj) if mod_docitem.is_obj_module(obj) else getattr(obj, "__module__", None),
			)
			node_entry += node1_paragraph
# The following three, Public_classes/functions/methods have the
# same structure, only different semantic roles and style classes.
# The content is simply a list of resolvable clickable objects.
		elif label in ("Public_classes",):
			node1_paragraph = nodes.paragraph()
			render_linked_public_entries(
				node1_paragraph,
				cast(Sequence[str], item_section.items()),
				objname_q, "wtrl_class", ctx.add_role_class, label)
			node_entry += node1_paragraph
		elif label in ("Public_functions","Public_methods"):
			node1_paragraph = nodes.paragraph()
			render_linked_public_entries(
				node1_paragraph,
				cast(Sequence[str], item_section.items()),
				objname_q, "wtrl_func", ctx.add_role_func, label)
			node_entry += node1_paragraph
# Catch-all. Scan HTML for "TBD" in order to detect bugs.
		else:
			node_paragraph = nodes.paragraph(text="TBD")
			node_entry += node_paragraph

		node_row += node_entry
		node_tbody += node_row

	return [node_table]

def build_sphinx_nodes_full(ctx : context, class_obj: Any, session: mod_docitem.DocSession) -> List[nodes.Node]:
	"""
	Preamble:
		profile:
			function
		normative_sections:
			Contract, Parameters, Returns, Raises
		scope:
			extension
	Contract:
		general:
			|Must| parse and validate the Waterloo docstring of |var|`class_obj`.
			|Must| validate the class method coverage declared by the class docstring.
			|Must| return an empty node list if the class docstring is outside the current Waterloo scope.
			|Must| render the class docstring with |func|`build_sphinx_nodes`.
			|Must| recursively render nested classes listed in |label|`Public_classes` if they exist on |var|`class_obj`.
			|Must| render public methods listed in |label|`Public_methods` if they exist, resolve to function objects, have docstrings, validate successfully, and are visible in the current Waterloo scope.
			|Must| insert method block prolog nodes before rendered public methods.
			|Must| render documented property accessor methods for property entries listed in |label|`Public_variables`.
			|Must| reuse |var|`session` for parsing and validation work performed during the recursive render pass.
			|May| skip listed members that cannot be found, cannot be represented as function objects, or do not have docstrings.
	Parameters:
		ctx:
			Rendering context providing Sphinx state, configuration, diagnostics, inline parsing, and Waterloo role helpers.
		class_obj:
			The class object to render.
		session:
			Session object used for parser and validator state shared across the recursive render pass.
	Returns:
		List of |type|`docutils.nodes.Node` representing the class, nested classes, public methods, and documented property accessors.
	Raises:
		RuntimeError:
			|Must| raise if |var|`class_obj` has no docstring.
			|May| raise if parsing or validation of the class docstring fails.
			|May| raise if rendering the class docstring fails.
		NotImplementedError:
			|May| forward unsupported section-shape errors from |func|`build_sphinx_nodes`.
		ValueError:
			|May| forward free-form itemization errors from |func|`build_sphinx_nodes`.
		BaseException:
			|May| forward exceptions from Sphinx or the Waterloo parser/validator.
	Notes:
		Member errors:
			The current method-rendering branch is intentionally tolerant and may skip problematic methods instead of aborting the complete class rendering pass.
		Scope filtering:
			Unlike |func|`build_sphinx_nodes`, this helper currently omits an out-of-scope class without rendering a placeholder.
		Last reviewed:
			2026-07-23
	"""
# Tracer
	tr = ctx.tr
	with mod_docitem.traced_section(tr, class_obj.__name__):
		nodes_out: List[nodes.Node] = []

# Validate class docstring and Method_overview coverage
		class_doc_txt = mod_docitem.get_obj_docstring(class_obj)
		if not class_doc_txt:
			raise RuntimeError(f"class {class_obj} has no docstring.")
		top = cast(mod_docitem.docitem_docstring_class,mod_docitem.validate_docstring(tr,class_obj, top=None, session=session))
		mod_docitem.validate_class_method_coverage(tr,class_obj,top,session=session)
		assert isinstance(class_doc_txt, str)

		tree_cls = mod_docitem.parse_indent_docstring(tr,class_doc_txt, session)
		di_cls = mod_docitem.docitem_docstring_class()
		di_cls.parse(tr,tree_cls)
		mod_docitem.validate_docstring(tr,class_obj,di_cls, session=session)
		if not _is_doc_visible_in_current_scope(ctx, di_cls):
# Scope-aware rendering omits invisible objects entirely. If later
# we need author-facing placeholders, this is the class-level exit to adapt.
			return []

# Render class block
		nodes_out.extend(build_sphinx_nodes(ctx, class_obj, di_cls))

# Render public classes
		if "Public_classes" in di_cls.items():
#			nodes_out.extend(ctx.build_prolog_method_overview(ctx))
			pc_node = di_cls._items["Public_classes"]
			assert isinstance(pc_node, mod_docitem.docitem_public_classes)
			if len(pc_node.items()) > 0:
				rubric = nodes.rubric()
				rubric += ctx.parse(rubric, ctx.i_line, f"Nested classes in {ctx.add_role_type(class_obj.__name__)}")
				nodes_out.append(rubric)
			for cls_name in pc_node.items():
				if not hasattr(class_obj, cls_name):
					continue
				cls_obj = getattr(class_obj, cls_name)
# Recusrive call
				nodes_out.extend(build_sphinx_nodes_full(ctx,cls_obj, session=session))


# Render public methods
		if "Public_methods" in di_cls.items():
			try:
				pm_node = di_cls._items["Public_methods"]
				assert isinstance(pm_node, mod_docitem.docitem_public_methods)
				if len(pm_node.items()) > 0:
					rubric = nodes.rubric()
					rubric += ctx.parse(rubric, ctx.i_line, f"Public Methods in class {ctx.add_role_type(mod_docitem.get_obj_name(class_obj))}")
					nodes_out.append(rubric)
				for meth_name in pm_node.items():
					if not hasattr(class_obj, meth_name):
						continue
					meth_obj = getattr(class_obj, meth_name)
					func_obj = mod_docitem.get_func_obj_from_callable(meth_obj)
					if not func_obj:
						continue
					func_doc_txt = mod_docitem.get_obj_docstring(func_obj)
					if not func_doc_txt:
						continue
					tree_m = mod_docitem.parse_indent_docstring(tr,func_doc_txt, session)

					profile = mod_docitem.get_profile_of_tree(tr,tree_m)
					di_m :  mod_docitem.docitem_base
					if profile == "inherited_method":
						di_m = mod_docitem.docitem_docstring_inherited_method()
					else:
						di_m = mod_docitem.docitem_docstring_method()

					di_m.parse(tr,tree_m)
					mod_docitem.validate_docstring(tr,func_obj,di_m, session=session)
					if not _is_doc_visible_in_current_scope(ctx, di_m):
						continue
					nodes_out.extend(ctx.build_prolog_method_block(ctx, None, class_obj, func_obj))
					nodes_out.extend(build_sphinx_nodes(ctx, func_obj, di_m))
			except:
				pass
# Render properties.
		if "Public_variables" in di_cls.items():
			node_methods = di_cls._items["Public_variables"]
			assert isinstance(node_methods, mod_docitem.docitem_public_variables)
# Iterate over property candidates
			for prop_name in node_methods.items():
				if not hasattr(class_obj, prop_name):
					continue
# Extract and check if it is a property
				prop_obj = inspect.getattr_static(class_obj, prop_name)
				if not isinstance(prop_obj, property):
					continue
# Extract method objects
				meth_objs: list[Tuple[Callable[...,Any],str]] = []
# Check for existence, just to be sure. Insert only if it is a method object.
				for attr_name in ("fget", "fset", "fdel"):
					meth = getattr(prop_obj, attr_name)
					if meth is not None:
						meth_objs.append((meth,prop_name + "." + attr_name))
				for func_obj,func_name in meth_objs:
					func_doc_txt = mod_docitem.get_obj_docstring(func_obj)
					if not func_doc_txt:
						continue
					tree_m = mod_docitem.parse_indent_docstring(tr,func_doc_txt, session)

					profile = mod_docitem.get_profile_of_tree(tr,tree_m)
					di_prop_meth :  mod_docitem.docitem_base
					if profile == "inherited_method":
						di_prop_meth = mod_docitem.docitem_docstring_inherited_method()
					else:
						di_prop_meth = mod_docitem.docitem_docstring_method()

					di_prop_meth.parse(tr,tree_m)
					mod_docitem.validate_docstring(tr,func_obj,di_prop_meth, session=session)
					if not _is_doc_visible_in_current_scope(ctx, di_prop_meth):
						continue
#					nodes_out.extend(ctx.build_prolog_method_block(ctx, None, prop_obj, func_obj))
					nodes_out.extend(build_sphinx_nodes(ctx, func_obj, di_prop_meth))
		return nodes_out

#===== Sphinx extension stuff =================================#


#----- begin Sphinx nodes for function signatures -------------#




#----- end Sphinx nodes for function signatures ---------------#

#----- begin node builder functions ---------------------------#

def wtrl_build_autodoc_module_nodes(app: SphinxAppProtocol | Any, inliner: InlinerProtocol, lineno: int, qname: str) -> list[nodes.Node]:
	"""
Preamble:
	profile:
		function
	normative_sections:
		Contract, Parameters, Returns, Raises
	scope:
		extension
Contract:
	general:
		|Must| create a Waterloo rendering context for the active Sphinx application and source line.
		|Must| resolve the dotted module name |var|`qname` to a Python module object, taking the current Waterloo module state into account.
		|Must| return diagnostic nodes if |var|`qname` cannot be resolved.
		|Must| return diagnostic nodes if |var|`qname` does not resolve to a module.
		|Must| return diagnostic nodes if the resolved module has no non-empty docstring.
		|Must| parse and validate the module's Waterloo docstring.
		|Must| return structured tracer diagnostic nodes if parsing or validation fails.
		|Must| render the parsed docstring with |func|`build_sphinx_nodes`.
Description:
	Implementation of directive |attr|`.. wtrl_autodoc_module::`.
Parameters:
	app:
		The Sphinx application instance that carries configuration and environment state.
	inliner:
		The Docutils inliner used to parse inline markup into nodes.
	lineno:
		Line number in the source document.
	qname:
		The qualified module name to build nodes for.
Returns:
	List of generated |type|`docutils.nodes.Node` representing the module documentation or a diagnostic replacement.
Raises:
	BaseException:
		|May| forward unexpected exceptions from context creation, inline parsing, or |func|`build_sphinx_nodes`.
Notes:
	Diagnostics:
		Expected directive failures are rendered into the document instead of being raised as hard Sphinx build errors.
	Last reviewed:
		2026-07-23
	"""
	ctx = make_context(app, lambda parent, ln, txt: parse_inline(inliner,parent,ln,txt), lineno)
	tr = ctx.tr
	session = mod_docitem.DocSession()
	with mod_docitem.traced_section(tr, qname):
		try:
			module_obj, _, _, _ = resolve_qualified_name(ctx, qname)
		except Exception as e:
# Catch expected resolver failures, but do not mask hard process-control exceptions.
			return _emit_runtime_diagnostics(app, qname, lineno, f"{qname} cannot be resolved: {str(e)}")
		if not mod_docitem.is_obj_module(module_obj):
			return _emit_runtime_diagnostics(app, qname, lineno, f"{qname} does not resolve to a module.")
		mod_doc_txt = mod_docitem.get_obj_docstring(module_obj)
		if not mod_doc_txt or not mod_doc_txt.strip():
			return _emit_runtime_diagnostics(app, qname, lineno, f"{qname} has no docstring.")
# Todo: think about diagnostics channel.
		try:
			tree_mod = mod_docitem.parse_indent_docstring(tr,mod_doc_txt, session)
			di_mod = mod_docitem.docitem_docstring_module()
			di_mod.parse(tr,tree_mod)
			mod_docitem.validate_docstring(tr,module_obj, di_mod, session=session)
		except BaseException as e:
			return _emit_tracer_diagnostics(tr,app,qname,lineno)
		return build_sphinx_nodes(ctx, module_obj, di_mod)

def wtrl_build_autodoc_function_nodes(app: SphinxAppProtocol | Any, inliner: InlinerProtocol, lineno: int, qname: str) -> list[nodes.Node]:
	"""
Preamble:
	profile:
		function
	normative_sections:
		Contract, Parameters, Returns, Raises
	scope:
		extension
Contract:
	general:
		|Must| create a Waterloo rendering context for the active Sphinx application and source line.
		|Must| resolve the dotted function name |var|`qname` to a callable, taking the current Waterloo module/class state into account.
		|Must| return diagnostic nodes if |var|`qname` cannot be resolved.
		|Must| return diagnostic nodes if |var|`qname` does not resolve to a callable.
		|Must| return diagnostic nodes if the resolved callable has no non-empty docstring.
		|Must| parse and validate the function's Waterloo docstring.
		|Must| return structured tracer diagnostic nodes if parsing or validation fails.
		|Must| render |value|`function` and |value|`method` profiles as method docstrings.
		|Must| render all other accepted callable profiles as inherited-method docstrings.
		|Must| render the parsed docstring with |func|`build_sphinx_nodes`.
Description:
	Implementation of directive |attr|`.. wtrl_autodoc_function::`.
Parameters:
	app:
		The Sphinx application instance that carries configuration and environment state.
	inliner:
		The Docutils inliner used to parse inline markup into nodes.
	lineno:
		Line number in the source document.
	qname:
		The qualified function name to document.
Returns:
	List of generated |type|`docutils.nodes.Node` representing the callable documentation or a diagnostic replacement.
Raises:
	BaseException:
		|May| forward unexpected exceptions from context creation, inline parsing, or |func|`build_sphinx_nodes`.
Notes:
	Diagnostics:
		Expected directive failures are rendered into the document instead of being raised as hard Sphinx build errors.
	Last reviewed:
		2026-07-23
	"""
	ctx = make_context(app, lambda parent, ln, txt: parse_inline(inliner, parent, ln, txt), lineno)
	tr = ctx.tr
	session = mod_docitem.DocSession()

	with mod_docitem.traced_section(tr, qname):
		try:
			function_obj, _, _, _ = resolve_qualified_name(ctx, qname)
		except Exception as e:
# Catch expected resolver failures, but do not mask hard process-control exceptions.
			return _emit_runtime_diagnostics(app, qname, lineno, f"{qname} cannot be resolved: {str(e)}")
		if not callable(function_obj):
			return _emit_runtime_diagnostics(app, qname, lineno, f"{qname} does not resolve to a callable.")
		func_doc_txt = mod_docitem.get_obj_docstring(function_obj)
		if not func_doc_txt or not func_doc_txt.strip():
			return _emit_runtime_diagnostics(app, qname, lineno, f"{qname} has no docstring.")

		try:
			tree_meth = mod_docitem.parse_indent_docstring(tr,func_doc_txt, session)
		except BaseException as e:
			return _emit_tracer_diagnostics(tr,app,qname,lineno)
		if mod_docitem.get_profile_of_tree(mod_docitem.tracer(),tree_meth) in ("function","method"):
			try:
				di_meth = mod_docitem.docitem_docstring_method()
				di_meth.parse(tr,tree_meth)
				mod_docitem.validate_docstring(tr,function_obj, di_meth, session=session)
			except BaseException as e:
				return _emit_tracer_diagnostics(tr,app,qname,lineno)
			return build_sphinx_nodes(ctx, function_obj, di_meth)
		else:
			try:
				di_inhmeth = mod_docitem.docitem_docstring_inherited_method()
				di_inhmeth.parse(tr,tree_meth)
				mod_docitem.validate_docstring(tr,function_obj, di_inhmeth, session=session)
			except BaseException as e:
				return _emit_tracer_diagnostics(tr,app,qname,lineno)
			return build_sphinx_nodes(ctx, function_obj, di_inhmeth)

def wtrl_build_autodoc_class_nodes(app: SphinxAppProtocol | Any, inliner: InlinerProtocol, lineno: int, qname: str) -> list[nodes.Node]:
	"""
Preamble:
	profile:
		function
	normative_sections:
		Contract, Parameters, Returns, Raises
	scope:
		extension
Contract:
	general:
		|Must| create a Waterloo rendering context for the active Sphinx application and source line.
		|Must| resolve the dotted class name |var|`qname` to a class, taking the current Waterloo module/class state into account.
		|Must| return diagnostic nodes if |var|`qname` cannot be resolved.
		|Must| return diagnostic nodes if |var|`qname` does not resolve to a class.
		|Must| return diagnostic nodes if the resolved class has no non-empty docstring.
		|Must| parse and validate the class' Waterloo docstring.
		|Must| return structured tracer diagnostic nodes if parsing or validation fails.
		|Must| render the parsed docstring with |func|`build_sphinx_nodes`.
Description:
	Implementation of directive |attr|`.. wtrl_autodoc_class::`.
Parameters:
	app:
		The Sphinx application instance that carries configuration and environment state.
	inliner:
		The Docutils inliner used to parse inline markup into nodes.
	lineno:
		Line number in the source document.
	qname:
		The qualified class name to document.
Returns:
	List of generated |type|`docutils.nodes.Node` representing the class documentation or a diagnostic replacement.
Raises:
	BaseException:
		|May| forward unexpected exceptions from context creation, inline parsing, or |func|`build_sphinx_nodes`.
Notes:
	Diagnostics:
		Expected directive failures are rendered into the document instead of being raised as hard Sphinx build errors.
	Last reviewed:
		2026-07-23
	"""
	ctx = make_context(app, lambda parent, ln, txt: parse_inline(inliner, parent, ln, txt), lineno)
	tr = ctx.tr
	session = mod_docitem.DocSession()
	with mod_docitem.traced_section(tr, qname):
		try:
			obj, _, _, _ = resolve_qualified_name(ctx, qname)
		except Exception as e:
# Catch expected resolver failures, but do not mask hard process-control exceptions.
			return _emit_runtime_diagnostics(app, qname, lineno, f"{qname} cannot be resolved: {str(e)}")
		if not mod_docitem.is_obj_class(obj):
			return _emit_runtime_diagnostics(app, qname, lineno, f"{qname} does not resolve to a class.")
		class_doc_txt = mod_docitem.get_obj_docstring(obj)
		if not class_doc_txt or not class_doc_txt.strip():
			return _emit_runtime_diagnostics(app, qname, lineno, f"{qname} has no docstring.")
		try:
			tree_mod = mod_docitem.parse_indent_docstring(tr,class_doc_txt, session)
			di_node = mod_docitem.docitem_docstring_class()
			di_node.parse(tr,tree_mod)
			mod_docitem.validate_docstring(tr,obj, di_node, session=session)
		except BaseException as e:
			return _emit_tracer_diagnostics(tr,app,qname,lineno)
		return build_sphinx_nodes(ctx, obj,di_node)

def wtrl_build_autodoc_class_full_nodes(app: SphinxAppProtocol | Any, inliner: InlinerProtocol, lineno: int, qname: str) -> list[nodes.Node]:
	"""
Preamble:
	profile:
		function
	normative_sections:
		Contract, Parameters, Returns, Raises
	scope:
		extension
Contract:
	general:
		|Must| create a Waterloo rendering context for the active Sphinx application and source line.
		|Must| resolve the dotted class name |var|`qname` to a class, taking the current Waterloo module/class state into account.
		|Must| return diagnostic nodes if |var|`qname` cannot be resolved.
		|Must| return diagnostic nodes if |var|`qname` does not resolve to a class.
		|Must| return diagnostic nodes if the resolved class has no non-empty docstring.
		|Must| delegate recursive class, nested-class, method, and property-accessor rendering to |func|`build_sphinx_nodes_full`.
		|Must| return runtime diagnostic nodes if |func|`build_sphinx_nodes_full` raises |type|`RuntimeError`.
		|Must| return structured tracer diagnostic nodes if recursive rendering fails with another expected exception.
Description:
	Implementation of directive |attr|`.. wtrl_autodoc_class_full::`.
Parameters:
	app:
		The Sphinx application instance that carries configuration and environment state.
	inliner:
		The Docutils inliner used to parse inline markup into nodes.
	lineno:
		Line number in the source document.
	qname:
		The qualified name of the class to be documented.
Returns:
	List of generated |type|`docutils.nodes.Node` representing the recursively rendered class documentation or a diagnostic replacement.
Raises:
	BaseException:
		|May| forward unexpected exceptions from context creation, inline parsing, or diagnostic rendering.
Notes:
	Diagnostics:
		Expected directive failures are rendered into the document instead of being raised as hard Sphinx build errors.
	Recursion:
		The traversal policy is implemented by |func|`build_sphinx_nodes_full`; this directive wrapper only resolves the top-level class and translates failures into Sphinx nodes.
	Last reviewed:
		2026-07-23
	"""
	ctx = make_context(app, lambda parent, ln, txt: parse_inline(inliner, parent, ln, txt), lineno)
	tr = ctx.tr
	session = mod_docitem.DocSession()
	with mod_docitem.traced_section(tr, qname):
		try:
			obj, _, _, _ = resolve_qualified_name(ctx, qname)
		except Exception as e:
# Catch expected resolver failures, but do not mask hard process-control exceptions.
			return _emit_runtime_diagnostics(app, qname, lineno, f"{qname} cannot be resolved: {str(e)}")
		if not mod_docitem.is_obj_class(obj):
			return _emit_runtime_diagnostics(app, qname, lineno, f"{qname} does not resolve to a class.")
		class_doc_txt = mod_docitem.get_obj_docstring(obj)
		if not class_doc_txt or not class_doc_txt.strip():
			return _emit_runtime_diagnostics(app, qname, lineno, f"{qname} has no docstring.")
		try:
			return build_sphinx_nodes_full(ctx, obj, session=session)
		except RuntimeError as e:
			return _emit_runtime_diagnostics(app, qname, lineno, str(e))
		except Exception as e:
			return _emit_tracer_diagnostics(tr,app,qname,lineno)
