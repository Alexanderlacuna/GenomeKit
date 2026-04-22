from __future__ import annotations


class GCCalculator:
    """Calculate GC-content and AT/GC ratio for a DNA sequence."""

    def __init__(self, sequence: str) -> None:
        self.sequence = sequence.upper()

    def analyze(self) -> dict[str, float]:
        """
        Return GC statistics.

        Returns:
            A dictionary with gc_content (percentage), gc_ratio,
            and total_length.
        """
        length = len(self.sequence)
        if length == 0:
            return {"gc_content": 0.0, "gc_ratio": 0.0, "total_length": 0}

        gc = self.sequence.count("G") + self.sequence.count("C")
        at = self.sequence.count("A") + self.sequence.count("T")

        gc_content = (gc / length) * 100
        gc_ratio = gc / at if at > 0 else float("inf")

        return {
            "gc_content": round(gc_content, 2),
            "gc_ratio": round(gc_ratio, 2),
            "total_length": length,
        }
