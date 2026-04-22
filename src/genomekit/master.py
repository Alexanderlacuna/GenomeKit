from __future__ import annotations

from genomekit.modules.gc_calculator import GCCalculator
from genomekit.modules.primer_finder import PrimerFinder


class GenomeKit:
    """Coordinator class that validates DNA sequences and delegates to analysis tools."""

    def __init__(self, sequence: str) -> None:
        """
        Initialize GenomeKit with a validated DNA sequence.

        Args:
            sequence: A DNA sequence to be analysed.

        Raises:
            ValueError: If the input is not a non-empty string or contains invalid characters.
        """
        if not isinstance(sequence, str) or len(sequence) == 0:
            raise ValueError("Input sequence must be a non-empty string")

        invalid = set(sequence.upper()) - {"A", "T", "C", "G"}
        if invalid:
            raise ValueError(
                f"Input sequence must only contain A, T, C, and G characters. "
                f"Invalid characters found: {sorted(invalid)}"
            )

        self.sequence = sequence.upper()
        self._gc = GCCalculator(self.sequence)
        self._primer = PrimerFinder(self.sequence)

    def gc_content(self) -> dict[str, float]:
        """Return GC statistics for the sequence."""
        return self._gc.analyze()

    def primer_finder(self) -> list[dict]:
        """
        Find potential forward and reverse primers.

        Returns:
            A list of dictionaries with primer sequences and suitability verdicts.
        """
        return self._primer.find()
