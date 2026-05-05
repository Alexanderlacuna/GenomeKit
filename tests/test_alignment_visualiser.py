import os

from genomekit.modules.alignment_visualiser import dotplot


# Test 1: file is created
def test_file_created():
    seq1 = "AGCT"
    seq2 = "ACGT"
    filename = "test_dotplot.txt"

    dotplot(seq1, seq2, filename)

    assert os.path.exists(filename), "File was not created"

    os.remove(filename)


# Test 2: file is not empty
def test_file_not_empty():
    seq1 = "AGCT"
    seq2 = "ACGT"
    filename = "test_dotplot.txt"

    dotplot(seq1, seq2, filename)

    assert os.path.getsize(filename) > 0, "File is empty"

    os.remove(filename)


# Test 3: header (seq2) is correctly written
def test_header():
    seq1 = "AGCT"
    seq2 = "ACGT"
    filename = "test_dotplot.txt"

    dotplot(seq1, seq2, filename)

    with open(filename) as f:
        first_line = f.readline()

    assert first_line == "  " + " ".join(seq2) + "\n", "Header is incorrect"

    os.remove(filename)


# Test 4: Contains at least one match
def test_match_symbol():
    seq1 = "AGCT"
    seq2 = "ACGT"
    filename = "test_dotplot.txt"

    dotplot(seq1, seq2, filename)

    with open(filename) as f:
        content = f.read()

    assert "." in content, "Match symbol '.' not found"

    os.remove(filename)


# Test 5: Handles sequences with no regions of similarity
def test_no_matches():
    seq1 = "AAAA"
    seq2 = "TTTT"
    filename = "test_dotplot.txt"

    dotplot(seq1, seq2, filename)

    with open(filename) as f:
        content = f.read()

    assert "." not in content, "Unexpected match found"

    os.remove(filename)


# Test 6: Handles empty input sequences
def test_empty_sequences():
    seq1 = ""
    seq2 = ""
    filename = "test_dotplot.txt"

    dotplot(seq1, seq2, filename)

    assert os.path.exists(filename), "File not created for empty input"
    assert os.path.getsize(filename) > 0, "File should still contain header"

    os.remove(filename)
