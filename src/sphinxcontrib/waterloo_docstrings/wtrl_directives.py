from __future__ import annotations
from typing import Any, Callable, cast

from sphinxcontrib.waterloo_docstrings.wtrl_protocol import (
	InlinerProtocol,
	SphinxAppProtocol
	)
from docutils import nodes
from docutils.parsers.rst import Directive

from sphinxcontrib.waterloo_docstrings.wtrl_state import (
	wtrl_build_push_current_module_nodes,
	wtrl_build_push_current_class_nodes,
	wtrl_build_push_current_scope_nodes,
	wtrl_build_pop_current_module_nodes,
	wtrl_build_pop_current_class_nodes,
	wtrl_build_pop_current_scope_nodes,
	)
from sphinxcontrib.waterloo_docstrings.wtrl_signature import (
	wtrl_build_method_signature_nodes,
	wtrl_build_function_signature_nodes,
	wtrl_build_method_signature_block_nodes,
	wtrl_build_function_signature_block_nodes
	)
from sphinxcontrib.waterloo_docstrings.wtrl_autodoc import (
	wtrl_build_autodoc_module_nodes,
	wtrl_build_autodoc_function_nodes,
	wtrl_build_autodoc_class_nodes,
	wtrl_build_autodoc_class_full_nodes
	)
#----- begin directive classes --------------------------------#
class WtrlDirectiveBase(Directive):
	required_arguments = 1
	has_content = False

	def _run(self,node_builder: Callable[[SphinxAppProtocol | Any, InlinerProtocol, int, str], list[nodes.Node]]) -> list[nodes.Node]:
		env = self.state.document.settings.env
		app = env.app
		qname = self.arguments[0].strip()

		try:
			return node_builder(app, cast(InlinerProtocol, self.state.inliner), self.lineno, qname)
		except Exception as e:
		 # Directive-style error message with file/line.
			raise self.error(str(e))

class WtrlAutodocModuleDirective(WtrlDirectiveBase):
	def run(self) -> list[nodes.Node]:
		return self._run(wtrl_build_autodoc_module_nodes)

class WtrlAutodocFunctionDirective(WtrlDirectiveBase):
	def run(self) -> list[nodes.Node]:
		return self._run(wtrl_build_autodoc_function_nodes)

class WtrlAutodocClassDirective(WtrlDirectiveBase):
	def run(self) -> list[nodes.Node]:
		return self._run(wtrl_build_autodoc_class_nodes)

class WtrlAutodocClassFullDirective(WtrlDirectiveBase):
	def run(self) -> list[nodes.Node]:
		return self._run(wtrl_build_autodoc_class_full_nodes)

class WtrlPushCurrentModuleDirective(WtrlDirectiveBase):
	def run(self) -> list[nodes.Node]:
		return self._run(wtrl_build_push_current_module_nodes)

class WtrlPushCurrentClassDirective(WtrlDirectiveBase):
	def run(self) -> list[nodes.Node]:
		return self._run(wtrl_build_push_current_class_nodes)

class WtrlPopCurrentModuleDirective(WtrlDirectiveBase):
	def run(self) -> list[nodes.Node]:
		return self._run(wtrl_build_pop_current_module_nodes)

class WtrlPopCurrentClassDirective(WtrlDirectiveBase):
	def run(self) -> list[nodes.Node]:
		return self._run(wtrl_build_pop_current_class_nodes)

class WtrlPushCurrentScopeDirective(WtrlDirectiveBase):
	def run(self) -> list[nodes.Node]:
		return self._run(wtrl_build_push_current_scope_nodes)

class WtrlPopCurrentScopeDirective(WtrlDirectiveBase):
	required_arguments = 1
	optional_arguments = 0
	def run(self) -> list[nodes.Node]:
		env = self.state.document.settings.env
		app = env.app
		scope_tag = self.arguments[0].strip()
		return wtrl_build_pop_current_scope_nodes(app, cast(InlinerProtocol, self.state.inliner), self.lineno, scope_tag)

class WtrlMethodSignatureDirective(WtrlDirectiveBase):
	def run(self) -> list[nodes.Node]:
		return self._run(wtrl_build_method_signature_nodes)

class WtrlFunctionSignatureDirective(WtrlDirectiveBase):
	def run(self) -> list[nodes.Node]:
		return self._run(wtrl_build_function_signature_nodes)

class WtrlMethodSignatureBlockDirective(WtrlDirectiveBase):
	def run(self) -> list[nodes.Node]:
		return self._run(wtrl_build_method_signature_block_nodes)

class WtrlFunctionSignatureBlockDirective(WtrlDirectiveBase):
	def run(self) -> list[nodes.Node]:
		return self._run(wtrl_build_function_signature_block_nodes)

#----- end directive classes ----------------------------------#

def setup_directives(app: Any) -> None:
# Render documentation boxes.
	app.add_directive("wtrl_autodoc_module", WtrlAutodocModuleDirective)
	app.add_directive("wtrl_autodoc_function", WtrlAutodocFunctionDirective)
	app.add_directive("wtrl_autodoc_method", WtrlAutodocFunctionDirective)
	app.add_directive("wtrl_autodoc_class", WtrlAutodocClassDirective)
# Render box for class and all member classes and methods, recursively.
	app.add_directive("wtrl_autodoc_class_full", WtrlAutodocClassFullDirective)
# Current module
	app.add_directive("wtrl_push_current_module", WtrlPushCurrentModuleDirective)
	app.add_directive("wtrl_pop_current_module", WtrlPopCurrentModuleDirective)
# Current class
	app.add_directive("wtrl_push_current_class", WtrlPushCurrentClassDirective)
	app.add_directive("wtrl_pop_current_class", WtrlPopCurrentClassDirective)
# Current scope
	app.add_directive("wtrl_push_current_scope", WtrlPushCurrentScopeDirective)
	app.add_directive("wtrl_pop_current_scope", WtrlPopCurrentScopeDirective)
# Method signature
	app.add_directive("wtrl_method_signature", WtrlMethodSignatureDirective)
	app.add_directive("wtrl_method_signature_block", WtrlMethodSignatureBlockDirective)
# Function signature
	app.add_directive("wtrl_function_signature", WtrlFunctionSignatureDirective)
	app.add_directive("wtrl_function_signature_block", WtrlFunctionSignatureBlockDirective)

