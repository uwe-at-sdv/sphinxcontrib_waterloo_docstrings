r"""
Preamble:
	profile:
		module
	normative_sections:
		Contract
	scope:
		extension
Contract:
	general:
		|Must| provide helpers for Waterloo roles in Sphinx.
Notes:
	Usage:
		Do not import this module directly. Use the functions via the |ref|`extension <wtrl://sphinxcontrib.waterloo_docstrings.extension>` module instead.
"""
from __future__ import annotations
from typing import Any, Final, List, Mapping, cast
from docutils import nodes
from docutils.parsers.rst import roles
from sphinx.roles import XRefRole
import re

from sphinxcontrib.waterloo_docstrings.wtrl_context import (
	context,
	make_context,
	)
from sphinxcontrib.waterloo_docstrings.wtrl_parse import (
	parse_inline,
	)
from sphinxcontrib.waterloo_docstrings.wtrl_roles import (
	RoleHandler,
	RolePara,
	RoleResult,
	)
from sphinxcontrib.waterloo_docstrings.wtrl_state import (
	is_target_obj_visible_in_current_scope,
	resolve_qualified_name
	)
import sdv.doc.waterloo.docitem as mod_docitem

# Official markup resolver: converts |role|`text` into :wtrl_role:`text`
WTRL_TOKEN_REPLACEMENTS: Final[Mapping[str, str]] = {
	"Must": ":wtrl_norm:`Must`",
	"must": ":wtrl_norm:`must`",
	"Must_not": ":wtrl_norm:`Must not`",
	"must_not": ":wtrl_norm:`must not`",
	"Should": ":wtrl_norm:`Should`",
	"should": ":wtrl_norm:`should`",
	"Should_not": ":wtrl_norm:`Should not`",
	"should_not": ":wtrl_norm:`should not`",
	"May": ":wtrl_norm:`May`",
	"may": ":wtrl_norm:`may`",
	"Self": ":wtrl_value:`Self`",
	"None": ":wtrl_value:`None`",
	"True": ":wtrl_value:`True`",
	"False": ":wtrl_value:`False`",
	"empty": ":wtrl_value:`<empty>`",
}

RE_WTRL_NAKED_TOKEN_COMPILED: Final[re.Pattern[str]] = re.compile(
	r"(?<!\\)\|(" + "|".join(re.escape(k) for k in WTRL_TOKEN_REPLACEMENTS) + r")\|"
)
RE_WTRL_MARKUP_START_COMPILED: Final[re.Pattern[str]] = re.compile(
	r"(?<!\\)\|" + mod_docitem.WTRL_MARKUP_ROLES + r"\|`"
)
RE_RST_ANGLE_REF_COMPILED: Final[re.Pattern[str]] = re.compile(
	r"^\s*([^<>`]+?)\s*<\s*([^>\s]+)\s*>\s*$"
)

WTRL_STD_REF_ROLE = XRefRole(warn_dangling=True)
RST_TEXT_ESCAPE_CHARS: Final[frozenset[str]] = frozenset("\\`*_|:<>")
RST_ROLE_BODY_ESCAPE_CHARS: Final[frozenset[str]] = frozenset("\\`")

def _escape_chars(text: str, chars: frozenset[str]) -> str:
	return "".join("\\" + ch if ch in chars else ch for ch in text)

def escape_rst_text_segment(text: str) -> str:
	return _escape_chars(text, RST_TEXT_ESCAPE_CHARS)

def escape_rst_role_body(text: str) -> str:
	return _escape_chars(text, RST_ROLE_BODY_ESCAPE_CHARS)

def _find_role_body_end(text: str, role: str, body_start: int) -> tuple[int, str] | None:
	if role == "lit":
		i_double = text.find("``", body_start)
		if i_double >= 0:
			return i_double + 1, text[body_start:i_double + 1]
	i_single = text.find("`", body_start)
	if i_single < 0:
		return None
	return i_single, text[body_start:i_single]

