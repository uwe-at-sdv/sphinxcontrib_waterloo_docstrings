r"""
Preamble:
	profile:
		module
	normative_sections:
		Contract
Contract:
	general:
		|Must| provide a smoke test for the Sphinx extension
"""

# Base classes with simple waterloo docstrings to test the Sphinx extension.
class A:
	r"""
	Preamble:
		profile:
			class
		normative_sections:
			Contract
	Contract:
		general:
		constructor:
	"""
	def spam(self,a: int, b: float) -> str:
		r"""
		Preamble:
			profile:
				method
			normative_sections:
				Contract, Parameters, Returns, Raises
		Contract:
			general:
		Parameters:
			a:
				an integer
			b:
				a float
		Returns:
			The concatentation of the string representations of a and b.
		Raises:
		"""
		return f"{a} {b}"
class B:
	r"""
	Preamble:
		profile:
			class
		normative_sections:
			Contract
	Contract:
		general:
		constructor:
	"""
	pass

class X(A,B):
	r"""
	Preamble:
		profile:
			class
		normative_sections:
			Contract, Derived_from
	Contract:
		general:
		constructor:
	Derived_from:
		A, B
			"""
	def spam(self,a: int, b: float) -> str:
		r"""
		Preamble:
			profile:
				inherited_method
			normative_sections:
				Contract, Returns
		Contract:
			general:
				|Must| demonstrate how the Sphinx extension handles inherited methods.
				|Must| extend the base method's return value with "inherited".
			base:
				A.spam
		"""
		return f"inherited {a} {b}"
