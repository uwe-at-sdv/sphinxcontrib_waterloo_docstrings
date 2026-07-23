r"""
Preamble:
	profile:
		module
	normative_sections:
		Contract,
		Public_classes,
		Public_functions
Description:
	This module provides the Sphinx integration layer for the Waterloo documentation system.
	|
	The implementation operates directly on Docutils nodes and defines custom Docutils roles
	to generate structured documentation output from Waterloo-style docstrings.
	|
	Sphinx is used as the execution and rendering framework, but the internal data model is based
	on the Docutils abstract syntax tree (AST). All document structure, including sections,
	tables, lists, rubrics, and inline markup, is represented using Docutils node classes.
	|
	The module introduces a configurable |type|`context` object which encapsulates all
	project-specific presentation logic, including role expansion, symbol rendering, and
	HTML layout decisions. This context is configured by the target project via its
	|file|`conf.py` and is intentionally decoupled from the core implementation.
	|
	To support concise and unambiguous normative documentation, the module maintains explicit
	scope stacks with the semantics "current module" and "current class". These scopes define
	the implicit ownership of subsequently documented functions and methods and are modified
	using dedicated Docutils roles or directives.
	|
	The primary goal of this module is correctness, completeness, and reproducibility of
	normative documentation. Readability and visual presentation are considered secondary
	and are handled through configurable rendering layers.
Terminology:
	Docutils node:
		An element of the Docutils abstract syntax tree (AST),
		such as |type|`paragraph`, |type|`section`, or |type|`literal`.
	Docutils role:
		An inline markup construct of the form ``:role:`content``` implemented
		using the Docutils role API. Custom roles provided by this module are
		registered via Sphinx but conceptually belong to Docutils.
	Sphinx extension:
		A Python module loaded by Sphinx to extend its parsing, transformation,
		or rendering behavior. This module is implemented as a Sphinx extension
		but operates primarily on Docutils data structures.
Contract:
	general:
		|Must| provide classes and functions for buidling Docutils nodes from docstring trees.
		|Must| provide a default layout for HTML output from Sphinx.
		|Must| provide a class |type|`context` which provides abstract roles to be configured by the target project's |file|`conf.py`.
		|Must| provide a function for building Docutils nodes from a module docstring in waterloo format.
		|Must| provide a function for building Docutils nodes from a function docstring in waterloo format.
		|Must| provide a function for building Docutils nodes from a class docstring in waterloo format.
		|Must| provide a function for building Docutils nodes from a class docstring and the class' method docstrings in waterloo format.
		|Must| provide a Docutils role for rendering a function prototype.
		|Must| provide a Docutils role for rendering a method prototype.
		|Must| maintain a stack with semantics "current module" and |func|`push`-, |func|`pop`-, |func|`get`-methods.
		|Must| maintain a stack with semantics "current class" and |func|`push`-, |func|`pop`-, |func|`get`-methods.
		|Must| provide Docutils roles or directives for modifying these stacks.
Public_classes:
	context
Class_overview:
	context:
		Internal class, please ignore
Public_functions:
	build_sphinx_nodes,
	build_sphinx_nodes_full,
	resolve_qualified_name,
	wtrl_build_autodoc_module_nodes,
	wtrl_build_autodoc_function_nodes,
	wtrl_build_autodoc_class_nodes,
	wtrl_build_autodoc_class_full_nodes,

	wtrl_build_push_current_module_nodes,
	wtrl_build_push_current_class_nodes,
	wtrl_build_push_current_scope_nodes,
	wtrl_build_pop_current_module_nodes,
	wtrl_build_pop_current_class_nodes,
	wtrl_build_pop_current_scope_nodes,

	wtrl_build_method_signature_nodes,
	wtrl_build_function_signature_nodes,
	wtrl_build_method_signature_block_nodes,
	wtrl_build_function_signature_block_nodes,

	wtrl_attr_role,
	wtrl_class_role,
	wtrl_cmd_role,
	wtrl_dfn_role,
	wtrl_file_role,
	wtrl_func_role,
	wtrl_label_role,
	wtrl_lit_role,
	wtrl_mod_role,
	wtrl_norm_role,
	wtrl_op_role,
	wtrl_opt_role,
	wtrl_tag_role,
	wtrl_type_role,
	wtrl_value_role,
	wtrl_var_role,
	wtrl_var_type_role,

Function_overview:
	build_sphinx_nodes:
		Build a list of Docutils nodes from a docstring tree.
	build_sphinx_nodes_full:
		Build a list of Docutils nodes of a class object and its member functions from a docstring tree.
	resolve_qualified_name:
		Analyze a qualified name and return the object it refers to plus resolved name components.

	wtrl_build_autodoc_module_nodes:
		Implementation of role |attr|`.. wtrl_autodoc_module::`
	wtrl_build_autodoc_function_nodes:
		Implementation of role |attr|`.. wtrl_autodoc_function::`
	wtrl_build_autodoc_class_nodes:
		Implementation of role |attr|`.. wtrl_autodoc_class::`
	wtrl_build_autodoc_class_full_nodes:
		Implementation of role |attr|`.. wtrl_autodoc_class_full::`

	wtrl_build_push_current_module_nodes:
		Implementation of directive |attr|`.. wtrl_push_current_module::`
	wtrl_build_push_current_class_nodes:
		Implementation of directive |attr|`.. wtrl_push_current_class::`
	wtrl_build_push_current_scope_nodes:
		Implementation of directive |attr|`.. wtrl_push_current_scope::`
	wtrl_build_pop_current_module_nodes:
		Implementation of directive |attr|`.. wtrl_pop_current_module::`
	wtrl_build_pop_current_class_nodes:
		Implementation of directive |attr|`.. wtrl_pop_current_class::`
	wtrl_build_pop_current_scope_nodes:
		Implementation of directive |attr|`.. wtrl_pop_current_scope::`

	wtrl_build_method_signature_nodes:
		Implementation of directive |attr|`.. wtrl_method_signature::`
		Render a method signature with optional class context and inline markup.
		Rendering in a single line can be inconvenient for long signatures; consider using |func|`wtrl_build_method_signature_block_nodes`.
	wtrl_build_function_signature_nodes:
		Implementation of directive |attr|`.. wtrl_function_signature::`
		Render a function signature with inline markup.
		Rendering in a single line can be inconvenient for long signatures; consider using |func|`wtrl_build_function_signature_block_nodes`.
	wtrl_build_method_signature_block_nodes:
		Implementation of directive |attr|`.. wtrl_method_signature_block::`
		Render a method signature with optional class context and inline markup in a block layout.
	wtrl_build_function_signature_block_nodes:
		Implementation of directive |attr|`.. wtrl_function_signature_block::`
		Render a function signature with inline markup in a block layout.

	wtrl_attr_role:
		Implementation of role |attr|`:wtrl_attr:`
	wtrl_class_role:
		Implementation of role |attr|`:wtrl_class:`
	wtrl_cmd_role:
		Implementation of role |attr|`:wtrl_cmd:`
	wtrl_dfn_role:
		Implementation of role |attr|`:wtrl_dfn:`
	wtrl_file_role:
		Implementation of role |attr|`:wtrl_file:`
	wtrl_func_role:
		Implementation of role |attr|`:wtrl_func:`
	wtrl_label_role:
		Implementation of role |attr|`:wtrl_label:`
	wtrl_lit_role:
		Implementation of role |attr|`:wtrl_lit:`
	wtrl_mod_role:
		Implementation of role |attr|`:wtrl_mod:`
	wtrl_norm_role:
		Implementation of role |attr|`:wtrl_norm:`
	wtrl_op_role:
		Implementation of role |attr|`:wtrl_op:`
	wtrl_opt_role:
		Implementation of role |attr|`:wtrl_opt:`
	wtrl_tag_role:
		Implementation of role |attr|`:wtrl_tag:`
	wtrl_type_role:
		Implementation of role |attr|`:wtrl_type:`
	wtrl_value_role:
		Implementation of role |attr|`:wtrl_value:`
	wtrl_var_role:
		Implementation of role |attr|`:wtrl_var:`
	wtrl_var_type_role:
		Implementation of role |attr|`:wtrl_var_type:`
Notes:
	Last reviewed:
		2026-07-16
"""

