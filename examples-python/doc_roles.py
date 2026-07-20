r"""
Preamble:
	profile:
		module
	normative_sections:
		Contract, Definitions
Definitions:
	Unicorn:
		A sample definition we need for demonstrating the |lit|`term` token.
Contract:
	general:
		|Must| visualize the semantic markup for documentation and testing
Notes:
	Attribute:
		* Rendering: |attr|`abc`, |attr|`ABC`
		* Code: |lit|`|attr|`abc``, |lit|`|attr|`ABC``
		* Semantics: keys in JSON, TOML, YAML; attributes in XML
		* Example: "In the rendered artifact |attr|`__WTRL_VERSION__` contains the version string"
	Class:
		* Rendering: |class|`abc`, |class|`ABC`
		* Code: |lit|`|class|`abc``, |lit|`|class|`ABC``
		* Semantics: classes in programming languages; maybe tables in database query languages
		* Example: "See docstring of class |class|`tracer` for details."
	Command:
		* Rendering: |cmd|`abc`, |cmd|`ABC`
		* Code: |lit|`|cmd|`abc``, |lit|`|cmd|`ABC``
		* Semantics: Command line tools, subcommands of tools
		* Example: "In the terminal invoke |cmd|`waterlint` |cmd|`validate` |opt|`--basedir` |file|`/path/to/input`"
	Definition:
		* Rendering: |dfn|`abc`, |dfn|`ABC`
		* Code: |lit|`|dfn|`abc``, |lit|`|dfn|`ABC``
		* Semantics: A term defined in a |label|`Definitions` or |label|`Terminology` section.
		* Example: "A |dfn|`Unicorn` is a mythical equine of the genus Monocerus..."
		* Note: In the context of Waterloo Docstrings this token mainly appears in\
		the |label|`Definitions` section, and it has an impact on the |lit|`|term|` token.
	File:
		* Rendering: |file|`/path/to/abc`, |file|`S:\ABC`
		* Code: |lit|`|file|`/path/to/abc``, |lit|`|file|`S:\\ABC``
		* Semantics: A path in the file system
		* Example: "Add |file|`$ROOT_DIR/examples-python` to your |var|`PATH` environment variable."
	Function:
		* Rendering: |func|`print`, |func|`MyClass.my_method`
		* Code: |lit|`|func|`print``, |lit|`|class|`|MyClass.my_method|``
		* Semantics: A function name, or function call syntax.
		* Example: "Call |func|`update` after configuring."
		* Note: It is a matter of taste how callable class objects should be marked, with |class|`obj`|op|`()` or |func|`obj`|op|`()`.
		* Caveat: A more concise way for the combination class/method is to wrap the class name separately: |class|`MyClass`|op|`.`|func|`my_method`\
		which is written like |lit|`|class|`MyClass`|op|`.`|func|`my_method``. Note however that the monochrome\
		method is easier to process for an LLM, since more markup means more "noise". There seems to be a "sweet spot"\
		for the amount of markup to be applied ideally.
	Key:
		* Rendering: |key|`Q`, |key|`CTRL` + |key|`Z`
		* Code: |lit|`|key|`Q``, |lit|`|key|`CTRL`` |lit|`+` |lit|`|key|`Z``
		* Semantics: A key on the keyboard
		* Example: "Press |key|`CTRL` + |key|`SHIFT` + |key|`P` to open the command palette."
		* Note: Combined keys require white space around the |lit|`+` operator.
	Label:
		* Rendering: |label|`abc`, |label|`ABC`
		* Code: |lit|`|label|`abc``, |lit|`|label|`ABC``
		* Semantics: A title, headline, section marker, rubric marker
		* Example: "The |label|`Preamble` | must | be present in each docstring."
	Literal:
		* Rendering: |lit|`abc`, |lit|`ABC`
		* Code: |lit|`|lit|`abc``, |lit|`|lit|`ABC``
		* Semantics: Generally a literal snippet, e.g. for code; a catchall for cases not covered by other semantics rolls.
		* Example: "User |lit|`waltraud` at host |lit|`fancybox`."
	Module:
		* Rendering: |mod|`abc`, |mod|`ABC`
		* Code: |lit|`|mod|`abc``, |lit|`|mod|`ABC``
		* Semantics: A module or a plugin; something that can be imported or included.
		* Example: "Class |class|`tracer` is defined in module |mod|`docitem_helper`."
	Normativity token:
		* Rendering: |norm|`Should`, |norm|`must`
		* Code: |lit|`|norm|`Should``, |lit|`|norm|`must``
		* Semantics: A role for marking normativity keywords.
		* Example: "Normativity keyword '|norm|`should`' expresses a requirement to be fulfilled under normal conditions."
		* Note: The range of applications for this role is limited, since it is mainly for speaking about normativity,\
		not for composing a normative statement.
	Operator:
		* Rendering: |op|`+`, |op|`*`
		* Code: |lit|`|op|`+``, |lit|`|op|`*``
		* Semantics: Any kind of operator in programming or markup languages.
		* Example: "In Python, '|op|`not`' is an operator."
	Notes:
		* Rendering: |opt|`-a`, |opt|`--no-debug`
		* Code: |lit|`|opt|`-a``, |lit|`|opt|`--no-debug``
		* Semantics: An option for a commandline call
		* Example: "List all files in long format: |cmd|`ls` |opt|`-la`"
	Package:
		* Rendering: |pkg|`abc`, |pkg|`ABC`
		* Code: |lit|`|pkg|`abc``, |lit|`|pkg|`ABC``
		* Semantics: A package; something that can be installed.
		* Example: "We recommend to install Sphinx theme |pkg|`furo`."
		* Example: "Import module |pkg|`sdv.doc.waterloo`|op|`.`|mod|`docitem_helper`..."
	Tag:
		* Rendering: |tag|`<abc>`, or <|tag|`ABC` |attr|`attr` = |value|`"value"`>
		* Code: |lit|`|tag|`<abc>``, or <|lit|`|tag|`ABC` |attr|`attr` = |value|`"value"``>
		* Semantics: A tag in XML; maybe the key of a compound object in JSON or a section marker in TOML.
	Term:
		* Rendering: |term|`Unicorn`
		* Code: |lit|`|term|`Unicorn``
		* Semantics: Refer to a term defined in the |label|`Definitions` section.
		* Example: "Following our definition of a |term|`Unicorn` we can easily conclude that..."
	Type:
		* Rendering: |type|`float`, |type|`BaseException`
		* Code: |lit|`|type|`float``, |lit|`|type|`BaseException``
		* Semantics: A type. This overlaps with the |lit|`|class|` role.
		* Example: "All parameters | must | have type |type|`int` or |type|`float`.
	URL:
		* Rendering: |url|`https://github.com`
		* Code: |lit|`|url|`https://github.com``
		* Semantics: A non-clickable URL
		* Example: "The Schema ID is |url|`https://sci-d-vis.com/schema/wtrl-json-0.1.0.schema.json`."
		* Note: For clickable URLs, use the |ref| role instead.
	Value:
		* Rendering: |value|`12345`, |value|`"ABC"`
		* Code: |lit|`|value|`12345``, |lit|`|value|`"ABC"``
		* Semantics: A non-assignable value; an R-value; a symbolic constant.
		* Example: "Specify date in ISO 8601 format, e.g. |value|`2026-07-17`."
	Variable:
		* Rendering: |var|`use_color`, |var|`PATH`
		* Code: |lit|`|var|`use_color``, |lit|`|var|`PATH``
		* Semantics: An assignable object; a function parameter; a named value; a constant some value is assigned to.
		* Example: "Parameter |var|`text` contains the text to be rendered."
	Variable and type:
		* Rendering: |var_type|`use_color:bool`
		* Code: |lit|`|var_type|`use_color:bool``
		* Semantics: A pair of variable and type in colon notation.
		* Example: "Annotate the parameter list like so: (|var_type|`a:int`, |var_type|`b:str`,...)."
"""

