# This is how the class is used in wtrl_directives.py.
# wtrl_build_autodoc_module_nodes is defined in wtrl_autodoc.py

# Directive class derived from the common base class.
class WtrlAutodocModuleDirective(WtrlDirectiveBase):
	def run(self) -> list[nodes.Node]:
		return self._run(wtrl_build_autodoc_module_nodes)

# More directive classes here...

# Invoked by the extension's setup-function.
def setup_directives(app: SphinxAppProtocol) -> None:
	app.add_directive("wtrl_autodoc_module", WtrlAutodocModuleDirective)
	# More directives here...
