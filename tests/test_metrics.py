from vlm_checklist_lite.metrics import exact_match, token_f1


def test_exact_match_normalization() -> None:
    assert exact_match("The Cat", "the cat") == 1.0


def test_token_f1_partial_overlap() -> None:
    score = token_f1("metal box", "the metal box")
    assert 0.7 < score < 1.0
