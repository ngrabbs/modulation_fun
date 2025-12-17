# Architecture: Lesson 1 — BPSK with Matched Filter

This document describes the proposed architecture for the first shippable slice of the Waveform Teaching App: **Lesson 1 (BPSK + matched filter)**.

---

## 1. Architecture Goals

* **Clarity first:** readable code and visuals aligned with the lesson steps.
* **Deterministic + testable:** core DSP logic is pure functions with reproducible noise via seeds.
* **Fast iteration:** minimal infrastructure so we can ship Lesson 1 quickly.
* **Agent-friendly repo:** small modules, strong boundaries, easy to test locally + in CI.

---

## 2. Tech Stack (MVP)

### Recommended UI approach: **Streamlit**

Rationale:

* Fast to build an interactive UI with sliders, text inputs, and multiple plots.
* Supports Markdown and LaTeX-style math blocks in the UI.
* Keeps the whole MVP in Python, lowering friction.

### Core libraries

* Numerical: `numpy`
* Plotting: `matplotlib`
* Testing: `pytest`
* Formatting/linting (choose one set):

  * `ruff` (lint) + `black` (format) + optional `mypy` (types)

> Note: If you later want a “drag/drop block graph” UX, we can move to a web front-end (React) and keep the same core engine. For Lesson 1, Streamlit is the shortest path.

---

## 3. High-Level System Context

### What talks to what

* **User** interacts with the **Lesson 1 UI**
* UI calls the **Signal Chain Engine** (pure functions) to compute each stage
* UI renders:

  * Plots from computed arrays
  * LaTeX equations + short explanations
  * Output comparison and error metrics

No external services are required for Lesson 1.

---

## 4. Container / Component Breakdown

### Containers (MVP)

* **App UI (Streamlit)**: presentation + controls + layout
* **Core Engine (Python package)**: pure functions implementing DSP stages
* **Docs**: vision/requirements/architecture and future ADRs

### Components (Core Engine)

* **Bit Input + Validation**
* **Mapping (bits → symbols)**
* **Pulse Shaping (symbols → samples)**
* **AWGN Channel (samples → noisy samples)**
* **Matched Filter (noisy samples → filtered samples)**
* **Sampler + Decision (filtered samples → recovered bits)**
* **Metrics (errors, indices, optional BER)**

---

## 5. Data Model

### Primary data structures

Use lightweight dataclasses so stages are explicit and typed.

* `LessonParams`

  * `bitstring: str`
  * `sps: int`
  * `snr_db: float`
  * `mapping: Literal["0->-1", "0->+1"]`
  * `seed: int`

* `SignalStage`

  * `name: str`
  * `x: np.ndarray` (time axis samples, optional)
  * `y: np.ndarray` (signal samples)
  * `meta: dict` (symbol boundaries, sample indices, etc.)

* `LessonRun`

  * `params: LessonParams`
  * `stages: list[SignalStage]`
  * `input_bits: np.ndarray`
  * `output_bits: np.ndarray`
  * `errors: dict` (count, indices)

This gives the UI a single thing to render: a list of stages.

---

## 6. Signal Chain Design (Lesson 1)

### Pipeline (fixed for MVP)

1. **Parse bits**: `"01011010" → [0,1,0,1,1,0,1,0]`
2. **Map to symbols**: {0,1} → {−1,+1} (or inverted)
3. **Pulse shaping**: rectangular pulse → upsample with `sps`
4. **AWGN**: add Gaussian noise based on `snr_db` and signal power
5. **Matched filter**: `h = reverse(pulse)`; apply convolution
6. **Sample**: pick symbol decision instants (ideal timing)
7. **Decide**: threshold at 0 → recovered symbols → recovered bits
8. **Compare**: error count + indices

### Timing convention

* For rectangular pulse and matched filter, decision instants should be consistent and visually marked.
* We will define symbol boundaries in sample indices and store them in `stage.meta`.

---

## 7. UI Architecture (Streamlit)

### Page layout (recommended)

* Left sidebar: parameters

  * bitstring input + presets
  * `sps` slider
  * `snr_db` slider
  * mapping toggle
  * seed input
  * Run button (or auto-run)

* Main content:

  * Stepper or tabs for stages (NRZ → TX → RX → MF → Decisions)
  * Each step contains:

    * 1–2 plots
    * key equation(s) + “what to notice”

* Bottom panel:

  * input vs output bits comparison
  * error count + indices

### Rendering approach

* Compute the full `LessonRun` from params.
* Render plots stage-by-stage.
* Keep math/explanations in a `lesson_content.py` module (structured text + latex strings).

---

## 8. Repo Layout (Proposed)

```
waveform-teaching-app/
  AGENTS.md
  README.md
  pyproject.toml
  src/
    waveform_app/
      __init__.py
      lesson1/
        pipeline.py          # orchestrates stages
        stages.py            # pure DSP stage functions
        models.py            # dataclasses for params/run/stage
        plots.py             # matplotlib plot builders
        content.py           # markdown + latex strings per step
  app/
    streamlit_app.py         # Streamlit entrypoint
  tests/
    test_lesson1_pipeline.py
    test_validation.py
  docs/
    00-vision.md
    10-requirements.md
    20-architecture.md
    adr/
```

---

## 9. API Boundaries

### Public functions (core engine)

* `validate_bitstring(bitstring: str) -> None | raises`
* `run_lesson1(params: LessonParams) -> LessonRun`

### Stage functions (pure)

* `bits_to_symbols(bits, mapping) -> np.ndarray`
* `symbols_to_waveform(symbols, sps, pulse="rect") -> np.ndarray`
* `add_awgn(x, snr_db, seed) -> np.ndarray`
* `matched_filter(x, pulse, sps) -> np.ndarray`
* `sample_and_decide(x_mf, sps, n_symbols) -> (symbols_hat, bits_hat, sample_indices)`

UI should not do math—UI calls `run_lesson1()`.

---

## 10. Determinism & Randomness

* A fixed default seed enables reproducibility.
* Noise generation uses `numpy.random.default_rng(seed)`.
* Store the seed used in `LessonRun.params`.

---

## 11. Testing Strategy

### Unit tests

* Input validation (reject non-binary strings)
* Mapping correctness
* Matched filter output behavior in the no-noise case

### Integration tests (Lesson 1 pipeline)

* High SNR should decode perfectly for known pattern (TP1)
* Low SNR should sometimes create errors (TP2)

> Tests should avoid brittle “exact error counts” at low SNR. Prefer assertions like “not always zero errors” with fixed seed, or verify noise variance.

---

## 12. Observability (MVP)

* Simple structured logging to console:

  * parameters used
  * runtime per run
  * error count

(Full tracing/metrics is not required for Lesson 1.)

---

## 13. Deployment / Running

* Local run:

  * `pip install -e .`
  * `streamlit run app/streamlit_app.py`

* CI (GitHub Actions):

  * `pytest`
  * `ruff` / `black --check`

---

## 14. ADRs to Create (Next)

Add these in `docs/adr/` as decisions become real:

* ADR-0001: Choose Streamlit for MVP UI
* ADR-0002: Baseband pulses for Lesson 1 (no explicit carrier)
* ADR-0003: Matplotlib for plotting
* ADR-0004: ruff/black/pytest tooling

---

## 15. Open Questions

* Should Lesson 1 include an optional “show carrier” view as an extra tab?
* Do we want live-update on parameter changes, or explicit “Run” button only?
* Do we want a BER estimate mode (repeat trials) in Lesson 1, or keep it single-shot?
