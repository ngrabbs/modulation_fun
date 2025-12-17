Repository Guidelines (AGENTS)

This file tells coding agents how to work in this repository. Follow it exactly.

⸻

Project Goal

Build an educational Waveform Teaching App (Python) starting with Lesson 1: BPSK + Matched Filter.

Primary goals for this repo:
	•	Clear, correct DSP logic
	•	Reproducible results (seeded randomness)
	•	Small, reviewable PRs (one issue per PR)
	•	Tests and lint always run and pass

⸻

Source of Truth

When requirements conflict, use this priority order:
	1.	docs/10-requirements.md
	2.	docs/20-architecture.md
	3.	docs/30-backlog.md / GitHub Issue description
	4.	This AGENTS.md

If something is ambiguous, do not guess. Add a short note to the PR describing the ambiguity and the chosen interpretation.

⸻

Repository Layout

Expected structure:

app/                       # UI entrypoints (Streamlit)
src/waveform_app/          # Python package
  lesson1/                 # Lesson 1 implementation
tests/                     # pytest tests
docs/                      # product docs (vision/req/arch/backlog)
.github/                   # CI and templates

Keep DSP logic out of the UI. The UI should call the core engine API.

⸻

Coding Standards
	•	Language: Python 3.10+ (prefer 3.12 compatibility, but don’t require it)
	•	Prefer small, pure functions for DSP stages.
	•	Use type hints on public APIs and dataclasses.
	•	Use dataclasses for models (LessonParams, SignalStage, LessonRun).
	•	Determinism: use numpy.random.default_rng(seed); never use global RNG state.

Do / Don’t
	•	✅ Do: add docstrings explaining signal conventions (SNR definition, sampling indices, etc.)
	•	✅ Do: keep math steps readable and aligned to the lesson narrative
	•	❌ Don’t: refactor unrelated code while implementing a task
	•	❌ Don’t: add dependencies unless the issue explicitly calls for it

⸻

Tooling

Formatting & Linting

Use the repo’s configured tools (typically):
	•	ruff for linting
	•	black for formatting
	•	optional mypy for types

If configuration files exist, follow them.

Testing

Primary test runner: pytest

All PRs must include:
	•	new/updated tests for new behavior (where reasonable)
	•	passing test output in the PR description

⸻

How to Run (Local)

When the repo is bootstrapped, the standard commands should be:
	•	Install (editable):
	•	python3 -m venv venv
	•	source venv/bin/activate
	•	python -m pip install -e .
	•	Run tests:
	•	pytest
	•	Run app:
	•	streamlit run app/streamlit_app.py

If these commands don’t work yet (early issues), implement the missing pieces so they do.

⸻

PR Workflow (Required)

1) Plan → 2) Implement → 3) Verify

Every task must follow this flow:
	1.	Plan: briefly describe what you will change and which files
	2.	Implement: smallest change that satisfies acceptance criteria
	3.	Verify: run required commands and include output

PR Size Rules
	•	One GitHub issue per PR
	•	Keep diffs small and focused
	•	Avoid drive-by formatting changes

PR Description Template

Include this in the PR body:
	•	Issue: #
	•	Summary:
	•	How to test:
	•	commands run + output
	•	Screenshots: (UI changes only)
	•	Notes / assumptions:

⸻

Core Engine API Contract (Lesson 1)

The UI should depend on a single orchestrator function:
	•	run_lesson1(params: LessonParams) -> LessonRun

Stage functions must remain pure (no UI, no file I/O).

⸻

Plotting Rules
	•	Use matplotlib
	•	Each plot:
	•	title
	•	axis labels
	•	clearly marked symbol boundaries and sampling instants where relevant
	•	Plot functions should return matplotlib.figure.Figure (easy to test/smoke-test).

⸻

LaTeX / Math Rendering

Lesson text and equations live in src/waveform_app/lesson1/content.py.
	•	Keep per-step explanations short (2–4 sentences).
	•	Equations must match the lesson requirements.

⸻

Commit & Branch Conventions
	•	Branch name: issue-<number>-short-slug
	•	Commit messages: imperative, e.g., Add matched filter stage

⸻

When You Are Unsure

If any of these are unclear:
	•	SNR definition
	•	sampling index convention
	•	stage naming/order

Do this:
	1.	Add a short comment in code explaining the assumption
	2.	Add a note in PR “Notes / assumptions”
	3.	Prefer choices that make plots and teaching clarity better