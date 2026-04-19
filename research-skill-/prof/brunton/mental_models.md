# mental_models.md — Brunton-Style Mental Models

> These mental models translate Steven L. Brunton’s public research and teaching themes into practical reasoning tools.

---

## 1. Data Are Snapshots of a Dynamical System

Do not view a dataset as independent rows first. View it as a trajectory:

```math
x_1 \to x_2 \to x_3 \to \cdots
```

The key object is the rule that advances the system:

```math
x_{k+1} = F(x_k), \qquad \dot{x}=f(x).
```

### Use this when

You are tempted to run generic ML. Ask first: “What is the state, and what evolves it?”

### Failure mode

Treating time series as i.i.d. data destroys the geometry of dynamics.

---

## 2. High-Dimensional Does Not Mean High-Complexity

A system may have millions of variables but only a few dominant coherent structures.

```math
X \approx U_r \Sigma_r V_r^\top, \qquad r \ll n.
```

### Practical intuition

Turbulence, video, sensor arrays, and climate fields may look huge, but often contain recurring patterns.

### Failure mode

Using a large black-box model before checking low-rank structure.

---

## 3. SVD Is a Microscope

The SVD reveals:

- dominant spatial modes,
- dominant temporal coordinates,
- energy distribution,
- noise floor,
- compression potential.

### Question to ask

“What are the few directions in data-space that explain most structured variation?”

### Failure mode

Selecting rank by “95% energy” alone. Control-relevant but low-energy modes may matter.

---

## 4. Coherent Structures Are the Atoms of High-Dimensional Dynamics

In fluid mechanics and many spatiotemporal systems, dynamics are organized by coherent patterns.

### Practical form

Instead of modeling every grid cell, model the amplitudes of coherent structures.

```math
q(x,t) \approx \sum_{i=1}^{r} a_i(t)\phi_i(x)
```

### Failure mode

Compression that preserves visual reconstruction but destroys dynamics.

---

## 5. DMD Finds the Best Linear Time-Stepper

DMD asks:

```math
X' \approx A X.
```

It discovers modes with growth/decay and oscillation rates.

### Mental picture

DMD decomposes a movie into spatial patterns that each oscillate or decay at a characteristic rate.

### Failure mode

Assuming a linear model is globally true. DMD may be local, approximate, rank-sensitive, and noise-sensitive.

---

## 6. Koopman Thinking: Nonlinear Dynamics Can Be Linear in the Right Observables

The state may evolve nonlinearly:

```math
x_{k+1}=F(x_k)
```

but functions of the state may evolve linearly under a Koopman operator:

```math
g(x_{k+1}) = \mathcal{K}g(x_k).
```

### Practical intuition

Sometimes the right features turn nonlinear dynamics into linear dynamics.

### Failure mode

Using too many lifted features without regularization, creating an unstable or uninterpretable model.

---

## 7. The Right Coordinates Make the System Simple

SINDy only works if the dynamics are sparse in the chosen variables and library.

### Question to ask

“Are my measured variables the coordinates in which the physics is simple?”

### If no

Try:

- delay coordinates,
- physical transformations,
- modal coordinates,
- autoencoders,
- dimensional analysis,
- conserved variables.

### Failure mode

Declaring “SINDy failed” when the coordinates were wrong.

---

## 8. Sparsity Is Occam’s Razor for Governing Equations

Many physical laws use few active terms:

```math
\dot{x} = -x + x^3
```

not an arbitrary dense function.

### Practical intuition

Build a big candidate library, then select the few terms that truly matter.

### Failure mode

A large library with collinear terms can produce false discoveries.

---

## 9. SINDy Is Sparse Regression Plus Dynamical Validation

The regression step is not enough.

A discovered equation must:

- simulate correctly,
- generalize to new initial conditions,
- respect known physics,
- remain stable,
- use interpretable active terms.

### Failure mode

Good derivative fit but bad trajectory simulation.

---

## 10. Libraries Are Hypothesis Spaces

The SINDy library is not just a feature matrix. It encodes your hypotheses about possible physics.

```math
\Theta(x)= [1, x, x^2, xy, \sin(x), ...]
```

### Question to ask

“What mechanisms am I allowing the model to discover?”

### Failure mode

If the true term is absent, the algorithm cannot discover it.

---

## 11. Derivatives Are Expensive Information

For continuous-time model discovery:

```math
\dot{X} \approx \Theta(X)\Xi
```

bad derivative estimates can ruin the model.

### Use

- smoothing,
- polynomial fits,
- total variation derivatives,
- weak/integral formulations,
- cross-validation.

### Failure mode

Differentiating noisy data directly with finite differences.

---

## 12. Measurement Design Is Modeling

What you measure determines what you can discover.

### Ask

- Are the sensors enough to reconstruct the state?
- Is the sampling fast enough?
- Is the system sufficiently excited?
- Are hidden variables missing?
- Are actuators included?

### Failure mode

Trying to infer controlled dynamics from passive data.

