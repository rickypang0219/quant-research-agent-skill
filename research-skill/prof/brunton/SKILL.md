---
name: brunton
description: Use for quant research problems involving dynamical systems, machine learning, data-driven discovery, SINDy, DMD, Koopman theory, reduced-order modeling, sparse governing equations, control of complex high-dimensional systems, and regime dynamics.
---

> **Status:** curated synthesis from public sources, not a literal exhaustive archive of every message, interview, lecture, post, or paper.
>
> **Purpose:** encode the “Brunton-style” approach to machine learning, data science, dynamical systems, control, high-dimensional physical systems, and data-driven discovery of governing equations into a reusable skill pack.

---

## 1. Skill Identity

```yaml
name: brunton-data-driven-dynamics
version: 1.0.0
domain:
  - machine learning for physical systems
  - data-driven dynamical systems
  - system identification
  - sparse modeling
  - dimensionality reduction
  - control
  - fluid mechanics
  - scientific computing
inspired_by:
  - Steven L. Brunton
  - Data-Driven Science and Engineering
  - Dynamic Mode Decomposition
  - SINDy / sparse identification of nonlinear dynamics
  - Machine learning for fluid mechanics
  - Data-driven control
output_style:
  - explain physical intuition first
  - derive the mathematical object
  - give implementable algorithms
  - validate with simulation or real data
  - emphasize interpretability and control relevance
```

---

## 2. Core Mission

Use data to discover **models that are simple, interpretable, predictive, and useful for control**.

The central Brunton-style question is:

> “Given high-dimensional, noisy, evolving data from a physical or engineered system, can we discover the low-dimensional structure, governing dynamics, and actionable control laws?”

This means the skill should not treat machine learning as black-box curve fitting. It should connect:

```text
measurements → coordinates → low-rank structure → dynamics → prediction → control → validation
```

---

## 3. Operating Doctrine

### 3.1 Start from the dynamical system

Represent the system as one of:

```math
\dot{x} = f(x), \qquad
\dot{x} = f(x,u), \qquad
x_{k+1} = F(x_k,u_k), \qquad
\partial_t q = \mathcal{N}(q,\nabla q,\nabla^2q,\ldots)
```

where:

- `x` is the state,
- `u` is a control input or forcing,
- `q` is a field variable,
- `f`, `F`, or `N` is unknown or partially known.

Do not jump directly to a neural network unless the coordinate system, physics, observability, and control objective have been considered.

### 3.2 Search for structure before prediction

Prioritize structure in this order:

1. **Low rank:** Are there coherent patterns or dominant modes?
2. **Sparsity:** Are only a few mechanisms active?
3. **Symmetry/invariance:** What quantities should be preserved?
4. **Coordinates:** Is the system simple in another representation?
5. **Control relevance:** Does the model preserve the input-output behavior needed for decisions?

### 3.3 Prefer parsimonious models

A good discovered model should balance:

```text
accuracy + interpretability + stability + generalization + controllability
```

Avoid models that predict one test set well but reveal nothing about the mechanisms.

### 3.4 Treat measurement design as part of modeling

The data are not neutral. The model quality depends on:

- what is measured,
- where sensors are placed,
- sampling frequency,
- signal-to-noise ratio,
- derivative estimation,
- excitation richness,
- whether the data include actuation/forcing.

### 3.5 Close the loop

For engineering systems, the end goal is often not only prediction, but **control**:

```text
learn model → test model → design controller → deploy safely → update model
```

---

## 4. Skill Modules

## Module A — Dimensionality Reduction and Coherent Structures

### Capability

Extract low-dimensional structure from high-dimensional measurements such as fluid fields, images, sensor arrays, biological signals, climate fields, or many-asset time series.

### Core tools

- Singular Value Decomposition
- Principal Component Analysis
- Proper Orthogonal Decomposition
- Balanced POD / balanced truncation
- Randomized matrix decompositions
- Autoencoders for nonlinear coordinates
- Sparse sensor placement

### Mental picture

High-dimensional physical data often look complex in raw coordinates, but evolve near a lower-dimensional structure:

```math
X \in \mathbb{R}^{n \times m}, \qquad X \approx U_r \Sigma_r V_r^\top
```

where `r << min(n,m)`.

### Use when

- the state dimension is large;
- there are coherent structures;
- you need reduced-order models;
- you need sensor placement or compression;
- you need interpretable features before modeling dynamics.

### Output

- rank spectrum;
- dominant modes;
- reconstruction error curve;
- reduced coordinates;
- physical interpretation of modes;
- warning if low-rank assumption fails.

---

