# Welcome to GenomeKit 🧬

Hello! If you are reading this, you are about to build a piece of a real bioinformatics toolkit. This guide explains what the project is, how the pieces fit together, and what you need to know before you write your first line of code.

Read this first. Then read `CONTRIBUTING.md` for the detailed rules.

---

## What is GenomeKit?

GenomeKit is a **collaborative Python package** that analyzes DNA sequences. Think of it as a Swiss Army knife for genomes: one tool finds primers, another finds genes (ORFs), another counts k-mers, and so on.

By the end of the semester, we will have **~12 different analysis tools** that all live inside one installable Python package.

---

## The Big Picture: How It All Fits Together

Instead of everyone writing standalone scripts, we are building one shared library. Here is the architecture:

```
genomekit/                          ← The Python package
├── __init__.py                     ← Makes it importable
├── master.py                       ← GenomeKit class (the coordinator)
└── modules/
    ├── primer_finder.py            ← Sophia's tool
    ├── orf_predictor.py            ← Terry's tool
    ├── kmer_counter.py             ← Mwasya's tool
    ├── restriction_enzyme.py       ← Getnet's tool
    └── ...                         ← Your tool here!

tests/                              ← Test files (one per module)
├── test_primer_finder.py
├── test_orf_predictor.py
└── ...

pyproject.toml                      ← Package config (dependencies, metadata)
```

### Three key ideas

1. **GenomeKit is a coordinator.**  
   It receives a DNA string, validates it, and passes it to each analysis tool. It does not do the biology itself.

2. **Each module is an independent tool.**  
   Your code lives in its own file. It accepts a sequence as input and returns results. It does not need to know about the other 11 tools.

3. **We use composition, not inheritance.**  
   You will write a plain class (or function) that `GenomeKit` holds as an attribute. We do **not** use the mixin pattern. See `CONTRIBUTING.md` for examples.

---

## What You Will Build

Each student owns **one module**. Your deliverable is:

1. **A Python file** in `src/genomekit/modules/` (e.g., `orf_predictor.py`)
2. **A test file** in `tests/` (e.g., `test_orf_predictor.py`) with at least 3 tests
3. **Integration into `GenomeKit`** — two lines in `master.py` so your tool is accessible via `kit.your_tool()`

---

## Skills You Will Practice

Even if you have never built a Python package before, this project will teach you:

| Skill | Why It Matters |
|-------|----------------|
| **Python classes (OOP)** | You will design a real class with `__init__`, methods, and private helpers. You will learn composition ("has-a") instead of inheritance ("is-a") |
| **Bioinformatics domain** | PCR primer design, gene finding (ORFs), restriction mapping, k-mer analysis, mutation modeling — concepts used in real research pipelines |
| **Git & GitHub** | Forking, branching, syncing with upstream, resolving merge conflicts — the standard open-source workflow |
| **Testing** | Writing tests that prove your code works and catch accidental breakages when others change things |
| **Code quality** | Ruff enforces consistent style; CI/CD (GitHub Actions) proves "it passes on my laptop" is not enough |
| **Collaboration** | Reading code written by 11 other people, opening Pull Requests, and addressing review feedback |
| **Packaging** | Building a pip-installable Python package with `pyproject.toml`, not just standalone scripts |
| **Extended features (optional)** | If time allows: CLI (`argparse`), Streamlit dashboard, Docker, FASTA parsing — these turn the project into a resume-worthy portfolio piece |

---

## The Workflow (From Start to Finish)

### Step 1: Fork the repo
Click the **"Fork"** button on the original repository. This creates your own copy at `https://github.com/your-username/genomekit`.

### Step 2: Clone your fork

```bash
git clone https://github.com/your-username/genomekit.git
cd genomekit
```

### Step 3: Add upstream remote (one-time)

```bash
git remote add upstream https://github.com/original-owner/genomekit.git
```

This lets you pull the latest changes from upstream into your fork.

