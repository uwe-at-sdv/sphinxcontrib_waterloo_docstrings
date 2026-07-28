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
		|Must| provide protocol definitions for Sphinx Inliner and Sphinx App objects to enable type checking and static analysis.
Notes:
	Usage:
		Do not import this module directly. Use the functions via the |ref|`extension <wtrl://sphinxcontrib.waterloo_docstrings.extension>` module instead.
"""
from __future__ import annotations
from typing import Any, Callable, Dict, Final, get_type_hints, get_origin, get_args, Generator, Iterable, Iterator, List, Mapping, NewType, NoReturn, Protocol, Sequence, Set, Tuple, Type, TypeAlias, TypeGuard, Union, cast

from docutils import nodes

# Introduced in typing later than Python 3.10.
Struct: TypeAlias = Any

# Required by InlinerDocument.
class InlinerDocumentSettings(Protocol):
	language_code: str
	env: Any

# Required by InlinerProtocol.
class InlinerDocument(Protocol):
	settings: InlinerDocumentSettings
	reporter: Any

class InlinerProtocol(Protocol):
	r"""
	Preamble:
		profile:
			class
		normative_sections:
			Contract
	Contract:
		general:
			|Must| describe the subset of the Docutils/Sphinx inliner interface used by Waterloo role and directive rendering.
			|Must| expose the document and reporter attributes used by helper functions that parse inline markup.
			|Must| expose a parse method that converts inline reStructuredText into Docutils nodes.
			|Must| be used for structural typing and developer documentation only.
		constructor:
	Notes:
		Runtime:
			This protocol is structural and is not instantiated by the extension.
			Sphinx provides the concrete object at runtime.

	"""
	document: InlinerDocument
	reporter: Any

	def parse(self, text: str, lineno: int, memo: Struct, parent: nodes.Element) -> tuple[list[nodes.Node], list[nodes.Node]]: ...

class SphinxEnvProtocol(Protocol):
	r"""
	Preamble:
		profile:
			class
		normative_sections:
			Contract
	Contract:
		general:
			|Must| describe the subset of the Sphinx build-environment interface used by this extension.
			|Must| expose the current document name used for diagnostics and context-sensitive rendering.
			|Must| expose the Waterloo context configurator storage used while rendering directives and roles.
			|Must| be used for structural typing and developer documentation only.
		constructor:
	Notes:
		Runtime:
			This protocol is structural and is not instantiated by the extension.
			Sphinx provides the concrete object at runtime.

	"""
	docname: str
	docitem_context_configurator: Dict[str, Any] | None

class SphinxAppProtocol(Protocol):
	r"""
	Preamble:
		profile:
			class
		normative_sections:
			Contract
	Contract:
		general:
			|Must| describe the subset of the Sphinx application interface used by this extension.
			|Must| expose the build environment, configuration object, and Waterloo context configurator storage.
			|Must| provide the structural shape expected by directive, state, signature, and autodoc helpers.
			|Must| be used for structural typing and developer documentation only.
		constructor:
	Notes:
		Runtime:
			This protocol is structural and is not instantiated by the extension.
			Sphinx provides the concrete object at runtime.

	"""
	env: SphinxEnvProtocol
	config: Any
	docitem_context_configurator: Dict[str, Any] | None
