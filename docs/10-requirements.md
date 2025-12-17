Requirements: Lesson 1 — BPSK with Matched Filter (Default Demo)

This document defines executable requirements for the first shippable slice of the Waveform Teaching App: Lesson 1.

⸻

1. Scope

In Scope (Lesson 1)
	•	A guided, end-to-end chain:
	•	Input bits → NRZ mapping → BPSK baseband waveform → AWGN → matched filter → symbol sampling → hard decision → recovered bits
	•	Visuals for each stage (plots)
	•	LaTeX-rendered equations for key concepts
	•	Parameter controls relevant to Lesson 1 (bit pattern, samples-per-symbol, SNR, pulse shape for MVP)
	•	Verification outputs (bit errors, optional BER estimate via repeat trials)

Out of Scope (Lesson 1)
	•	RTL-SDR / Pluto / hardware I/O
	•	Timing recovery / carrier recovery loops (assume ideal timing)
	•	FSK/QPSK/QAM/OFDM
	•	Complex pulse shaping beyond rectangular (raised cosine can be Phase 2)
	•	Drag-and-drop block graph editor (Lesson 1 can be a fixed pipeline)

⸻

2. Users & Use Cases

Primary user

A student/self-learner who wants intuition for how bits become a waveform and how matched filtering enables reliable recovery in AWGN.

Primary use case
	•	User opens app → sees Lesson 1 loaded → runs the chain → lowers SNR until errors appear → understands why.

⸻

3. Functional Requirements (User Stories + Acceptance Criteria)

FR1 — Default lesson loads and runs

User story: As a user, I want Lesson 1 to load by default so I can immediately see a working example.

Acceptance criteria:
	•	On first launch, Lesson 1 is selected and ready to run.
	•	A default bit pattern is pre-filled (e.g., 01011010).
	•	Default parameters produce zero bit errors (e.g., high SNR).

⸻

FR2 — Bit input and validation

User story: As a user, I want to input bits so I can see how my data affects the waveform.

Acceptance criteria:
	•	User can enter a bitstring containing only 0 and 1.
	•	App rejects invalid input (empty string, non-binary characters) with a clear message.
	•	App supports bit lengths from 1 to 64 for Lesson 1.
	•	App provides a “Load preset” option for at least:
	•	01011010
	•	10101010
	•	11110000

⸻

FR3 — Parameter controls

User story: As a user, I want to adjust parameters (SNR, samples per symbol, amplitude convention) so I can explore effects.

Acceptance criteria:
	•	User can set:
	•	Samples per symbol sps (integer, 4–200)
	•	SNR in dB (float, e.g., −2 to 30)
	•	Mapping convention (toggle): 0→−1, 1→+1 (default) or 0→+1, 1→−1
	•	Changing parameters updates the chain outputs after re-run (or live update if implemented).

⸻

FR4 — NRZ mapping stage

User story: As a user, I want to see NRZ mapping so I can connect discrete bits to a piecewise-constant waveform.

Acceptance criteria:
	•	App displays NRZ mapped sequence as values in {−1, +1} (or per chosen convention).
	•	App shows a plot labeled “NRZ (symbol values)” where symbol boundaries are visually apparent.

⸻

FR5 — BPSK waveform generation (baseband MVP)

User story: As a user, I want to see a BPSK signal waveform so I understand symbol shaping over time.

Acceptance criteria:
	•	App generates a baseband waveform using a pulse shape p(t).
	•	For Lesson 1 MVP, p(t) may be rectangular of duration T.
	•	App displays time-domain plot labeled “BPSK transmit waveform”.
	•	App displays the per-symbol sample points used for decisions (markers).

Note: Lesson 1 can treat BPSK as baseband \pm 1 pulses (carrier-free) for clarity; an optional “show carrier” visualization may be added later.

⸻

FR6 — AWGN channel

User story: As a user, I want to add noise so I can see how SNR impacts the waveform and decisions.

Acceptance criteria:
	•	App adds Gaussian noise to the transmit waveform to produce a received waveform.
	•	User-selected SNR changes noise power in a consistent way.
	•	App displays time-domain plot labeled “Received waveform (AWGN)”.

⸻

FR7 — Matched filter stage

User story: As a user, I want to see matched filtering so I understand why it improves detection.

