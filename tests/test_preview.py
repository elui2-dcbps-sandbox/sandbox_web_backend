from sandbox_web_backend import preview_record


def test_preview_record_trims_name():
    assert preview_record("  sample  ") == {"name": "sample", "kind": "synthetic"}


def test_preview_record_allows_empty_name():
    assert preview_record("") == {"name": "", "kind": "synthetic"}
