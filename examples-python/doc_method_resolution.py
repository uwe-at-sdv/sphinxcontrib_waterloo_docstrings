r"""
Preamble:
	profile:
		module
	normative_sections:
		Contract, Public_classes, Public_functions, Public_constants
Contract:
	general:
Public_classes:
	A, B, X, Y
Public_functions:
Public_constants:
	CONSTANT_1:
		An important constant
	CONSTANT_2:
		Another important constant
"""

from __future__ import annotations
from typing import Dict, Final, List, TypeAlias

CONSTANT_1: Final[int] = 42
CONSTANT_2: Final[int] = 1337

class A:
	r"""
	Preamble:
		profile:
			class
		normative_sections:
			Contract, Public_variables, Public_methods
	Contract:
		general:
		constructor:
	Public_variables:
		v:
			A variable
	Public_methods:
		m
	Method_overview:
		m:
			A method
	"""
	class INSIDE_A:
		r"""
		Preamble:
			profile:
				class
			normative_sections:
				Contract, Public_constants
		Contract:
			general:
			constructor:
		Public_constants:
			INSIDE_A_CONSTANT_1:
				An important constant
			INSIDE_A_CONSTANT_2:
				Another important constant
		"""
		INSIDE_A_CONSTANT_1: Final[int] = 111
		INSIDE_A_CONSTANT_2: Final[int] = 222
	v: int = 123
	def m(self) -> None:
		r"""
		Preamble:
			profile:
				method
			normative_sections:
				Contract, Parameters, Returns, Raises
		Contract:
			general:
		Parameters:
		Returns:
		Raises:
		See_also:
			B.m, B.v, Y.INSIDE_Y.INSIDE_Y_TYPE_1, Y.INSIDE_Y.INSIDE_Y_TYPE_2
		"""
		pass

class B:
	r"""
	Preamble:
		profile:
			class
		normative_sections:
			Contract, Public_variables, Public_methods
	Contract:
		general:
		constructor:
	Public_variables:
		v:
			A variable
	Public_methods:
		m
	Method_overview:
		m:
			A method
	"""
	v: int = 456
	def m(self) -> None:
		r"""
		Preamble:
			profile:
				method
			normative_sections:
				Contract, Parameters, Returns, Raises
		Contract:
			general:
		Parameters:
		Returns:
		Raises:
		See_also:
			A.m, A.v, A.INSIDE_A.INSIDE_A_CONSTANT_1, A.INSIDE_A.INSIDE_A_CONSTANT_2
		"""
		pass

class X:
	r"""
	Preamble:
		profile:
			class
		normative_sections:
			Contract, Public_variables, Public_methods
	Contract:
		general:
		constructor:
	Public_variables:
		v:
			A variable
	Public_methods:
		m
	Method_overview:
		m:
			A method
	"""
	v: int = 777
	def m(self) -> None:
		r"""
		Preamble:
			profile:
				method
			normative_sections:
				Contract, Parameters, Returns, Raises
		Contract:
			general:
		Parameters:
		Returns:
		Raises:
		See_also:
			Y.m, Y.v, CONSTANT_1, CONSTANT_2
		"""
		pass

class Y:
	r"""
	Preamble:
		profile:
			class
		normative_sections:
			Contract, Public_variables, Public_methods
	Contract:
		general:
		constructor:
	Public_variables:
		v:
			A variable
	Public_methods:
		m
	Method_overview:
		m:
			A method
	"""
	class INSIDE_Y:
		r"""
		Preamble:
			profile:
				class
			normative_sections:
				Contract, Public_types
		Contract:
			general:
			constructor:
		Public_types:
			INSIDE_Y_TYPE_1:
				An important type
			INSIDE_Y_TYPE_2:
				Another important type
		"""
		INSIDE_Y_TYPE_1: TypeAlias = List[int]
		INSIDE_Y_TYPE_2: TypeAlias = Dict[str, float]
	v: int = 888
	def m(self) -> None:
		r"""
		Preamble:
			profile:
				method
			normative_sections:
				Contract, Parameters, Returns, Raises
		Contract:
			general:
		Parameters:
		Returns:
		Raises:
		See_also:
			X.m, X.v, CONSTANT_1, CONSTANT_2
		"""
		pass