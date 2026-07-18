from __future__ import annotations
from typing import Any, Callable, Dict, Final, get_type_hints, get_origin, get_args, Generator, Iterable, Iterator, List, Mapping, NewType, NoReturn, Protocol, Sequence, Set, Tuple, Type, TypeAlias, TypeGuard, Union, cast

from docutils import nodes

# Introduced in typing later than Python 3.10.
Struct: TypeAlias = Any

class InlinerDocumentSettings(Protocol):
	language_code: str
	env: Any


class InlinerDocument(Protocol):
	settings: InlinerDocumentSettings
	reporter: Any


class InlinerProtocol(Protocol):
	document: InlinerDocument
	reporter: Any

	def parse(self, text: str, lineno: int, memo: Struct, parent: nodes.Element) -> tuple[list[nodes.Node], list[nodes.Node]]: ...


class SphinxEnvProtocol(Protocol):
	docname: str
	docitem_context_configurator: Dict[str, Any] | None


class SphinxAppProtocol(Protocol):
	env: SphinxEnvProtocol
	config: Any
	docitem_context_configurator: Dict[str, Any] | None


class DirectiveStateProtocol(Protocol):
	inliner: InlinerProtocol
	document: InlinerDocument


class DirectiveLike(Protocol):
	state: DirectiveStateProtocol
	lineno: int