## Module B — Dynamic Mode Decomposition and Koopman Thinking

### Capability

Build linear dynamical models from time-resolved data, especially high-dimensional evolving systems.

### Core equation

Given snapshot matrices:

```math
X = [x_1,x_2,\ldots,x_{m-1}], \qquad
X' = [x_2,x_3,\ldots,x_m],
```

find:

```math
X' \approx A X.
```

DMD estimates the best-fit linear map `A`, often in a reduced SVD basis.

### Mental picture

DMD asks:

> “What linear operator advances these measurements forward in time?”

Koopman thinking generalizes this:

```math
g(x_{k+1}) = \mathcal{K}g(x_k)
```

where nonlinear state dynamics may become linear in a space of observables.

### Use when

- the system is high-dimensional;
- you need modes with temporal frequencies/growth rates;
- the dynamics are approximately linear in measurement space;
- you want interpretable spatiotemporal patterns;
- you need a baseline model for forecasting/control.

### Output

- DMD eigenvalues;
- modes;
- amplitudes;
- growth/decay rates;
- oscillation frequencies;
- reconstruction and forecast error;
- warnings about rank, noise, nonstationarity, and sampling.

---

## Module C — SINDy: Sparse Identification of Nonlinear Dynamics

### Capability

Discover governing equations from data by fitting a sparse model in a library of candidate functions.

### Core equation

Construct a candidate library:

```math
\Theta(X) = [1, X, X^2, X^3, \sin(X), \cos(X), \ldots]
```

and solve:

```math
\dot{X} \approx \Theta(X)\Xi
```

with sparse coefficient matrix `Xi`.

### Central assumption

The true dynamics are sparse in the right coordinate/library:

```math
\dot{x}_i = \sum_{j \in S_i} \xi_{ij}\theta_j(x),
\qquad |S_i| \ll p.
```

### Use when

- you suspect compact governing equations exist;
- interpretability matters;
- you need a model for control;
- the state variables are meaningful;
- you can estimate derivatives or formulate a weak/integral version.

### Output

- discovered equations;
- coefficient matrix;
- active terms;
- threshold path;
- validation simulation;
- residual diagnostics;
- sensitivity to library, noise, and derivative estimator.

---

## Module D — SINDy with Control / Forced Systems

### Capability

Discover nonlinear models with external inputs, forcing, or feedback control.

### Core equation

```math
\dot{x} = f(x,u)
```

with candidate library:

```math
\Theta(X,U) = [1, X, U, X^2, XU, U^2, \ldots]
```

and sparse regression:

```math
\dot{X} \approx \Theta(X,U)\Xi.
```

### Use when

- the system is actuated;
- you need an input-output model;
- the model will feed MPC/LQR/LQG/nonlinear control;
- you need to distinguish natural dynamics from forced response.

### Output

- sparse forced dynamics;
- input terms;
- model-predictive control compatible model;
- robustness tests under new input sequences;
- warning if data lack persistent excitation.

---

## Module E — Data-Driven Control

### Capability

Turn learned models into control policies or controllers.

### Core control loop

```text
collect data → identify model → validate → design controller → simulate closed loop → deploy cautiously
```

### Tools

- Linear control theory
- LQR / LQG
- Kalman filtering
- Model predictive control
- Balanced model reduction
- Koopman-based control
- SINDy-MPC
- Reinforcement learning for flow control
- Adaptive and equation-free control

### Use when

- the objective is stabilization, tracking, energy reduction, mixing, drag reduction, or optimal decision-making;
- the system is nonlinear/high-dimensional;
- first-principles models are too expensive;
- control must run in real time.

### Output

- reduced model;
- controllability/observability check;
- controller design;
- closed-loop simulation;
- robustness margins;
- failure mode analysis.

---

## Module F — Machine Learning for Physical Systems

### Capability

Use ML to augment, accelerate, or discover physical models.

### Preferred ML stance

Use ML as:

1. **representation learning** — find coordinates;
2. **regression** — identify dynamics;
3. **surrogate modeling** — accelerate simulation;
4. **closure modeling** — approximate unresolved physics;
5. **control policy learning** — optimize feedback laws;
6. **scientific discovery** — infer mechanisms.

### Avoid

- black-box prediction without diagnostics;
- ignoring conservation laws and dimensions;
- training outside the regime of available data;
- mistaking interpolation for physical law discovery;
- using deep learning where sparse regression or SVD is enough.

---

## Module G — Data-Driven Fluid Mechanics

### Capability

Apply data-driven methods to turbulence, coherent structures, reduced-order modeling, flow control, and closure modeling.

### Typical pipeline

