# Backlog Breakdown: Lesson 1 (BPSK + Matched Filter)

This backlog is designed for **Codex/agent execution**: one issue ≈ one small PR.

---

## Definition of Done (applies to every issue)

* Code compiles/runs locally
* `pytest` passes
* Lint/format checks pass (as configured)
* Acceptance criteria met
* No unrelated refactors
* PR description includes:

  * what changed
  * how to test
  * screenshots for UI changes (if applicable)

---

## Issue 1 — Repo bootstrap (pyproject, package skeleton, tooling)

**Goal:** Create a runnable Python package layout and basic dev tooling.

**Scope:**

* Add `pyproject.toml` with dependencies (numpy, matplotlib, streamlit, pytest)
* Create `src/waveform_app/__init__.py`
* Add `app/streamlit_app.py` placeholder that launches
* Add minimal `tests/` scaffold with one passing test

**Acceptance criteria:**

* `pip install -e .` works
* `streamlit run app/streamlit_app.py` starts without errors (can display “Hello Lesson 1”)
* `pytest` runs and passes

**How to test:**

* `python -m pip install -e .`
* `pytest`
* `streamlit run app/streamlit_app.py`

**Files:**

* `pyproject.toml`, `src/waveform_app/*`, `app/streamlit_app.py`, `tests/*`

---

## Issue 2 — Lesson 1 models + validation

**Goal:** Implement dataclasses and bitstring validation.

**Scope:**

* Add `LessonParams`, `SignalStage`, `LessonRun` dataclasses
* Implement `validate_bitstring(bitstring)` with clear error messages
* Implement presets list

**Acceptance criteria:**

* Invalid inputs (empty, non-binary) raise/return a user-friendly error
* Valid bitstrings length 1–64 accepted
* Presets include: `01011010`, `10101010`, `11110000`

**How to test:**

* `pytest -k validation`

**Files:**

* `src/waveform_app/lesson1/models.py`
* `src/waveform_app/lesson1/validation.py` (or `stages.py` if you prefer)
* `tests/test_validation.py`

---

## Issue 3 — Core DSP stages: bits→symbols and pulse waveform

**Goal:** Implement NRZ mapping and rectangular pulse waveform generation.

**Scope:**

* `bits_to_symbols(bits, mapping)`
* `symbols_to_waveform(symbols, sps)` using rectangular pulse (repeat each symbol `sps` samples)
* Stage metadata: symbol boundaries indices

**Acceptance criteria:**

* Mapping toggle works:

  * default `0→-1, 1→+1`
  * inverted mapping supported
* Waveform length is `n_symbols * sps`
* Symbol boundaries are available for plotting

**How to test:**

* `pytest -k mapping`

**Files:**

* `src/waveform_app/lesson1/stages.py`
* `tests/test_lesson1_stages.py`

---

## Issue 4 — AWGN channel with deterministic seed

**Goal:** Add noise stage with reproducible output.

**Scope:**

* `add_awgn(x, snr_db, seed)` using `numpy.random.default_rng(seed)`
* Define SNR interpretation consistently (document in docstring)

**Acceptance criteria:**

* Same input + seed produces identical noisy output
* Increasing SNR decreases noise variance
* Low SNR visibly corrupts the waveform

**How to test:**

* `pytest -k awgn`

**Files:**

* `src/waveform_app/lesson1/stages.py`
* `tests/test_awgn.py`

---

## Issue 5 — Matched filter stage (rectangular pulse)

**Goal:** Implement matched filtering and decision-instants metadata.

**Scope:**

* `matched_filter(x, sps)` for rectangular pulse (equivalent to convolution with ones of length `sps`)
* Provide sample indices for decision points

**Acceptance criteria:**

* With no noise, sampled matched filter outputs correlate with transmitted symbols (scaled)
* Decision instants indices are consistent and within bounds

**How to test:**

* `pytest -k matched_filter`

**Files:**

* `src/waveform_app/lesson1/stages.py`
* `tests/test_matched_filter.py`

---