#----- begin helper for resolving forward references ---------#

class wtrl_pending_ref(nodes.Inline, nodes.Element):
	pass

def make_pending_wtrl_ref(label: str, qname: str, target_fqn: str, target_anchor: str) -> wtrl_pending_ref:
	node = wtrl_pending_ref("", nodes.inline("", label))
	node["wtrl_label"] = label
	node["wtrl_qname"] = qname
	node["wtrl_target_fqn"] = target_fqn
	node["wtrl_target_anchor"] = target_anchor
	return node

#----- end helper for resolving forward references -----------#

def parse_ref_body(body: str) -> tuple[str, str]:
	"""Return the visible label and target from a Waterloo ref body."""
	m_ext = mod_docitem.RE_WTRL_ANGLE_HTTPS_REF_COMPILED.match(body)
	if m_ext:
		return m_ext.group(1).strip(), m_ext.group(2).strip()
	m_wtrl = mod_docitem.RE_WTRL_ANGLE_WTRL_REF_COMPILED.match(body)
	if m_wtrl:
		return m_wtrl.group(1).strip(), m_wtrl.group(2).strip()
	m_rst = RE_RST_ANGLE_REF_COMPILED.match(body)
	if m_rst:
		return m_rst.group(1).strip(), m_rst.group(2).strip()
	return body, ""

def _make_context_from_role(para: RolePara) -> context | None:
	env = getattr(para.inliner.document.settings, "env", None)
	app = getattr(env, "app", None)
	if app is None:
		return None
	return make_context(
		app,
		lambda parent, ln, txt: parse_inline(para.inliner, parent, ln, txt),
		para.lineno,
	)

def _make_unresolved_ref(label: str, *, css_class: str = "wtrl_ref_unresolved") -> nodes.inline:
	return nodes.inline(label, label, classes=["wtrl_ref", css_class])

def _make_external_ref(label: str, target: str) -> nodes.reference:
	return nodes.reference("", "", nodes.inline(label, label), refuri=target, classes=["wtrl_ref"])

def _mark_as_wtrl_ref(node_list: List[nodes.Node]) -> None:
	for node in node_list:
		if isinstance(node, nodes.Element):
			classes = node["classes"]
			if "wtrl_ref" not in classes:
				classes.append("wtrl_ref")

def wtrl_ref_role(para: RolePara) -> RoleResult:
	label, target = parse_ref_body(para.text)
	if target.startswith(("http://", "https://")):
		return [_make_external_ref(label, target)], []
	if target.startswith("wtrl://"):
		qname = target[len("wtrl://"):]
		ctx = _make_context_from_role(para)
		if ctx is None:
			return [_make_unresolved_ref(label)], []
		try:
			target_obj, _, _, _ = resolve_qualified_name(ctx, qname)
		except Exception as exc:
			msg = para.inliner.reporter.warning(
				f"WTRL ref target '{qname}' cannot be resolved: {exc}",
				line=para.lineno,
			)
			return [_make_unresolved_ref(label)], [msg]
		if not is_target_obj_visible_in_current_scope(ctx, target_obj):
			return [_make_unresolved_ref(label, css_class="wtrl_ref_out_of_scope")], []
		target_fqn = mod_docitem.get_obj_fully_qualified_name(target_obj)
		target_anchor = mod_docitem.build_anchor(target_obj)
		return [make_pending_wtrl_ref(label, qname, target_fqn, target_anchor)], []
	text = f"{label} <{target}>" if target else label
	node_list, msg_list = WTRL_STD_REF_ROLE(
		"std:ref",
		para.rawtext,
		text,
		para.lineno,
		para.inliner,
		options=dict(para.options or {}),
		content=para.content or [],
	)
	nodes_out = list(node_list)
	_mark_as_wtrl_ref(nodes_out)
	return nodes_out, list(msg_list)

