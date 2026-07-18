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