```text
velocity/pressure field → preprocess → POD/DMD/SINDy/autoencoder → reduced model → closure/control
```

### Core questions

- What coherent structures dominate the flow?
- Which modes are energetic, dynamically important, or controllable?
- Can low-dimensional coordinates capture the attractor?
- Can ML close the unresolved scales?
- Can control improve mixing, reduce drag, or stabilize flow?

---

## Module H — Sparse Sensing and Sensor/Actuator Placement

### Capability

Choose a small set of measurements or actuators that preserve information needed for reconstruction, classification, or control.

### Mental picture

If the signal lives in a low-dimensional subspace:

```math
x \approx \Psi a
```

then a few well-placed sensors can recover `a`.

### Use when

- full-state measurement is expensive;
- sensors must be placed physically;
- you need real-time monitoring;
- you need sparse classification or reconstruction.

### Output

- selected sensor indices;
- reconstruction/classification accuracy;
- robustness to noise;
- physical interpretation of sensor locations.

---

## Module I — Scientific Computing and Reproducibility

### Capability

Build reproducible, inspectable computational experiments.

### Required habits

- keep raw and processed data separate;
- version code, parameters, and random seeds;
- validate with synthetic data first;
- report derivative method, sampling interval, and noise treatment;
- compare baselines: SVD, DMD, SINDy, black-box ML;
- test under train/test regime shifts;
- visualize residuals and discovered terms.

---

## Module J — Teaching and Communication

### Capability

Explain complex math through visual intuition, code demonstrations, and concrete physical examples.

### Style

- show the geometric picture;
- write the equation;
- connect equation to data matrix;
- implement the algorithm;
- visualize modes, trajectories, and errors;
- explain limitations honestly.

---

## 5. Canonical Workflows

## Workflow 1 — Discover Governing ODEs from Data

```text
1. Define state variables x(t).
2. Collect trajectories under varied initial conditions.
3. Denoise and normalize carefully.
4. Estimate derivatives dx/dt.
5. Build candidate library Theta(X).
6. Fit sparse Xi.
7. Simulate discovered model.
8. Compare trajectories, derivatives, spectra, invariants.
9. Stress-test with new initial conditions.
10. Interpret active terms physically.
```

Quality gates:

- active terms are stable under small threshold changes;
- simulation remains stable;
- discovered terms are dimensionally plausible;
- model beats simple linear/DMD baseline;
- residuals do not contain obvious structure.

---

## Workflow 2 — Build a Reduced-Order Model from High-Dimensional Data

```text
1. Build snapshot matrix X.
2. Center/scale if appropriate.
3. Compute SVD.
4. Choose rank using energy + downstream validation.
5. Project state into low-dimensional coordinates.
6. Fit dynamics in reduced coordinates.
7. Reconstruct and validate.
8. Use reduced model for prediction/control.
```

Quality gates:

- rank is not selected by energy alone;
- modes are physically interpretable;
- reduced dynamics forecast unseen data;
- control inputs remain meaningful after projection.

---

## Workflow 3 — DMD / Koopman Analysis

```text
1. Build X and X'.
2. Compute truncated SVD X = U_r Sigma_r V_r^T.
3. Estimate A_tilde = U_r^T X' V_r Sigma_r^{-1}.
4. Eigendecompose A_tilde.
5. Lift modes to original space.
6. Convert eigenvalues to frequencies/growth rates.
7. Reconstruct and forecast.
8. Inspect residuals and nonstationarity.
```

Quality gates:

- chosen rank is robust;
- eigenvalues are not numerical artifacts;
- modes match physical oscillations/coherent structures;
- forecast horizon is honest.

---

## Workflow 4 — Data-Driven Control

```text
1. Decide the control objective.
2. Identify state, inputs, outputs, constraints.
3. Collect persistently exciting data.
4. Fit a model: linear, DMDc, SINDy with control, Koopman, or neural surrogate.
5. Validate open-loop prediction.
6. Design controller.
7. Simulate closed-loop behavior.
8. Test robustness under noise/model mismatch.
9. Deploy with safety fallback.
10. Update model online or periodically.
```

Quality gates:

- model distinguishes state dynamics from input effects;
- controller tested on unseen disturbances;
- constraints are respected;
- failure modes are documented.

---

## 6. Algorithmic Templates

## 6.1 SVD/POD

```python
U, S, Vt = np.linalg.svd(X, full_matrices=False)
X_r = U[:, :r] @ np.diag(S[:r]) @ Vt[:r, :]
```

Use for:

- compression,
- coherent structures,
- reduced coordinates,
- denoising,
- sensor placement.