Acceptance criteria:
	•	App applies a matched filter corresponding to the transmit pulse shape.
	•	For rectangular pulse, matched filter is time-reversed pulse (equivalent to a moving sum / integrate-and-dump behavior).
	•	App displays time-domain plot labeled “Matched filter output”.
	•	App highlights the symbol decision instants on the matched filter output.

⸻

FR8 — Symbol sampling and hard decision

User story: As a user, I want to sample and decide bits so I can see the final decode step.

Acceptance criteria:
	•	App samples the matched filter output at the correct symbol centers (ideal timing).
	•	App converts samples to bits using a threshold decision (default: 0).
	•	App displays:
	•	recovered bits (bitstring)
	•	number of bit errors vs input
	•	positions of errors (indices)

⸻

FR9 — Side-by-side comparison view

User story: As a user, I want to compare input bits and recovered bits so I can quickly see if it worked.

Acceptance criteria:
	•	UI shows input bitstring and recovered bitstring in the same view.
	•	Mismatching bits are visibly highlighted.

⸻

FR10 — Equations and explanations (LaTeX)

User story: As a user, I want key equations rendered nicely so I can connect plots to math.

Acceptance criteria:
	•	The lesson page renders the following equations (or equivalents) in LaTeX:
	•	BPSK baseband model: s(t) = a_k\,p(t), where a_k\in\{−1,+1\}
	•	Matched filter impulse response: h(t) = p(T - t)
	•	Decision rule: \hat{a}_k = \mathrm{sign}(y(kT))
	•	Each equation includes a brief “what to notice” bullet (1–2 lines).

⸻

FR11 — Guided lesson flow

User story: As a user, I want a clear guided sequence so I learn the concept in order.

Acceptance criteria:
	•	Lesson shows steps in order with a short heading and 2–4 sentence explanation per step.
	•	User can jump between steps (tabs or stepper) without losing parameter settings.

⸻

4. Non-Functional Requirements

NFR1 — Reproducibility
	•	Given the same inputs + seed, the noise and outputs should be reproducible.
	•	Provide a “Random seed” control (default fixed seed).

NFR2 — Performance
	•	For bit lengths ≤ 64 and sps ≤ 200, run/update should complete in < 200 ms on a typical laptop.

NFR3 — Clarity / UX
	•	Plots must have titles, axis labels, and legends where appropriate.
	•	Symbol boundaries and sampling instants should be visually indicated.

NFR4 — Portability
	•	Must run on macOS/Windows/Linux.
	•	Must not require SDR hardware.

⸻

5. Constraints & Assumptions
	•	Implementation language: Python.
	•	Plotting: matplotlib (or a UI-native plotting wrapper).
	•	LaTeX rendering: acceptable approaches include MathJax (web UI) or matplotlib mathtext (desktop).
	•	Lesson 1 assumes ideal timing (no timing offset) and ideal filter knowledge.

⸻

6. Edge Cases & Failure Modes
	•	Very low SNR: recovered bits should show errors; app must not crash.
	•	sps too small: warning or prevent values < 4.
	•	All-zeros or all-ones patterns: pipeline still works.
	•	Bit length 1: pipeline still works.
	•	Extremely high SNR: output should match input exactly.

⸻

7. Test Plan (Developer-Facing)

TP1 — Deterministic decode at high SNR
	•	Input: 01011010, sps=20, SNR=20 dB, fixed seed
	•	Expected: 0 bit errors

TP2 — Errors appear at low SNR
	•	Input: 01011010, sps=20, SNR=0 dB, fixed seed
	•	Expected: ≥ 1 bit error (exact count may depend on implementation; enforce “not always zero”)

TP3 — Validation
	•	Input: 01012
	•	Expected: user-facing validation error

TP4 — Matched filter correctness (rectangular pulse)
	•	With rectangular pulse and no noise, matched filter output sampled at symbol instants should match transmitted symbol values scaled by pulse energy.

⸻

8. Open Questions (To resolve in Architecture)
	•	UI choice: desktop (e.g., Qt) vs web app (e.g., Streamlit/Gradio/FastAPI+React)
	•	Plot layout: per-step panels vs scrollable “signal chain” timeline
	•	Whether to include an optional carrier visualization for BPSK (separate from baseband)