## Issue 6 — Sampling + hard decision + error metrics

**Goal:** Recover bits from matched filter output and compute errors.

**Scope:**

* `sample_and_decide(x_mf, sps, n_symbols)`
* `compare_bits(bits_in, bits_out)` returning count + indices

**Acceptance criteria:**

* High SNR (e.g., 20 dB) decodes `01011010` with 0 errors using fixed seed
* Output includes recovered bitstring and error indices

**How to test:**

* `pytest -k decision`

**Files:**

* `src/waveform_app/lesson1/stages.py`
* `src/waveform_app/lesson1/metrics.py`
* `tests/test_decision.py`

---

## Issue 7 — Orchestrated pipeline: `run_lesson1(params)`

**Goal:** Produce a `LessonRun` with ordered `SignalStage`s for the UI.

**Scope:**

* Implement `run_lesson1(params: LessonParams) -> LessonRun`
* Populate stages in order: NRZ, TX waveform, RX waveform, MF output
* Store metadata needed for plotting (boundaries, sample indices)

**Acceptance criteria:**

* Running the pipeline returns:

  * stages list with correct names/order
  * input bits and output bits
  * errors dict
* Determinism: with same params + seed, outputs match run-to-run

**How to test:**

* `pytest -k pipeline`

**Files:**

* `src/waveform_app/lesson1/pipeline.py`
* `tests/test_lesson1_pipeline.py`

---

## Issue 8 — Plot builders for Lesson 1 stages

**Goal:** Create matplotlib plots for each stage with labels and markers.

**Scope:**

* Plot functions:

  * `plot_nrz(stage)`
  * `plot_tx(stage)`
  * `plot_rx(stage)`
  * `plot_mf(stage)`
* Include:

  * titles
  * axis labels
  * symbol boundary markers
  * decision sample markers

**Acceptance criteria:**

* Every plot has title + axes labels
* Decision instants are clearly marked on MF plot

**How to test:**

* Manual: run Streamlit once Issue 9 lands
* Automated: basic smoke test that plot functions return `matplotlib.figure.Figure`

**Files:**

* `src/waveform_app/lesson1/plots.py`
* `tests/test_plots_smoke.py`

---

## Issue 9 — Streamlit UI for Lesson 1 (controls + stage tabs)

**Goal:** Build the Lesson 1 UI that renders controls, plots, and bit comparison.

**Scope:**

* Sidebar controls:

  * bitstring input + presets
  * `sps` slider (4–200)
  * `snr_db` slider (−2 to 30)
  * mapping toggle
  * seed input
  * Run button (explicit run for MVP)
* Main area:

  * tabs/stepper for stages (NRZ, TX, RX, MF, Decisions)
  * show plots in each tab
  * show input vs output bits with mismatches highlighted

**Acceptance criteria:**

* App loads with default params and displays 0 errors at high SNR
* Invalid bitstring shows friendly validation message without crashing
* Changing SNR then running updates plots and errors

**How to test:**

* `streamlit run app/streamlit_app.py`

**Files:**

* `app/streamlit_app.py`
* `src/waveform_app/lesson1/*`

---

## Issue 10 — Lesson content (LaTeX equations + “what to notice”)

**Goal:** Add curated text + LaTeX blocks per stage.

**Scope:**

* Create `content.py` with:

  * short explanations per step
  * LaTeX strings for:

    * ( s(t)=a_k p(t) )
    * ( h(t)=p(T-t) )
    * ( \hat{a}_k=\mathrm{sign}(y(kT)) )
  * 1–2 “what to notice” bullets per equation

**Acceptance criteria:**

* UI shows equations rendered (not raw text)
* Text stays short (2–4 sentences per step)

**How to test:**

* Manual: run Streamlit and verify rendering

**Files:**

* `src/waveform_app/lesson1/content.py`
* `app/streamlit_app.py`

---

## Optional follow-ups (after the first working demo)

* Add constellation plot at symbol-rate points
* Add BER estimate mode (repeat trials) behind a toggle
* Add optional “show carrier” visualization tab
