r"""
Preamble:
	profile:
		module
	normative_sections:
		Contract
Contract:
	general:
		|Must| demonstrate various error conditions and show how they are rendered in the Sphinx output.
"""

class X_no_docstring:
	pass

class X_empty_docstring:
	r"""
	"""
	pass

class X_not_a_wtrl_docstring:
	r"""
	Some text that is not a Waterloo Docstring.
	It does not contain a Preamble section.
	"""
	pass

class X_bad_contract:
	r"""
	Preamble:
		profile:
			class
		normative_sections:
			Contract
	Contract:
	"""
	pass

class X_not_in_public_scope:
	r"""
	Preamble:
		profile:
			class
		scope:
			extension
		normative_sections:
			Contract
	Contract:
		general:
			|Must| demonstrate that scope extension is not allowed in a class docstring.
		constructor:
			default
	"""
	pass