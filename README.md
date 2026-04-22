# GenomeKit

A collaborative genome analysis toolkit built by the Cohort 7 Bioinformatics class.

## Installation

```bash
git clone <repo-url>
cd genomekit
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Quick Start

```python
from genomekit import GenomeKit

kit = GenomeKit("ATCGATCGATCG")
print(kit.gc_content())
# {'gc_content': 50.0, 'gc_ratio': 1.0, 'total_length': 12}
```

## Development

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for setup instructions, coding standards, and the project assignment table.

See [`intro.md`](intro.md) for a high-level overview of the architecture.

## Running Tests

```bash
pytest tests -v
```

## Code Quality

```bash
ruff check src tests
ruff format --check src tests
```
