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