from __future__ import annotations
from importlib.metadata import PackageNotFoundError, version
from typing import Any, List, TypeAlias

import sys
from pathlib import Path

from docutils import nodes
from typing import no_type_check
from sphinx.util.nodes import make_refnode
from sphinx.util import logging

import sdv.doc.waterloo.docitem as mod_docitem

from sphinxcontrib.waterloo_docstrings.wtrl_context import (
	context,
	make_context
	)
# We must import these, since they are auto-documented.
from sphinxcontrib.waterloo_docstrings.wtrl_state import (
	resolve_qualified_name,
	wtrl_build_push_current_module_nodes,
	wtrl_build_push_current_class_nodes,
	wtrl_build_push_current_scope_nodes,
	wtrl_build_pop_current_module_nodes,
	wtrl_build_pop_current_class_nodes,
	wtrl_build_pop_current_scope_nodes,
	has_current_scope,
	get_current_scope,
	get_current_scope_set,
	is_target_obj_visible_in_current_scope
	)
from sphinxcontrib.waterloo_docstrings.wtrl_directives import (
	setup_directives
	)
from sphinxcontrib.waterloo_docstrings.wtrl_markup import (
	setup_markup_roles,
	wtrl_pending_ref,
	)
# We must import these, since they are auto-documented.
from sphinxcontrib.waterloo_docstrings.wtrl_parse import (
	parse_inline
	)
