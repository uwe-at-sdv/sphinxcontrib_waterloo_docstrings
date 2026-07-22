.. _chapter_configuration:

Configuration
=============

The extension is configured through ordinary Sphinx configuration variables in
the project's :wtrl_file:`conf.py` file. The values are read when Sphinx starts
building the documentation, so changes normally require a fresh Sphinx build.

This documentation uses the following Waterloo-specific settings:

.. literalinclude:: ./conf.py
	:start-after: start-config-variables
	:end-before: end-config-variables

The following sections describe the implemented configuration variables.


Diagnostics
-----------

These variables control how the extension reports invalid directive usage,
failed object resolution, and Waterloo validation errors.

* :wtrl_var:`wtrl_diagnostics_admonitions_enabled` [Default:
  :wtrl_value:`True`] -- Controls whether diagnostic messages are rendered into
  the generated document as admonitions. This is useful while authoring
  documentation because the error appears close to the directive that caused
  it. Chapter :ref:`Admonitions <chapter_admonitions>` shows examples of these
  rendered diagnostics.

* :wtrl_var:`wtrl_diagnostics_logging_enabled` [Default:
  :wtrl_value:`True`] -- Controls whether diagnostics are also emitted through
  Sphinx's standard logging channel. This is the build-terminal counterpart to
  diagnostic admonitions and is usually the right place to look in automated
  builds.

  Example:

  .. code:: text

	----- Tracer-----8<---------------------------------------------
	- Error [validation] - [doc_errors.X_bad_contract->Contract]
	  [Rule CON-023] Subsection 'general' does not exist.
        found:
                Contract:
        expected:
                Contract:
                        general:
                                ...
        hint:
                waterlint explain-subsection --label Contract.general --profile class
	----- Tracer----->8---------------------------------------------

* :wtrl_var:`wtrl_diagnostics_color_enabled` [Default:
  :wtrl_value:`False`] -- Enables ANSI coloring for structured validation
  diagnostics in the Sphinx log output. Leave this disabled when the build
  output is captured by tools that do not preserve ANSI escape sequences.

* :wtrl_var:`wtrl_current_object_logging_enabled` [Default:
  :wtrl_value:`False`] -- Logs the object currently being resolved, validated,
  or rendered. This is mainly a debugging aid for large documents where a later
  diagnostic does not make the active object obvious enough.


State And Scope
---------------

The Waterloo directives maintain a small build-time state: current module,
current class, and current documentation scope. The following variables control
how visible changes to that state are in the generated document and in the
build log.

* :wtrl_var:`wtrl_scope_filtered_object_placeholders_enabled` [Default:
  :wtrl_value:`True`] -- Controls whether objects filtered out by scope are
  represented by a small placeholder admonition. Without this placeholder the
  object simply disappears from the rendered document. With the placeholder
  enabled, the omission remains visible and easier to audit. An example is
  shown in subsection :ref:`Out of scope <subsection_out_of_scope>`.

  The active scope is controlled by state-changing directives as described in
  section :ref:`State changing directives <section_state_changing_directives>`.

* :wtrl_var:`wtrl_state_change_admonitions_enabled` [Default:
  :wtrl_value:`True`] -- Controls whether state-changing directives are rendered
  into the generated document. This can look verbose in finished prose, but it
  makes normative documentation easier to inspect because changes of module,
  class, and scope are visible in the artifact itself.

* :wtrl_var:`wtrl_state_change_logging_enabled` [Default:
  :wtrl_value:`True`] -- Controls whether state-changing directives are logged
  during the Sphinx build.


Import Resolution
-----------------

* :wtrl_var:`wtrl_basedirs` [Default: :wtrl_value:`[]` -- empty list] -- Lists
  directories that are added to :wtrl_mod:`sys.path` before Waterloo resolves
  module and object identifiers. Each path is resolved to an absolute path and
  inserted at the front of :wtrl_mod:`sys.path` if it is not already present.

  Use this variable for local example modules, generated modules, or project
  sources that are not installed in the Python environment used to run Sphinx.
  For this documentation, :wtrl_file:`conf.py` computes the path to
  :wtrl_file:`examples-python` relative to the configuration file:

  .. code:: python

	from pathlib import Path

	CONF_DIR = Path(__file__).resolve().parent
	path_to_examples = str((CONF_DIR / ".." / ".." / "examples-python").resolve())
	wtrl_basedirs = [
		path_to_examples
		]

  Installed packages usually do not need an entry in :wtrl_var:`wtrl_basedirs`.
  They only need to be importable by the same Python interpreter that runs the
  Sphinx build.
