r"""
Preamble:
	profile:
		module
	normative_sections:
		Contract
Contract:
	general:
		|Must| demonstrate how critical characters are rendered in Sphinx.
Notes:
	Backtick:
		` `` ``` ````
		Inline literal candidates: ``abc`` ```abc``` ``|lit|`abc````
	Backslash:
		\ \\ \\\ \\\\ - Escaped markup starts: \|abc| \|lit|`ABC` \:ref:`chapter_misc`
	Pipe:
		| || ||| |||| |abc|
		Waterloo-like role names as plain text: |lit| |ref| |url| |var_type|
	Colon:
		: :: ::: :::: :abc: :123: :abc:`def`
		Sphinx-like roles: :ref:`chapter_misc` :py:func:`print` :unknown:`abc`
	Asterisk:
		(begin) * ** *** **** *abc* **abc** a*b c**d
	Underscore:
		_ __ ___ abc_ _abc abc_def abc__def
	Angle brackets:
		< > <> <abc> <abc def> label <target> label <https://example.org/a:b?c=d#e>
	Brackets:
		[abc] (abc) {abc} [a[b]c] (a(b)c) {a{b}c}
	Inline URLs:
		https://example.org/a:b?c=d#e mailto:person@example.org file:///tmp/demo.txt
	HTML-like text:
		<span class="x">text</span> <br/> <input name="x:y"/>
	Quoted tokens:
		"Token" 'Token' `Token` "|abc|" '|abc|' `|abc|`
	Mixed Waterloo markup:
		|lit|`abc:def`ghi`` |url|`https://example.org/a:b` |var_type|`name:float`
	Malformed Waterloo markup:
		|lit|`abc |lit|abc` |lit|`abc`` |ref|`label <target`
"""