# Functions. We must import these, since they are auto-documented.
from sphinxcontrib.waterloo_docstrings.wtrl_roles import (
	wtrl_attr_role,
	wtrl_class_role,
	wtrl_cmd_role,
	wtrl_dfn_role,
	wtrl_file_role,
	wtrl_func_role,
	wtrl_key_role,
	wtrl_label_role,
	wtrl_lit_role,
	wtrl_mod_role,
	wtrl_norm_role,
	wtrl_op_role,
	wtrl_opt_role,
	wtrl_pkg_role,
	wtrl_tag_role,
	wtrl_term_role,
	wtrl_type_role,
	wtrl_url_role,
	wtrl_value_role,
	wtrl_var_role,
	wtrl_var_type_role,
	)
from sphinxcontrib.waterloo_docstrings.wtrl_roles import (
	setup_roles
	)
# We must import these, since they are auto-documented.
from sphinxcontrib.waterloo_docstrings.wtrl_signature import (
	wtrl_build_method_signature_nodes,
	wtrl_build_function_signature_nodes,
	wtrl_build_method_signature_block_nodes,
	wtrl_build_function_signature_block_nodes,
	)
# We must import these, since they are auto-documented.
from sphinxcontrib.waterloo_docstrings.wtrl_autodoc import (
	build_sphinx_nodes,
	build_sphinx_nodes_full,
	wtrl_build_autodoc_module_nodes,
	wtrl_build_autodoc_class_nodes,
	wtrl_build_autodoc_function_nodes,
	wtrl_build_autodoc_class_full_nodes
	)

# Leave here for experimenting and debugging, even if unused.
logger = logging.getLogger(__name__)

#===== Typechecking ===========================================#

Struct: TypeAlias = Any


#----- Helpers ------------------------------------------------#

def _extension_version() -> str:
	try:
		return version("sphinxcontrib-waterloo-docstrings")
	except PackageNotFoundError:
		return "0.0.0"
def _add_static_path(config: Any, path : str) -> None:
	lst = list(getattr(config, "html_static_path", []) or [])
	if path not in lst:
		lst.append(path)
	config.html_static_path = lst

def _add_css_files(app: Any) -> None:
	app.add_css_file("common_styles.css")
	app.add_css_file("waterloo_base.css")

