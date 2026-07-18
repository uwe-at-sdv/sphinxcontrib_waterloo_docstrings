from __future__ import annotations
from typing import Final, List, Mapping, cast

import re,warnings

from sphinxcontrib.waterloo_docstrings.wtrl_context import (
	context,
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

def resolve_markup(text : str, ctx: context) -> str:
	def _resolve_wtrl_ref_uri(qname: str) -> str | None:
# Resolve object
		try:
			target_obj, _, _, _ = resolve_qualified_name(ctx, qname)
		except Exception as exc:
			warnings.warn(f"WTRL ref target '{qname}' cannot be resolved: {exc}", RuntimeWarning)
			return None
		if not is_target_obj_visible_in_current_scope(ctx, target_obj):
			return None
# Build anchor of object.
		target_anchor = mod_docitem.build_anchor(target_obj)
# Build fallback that works at least page internally,
# if we cannot access the current document name.
		env = getattr(ctx, "env", None)
		if env is None:
			return cast(str, "#" + target_anchor)
		from_docname = getattr(env, "docname", None)
		if not isinstance(from_docname, str) or not from_docname:
			return cast(str, "#" + target_anchor)
# Part of the best effort fallback strategy: If we fail to build the
# inter-page URI we can still hope the target is on the same page.
		target_docname: str = from_docname
		target_id: str = target_anchor
# At this point we already know that the enviroment is well-defined.
# Now extract the wtrl-specific index we accumulate in build_sphinx_nodes.
# Note that the first call to this function via parse_text happens deep inside
# build_sphinx_node, at a point where we already have wtrl_anchor_index.
# Yet, referencing objects rendered later than the current one fails
# if the target is in a different document (works intra-page, fails inter-page).
		index = getattr(env, "wtrl_anchor_index", None)
		target_fqn = mod_docitem.get_obj_fully_qualified_name(target_obj)
# But nonetheless we make sure the index exists and is a dict as expected.
		if isinstance(index, dict):
# Our helper _register_anchor adds anchor as tuple made of two components,
# the document name and the object anchor. If we find this structure
# we can extract the full inter-page URI. This conservative tests makes
# our code immune with respect to "creative" use of wtrl_anchor_index.
			loc = index.get(target_fqn)
			if (
				isinstance(loc, tuple)
				and len(loc) == 2
				and isinstance(loc[0], str)
				and isinstance(loc[1], str)
			):
				target_docname, target_id = loc
# Sphinx provides a mechanism for building the URI from source and target
# document name, provided we can get access to the Sphinx builder.
		builder = getattr(getattr(env, "app", None), "builder", None)
		if builder is not None:
			try:
# No need for inter-page URI if source and target document are the same.
				if from_docname == target_docname:
					return f"#{target_id}"
# Chill mypy. Use Sphinx builder and return URI,
				uri: str = cast(str,builder.get_relative_uri(from_docname, target_docname) + "#" + target_id)
				return uri
			except Exception as exc:
				warnings.warn(
					f"WTRL ref target '{qname}' resolved, but URI construction failed: {exc}",
					RuntimeWarning,
				)
				return None
# Fallback: Intra-page link.
		return "#" + target_id

	def _parse_ref_body(body: str) -> tuple[str, str]:
		"""Return the visible label and target from a Waterloo ref body."""
		m_ext = mod_docitem.RE_WTRL_ANGLE_HTTPS_REF_COMPILED.match(body)
		if m_ext:
			return m_ext.group(1).strip(), m_ext.group(2).strip()
		m_wtrl = mod_docitem.RE_WTRL_ANGLE_WTRL_REF_COMPILED.match(body)
		if m_wtrl:
			return m_wtrl.group(1).strip(), m_wtrl.group(2).strip()
		return body, ""

	def _repl(m: re.Match[str]) -> str:
		role = m.group(1)
		body = m.group(2)
		if role == "ref":
			label, target = _parse_ref_body(body)
			if target.startswith(("http://", "https://")):
				return f"`{label} <{target}>`_"
			if target.startswith("wtrl://"):
				qname = target[len("wtrl://"):]
# Resolve qualified name and build URI in Sphinx/reST style.
				uri = _resolve_wtrl_ref_uri(qname)
				if uri:
					return f"`{label} <{uri}>`_"
				return label
# Sphinx internal reference.
			return f":ref:`{body}`"
		return f":wtrl_{role}:`{body}`"

	def _replace_naked_tokens(segment: str) -> str:
		return RE_WTRL_NAKED_TOKEN_COMPILED.sub(lambda m: WTRL_TOKEN_REPLACEMENTS[m.group(1)], segment)

	out: List[str] = []
	i_pos = 0
	for m in mod_docitem.RE_WTRL_MARKUP_BACKTICK_COMPILED.finditer(text):
		out.append(_replace_naked_tokens(text[i_pos:m.start()]))
		out.append(_repl(m))
		i_pos = m.end()
	out.append(_replace_naked_tokens(text[i_pos:]))
	return "".join(out)
