
# Directive class derived from the common base class.
class WtrlPushCurrentModuleDirective(WtrlDirectiveBase):
	def run(self) -> list[nodes.Node]:
		return self._run(wtrl_build_push_current_module_nodes)

# More directive classes here...

# Invoked by the extension's setup-function.
def setup_directives(app: SphinxAppProtocol) -> None:
	# other calls to add_directive
	app.add_directive("wtrl_push_current_module", WtrlPushCurrentModuleDirective)
	# more calls to add_directive
