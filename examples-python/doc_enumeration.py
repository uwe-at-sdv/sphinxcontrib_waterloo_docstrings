def myfunc(a: int, b: float, c: str) -> None:
	r"""
	Preamble:
		profile:
			function
		normative_sections:
			Definitions, Contract, Parameters, Returns, Raises
		status:
			stable
		scope:
			public
	Description:
		This function exists only as a compact rendering showcase.
		Text-like Waterloo sections fall into two rendering groups.
		* Contract-style sections are rendered as bullet lists by default.
		+ This group includes |label|`Contract.general`, |label|`Contract.requires`, |label|`Contract.ensures`, |label|`Contract.invariants`, and |label|`Raises`.
		+ Entries in these sections are logical lines and do not support nested visual list levels.
		* Free-form sections support explicit visual list markers.
		+ This group includes |label|`Description`, |label|`Notes`, |label|`Definitions`, |label|`Terminology`, |label|`Parameters`, and |label|`Returns`.
		# Enumeration can be mixed into the same explicit marker hierarchy.
		# Consecutive enumeration entries form one visual enumeration block.
		+ After enumeration, itemization can continue at the previous level.
		* The surrounding section remains ordinary free-form text.
	Notes:
		Format:
			The Waterloo Docstrings |ref|`standard document <https://uwe-at-sdv.github.io/sdv_doc_waterloo/>` describes the syntax for itemization and enumeration.
			Nested visual lists are expressed with explicit list markers, not by adding indentation.
			The markers |lit|`*`, |lit|`+`, and |lit|`-` express itemization levels.
			The marker |lit|`#` expresses enumeration.
			Indentation remains reserved for the logical structure of the docstring.
		General note:
			Subsections in |label|`Notes` are rendered as free-form text.
			The free-form renderer supports explicit itemization and enumeration.
			* An item
			+ A sub-item
			# A sub-sub-item
			# Another sub-sub-item
			+ Another sub-item
			* Another item
	Contract:
		general:
			|Must| demonstrate which sections are rendered as contract-style bullet lists.
			|Must| demonstrate which sections are rendered as free-form text.
			|Must| keep contract entries as logical lines, not as nested visual lists.
		requires:
			|var|`a` |must| be even.
			|var|`b` |must| be larger than |value|`0`.
			|var|`c` |must| be a string in lowercase.
		ensures:
			The function |must| return |None|.
			The function |must| leave its inputs unchanged.
		invariants:
			The showcase |must| remain deterministic.
	Definitions:
		ExampleTerm:
			Definitions are free-form text.
			The renderer supports explicit itemization in definition content.
			* An item
			+ A sub-item
			- A sub-sub-item
			- Another sub-sub-item
			+ Another sub-item
			* Another item
	Terminology:
		Example term:
			Terminology is free-form text.
			The renderer supports explicit itemization in terminology content.
			* An item
			+ A sub-item
			- A sub-sub-item
			- Another sub-sub-item
			+ Another sub-item
			* Another item
	Parameters:
		a:
			Parameter descriptions are free-form text.
			The renderer supports explicit itemization in parameter content.
			* An item
			+ A sub-item
			- A sub-sub-item
			- Another sub-sub-item
			+ Another sub-item
			* Another item
		b:
			Enumeration is available as a visual list form.
			Numbering uses a single marker, not nested numeric labels such as |lit|`1.1`.
			# First enumerated item
			* A sub-item
			* Another sub-item
			# Second enumerated item
		c:
			Enumeration can appear below itemization levels.
			* An item
			+ A sub-item
			# A sub-sub-item
			# Another sub-sub-item
			+ Another sub-item
			* Another item
	Returns:
		The Returns section is free-form text.
		The renderer supports explicit itemization and enumeration in return descriptions.
		* An item
		+ A sub-item
		# A sub-sub-item
		# Another sub-sub-item
		+ Another sub-item
		* Another item
	Raises:
		BaseException:
			The |label|`Raises` section is rendered as a contract-style bullet list by default.
			Entries in this subsection are logical lines, not nested visual lists.
			|Must| raise if |lit|`<condition 1>`
			|Should| raise if |lit|`<condition 2>`
			|May| raise if |lit|`<condition 3>`
	See_also:
		list.of.qualified.identifiers, therefore.no.itemization.or.enumeration
	"""
	pass
