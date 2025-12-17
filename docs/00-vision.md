# Vision: Waveform Teaching App

## Problem Statement
Learning digital communications (encoding → modulation → channel effects → demodulation → decoding) is hard because students often see the steps as disconnected: a formula in a book, then a plot somewhere else, then a block diagram with no “feel” for how the signal transforms. This app will provide an end-to-end, step-by-step visual + mathematical walkthrough where users can input bits and watch the waveform evolve through selected processing blocks, with plots and equations that connect the “why” to the “what.”

## Target Users
- Primary: Students and self-learners studying Signals & Systems / DSP / Digital Communications (early undergrad to hobbyist SDR learners)
- Secondary: Amateur radio / SDR hobbyists who want intuition for modulation/demodulation chains

## Core User Goals (Jobs-to-be-Done)
1. **I want to enter a small bit sequence** (e.g., `0101` or `01011010`) and understand how it becomes a waveform.
2. **I want to choose processing steps** (encoding, modulation, filtering, noise, demodulation, decoding) and see the effect immediately.
3. **I want plots + equations side-by-side** so I can connect the math to the waveform changes.
4. **I want to verify recovery** by comparing the decoded output bits to the input bits, including cases where it fails (noise, timing, etc.).

## What This App Is
An interactive “signal chain explorer” that:
- Accepts user-provided bits (or generates a known pattern)
- Applies a sequence of selectable blocks (encode/modulate/etc.)
- Displays intermediate results at each block:
  - Time-domain plots (and optionally frequency-domain)
  - Key equations (LaTeX-rendered)
  - Parameter controls (symbol rate, samples-per-symbol, noise level, filter settings)
- Shows the final recovered bits + error metrics (bit errors / BER for small sequences)

## Success Metrics
- A user can complete a guided chain (bits → modulation → demod → bits) and correctly explain what changed at each step.
- The app can reproduce at least 2–3 canonical chains (e.g., NRZ → BPSK → AWGN → coherent demod → decisions) with clear plots and correct recovery at reasonable SNR.
- Time-to-first-understanding: A new user can run the default example and see meaningful plots within 2 minutes.
- Educational clarity: Each block page/step has (a) a plot, (b) a short explanation, (c) the key equation(s), and (d) a “what to notice” callout.

## Non-Goals (Explicitly Out of Scope for MVP)
- Not a full GNU Radio replacement or SDR hardware control app
- Not a full communications textbook or long-form course platform
- No real-time RF streaming initially (no RTL-SDR/Pluto integration in MVP)
- No advanced equalization, carrier recovery loops, or coding theory deep dives in MVP (can be Phase 2+)
- Not optimizing for very long bitstreams or high performance simulation at first

## MVP Scope (First Test-Drive Version)
- Input bits: manual entry + “random” + preset patterns
- Blocks (minimum set):
  1. Bit mapping / line coding (NRZ unipolar or bipolar)
  2. Symbol mapping for BPSK (0→-1, 1→+1)
  3. Pulse shaping (rectangular or simple raised cosine later)
  4. Channel: AWGN noise (slider SNR)
  5. Coherent demod (multiply by carrier reference or matched filter concept)
  6. Decision + recovered bits + error count
- Visuals:
  - Time-domain waveform plot for each step
  - Constellation plot for BPSK step (optional but high value)
- Math:
  - Render LaTeX equations for each block (key formulas only)

## Future Enhancements (Phase 2+ Ideas)
- Add FSK, QPSK, QAM, OFDM “path”
- Add timing offset / frequency offset and recovery concepts
- Add simple channel models (fading, multipath)
- Add “compare two chains” mode
- Add lesson mode: guided explanations + checkpoints

## Constraints & Assumptions
- Implementation language: Python
- Cross-platform: should run on macOS/Windows/Linux
- Must be usable without specialized hardware
- UI must support: interactive controls + plots + LaTeX rendering

## Open Questions (To Resolve in Requirements)
- UI framework choice (e.g., web-based Python app vs desktop GUI)
- How users build chains: fixed pipeline vs drag/drop block graph
- Depth level: “intro intuition” vs “math-heavy” toggle
- Minimum set of plots per block (time, freq, constellation)

## Example Lessons & Default Demo Chain

### Lesson 1: BPSK with Matched Filter (Default Demo)
**Purpose:** Build intuition for optimal detection in AWGN channels.

**Signal Flow:**
Input bits → NRZ mapping → BPSK modulation → AWGN channel → matched filter → symbol sampling → decision → recovered bits

**Key Concepts:**
- Bit-to-symbol mapping
- Energy per bit (Eb)
- Why the matched filter maximizes SNR
- Importance of sampling at the symbol decision instant

**Highlighted Equations (LaTeX-rendered):**
- BPSK signal:
  \\[
  s(t) = \\pm \\sqrt{E_b} p(t)
  \\]
- Matched filter impulse response:
  \\[
  h(t) = p(T - t)
  \\]
- Decision rule:
  \\[
  \\hat{b} = \\text{sign}(y(T))
  \\]

**User Takeaway:**
Noise spreads the waveform, but the matched filter concentrates signal energy and restores reliable decisions.

---

### Lesson 2: Frequency Shift Keying (FSK) Intuition
**Purpose:** Demonstrate how information can be encoded in frequency rather than amplitude or phase.

**Signal Flow:**
Input bits → FSK modulation (f₀ / f₁) → AWGN → noncoherent demodulation → decision

**Key Concepts:**
- Orthogonal frequencies
- Time-domain vs frequency-domain views
- Robustness vs bandwidth tradeoffs

**Visual Emphasis:**
- Time-domain waveform
- Frequency-domain (FFT) plot

**User Takeaway:**
Separating information in frequency simplifies detection but increases spectral usage.

---

### Lesson 3: Constellations & Noise (Why Errors Happen)
**Purpose:** Show how noise causes symbol and bit errors.

**Signal Flow:**
Input bits → BPSK / QPSK modulation → noise sweep → decision

**Key Concepts:**
- Constellation distance
- Noise variance and decision boundaries
- Symbol error vs bit error

**Visual Emphasis:**
- Animated constellation scatter plot as SNR decreases

**User Takeaway:**
Errors occur when noise pushes symbols across decision boundaries.

---

## Default Demo Experience
On first launch, the application should:
- Automatically load **Lesson 1: BPSK with Matched Filter**
- Use a known short bit pattern (e.g., `01011010`)
- Start at high SNR for near-perfect recovery
- Allow the user to gradually reduce SNR and observe when and why failures occur