def setup_markup_roles(app: Any) -> None:
	roles.register_local_role(
		"wtrl_ref",
		cast(RoleHandler,
			lambda name, rawtext, text, lineno, inliner, options=None, content=None:
				wtrl_ref_role(RolePara(name=name, rawtext=rawtext, text=text, lineno=lineno, inliner=inliner, options=options, content=content))),
	)

def resolve_markup(text : str, ctx: context) -> str:
	r"""
	Preamble:
		profile:
			function
		normative_sections:
			Contract, Parameters, Returns, Raises, See_also
		scope:
			extension
	Contract:
		general:
			|Must| convert Waterloo inline markup syntax into reStructuredText role directives.
			|Must| process both naked tokens and |role|`body` markup patterns.
			|Must| escape special RST characters in text segments while preserving markup boundaries.
			|Must| return the converted markup string ready for Sphinx processing.
	Parameters:
		text:
			The source text containing Waterloo markup patterns to resolve.
			Markup patterns include naked tokens (|Must|, |may|, |True|, |False|, etc.)
			and structured marks (|tag|`body`, e.g., |type|`str`, |attr|`enabled`).
		ctx:
			The |type|`context` object providing scope information for markup resolution,
			used by helper functions to resolve qualified names and check visibility.
			For currently simple roles this parameter is mostly structural, but reference
			markup and future context-aware transformations require access to the active
			Sphinx/Waterloo rendering state.
	Returns:
		The input text with all recognized Waterloo markup patterns converted to Sphinx role syntax.
		Text segments outside markup are escaped for RST special characters.
		The returned string is ready for parsing by the Sphinx RST parser.
	Raises:
		Exception:
			|May| propagate if context operations fail during markup resolution\
			(e.g., qualified name resolution in nested contexts).
	See_also:
		RST_TEXT_ESCAPE_CHARS, RST_ROLE_BODY_ESCAPE_CHARS, WTRL_TOKEN_REPLACEMENTS
	Notes:
		Markup_conversion:
			* Naked tokens like '|' + Must + '|' → :wtrl_norm:`Must`
			* Structured markup like '|' + role + '|' + `body` → :wtrl_role:`body`.
		Escaping:
			Text segments outside markup use |var|`RST_TEXT_ESCAPE_CHARS` (backslash, backtick, asterisk, underscore, pipe, angles).
			Role bodies use |var|`RST_ROLE_BODY_ESCAPE_CHARS` (backslash, backtick only).
		Context:
			The context parameter keeps this function aligned with the node-building pipeline.
			Most replacements are textual today, but |ref| markup, forward references, scope-sensitive rendering, and future role-specific normalization depend on contextual state.
		Performance:
			Uses compiled regex patterns for efficient token and markup boundary detection.
	"""
	def _repl(role: str, body: str) -> str:
		if role == "ref":
			return f":wtrl_ref:`{body}`"
		return f":wtrl_{role}:`{escape_rst_role_body(body)}`"

	def _resolve_text_segment(segment: str) -> str:
		seg_out: List[str] = []
		i_seg = 0
		for m_seg in RE_WTRL_NAKED_TOKEN_COMPILED.finditer(segment):
			seg_out.append(escape_rst_text_segment(segment[i_seg:m_seg.start()]))
			seg_out.append(WTRL_TOKEN_REPLACEMENTS[m_seg.group(1)])
			i_seg = m_seg.end()
		seg_out.append(escape_rst_text_segment(segment[i_seg:]))
		return "".join(seg_out)

	out: List[str] = []
	i_pos = 0
	while True:
		m = RE_WTRL_MARKUP_START_COMPILED.search(text, i_pos)
		if m is None:
			break
		role = m.group(1)
		body_start = m.end()
		body_end = _find_role_body_end(text, role, body_start)
		if body_end is None:
			i_pos = body_start
			continue
		i_end, body = body_end
		out.append(_resolve_text_segment(text[i_pos:m.start()]))
		out.append(_repl(role, body))
		i_pos = i_end + 1
	out.append(_resolve_text_segment(text[i_pos:]))
	return "".join(out)