---

## 13. Inputs Must Be Persistently Exciting

For controlled systems:

```math
\dot{x}=f(x,u)
```

the input `u` must vary enough to reveal its effect.

### Failure mode

If `u` barely changes, the model cannot distinguish natural dynamics from input response.

---

## 14. Prediction Is Not Control

A model that forecasts well over one horizon may still be bad for control.

Control needs:

- stability,
- input-output correctness,
- constraints,
- robustness,
- uncertainty awareness.

### Failure mode

Training a one-step predictor and deploying it in closed loop without robustness tests.

---

## 15. Control Closes the Scientific Loop

The strongest test of a model is whether it supports action.

```text
model → controller → closed-loop behavior → model update
```

### Use

When you want to move from passive understanding to engineering intervention.

---

## 16. Reduced-Order Models Must Preserve What Matters

A reduced model should preserve the structure needed for the task:

- prediction,
- control,
- stability,
- observability,
- actuation,
- conserved quantities,
- frequencies.

### Failure mode

A visually accurate reduced model that fails under feedback control.

---

## 17. Physics and ML Are Complements, Not Enemies

Use physics for:

- constraints,
- dimensions,
- invariants,
- symmetries,
- candidate libraries,
- sanity checks.

Use ML for:

- representation learning,
- regression,
- closure,
- model reduction,
- policy optimization,
- surrogate simulation.

### Failure mode

Pure black-box ML ignores decades of physical knowledge.

---

## 18. Dimensional Consistency Is a Filter for Nonsense

Terms in a governing equation must have compatible units.

### Use

Before accepting discovered terms, check dimensions.

### Failure mode

A statistically strong term that is dimensionally impossible.

---

## 19. Noise Creates Fake Complexity

Noise can make a simple law appear complicated.

### Practical rule

Increase model complexity only after ruling out:

- noise,
- drift,
- bad derivatives,
- unobserved variables,
- poor coordinates,
- sampling artifacts.

---

## 20. Ensemble Models Reveal Structural Confidence

Run model discovery across:

- bootstrap samples,
- noise perturbations,
- libraries,
- thresholds,
- trajectories.

Terms that survive are more trustworthy.

### Failure mode

Trusting one sparse regression result from one train/test split.

---

## 21. Sparse Sensors Exploit Known Patterns

If the state lies in a low-dimensional basis:

```math
x \approx \Psi a
```

then carefully chosen measurements can reconstruct `a`.

### Use

Sensor placement, actuator placement, classification, field reconstruction.

### Failure mode

Random sensors may miss the informative structure.

---

## 22. Model Discovery Is an Iterative Scientific Process

Do not expect one pipeline to solve the system.

```text
choose coordinates → build library → fit → validate → fail → revise coordinates/library/data
```

### Failure mode

Treating model discovery as a one-shot algorithm.

---

## 23. The Attractor Is Often the Real Object

For dissipative nonlinear systems, long-time behavior may live on an attractor.

### Use

Model the geometry of trajectories, not only pointwise error.

### Failure mode

A model with low short-term error but wrong attractor.

---

## 24. Stable Long-Term Simulation Matters

For dynamical models, small errors compound.

### Check

- fixed points,
- limit cycles,
- attractor geometry,
- energy behavior,
- boundedness,
- long-run statistics.

### Failure mode

A model that predicts one step well but explodes over time.

---

## 25. Good Models Are Falsifiable

A discovered equation should make predictions that can fail.

### Ask

“What experiment would prove this model wrong?”

### Failure mode

Only reporting success cases.

---

## 26. Interpretability Is a Scientific Output

A sparse equation, mode, or coordinate can be an explanation, not merely a predictor.

### Use

When the goal is understanding, not only performance.

### Failure mode

Equating accuracy with understanding.

---

## 27. Algorithms Need Regime Awareness

A model learned in one regime may fail in another.

### Check

- Reynolds number,
- forcing amplitude,
- operating point,
- boundary conditions,
- sampling frequency,
- control regime.

### Failure mode

Extrapolating outside training conditions.

---

## 28. Operator Thinking Bridges Data and Theory

DMD and Koopman theory shift attention from trajectories to operators.

### Use

When you want spectral objects:

- eigenvalues,
- eigenfunctions,
- modes,
- invariant subspaces,
- growth/decay rates.

### Failure mode

Confusing numerical DMD modes with exact Koopman eigenfunctions.

---

## 29. The Best Model Depends on the Task

For the same system:

- SVD may be best for compression,
- DMD for modal dynamics,
- SINDy for interpretable equations,
- autoencoders for nonlinear coordinates,
- MPC for control,
- neural networks for high-dimensional surrogates.

### Failure mode

Using one favorite method everywhere.

---

## 30. Explain with Geometry, Equations, and Code

A Brunton-style explanation usually has three layers:

```text
picture → math → implementation
```

### Use

When teaching or building intuition.

### Failure mode

Only deriving equations without showing the data matrix and algorithm.