#----- Events -------------------------------------------------#

def on_source_read(app: Any, docname: str, source: List[str]) -> None:
	pass

def on_builder_inited(app: Any) -> None:
	for path in app.config.wtrl_basedirs:
		path_s = str(Path(path).resolve())
		if path_s not in sys.path:
			sys.path.insert(0, path_s)

	cfg = app.config.docitem_context_config
	if cfg is None:
		return
	app.docitem_context_configurator = cfg

def on_doctree_resolved(app: Any, doctree: Any, docname: str) -> None:
	index = getattr(app.env, "wtrl_anchor_index", None)
	n_pending = 0
	n_resolved = 0
	for node in list(doctree.findall(wtrl_pending_ref)):
		n_pending += 1
		label = node.get("wtrl_label", node.astext())
		target_fqn = node.get("wtrl_target_fqn")
		target_anchor = node.get("wtrl_target_anchor")
		if (
			isinstance(index, dict)
			and isinstance(target_fqn, str)
			and isinstance(target_anchor, str)
		):
			loc = index.get(target_fqn)
			if (
				isinstance(loc, tuple)
				and len(loc) == 2
				and isinstance(loc[0], str)
				and isinstance(loc[1], str)
			):
				target_docname, target_id = loc
				node_ref = make_refnode(
					app.builder,
					docname,
					target_docname,
					target_id,
					nodes.inline("", str(label)),
					title=target_fqn,
				)
				node_ref["classes"] = ["wtrl_ref"]
				node.replace_self(node_ref)
				n_resolved += 1
				continue
		node.replace_self(nodes.inline(str(label), str(label), classes=["wtrl_ref", "wtrl_ref_unresolved"]))
	logger.info(f"DOCTREE-RESOLVED {docname} pending-refs={n_pending} resolved={n_resolved}")

#----- Setup --------------------------------------------------#

def setup(app: Any) -> dict[str, Any]:
	here = Path(__file__).resolve().parent
	ext_static = str(here / "_static")

# Official way to configure this extension.
# conf.py defines "docitem_context_config" and we tell the app instance.
# We cannot be sure if it exists, but that's how it is named.
	app.add_config_value("docitem_context_config",None,"env")

# We try to establish a naming convention:
# * Which component is affected
# * How the component is affected
# * Which values are possible (e.g. enabled/disabled -> boolean, etc.)
	app.add_config_value('wtrl_diagnostics_admonitions_enabled', True, 'env')
	app.add_config_value('wtrl_diagnostics_logging_enabled', True, 'env')
	app.add_config_value('wtrl_diagnostics_color_enabled', False, 'env')
	app.add_config_value('wtrl_current_object_logging_enabled', False, 'env')
# It can be very confusing not to see objects that are filtered out by the current scope, so default is True.
	app.add_config_value('wtrl_scope_filtered_object_placeholders_enabled', True, 'env')
# push and pop directives.
	app.add_config_value('wtrl_state_change_admonitions_enabled', True, 'env')
	app.add_config_value('wtrl_state_change_logging_enabled', True, 'env')
	app.add_config_value('wtrl_basedirs', [], 'env')

# Add a hook, so that we know when the builder is ready.
	app.connect("config-inited", lambda app, config: _add_static_path(config, ext_static))
	app.connect("builder-inited", on_builder_inited)
	app.connect("builder-inited", _add_css_files)
	app.connect("doctree-resolved", on_doctree_resolved)
	app.connect("source-read", on_source_read)

# Set up directives defined in wtrl_directives.py.
	setup_directives(app)

# Set up roles defined in wtrl_roles.py.
	setup_roles(app)
	setup_markup_roles(app)

	return {
	 "version": _extension_version(),
	 "parallel_read_safe": True,
	 "parallel_write_safe": True,
	 }


#===== Autotesting document consistency =======================#
if __name__ == "__main__":
	# Print version number of the installed extension.
	print(f"Waterloo Sphinx extension version: {_extension_version()}")