### Step 4: Set up your environment

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pre-commit install
```

### Step 5: Sync before you start (every time)

```bash
git checkout main
git fetch upstream
git rebase upstream/main
git push origin main
```

This ensures you are building on the latest version of the codebase.

### Step 6: Create a branch

```bash
git checkout -b feature/orf-predictor
```

### Step 7: Write code and tests

- Your module: `src/genomekit/modules/orf_predictor.py`
- Your tests: `tests/test_orf_predictor.py`

### Step 8: Run checks locally

```bash
ruff check src tests
ruff format --check src tests
pytest tests -v
```

### Step 9: Commit and push to your fork

```bash
git add .
git commit -m "Add ORF predictor module"
git push origin feature/orf-predictor
```

### Step 10: Open a Pull Request

Go to GitHub. You will see a banner: **"Compare & pull request"**. Click it and open a PR from your fork's `feature/orf-predictor` branch to **upstream** `main`.

### Step 11: Wait for CI

GitHub Actions will run Ruff + pytest. A red ❌ means fix and push again. A green ✅ means ready for review.

### Step 12: Address feedback and merge

Maintainers may leave review comments. Make changes, commit, push to the same branch — the PR updates automatically.

---

## What You Need to Know Before You Start

### Git basics
If you have only used GitHub's web interface, you need to be comfortable with:
- `git clone`, `git checkout -b`, `git add`, `git commit`, `git push`
- **Forking** a repo (creating your own copy on GitHub)
- Adding an **upstream remote** (`git remote add upstream ...`)
- Syncing your fork with the original repo (`git fetch upstream`)
- Opening a **Pull Request** from your fork to the original repo

### Why we use forks
This is how real open-source projects work (pandas, scikit-learn, etc.). Forking means:
- You have your own copy to experiment with
- You cannot accidentally break the upstream `main` branch
- You learn the industry-standard contribution workflow

### Virtual environments (`venv`)
A virtual environment is an isolated Python installation so your project dependencies do not clash with your system Python or other projects.

**`venv` vs. Conda:**

| | `venv` | Conda |
|---|---|---|
| Built-in? | ✅ Yes (Python 3.3+) | ❌ Must install separately |
| Best for | Pure Python projects | Projects needing non-Python tools (BLAST, R, etc.) |
| Speed | Instant | Slower |
| Size | ~15 MB | ~50–500 MB |

**For GenomeKit, use `venv`.** It requires zero installation — if you have Python, you already have `venv`. Conda must be downloaded and installed separately.

```bash
# Step 1: Create the environment (one-time only)
python -m venv .venv

# Step 2: Activate it (you must do this every time you open a new terminal)
source .venv/bin/activate        # Linux/Mac
# .venv\Scripts\activate         # Windows

# Step 3: Install the package
pip install -e ".[dev]"

# Step 4: Deactivate when done
deactivate
```

> **Important:** If you forget to activate the environment, `python` and `pip` will use your **system Python** instead. Watch for the `(.venv)` prefix in your terminal prompt — that means the environment is active.

> **Never commit `.venv/` to Git.** It contains OS-specific files. It is already listed in `.gitignore`.

### Python packages vs. scripts
A **script** is a single `.py` file you run directly. A **package** is a folder of organized code that you `import` and `pip install`. GenomeKit is a package.

### Tests
A test is a small script that runs your code with a known input and checks the output. If you change your code later, the test catches accidental breakages. We use `pytest`.

### Linting and formatting
**Linting** means checking your code for style issues (unused imports, missing spaces, etc.). **Formatting** means automatically fixing spacing and quotes so all 12 contributors write code that looks the same. We use **Ruff** for both.

---

## Getting Help

- **Read `CONTRIBUTING.md`** for the full technical rules and templates.
- **Ask questions in your team's chat** — if you are stuck, someone else probably is too.
- **Open a GitHub Issue** if you find a bug in someone else's code or in the shared setup.

---

## Quick Checklist Before You Code

- [ ] I have cloned the repo and created a virtual environment
- [ ] I have installed the package with `pip install -e ".[dev]"`
- [ ] I have read `CONTRIBUTING.md` Section 2 (Project Structure)
- [ ] I know which module I am building (check the project table in `CONTRIBUTING.md`)
- [ ] I have created a branch: `git checkout -b feature/my-module-name`

Ready? Read `CONTRIBUTING.md` next.
