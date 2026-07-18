from __future__ import annotations
from typing import Any, Callable, Dict, Final, List, Mapping, Sequence, TypeAlias, cast

from docutils.parsers.rst import roles

from dataclasses import dataclass
from docutils import nodes


from sphinxcontrib.waterloo_docstrings.wtrl_protocol import (
	InlinerProtocol,
	)

class context_roles:
	def __init__(self) -> None:
		pass
# We used to initialize these each time a context is created.
# Now they are static in the class, yet since they are called
# for an object ctx, we add a pro-forma parameter slf in the lambdas.
	add_role_attr = lambda slf,t:f":wtrl_attr:`{t}`"
	add_role_class = lambda slf,t:f":wtrl_class:`{t}`"
	add_role_cmd = lambda slf,t:f":wtrl_cmd:`{t}`"
	add_role_dfn = lambda slf,t:f":wtrl_dfn:`{t}`"
	add_role_file = lambda slf,t:f":wtrl_file:`{t}`"
	add_role_func = lambda slf,t:f":wtrl_func:`{t}`"
	add_role_key = lambda slf,t:f":wtrl_key:`{t}`"
	add_role_label = lambda slf,t:f":wtrl_label:`{t}`"
	add_role_lit = lambda slf,t:f":wtrl_lit:`{t}`"
	add_role_mod = lambda slf,t:f":wtrl_mod:`{t}`"
	add_role_norm = lambda slf,t:f":wtrl_norm:`{t}`"
	add_role_op = lambda slf,t:f":wtrl_op:`{t}`"
	add_role_opt = lambda slf,t:f":wtrl_opt:`{t}`"
	add_role_pkg = lambda slf,t:f":wtrl_pkg:`{t}`"
	add_role_tag = lambda slf,t:f":wtrl_tag:`{t}`"
	add_role_term = lambda slf,t:f":wtrl_term:`{t}`"
	add_role_type = lambda slf,t:f":wtrl_type:`{t}`"
	add_role_url = lambda slf,t:f":wtrl_url:`{t}`"
	add_role_value = lambda slf,t:f":wtrl_value:`{t}`"
	add_role_var = lambda slf,t:f":wtrl_var:`{t}`"
	add_role_var_type = lambda slf,t:f":wtrl_var_type:`{t}`"

# Just in order to avoid endless repetition of the same parameters in the role functions below.
@dataclass(frozen=True)
class RolePara:
	name: str
	rawtext: str
	text: str
	lineno: int
	inliner: InlinerProtocol
	options: Mapping[str,Any] | None
	content: list[str] | None

# This is a pair: the first list is the list of nodes to insert into the document,
# and the second list is a list of system messages (errors, warnings, etc.)
# that may have been generated during processing.
RoleResult = tuple[List[nodes.Node], list[nodes.Node]]

# Common role handler signature used by Docutils/Sphinx roles
RoleHandler: TypeAlias = Callable[..., tuple[Sequence[nodes.reference], Sequence[nodes.reference]]]

# We distinguish between literal and inline nodes to let the theme decide styling:
# literal nodes are typically rendered in monospace, inline nodes in regular font.
# This gives theme designers the flexibility to style these semantic distinctions.
# We also add CSS classes prefixed with "wtrl_" for cases where we need to override
# the theme's default styling, but modern themes like Furo usually handle this well
# without additional CSS customization.

def wtrl_attr_role(para: RolePara) -> RoleResult:
	r"""
	Preamble:
		profile:
			function
		normative_sections:
			Contract, Parameters, Returns, Raises
	Contract:
		general:
			|Must| create a |type|`docutils.nodes.literal` node with the text in |var|`para.text` and the CSS class |value|`wtrl_attr`.
	Parameters:
		para:
			|class|`RolePara` instance containing the role parameters.
	Returns:
		A tuple containing a list with the created |type|`docutils.nodes.literal` node and an empty list of system messages.
	Raises:
		BaseException:
			|May| propagate exceptions from |type|`docutils`.
	Notes:
		Examples:
			* JSON: { \"|attr|`my_attribute`\": \"|value|`my_value`\" }
	"""
	node = nodes.literal(para.text, para.text, classes=["wtrl_attr"])
	return [node], []

def wtrl_class_role(para: RolePara) -> RoleResult:
	node = nodes.literal(para.text, para.text, classes=["wtrl_class"])
	return [node], []

def wtrl_cmd_role(para: RolePara) -> RoleResult:
	node = nodes.literal(para.text, para.text, classes=["wtrl_cmd"])
	return [node], []

# inline, not literal
def wtrl_dfn_role(para: RolePara) -> RoleResult:
	node = nodes.inline(para.text, para.text, classes=["wtrl_dfn"])
	return [node], []

def wtrl_file_role(para: RolePara) -> RoleResult:
	node = nodes.literal(para.text, para.text, classes=["wtrl_file"])
	return [node], []

def wtrl_func_role(para: RolePara) -> RoleResult:
	node = nodes.literal(para.text, para.text, classes=["wtrl_func"])
	return [node], []

def wtrl_key_role(para: RolePara) -> RoleResult:
	node = nodes.literal(para.text, para.text, classes=["wtrl_key"])
	return [node], []

# inline, not literal
def wtrl_label_role(para: RolePara) -> RoleResult:
	node = nodes.inline(para.text, para.text, classes=["wtrl_label"])
	return [node], []

