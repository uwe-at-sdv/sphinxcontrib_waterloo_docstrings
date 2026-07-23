import sphinxcontrib.waterloo_docstrings.wtrl_markup as markup

def test_escape_rst_text_segment():
    assert markup.escape_rst_text_segment("abc") == "abc"
    assert markup.escape_rst_text_segment("a\\b") == "a\\\\b"
    assert markup.escape_rst_text_segment("a`b") == "a\\`b"
    assert markup.escape_rst_text_segment("a*b") == "a\\*b"
    assert markup.escape_rst_text_segment("a_b") == "a\\_b"
    assert markup.escape_rst_text_segment("a|b") == "a\\|b"
    assert markup.escape_rst_text_segment("a:b") == "a\\:b"
    assert markup.escape_rst_text_segment("a<b>c") == "a\\<b\\>c"

def test_escape_rst_role_body():
    assert markup.escape_rst_role_body("abc") == "abc"
    assert markup.escape_rst_role_body("a\\b") == "a\\\\b"
    assert markup.escape_rst_role_body("a`b") == "a\\`b"

def test_parse_ref_body():
    label, target = markup.parse_ref_body("label <target>")
    assert label == "label"
    assert target == "target"
    label, target = markup.parse_ref_body("github <https://github.com>")
    assert label == "github"
    assert target == "https://github.com"
    label, target = markup.parse_ref_body("docitem_helper <wtrl://sdv.doc.waterloo.docitem_helper>")
    assert label == "docitem_helper"
    assert target == "wtrl://sdv.doc.waterloo.docitem_helper"

def test_resolve_markup():
    resolved = markup.resolve_markup("|Must|",None)
    assert resolved == ":wtrl_norm:`Must`"
    resolved = markup.resolve_markup("|attr|`something`",None)
    assert resolved == ":wtrl_attr:`something`"
    # Test escaping of special characters in reStructuredText segments and role bodies.
    escaped = markup.resolve_markup(r"a\b`c*d_e|f:g<h>i", None)
    assert escaped == r"a\\b\`c\*d\_e\|f\:g\<h\>i"

