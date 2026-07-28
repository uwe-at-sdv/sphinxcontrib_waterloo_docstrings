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
		|Must| provide a function for inline parsing using a Sphinx Inliner object.
Notes:
	Usage:
		Do not import this module directly. Use the functions via the |ref|`extension <wtrl://sphinxcontrib.waterloo_docstrings.extension>` module instead.
"""
from __future__ import annotations
from typing import List

from sphinxcontrib.waterloo_docstrings.wtrl_protocol import (
	InlinerProtocol,
	)
from docutils import nodes
from docutils.parsers.rst import languages
from docutils.parsers.rst import states as rst_states

# Inline-Parser, der *messages nicht wegwirft*
def parse_inline(inliner: InlinerProtocol, parent: nodes.Element, ln: int, txt: str) -> List[nodes.Node]:
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
			|Must| parse inline reStructuredText content and preserve warning and error messages.
			|Must| append all generated messages to the parent element as child nodes.
			|Must| return all parsed content nodes without discarding messages.
	Description:
		This function wraps inliner.parse() to ensure that any warning or error messages
		generated during the parsing process are captured and added to the document tree
		instead of being silently discarded.
	Parameters:
		inliner:
			An inline element parser implementing InlinerProtocol. |Must| have a parse method
			and a document attribute with settings and reporter attributes.
		parent:
			The parent Element to which parsed content and messages will be appended.
		ln:
			The line number (integer) where the txt input begins in the source document.
		txt:
			The reStructuredText source string (str) to be parsed for inline markup.
	Returns:
		List of parsed docutils.nodes.Node instances representing the content found in txt.
		The returned list is created from the parse output; warning and error messages are
		appended directly to parent and not returned as part of the list.
	Raises:
		BaseException:
			Exceptions from underlying RST parsing or document handling |may| propagate depending on the inliner implementation.
	Notes:
		Key difference from direct inliner.parse() calls:
			This function always preserves document messages in the tree. Direct calls to
			inliner.parse() may discard messages, leading to silent data loss in warnings
			and error conditions.
	"""
	lang = languages.get_language(inliner.document.settings.language_code)

	memo_factory = getattr(rst_states, "Struct")
	memo = memo_factory(
	 document=inliner.document,
	 reporter=inliner.reporter,
	 language=lang,
	 title_styles=[],
	 section_level=0,
	 section_bubble_up_kludge=False,
	 inliner=inliner,
	)

	nodes_out, messages = inliner.parse(txt, ln, memo, parent)
	result: List[nodes.Node] = list(nodes_out)
	for msg in messages:
		parent += msg
	return result

