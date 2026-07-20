class A:
	r"""
	Preamble:
		profile:
			class
		normative_sections:
			Contract
	Contract:
		general:
			|Must| contain cross references for demonstration purposes.
		constructor:
	Notes:
		Reference to a documented object (same module):
			* Rendering: |ref|`B <wtrl://B>`
			* Code: |lit|`\|ref\|\`B <wtrl://B>\``
			* Semantics: Cross reference to a documented object.\
			For testing purposes, we use an unqualified name here, which\
			is resolved to the fully qualified name of the class B in this module.
		Reference to a documented object (different module):
			* Rendering: |ref|`build_sphinx_nodes <wtrl://sphinxcontrib.waterloo_docstrings.wtrl_autodoc.build_sphinx_nodes>`
			* Code: |lit|`\|ref\|\`build_sphinx_nodes <wtrl://sphinxcontrib.waterloo_docstrings.wtrl_autodoc.build_sphinx_nodes>\``
			* Semantics: Cross reference to a documented object.
			* Note: Forward reference.
		Reference to a non-existing object:
			* Rendering: |ref|`nonexisting_function <wtrl://sphinxcontrib.waterloo_docstrings.wtrl_autodoc.nonexisting_function>`
		Reference to a web page:
			* Rendering: |ref|`Python <https://www.python.org/>`
			* Code: |lit|`\|ref\|\`Python <https://www.python.org/>\``
			* Semantics: Cross reference to a web page.
				"""
	pass

class B:
	r"""
	Preamble:
		profile:
			class
		normative_sections:
			Contract
	Contract:
		general:
			|Must| contain cross references for demonstration purposes.
		constructor:
	Notes:
		Reference to a documented object:
			* Rendering: |ref|`A <wtrl://doc_cross_referencing.A>`
			* Code: |lit|`\|ref\|\`A <wtrl://doc_cross_referencing.A>\``
			* Semantics: Cross reference to a documented object.\
			For testing purposes, we use a fully qualified name here, which\
			is resolved to the fully qualified name of the class A in this module.
		Reference to a location in the document (same source file):
			* Rendering: |ref|`Directives <chapter_directives>`
			* Code: |lit|`\|ref\|\`Directives <chapter_directives>\``
			* Semantics: Cross reference to a location in the same file (here: |file|`roles.rst`).
		Reference to a non-existing location in the document:
			* Rendering: |ref|`Nowhere <chapter_nowhere>`
			* Code: |lit|`\|ref\|\`Nowhere <chapter_nowhere>\``
		Reference to a location in the document (different source file):
			* Rendering: |ref|`Introduction <chapter_introduction>`
			* Code: |lit|`\|ref\|\`Introduction <chapter_introduction>\``
			* Semantics: Cross reference to a location in a different file (here: |file|`introduction.rst`).
	"""
	pass

