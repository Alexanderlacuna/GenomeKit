from genomekit.modules.orf_predictor import find_orfs


def test_basic_orf():
    assert find_orfs("AAAATGAAATAGCCC") == ["ATGAAATAG"]
