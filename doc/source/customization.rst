.. _customization:

CSS Customization
=================

The Waterloo extension ships two stylesheets:

* :wtrl_file:`common_styles.css` defines reusable CSS variables.
* :wtrl_file:`waterloo_base.css` applies those variables to the generated
  Waterloo nodes.

This split is intentional. In most cases you should customize the variables in
:wtrl_file:`common_styles.css` or override them in your own project stylesheet.
Only change structural selectors from :wtrl_file:`waterloo_base.css` when you
want to redesign layout, spacing, or diagnostics.


Tested Themes
-------------

The default styles are tested with the following Sphinx themes:

* :wtrl_mod:`classic`
* :wtrl_mod:`alabaster`
* :wtrl_mod:`furo`

The extension tries to stay theme-neutral, but themes differ in typography,
spacing, dark-mode handling, and admonition styling. For that reason, the
default CSS should be understood as a portable baseline rather than a finished
visual identity for every possible theme.


:wtrl_file:`common_styles.css`
------------------------------

This stylesheet contains the shared visual vocabulary for Waterloo semantic
markup. Each role can be adjusted through CSS variables for color, font weight,
and font style.

The light-theme color variables are defined on :wtrl_class:`:root`:

.. literalinclude:: ../../src/sphinxcontrib/waterloo_docstrings/_static/common_styles.css
	:language: css
	:start-after: begin-roles
	:end-before: end-roles

The naming pattern is:

* :wtrl_attr:`--wtrl-`:wtrl_var:`<role>`:wtrl_attr:`-color`
* :wtrl_attr:`--wtrl-`:wtrl_var:`<role>`:wtrl_attr:`-font-weight`
* :wtrl_attr:`--wtrl-`:wtrl_var:`<role>`:wtrl_attr:`-font-style`

For dark mode, the stylesheet defines a second color set:

* :wtrl_attr:`--wtrl-dark-`:wtrl_var:`<role>`:wtrl_attr:`-color`

The active role colors are then switched to the dark variables for themes that
expose a dark-mode state. For :wtrl_pkg:`furo`, this state is stored on the
document body:

.. code:: css

	body[data-theme="dark"] {
		--wtrl-attr-color:var(--wtrl-dark-attr-color);
		/* further role colors */
		}

The stylesheet also contains a media-query fallback for themes or browsers that
use :wtrl_attr:`prefers-color-scheme`. Additional theme-specific activation
rules can be added later if another theme exposes dark mode differently.

If a role should keep the surrounding text color, use :wtrl_value:`currentColor`
as the role color. This is usually preferable to hard-coding a theme color
because it lets the active theme decide the foreground color.


Recommended Customization Pattern
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For most projects, the safest customization strategy is to leave the generated
Waterloo classes untouched and override only the CSS variables. Put these
overrides in a project stylesheet that is loaded after the Waterloo extension
stylesheets.

For light-mode colors, override the active variables directly:

.. code:: css

	:root {
		--wtrl-func-color:#005cc5;
		--wtrl-type-color:#6f42c1;
		--wtrl-var-color:#b31d28;

		/* further role colors */
		}

For themes with an explicit dark-mode selector, override the active variables
inside that selector:

.. code:: css

	body[data-theme="dark"] {
		--wtrl-func-color:#79b8ff;
		--wtrl-type-color:#b392f0;
		--wtrl-var-color:#ff7b72;

		/* further role colors */
		}

This approach keeps the semantic mapping stable: generated nodes still use
classes such as :wtrl_class:`.wtrl_func` and :wtrl_class:`.wtrl_type`, while the
project controls only their visual appearance.


:wtrl_file:`waterloo_base.css`
------------------------------

This stylesheet maps generated Waterloo nodes to concrete CSS classes. It
forwards the role-related variables from :wtrl_file:`common_styles.css` into
classes such as :wtrl_class:`.wtrl_func`, :wtrl_class:`.wtrl_type`, and
:wtrl_class:`.wtrl_var`. It also defines layout-related styles for signatures,
diagnostics, scope filtering, and unresolved references.

The following selectors are the most likely customization points.


Custom Admonitions
~~~~~~~~~~~~~~~~~~

State-changing directives render custom admonitions when
:wtrl_var:`wtrl_state_change_admonitions_enabled` is enabled. The extension
does not actively style these admonitions beyond assigning semantic CSS
classes. By default, their visual appearance is therefore inherited from the
active Sphinx theme.

The generated admonitions carry one message class:

* :wtrl_class:`.wtrl-current-module-message`
* :wtrl_class:`.wtrl-current-class-message`
* :wtrl_class:`.wtrl-current-scope-message`

