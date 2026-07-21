Configuration (todo: language)
==============================

The configuration variables are set in the project's :wtrl_file:`conf.py` file. For this document, as an example, we have:

.. literalinclude:: ./conf.py
	:start-after: start-config-variables
	:end-before: end-config-variables

The following is the complete list of implemented configuration variables.

* :wtrl_var:`wtrl_diagnostics_admonitions_enabled` [Default: :wtrl_value:`True`] -- This variable specifies if improper use of directives and errors from validation
  are rendered as admonitions in the target document. Chapter :ref:`Admonitions <chapter_admonitions>` gives an overview on these admonitions.

* :wtrl_var:`wtrl_diagnostics_logging_enabled` [Default: :wtrl_value:`True`] -- Specifies if improper use of directives and errors from validation are logged
  in Sphinx's standard logging channel. Example:

.. code:: raw

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


* :wtrl_var:`wtrl_diagnostics_color_enabled` [Default: :wtrl_value:`False`] -- Error messages from validation are often structured
  and have a simple syntax highlighting, which can be enabled by this configuration variable. Leave :wtrl_value:`False` if  your terminal
  or other Sphinx output channel does not render ANSI colors properly.

* :wtrl_var:`wtrl_current_object_logging_enabled` [Default: :wtrl_value:`False`] -- If enabled, the object being processed (validation or rendering)
  is shown in the logging. This might help debugging in case of problems.

* :wtrl_var:`wtrl_scope_filtered_object_placeholders_enabled` [Default: :wtrl_value:`True`] -- Docstring rendering may be omitted if the docstring
  is assigned a less open scope than the scope of the target document. By setting this configuration variable you will at least see a placeholder
  in form of a simple admonition the target document. An example is shown in subsection :ref:`Out of scope <subsection_out_of_scope>`. Note that the scope
  of the document is governed by an internal state which you can change by means of directives as described in section :ref:`State changing directives <section_state_changing_directives>`.

* :wtrl_var:`wtrl_state_change_admonitions_enabled` [Default: :wtrl_value:`True`] -- Specifies if state changing directives (see :ref:`State changing directives <section_state_changing_directives>`)
  are render into the target document. On one hand this might seem annoying, but for a normative docmentation it provides a certain degree of clarity.

* :wtrl_var:`wtrl_state_change_logging_enabled` [Default: :wtrl_value:`True`] -- Specifies if state changing directives are logged.

* :wtrl_var:`wtrl_basedirs` [Default: :wtrl_value:`[]` -- empty list] -- This is the list of directories the extension will scan in order to resolve packages and modules.
  For this document, as an example, our configuration in :wtrl_file:`conf.py` contains a snippet, which extracts the configuration's path and navigate over to the location of out examples:

.. code:: python

	from pathlib import Path

	...

	CONF_DIR = Path(__file__).resolve().parent
	path_to_examples = str((CONF_DIR / ".." / ".." / "examples-python").resolve())
	wtrl_basedirs = [
		path_to_examples
		]

.. note::

	If you are documenting an installed Python module or objects therein, no particular entry in :wtrl_var:`wtrl_basedirs` is required.
	The only condition is that the module must be resolvable in the current Python interpreter (the one you are running the Sphinx compiler in).
