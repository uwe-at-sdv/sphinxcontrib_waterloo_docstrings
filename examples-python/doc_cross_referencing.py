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
			* Semantics: This is a cross reference to a documented object.\
			For testing purposes, we use an unqualified name here, which\
			is resolved to the fully qualified name of the class B in this module.
		Reference to a documented object (different module):
			* Rendering: |ref|`build_sphinx_nodes <wtrl://sphinxcontrib.waterloo_docstrings.wtrl_autodoc.build_sphinx_nodes>`
		Reference to a web page:
			See |ref|`Python <https://www.python.org/>`
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
			* Semantics: This is a cross reference to a documented object.\
			For testing purposes, we use a fully qualified name here, which\
			is resolved to the fully qualified name of the class A in this module.
		Reference to a location in the document (same source file):
			* Rendering: |ref|`Directives <chapter_directives>`
			* Code: |lit|`\|ref\|\`Directives <chapter_directives>\``
			* Semantics: This is a cross reference to a location in the same file (here: |file|`functionality.rst`).
		Reference to a location in the document (different source file):
			* Rendering: |ref|`Introduction <chapter_introduction>`
			* Code: |lit|`\|ref\|\`Introduction <chapter_introduction>\``
			* Semantics: This is a cross reference to a location in a different file (here: |file|`introduction.rst`).
	"""
	pass