and one direction class:

* :wtrl_class:`.wtrl-current-module-push`
* :wtrl_class:`.wtrl-current-module-pop`
* :wtrl_class:`.wtrl-current-class-push`
* :wtrl_class:`.wtrl-current-class-pop`
* :wtrl_class:`.wtrl-current-scope-push`
* :wtrl_class:`.wtrl-current-scope-pop`

This makes it possible to style all state-change messages uniformly or to
distinguish module, class, and scope changes. For example:

.. code:: css

	.wtrl-current-module-message,
	.wtrl-current-class-message,
	.wtrl-current-scope-message {
		opacity:0.85;
		/* further shared admonition styling */
		}

	.wtrl-current-scope-push {
		border-left-color:#6f42c1;
		/* further scope-push styling */
		}


Multiline Signatures
~~~~~~~~~~~~~~~~~~~~

Multiline signatures are rendered as block elements. The outer block controls
the frame, padding, and border radius:

.. code:: css

	div.wtrl-signature-multiline {
		border: solid 0.1em #cce;
		padding:0.5em;
		border-radius:0.3em;
		}

This is a good place to align the signature block with the active theme. For
example, a theme with card-like elements might use a subtle shadow instead of a
plain border.

Parameter lines are rendered inside the block. The font family is usually
overridden by semantic roles inside the signature, so indentation is the more
interesting property to customize:

.. code:: css

	div.wtrl-signature-param {
		font-family: monospace;
		padding-left: 3em;
		}

The closing line, including the return type annotation, uses a separate class:

.. code:: css

	div.wtrl-signature-ret {
		font-family: monospace;
		padding-left: 0em;
		}

When a multiline signature appears inside a rendered Waterloo documentation
box, the surrounding section already provides visual structure. The nested
signature block therefore drops its own frame:

.. code:: css

	.wtrl-section div.wtrl-signature-multiline {
		border: 0;
		padding: 0em;
		}


Normative Keywords
~~~~~~~~~~~~~~~~~~

Normative keywords are marked with a small scales symbol:

.. code:: css

	.wtrl_norm::after
		{
		content: " \2696";
		font-weight:normal;
		font-style:normal;
		}

This is deliberately a matter of presentation, not semantics. The semantic
information is already present in the generated node class. You can change the
symbol, restyle it, or remove it entirely if it does not fit the surrounding
documentation.


Out Of Scope
~~~~~~~~~~~~

References to docstrings that are hidden by scope filtering are rendered with a
muted style:

.. code:: css

	.wtrl_out_of_scope, .wtrl_out_of_scope *
		{
		color:#777 !important;
		opacity:0.85;
		}

This marker should not look like an error. The target exists, but it is not
visible in the current documentation scope. A good redesign should communicate
that the reference is intentionally unavailable under the active scope rules.


Unresolved Links
~~~~~~~~~~~~~~~~

References to non-existing or unresolved docstrings use a stronger style:

.. code:: css

	span.wtrl_ref_unresolved
		{
		color: #f30;
		font-weight: bold;
		}

Unlike an out-of-scope reference, an unresolved reference usually means that the
source document should be fixed. It is therefore reasonable for this style to be
more visible than ordinary text.

Documentation box details
~~~~~~~~~~~~~~~~~~~~~~~~~

The following selector path allows to define the style of the left cell
on the documentation box headline:

.. code:: css

	table.wtrl-box > thead > tr > th .wtrl-obj-kind

and for specific docstring profiles:

.. code:: css

	table.wtrl-box > thead.wtrl-box-head-module > tr > th .wtrl-obj-kind
	table.wtrl-box > thead.wtrl-box-head-class > tr > th .wtrl-obj-kind
	table.wtrl-box > thead.wtrl-box-head-function > tr > th .wtrl-obj-kind
	table.wtrl-box > thead.wtrl-box-head-method > tr > th .wtrl-obj-kind
	table.wtrl-box > thead.wtrl-box-head-inherited_method > tr > th .wtrl-obj-kind

We recommend either to keep the color consistent to other nodes containing
data sensitive to the profile (like "context" in the screenshot below, which is a class)
or to pick some neutral color.

By default we place guillemots around the object kind in order
to create the look of a "prototype". This is done by definining selector paths:

.. code:: css

	table.wtrl-box > thead > tr > th .wtrl-obj-kind:before
	table.wtrl-box > thead > tr > th .wtrl-obj-kind:after

.. figure:: img/doc_docubox_cell_0_row_0.png
	:width: 100%

	Documentation box table head (here: Theme :wtrl_pkg:`furo`)

