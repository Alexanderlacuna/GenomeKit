# Contributor Guide: GenomeKit Project 🧬

Welcome! To keep our 12 modules clean and mergeable, please follow these standards.

Read `intro.md` first if you are new to the project.

---

## 1. Setup Your Environment

```bash
# Clone and enter the repo
git clone <repo-url>
cd genomekit

# Create a virtual environment (one-time)
python -m venv .venv

# Activate it (you must do this every time you open a new terminal)
source .venv/bin/activate        # Linux/Mac
# .venv\Scripts\activate         # Windows

# Install the package in editable mode with dev tools
pip install -e ".[dev]"

# Install pre-commit hooks (one-time)
pre-commit install
```

> **Never commit `.venv/` to Git.** It is already blocked by `.gitignore`.

---

## 2. Project Structure

Create your module inside `src/genomekit/modules/`.
Name it using lowercase and underscores (e.g., `orf_predictor.py`).

**Do NOT create a mixin.** Instead, write a plain class that accepts a sequence as an argument. `GenomeKit` will compose your module internally.

> **Note:** Since this is a class project focused on learning **Object-Oriented Programming (OOP)**, you must write a real class with `__init__` and methods.

### Example Template

Here is a simple module that calculates GC content. Use it as a model for your own tool.

**File:** `src/genomekit/modules/gc_calculator.py`

```python
from __future__ import annotations


class GCCalculator:
    """Calculate GC-content for a DNA sequence."""

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
```

**How GenomeKit uses it:**

```python
# src/genomekit/master.py
from genomekit.modules.gc_calculator import GCCalculator

class GenomeKit:
    def __init__(self, sequence: str):
        # validation happens here ...
        self.sequence = sequence.upper()
        self._gc = GCCalculator(self.sequence)

    def gc_content(self) -> dict[str, float]:
        """Return GC statistics for the sequence."""
        return self._gc.analyze()
```

**What you must deliver:**
1. Your module file in `src/genomekit/modules/<your_module>.py`
2. Integration into `GenomeKit` (2 lines in `master.py`: an import + an instance attribute)
3. A public wrapper method in `GenomeKit` (e.g., `def orf_predictor(self): ...`)
4. A test file in `tests/test_<your_module>.py`

---

## 3. Code Quality Standards

All code must pass the following before a PR can be merged:

- **Ruff** (linting + formatting)
- **pytest** (all tests must pass)

Run them locally:

```bash
ruff check src tests
ruff format --check src tests
pytest tests -v
```

Or let `pre-commit` run them automatically on every commit.

---

## 4. Testing

Testing is **mandatory**. Create a test file in `tests/` named after your module:

```
tests/test_gc_calculator.py
```

Every public method must have at least **three tests**:
1. **Happy path** — a normal, valid input that should succeed.
2. **Edge case** — boundary conditions (empty input, all one base, maximum values, etc.).
3. **Error case** — invalid input that should raise an exception.

### Example Test Template

```python
# tests/test_gc_calculator.py
import pytest

from genomekit.modules.gc_calculator import GCCalculator


def test_gc_happy_path():
    """A mixed sequence with known GC content."""
    calc = GCCalculator("ATCG")
    result = calc.analyze()
    assert result["total_length"] == 4
    assert result["gc_content"] == 50.0


def test_gc_all_at():
    """Edge case: 0% GC."""
    calc = GCCalculator("AAAA")
    result = calc.analyze()
    assert result["gc_content"] == 0.0
    assert result["gc_ratio"] == 0.0


def test_gc_empty_sequence():
    """Edge case: empty string."""
    calc = GCCalculator("")
    result = calc.analyze()
    assert result["total_length"] == 0
    assert result["gc_content"] == 0.0
```

Run your tests locally before pushing:

```bash
pytest tests/test_your_module.py -v
```

---

## 5. Submitting Changes (Fork Workflow)

We use the **fork + PR** model — the same workflow used in real open-source projects.

### If you have not set up your fork yet

```bash
# 1. Fork the repo on GitHub (click the "Fork" button on the original repo)

# 2. Clone YOUR fork
git clone https://github.com/your-username/genomekit.git
cd genomekit

# 3. Add the original repo as "upstream"
git remote add upstream https://github.com/original-owner/genomekit.git
```

### Before every new feature

```bash
# Sync your fork with the latest changes from upstream
git checkout main
git fetch upstream
git rebase upstream/main
git push origin main
```

### Working on your feature

```bash
# 1. Create a branch
git checkout -b feature/your-module-name

# 2. Write your code and tests

# 3. Run quality checks locally
ruff check src tests
ruff format --check src tests
pytest tests -v

# 4. Commit and push to YOUR fork
git add .
git commit -m "Add your module description"
git push origin feature/your-module-name

# 5. Open a Pull Request on GitHub (your fork → upstream main)
```

### If CI fails

Push fixes to the same branch. The PR updates automatically:

```bash
git add .
git commit -m "Fix failing test"
git push origin feature/your-module-name
```

---

## 6. Project Assignments

| Name   | Module file | Function Description |
|--------|-------------|----------------------|
| Sophia | `alignment_visualizer` | Compare the genome against itself or another sequence and return a text-based grid (dot plot) showing areas of similarity |
| Noella | `consensus_builder.py` | Given multiple sequences, determine the consensus base at each position. |
| Otiso | `ncbi_fetcher.py` | Fetch a DNA sequence from NCBI using an accession number (e.g., NM_000546). |
| Annah  | `mutation_simulator.py` | Randomly introduce SNPs, insertions, or deletions at a user-defined rate. |
| Agnetor| `file_io.py` | Read `.fasta` files and save analysis results to standardized formats. |
| Alex   | `indel_mapper.py` | Map insertion and deletion sites relative to a reference sequence. |
| Moreka | `molecular_weight.py` | Calculate predicted melting temperature (Tm) and molecular weight. |
| Terry  | `orf_predictor.py` | Scan all 6 reading frames for ORFs starting with ATG and ending with a stop codon. |
| Yann   | `cpg_mapper.py` | Identify high CpG frequency regions (potential gene promoters). |
| Clement| `primer_finder.py` |Check 5' and 3' ends for primer suitability (GC content, hairpins).  |
| Getnet | `restriction_enzyme.py` | Find exact cut indices for a given recognition site (e.g., GAATTC for EcoRI). |
| Mwasya | `kmer_counter.py` | Count all unique k-length words (e.g., k=3: AAA, AAT, etc.). |
| Bonus  | `seq_valudator.py` | Validate and sanitize DNA sequences (remove whitespace, check alphabet).|

---

## 7. Docstring Style

Use **Google-style docstrings**. Example:

```python
def find_orfs(self, min_length: int = 100) -> list[dict]:
    """
    Scan all six reading frames for open reading frames.

    Args:
        min_length: Minimum ORF length in amino acids. Defaults to 100.

    Returns:
        A list of dictionaries, each containing start index, end index,
        and the nucleotide sequence of the ORF.
    """
```

[Full Google style guide](https://google.github.io/styleguide/pyguide.html)
