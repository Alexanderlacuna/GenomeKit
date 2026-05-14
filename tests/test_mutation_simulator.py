import pytest

from genomekit.modules.mutation_simulator import MutSimulater


def test_init():
    """Test if seq capitalized"""
    dna = MutSimulater("Agtc")
    assert dna.seq == list("AGTC")


def test_invalid_seq():
    """Test invalid bases and empty input raise ValueError"""

    with pytest.raises(ValueError):
        MutSimulater("ApGG")

    with pytest.raises(ValueError):
        MutSimulater("")


# output type
def test_simulator():
    "Tests if mutation is as expected"
    dna = MutSimulater("AGgggtttt")
    log, mutated_seq = dna.mut_simulation()

    assert isinstance(log, list)
    assert isinstance(mutated_seq, list)


# checking function  functionality
def test_mutation():
    """Assert if the right mutation is performed"""
    dna = MutSimulater("AGgggtttt")
    mutation_pos, mutated = dna.mut_simulation()

    dna_l = len(dna.seq)
    mutated_l = len(mutated)

    length_change = 0

    for mut_type, pos in mutation_pos:
        if mut_type == "insertion":
            length_change += 1

        elif mut_type == "deletion":
            length_change -= 1

        elif mut_type == "substitution":
            adjusted_pos = pos + length_change
            assert dna[pos] != mutated[adjusted_pos], "Substitution failed"

    assert dna_l + length_change == mutated_l, "Length mismatch"