def wtrl_lit_role(para: RolePara) -> RoleResult:
	node = nodes.literal(para.text, para.text, classes=["wtrl_lit"])
	return [node], []

def wtrl_mod_role(para: RolePara) -> RoleResult:
	node = nodes.literal(para.text, para.text, classes=["wtrl_mod"])
	return [node], []

# inline, not literal
def wtrl_norm_role(para: RolePara) -> RoleResult:
	node = nodes.inline(para.text, para.text, classes=["wtrl_norm"])
	return [node], []

def wtrl_op_role(para: RolePara) -> RoleResult:
	node = nodes.literal(para.text, para.text, classes=["wtrl_op"])
	return [node], []

def wtrl_opt_role(para: RolePara) -> RoleResult:
	node = nodes.literal(para.text, para.text, classes=["wtrl_opt"])
	return [node], []

def wtrl_pkg_role(para: RolePara) -> RoleResult:
	node = nodes.literal(para.text, para.text, classes=["wtrl_pkg"])
	return [node], []

def wtrl_tag_role(para: RolePara) -> RoleResult:
	node = nodes.literal(para.text, para.text, classes=["wtrl_tag"])
	return [node], []

# inline, not literal
def wtrl_term_role(para: RolePara) -> RoleResult:
	node = nodes.inline(para.text, para.text, classes=["wtrl_term"])
	return [node], []

def wtrl_type_role(para: RolePara) -> RoleResult:
	node = nodes.literal(para.text, para.text, classes=["wtrl_type"])
	return [node], []

def wtrl_url_role(para: RolePara) -> RoleResult:
	node = nodes.literal(para.text, para.text, classes=["wtrl_url"])
	return [node], []

def wtrl_value_role(para: RolePara) -> RoleResult:
	node = nodes.literal(para.text, para.text, classes=["wtrl_value"])
	return [node], []

def wtrl_var_role(para: RolePara) -> RoleResult:
	node = nodes.literal(para.text, para.text, classes=["wtrl_var"])
	return [node], []

def wtrl_var_type_role(para: RolePara) -> RoleResult:
	r"""
	Preamble:
		profile:
			function
		normative_sections:
			Contract, Parameters, Returns, Raises
	Contract:
		general:
			|Must| parse the text in |var|`para.text` as a variable name and type separated by a colon.
			|Must| create a list of |type|`docutils.nodes.Node` representing the variable name, the colon, and the type with appropriate CSS classes.
			|May| report an error if the text does not contain a colon or if either the variable name or type is empty.
	Parameters:
		para:
			|class|`RolePara` instance containing the role parameters.
	Returns:
		A tuple containing a list of |type|`docutils.nodes.Node` representing the variable name and type,
		and a list of system messages (errors, warnings, etc.) that |may| have been generated during processing.
	Raises:
	Notes:
		Examples:
			* |var_type|`n: int`
			* |var_type|`q: float`
			* |var_type|`para: RolePara`
			* |var_type|`result: tuple[List[nodes.Node], list[nodes.Node]]`
	"""
	if ":" not in para.text:
		msg = para.inliner.reporter.error(
		 f"wtrl_var_type expects 'var:type', got '{para.text}'",
		 line=para.lineno,
		)
		return [], [msg]

	var, type_ = (s.strip() for s in para.text.split(":", 1))
	if not var or not type_:
		msg = para.inliner.reporter.error(
		 f"wtrl_var_type expects 'var:type' with non-empty var and type, got '{para.text}'",
		 line=para.lineno,
		)
		return [], [msg]

	node = nodes.inline('', '', classes=["wtrl_var_type"])
	node += nodes.inline(var, var, classes=["wtrl_var"])
	node += nodes.inline(": ", ": ", classes=["wtrl_op"])
	node += nodes.inline(type_, type_, classes=["wtrl_type"])
	return [node], []


role_map: Final[Dict[str,Callable[[RolePara],RoleResult]]] = {
	"wtrl_attr":wtrl_attr_role,
	"wtrl_class":wtrl_class_role,
	"wtrl_cmd":wtrl_cmd_role,
	"wtrl_dfn":wtrl_dfn_role,
	"wtrl_file":wtrl_file_role,
	"wtrl_func":wtrl_func_role,
	"wtrl_key":wtrl_key_role,
	"wtrl_label":wtrl_label_role,
	"wtrl_lit":wtrl_lit_role,
	"wtrl_mod":wtrl_mod_role,
	"wtrl_norm":wtrl_norm_role,
	"wtrl_op":wtrl_op_role,
	"wtrl_opt":wtrl_opt_role,
	"wtrl_pkg":wtrl_pkg_role,
	"wtrl_tag":wtrl_tag_role,
	"wtrl_term":wtrl_term_role,
	"wtrl_type":wtrl_type_role,
	"wtrl_url":wtrl_url_role,
	"wtrl_value":wtrl_value_role,
	"wtrl_var":wtrl_var_role,
	"wtrl_var_type":wtrl_var_type_role,
	}

# Parameter `app` not required here, but we leave it just in case.
def setup_roles(app: Any) -> None:
	for name,func in role_map.items():
		roles.register_local_role(name, cast(RoleHandler,
			lambda	name, rawtext, text, lineno, inliner, options=None, content=None, func=func:
				func(RolePara(name=name, rawtext=rawtext, text=text, lineno=lineno, inliner=inliner, options=options, content=content))))

