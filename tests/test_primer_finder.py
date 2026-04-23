import random
import time

import pytest

from genomekit.modules.primer_finder import Primer


# The Gold standard
def test_primer_finder_happy_path():
    """A normal 50-bp sequence with moderate GC."""
    finder = Primer("ccatcttcttcatagattttattactgcgtacggacggattcacggggat")
    result = finder.find_primer()

    assert isinstance(result, Primer.PrimerFinderResults)
    assert result.forward == "CCATCTTCTTCATAGATTTT"
    assert result.for_verdict is False
    assert result.reverse == "ACGGACGGATTCACGGGGAT"
    assert result.rev_verdict is True


def test_batch_processing_logic():
    finder = Primer.from_multiple(
        [
            "tcttgaacattgacaattactaatacctcgtataccataaaggtgtcacc",
            "tttagatagagccctgtcggcggtgagtcttaccgtttcccagagcttca",
            "tttagatagagccctgtcgggaaagggcgctaccgtttcccagagcttca",
        ]
    )
    result_stream = Primer.run_batch(finder)
    summary = Primer.PrimerFinderBatchResults(result_stream)

    assert summary.total == 3
    assert summary.full_pass == 2
    assert summary.forward_pass == 2


# The edge case
def test_primer_finder_extreme_gc():
    """Edge case: 100% GC at both ends — should fail the GC window."""
    finder = Primer("G" * 20 + "A" * 10 + "C" * 20)
    result = finder.find_primer()

    assert result.for_verdict is False
    assert result.rev_verdict is False


# The error case
def test_primer_finder_short_sequence():
    """Error case: sequence shorter than 20 bp cannot yield a primer."""
    with pytest.raises(ValueError, match="at least 20 bases"):
        finder = Primer("ATCG")
        finder.find_primer()


# Test efficiency
def generate_random_dna(length: int) -> str:
    return "".join(random.choices("ATCG", k=length))


def test_run_batch_performace():
    sequences = [generate_random_dna(100) for _ in range(100_000)]
    primers = Primer.from_multiple(sequences)

    start = time.perf_counter()
    summary = Primer.PrimerFinderBatchResults(Primer.run_batch(primers))
    elapsed = time.perf_counter() - start

    assert summary.total == 100_000
    assert elapsed < 15.0, f"Batch processing took too long: {elapsed:.2f}s"