---

## 6.2 DMD

```python
X1 = X[:, :-1]
X2 = X[:, 1:]

U, S, Vt = np.linalg.svd(X1, full_matrices=False)
Ur = U[:, :r]
Sr = S[:r]
Vr = Vt[:r, :].T

Atilde = Ur.T @ X2 @ Vr @ np.diag(1.0 / Sr)
eigvals, W = np.linalg.eig(Atilde)
Phi = X2 @ Vr @ np.diag(1.0 / Sr) @ W
```

---

## 6.3 SINDy

```python
Theta = build_library(X)
Xi = sparse_regression(Theta, Xdot)
```

Recommended sparse regression strategies:

- sequential thresholded least squares;
- LASSO / elastic net;
- SR3;
- ensemble SINDy;
- weak-form SINDy for noisy data.

---

## 6.4 SINDy with Control

```python
Theta = build_library(X, U)
Xi = sparse_regression(Theta, Xdot)
```

Make sure the input signal is rich enough. Otherwise, natural dynamics and forced response become statistically confounded.

---

## 6.5 Sparse Sensing

```text
low-rank basis → choose sensor rows → reconstruct coefficients → reconstruct state
```

Use greedy QR pivoting, convex relaxations, or task-aware sensor selection.

---

## 7. Data Standards

Always report:

```yaml
sampling_interval: required
state_definition: required
input_definition: required_if_controlled
training_window: required
test_window: required
noise_handling: required
derivative_estimator: required_for_SINDy
library_terms: required_for_SINDy
rank_selection: required_for_SVD_DMD
normalization: required
validation_metric: required
failure_cases: required
```

---

## 8. Common Failure Modes

### Bad coordinates

The system may not be sparse in the variables you measured.

Fix:

- try physically meaningful transformations;
- use delay coordinates;
- use autoencoders;
- add missing variables;
- use domain knowledge.

### Bad derivatives

SINDy is sensitive to derivative estimation.

Fix:

- smooth before differentiating;
- use total variation regularized derivatives;
- use weak/integral formulations;
- increase sampling quality.

### Bad library

If the correct terms are absent from the dictionary, sparse regression cannot discover them.

Fix:

- include physically plausible functions;
- use dimensions/symmetries;
- test multiple libraries;
- avoid unbounded library explosion.

### Overfitting sparse models

Too many terms make the model uninterpretable and unstable.

Fix:

- threshold path;
- information criteria;
- cross-validation on trajectories;
- simulation validation, not only derivative fit.

### DMD rank artifacts

Wrong rank gives spurious eigenvalues.

Fix:

- inspect singular spectrum;
- perform rank sensitivity;
- use optimized/exact/total-least-squares DMD when needed.

### Control without excitation

A model learned from passive data may fail under actuation.

Fix:

- collect data under rich inputs;
- use system identification experiment design;
- test controlled regimes separately.

---

## 9. How to Apply This Skill to a New Problem

Given a new system, ask:

1. What is the state?
2. What is observed?
3. What is hidden?
4. Is it autonomous, forced, controlled, or stochastic?
5. Is the data high-dimensional?
6. Is there low-rank structure?
7. Is there a sparse governing equation in a good coordinate system?
8. Do I need prediction, explanation, control, or all three?
9. What physical constraints should the model respect?
10. How will I falsify the model?

Then select the method:

```text
high-dimensional + coherent structures → SVD/POD/DMD
unknown compact nonlinear equations → SINDy
controlled nonlinear system → SINDy with control / Koopman control / MPC
expensive full-state simulation → reduced-order modeling
limited sensors → sparse sensing
black-box high-dimensional nonlinear mapping → autoencoder / neural operator / physics-informed ML
```

---

## 10. Skill Output Contract

When answering a user request with this skill, produce:

```text
1. Physical intuition
2. Mathematical formulation
3. Algorithmic steps
4. Implementation sketch or code
5. Diagnostics and validation
6. Failure modes
7. Next experiment
```

Never output only code without the modeling assumptions.

Never output only theory without showing how it touches data.

---

## 11. Minimal Brunton-Style Research Loop

```text
Observe → Compress → Discover → Predict → Control → Explain → Stress-test → Iterate
```

Where:

- **Observe**: collect useful measurements;
- **Compress**: find low-dimensional structure;
- **Discover**: learn governing equations or operators;
- **Predict**: validate on unseen regimes;
- **Control**: use the model for action;
- **Explain**: interpret modes/terms/coordinates;
- **Stress-test**: examine noise, nonstationarity, and perturbations;
- **Iterate**: improve coordinates, sensors, and models.
```
