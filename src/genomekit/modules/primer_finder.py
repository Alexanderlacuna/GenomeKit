from __future__ import annotations

from collections.abc import Generator, Iterator


class Primer:
    """
    Analyse primer properties from DNA sequences
    """

    def __init__(self, sequence: str) -> None:
        if len(sequence) < 20:
            raise ValueError("Sequence must be at least 20 bases to extract primers")
        self.sequence = sequence.upper()

    @classmethod
    def from_multiple(cls, sequences: list[str]) -> Generator[Primer, None, None]:
        return (cls(seq) for seq in sequences)

    def __str__(self) -> str:
        return self.sequence

    def __repr__(self) -> str:
        return self.__str__()

    def find_primer(self) -> Primer.PrimerFinderResults:
        """
        Check the first and last 20 bp of a DNA sequence for primer-like properties.
        Utilises 3 criteria
        1. Whether the gc content is between 40-60
        2. Whether the sequence can form an internal dime
        3. Whether the melting temperature is between 60-65c

        Returns:
            FIXME: Update what is returned
            A list with one dictionary containing the forward/reverse
            primer sequences and their verdicts.
        """
        front_seq = self.sequence[:20]
        back_seq = self.sequence[-20:]

        front_gc = self._gc_content(front_seq)
        back_gc = self._gc_content(back_seq)

        front_hairpin = self._find_hairpin(front_seq)
        back_hairpin = self._find_hairpin(back_seq)

        front_temp = self._melt_temp(front_seq)
        back_temp = self._melt_temp(back_seq)

        front_verdict = (40 <= front_gc <= 60) and not (front_hairpin) and (60 <= front_temp <= 65)
        back_verdict = (40 <= back_gc <= 60) and not (back_hairpin) and (60 <= back_temp <= 65)

        results = {
            "forward_primer": front_seq,
            "forward_verdict": front_verdict,
            "reverse_primer": back_seq,
            "reverse_verdict": back_verdict,
        }
        return self.PrimerFinderResults(results, factory=type(self))

    class PrimerFinderResults:
        """Class to store find primer results"""

        # BUG: Can the forward and reverse primers be made objects of class DNA?
        def __init__(self, data_dict, factory):
            self.forward = data_dict["forward_primer"]
            self.for_verdict = data_dict["forward_verdict"]
            self.reverse = data_dict["reverse_primer"]
            self.rev_verdict = data_dict["reverse_verdict"]

        def __repr__(self):
            return (
                f"\n{'Primer Finder Results ':=^70}\n"
                f"Forward Primer Sequence: {self.forward} | Verdict: {self.for_verdict}\n"
                f"Backward Primer Sequence: {self.reverse} | Verdict: {self.rev_verdict}\n"
                f"{'=' * 70}"
            )

    @classmethod
    def run_batch(cls, sequences: Iterator[Primer]) -> Iterator[Primer.PrimerFinderResults]:
        """
        Accept a list of sequences provided by a user and find primers on them.

        Args:
            A list of sequences of class Primer ideally obtained using from_multiple() method
        """
        for seq in sequences:
            yield seq.find_primer()

    class PrimerFinderBatchResults:
        """Class to process a stream of results and produce a summary report"""

        # BUG: Think of how to tie the results to sequence IDs
        def __init__(self, data_stream: Iterator[Primer.PrimerFinderResults]):
            # Initialise the summary counters
            self.total = 0
            self.full_pass = 0
            self.forward_pass = 0
            self.reverse_pass = 0

            # Loop through the stream
            for result in data_stream:
                self.total += 1
                if result.for_verdict:
                    self.forward_pass += 1
                if result.rev_verdict:
                    self.reverse_pass += 1
                if result.for_verdict and result.rev_verdict:
                    self.full_pass += 1

        def __repr__(self):
            return (
                f"\n{'Primer Finder Results ':=^40}\n"
                f"Sequences processed:  {self.total}\n"
                f"Valid full Primers:   {self.full_pass}\n"
                f"Valid Forward Primer: {self.forward_pass}\n"
                f"Valid Reverse Primer: {self.reverse_pass}\n"
                f"{'=' * 40}"
            )

    def _gc_content(self, seq: str) -> float:
        """Return the GC content percentage of a sequence."""
        if len(seq) == 0:
            return 0.0
        return ((seq.count("G") + seq.count("C")) / len(seq)) * 100

    def _melt_temp(self, seq: str) -> float:
        if len(seq) == 0:
            return 0.0
        return 4 * (seq.count("G") + seq.count("C")) + 2 * (seq.count("A") + seq.count("T"))

    def _find_hairpin(self, seq: str) -> bool:
        """
        Check whether a sequence can form a hairpin
        (complementary base pairing within the same sequence).

        Args:
            seq: The sequence to check.

        Returns:
            True if a hairpin is found, False otherwise.
        """
        comp = {"A": "T", "T": "A", "G": "C", "C": "G"}
        for i in range(len(seq)):
            # j starts after a minimum loop of 3; stem length is 3
            for j in range(i + 6, len(seq) - 2):
                stem_a = seq[i : i + 3]
                stem_b = seq[j : j + 3]
                target = "".join(comp.get(base, "N") for base in stem_a)[::-1]
                if target == stem_b:
                    return True
        return False
