# examples.md — Brunton-Style Examples and Templates

> These examples are intentionally compact. They are meant to show reusable patterns for model discovery, DMD, sparse regression, and control-oriented thinking.

---

## Example 1 — Discover a Governing ODE with SINDy

### Problem

You observe a scalar nonlinear system:

```math
\dot{x} = -x + x^3
```

but you only have data `x(t)`. Recover the equation from data.

### Workflow

```text
1. Simulate or observe x(t).
2. Estimate dx/dt.
3. Build candidate library [1, x, x^2, x^3].
4. Solve sparse regression.
5. Interpret active terms.
6. Validate by simulating the discovered model.
```

### Minimal Python

```python
import numpy as np

def simulate_system(x0=0.5, dt=0.01, steps=2000):
    x = np.zeros(steps)
    x[0] = x0
    for k in range(steps - 1):
        x[k + 1] = x[k] + dt * (-x[k] + x[k] ** 3)
    return x

def build_library_1d(x):
    return np.column_stack([
        np.ones_like(x),
        x,
        x**2,
        x**3,
    ])

def sequential_thresholded_least_squares(Theta, y, threshold=0.05, max_iter=10):
    xi = np.linalg.lstsq(Theta, y, rcond=None)[0]

    for _ in range(max_iter):
        small = np.abs(xi) < threshold
        xi[small] = 0.0

        active = ~small
        if not np.any(active):
            break

        xi_active = np.linalg.lstsq(Theta[:, active], y, rcond=None)[0]
        xi[active] = xi_active

    return xi

dt = 0.01
x = simulate_system(dt=dt)

# central difference derivative
xdot = (x[2:] - x[:-2]) / (2 * dt)
x_mid = x[1:-1]

Theta = build_library_1d(x_mid)
xi = sequential_thresholded_least_squares(Theta, xdot, threshold=0.05)

terms = ["1", "x", "x^2", "x^3"]
for term, coef in zip(terms, xi):
    if abs(coef) > 1e-8:
        print(f"{coef:+.4f} * {term}")
```

### Expected discovered structure

```math
\dot{x} \approx -1.0x + 1.0x^3
```

### Diagnostics

Do not stop at coefficients. Also check:

```text
- Does the discovered equation simulate correctly?
- Does it generalize to new initial conditions?
- Are terms stable under noise?
- Is the threshold too aggressive?
- Are derivatives reliable?
```

---

## Example 2 — DMD for a Time-Evolving State Matrix

### Problem

You have time snapshots:

```math
x_1, x_2, \ldots, x_m \in \mathbb{R}^n
```

and want a linear time-stepper:

```math
x_{k+1} \approx A x_k.
```

### Minimal DMD

```python
import numpy as np

def dmd(X, rank):
    """
    X shape: (n_state, n_time)
    """
    X1 = X[:, :-1]
    X2 = X[:, 1:]

    U, S, Vt = np.linalg.svd(X1, full_matrices=False)

    Ur = U[:, :rank]
    Sr = S[:rank]
    Vr = Vt[:rank, :].T

    A_tilde = Ur.T @ X2 @ Vr @ np.diag(1.0 / Sr)

    eigvals, W = np.linalg.eig(A_tilde)
    Phi = X2 @ Vr @ np.diag(1.0 / Sr) @ W

    return eigvals, Phi, A_tilde

def dmd_frequencies(eigvals, dt):
    omega = np.log(eigvals) / dt
    growth = omega.real
    frequency = omega.imag / (2 * np.pi)
    return growth, frequency
```

### Interpretation

- `eigvals` near the unit circle: persistent oscillatory modes.
- `abs(eigvals) < 1`: decaying modes.
- `abs(eigvals) > 1`: growing modes.
- imaginary part of `log(eigval)/dt`: oscillation frequency.

### Diagnostics

```text
- Rank sensitivity
- Reconstruction error
- Forecast horizon
- Noise robustness
- Whether modes have physical meaning
```

---

## Example 3 — SINDy with Control

### Problem

You observe a controlled system:

```math
\dot{x} = f(x,u)
```

and want a sparse model useful for control.

### Library

For scalar `x` and scalar `u`:

```math
\Theta(x,u) = [1, x, u, x^2, xu, u^2, x^3, x^2u, xu^2, u^3].
```

### Minimal code

```python
import numpy as np

def build_library_xu(x, u):
    return np.column_stack([
        np.ones_like(x),
        x,
        u,
        x**2,
        x*u,
        u**2,
        x**3,
        x**2*u,
        x*u**2,
        u**3,
    ])

def sindy_with_control(x, u, xdot, threshold=0.05):
    Theta = build_library_xu(x, u)
    xi = np.linalg.lstsq(Theta, xdot, rcond=None)[0]

    for _ in range(10):
        small = np.abs(xi) < threshold
        xi[small] = 0.0

        active = ~small
        if not np.any(active):
            break

        xi[active] = np.linalg.lstsq(Theta[:, active], xdot, rcond=None)[0]

    return xi
```

### Control-specific warnings

```text
- If u is not rich enough, input terms cannot be identified.
- If u is feedback from x, x and u may be highly correlated.
- Validate under input sequences not used in training.
- Do not deploy in closed loop without robustness tests.
```

---

## Example 4 — High-Dimensional Physical Data Pipeline

### Problem

You have a matrix:

```math
X \in \mathbb{R}^{n \times m}
```

where `n` is the number of spatial degrees of freedom and `m` is the number of time snapshots.

### Brunton-style pipeline

```python
import numpy as np

def low_rank_pipeline(X, ranks=(2, 5, 10, 20)):
    U, S, Vt = np.linalg.svd(X, full_matrices=False)

    energy = np.cumsum(S**2) / np.sum(S**2)

    recon_errors = {}
    for r in ranks:
        Xr = U[:, :r] @ np.diag(S[:r]) @ Vt[:r, :]
        err = np.linalg.norm(X - Xr, ord="fro") / np.linalg.norm(X, ord="fro")
        recon_errors[r] = err

    return {
        "U": U,
        "S": S,
        "Vt": Vt,
        "energy": energy,
        "reconstruction_errors": recon_errors,
    }
```

### Follow-up questions

```text
- What do the leading modes represent physically?
- Is the singular spectrum rapidly decaying?
- Is the chosen rank robust?
- Can the modal coefficients be modeled with DMD or SINDy?
- Are important control directions low-energy?
```

---

## Example 5 — Sparse Sensor Placement Intuition

### Problem

You cannot measure the full state `x`, but you know it is approximately low rank:

```math
x \approx \Psi a.
```

You need a few sensors to recover `a`.

### Simple greedy sensor selection

```python
import numpy as np

def greedy_sensor_selection(Psi, n_sensors):
    """
    Simple greedy row selection based on maximizing volume-like novelty.
    Psi shape: (n_locations, r_modes)
    """
    selected = []
    residual_basis = Psi.copy()

    for _ in range(n_sensors):
        row_scores = np.linalg.norm(residual_basis, axis=1)
        row_scores[selected] = -np.inf

        idx = int(np.argmax(row_scores))
        selected.append(idx)

        # Remove component explained by selected row direction
        q = residual_basis[idx:idx+1, :]
        denom = float(q @ q.T)
        if denom > 1e-12:
            projection = residual_basis @ q.T @ q / denom
            residual_basis = residual_basis - projection

    return selected
```

### Better production tools

Use QR pivoting, convex sensor placement, task-aware placement, or libraries designed for sparse sensing.

### Diagnostics

```text
- Reconstruction error vs number of sensors
- Sensitivity to noise
- Sensor redundancy
- Physical feasibility of sensor locations
```

---

## Example 6 — Model Discovery Checklist

Use this before claiming that you have discovered a governing equation.

```markdown
# Model Discovery Checklist

## Data
- [ ] Sampling interval is known.
- [ ] Units are known.
- [ ] Noise level is estimated.
- [ ] Training and test trajectories are separated.
- [ ] Initial conditions vary enough.

## Coordinates
- [ ] State variables are physically meaningful.
- [ ] Hidden variables are considered.
- [ ] Delay coordinates considered if state is incomplete.
- [ ] Normalization is documented.

## Library
- [ ] Candidate terms are physically plausible.
- [ ] Terms are dimensionally compatible.
- [ ] Library is not unnecessarily huge.
- [ ] Alternative libraries were tested.

## Regression
- [ ] Sparse threshold path is inspected.
- [ ] Coefficient stability is checked.
- [ ] Collinearity is diagnosed.
- [ ] Ensemble or bootstrap test is performed.

## Validation
- [ ] Derivative fit is reported.
- [ ] Trajectory simulation is tested.
- [ ] New initial conditions are tested.
- [ ] Long-run behavior is tested.
- [ ] Failure cases are documented.
```

---

## Example 7 — Data-Driven Control Research Plan

### Goal

Learn a model for a nonlinear controlled system and design a controller.

### Milestones

#### Milestone 1 — Baseline data

```text
Collect trajectories with varied initial conditions and varied inputs.
```

Deliverables:

- state matrix `X`,
- input matrix `U`,
- output matrix `Y`,
- train/test split.

#### Milestone 2 — Linear baseline

```text
Fit linear model: x_{k+1} = A x_k + B u_k.
```

Deliverables:

- one-step error,
- multi-step error,
- stability/eigenvalue analysis.

#### Milestone 3 — Nonlinear sparse model

```text
Fit SINDy with control.
```

Deliverables:

- active terms,
- coefficient stability,
- simulation under unseen inputs.

#### Milestone 4 — Controller

```text
Design MPC, LQR around operating point, or Koopman/SINDy-MPC controller.
```

Deliverables:

- closed-loop simulation,
- constraint satisfaction,
- robustness test.

#### Milestone 5 — Stress test

```text
Inject noise, disturbances, model mismatch, and operating-point shifts.
```

Deliverables:

- failure map,
- safe operating envelope,
- fallback policy.

---

## Example 8 — Applying the Skill to Quant / Market Data

Although Brunton’s work is rooted in physical and engineered systems, the same modeling discipline can help structure market research.

### Translation

```text
physical state           → market state vector
sensors                  → observed features/order-book/returns
coherent structures      → latent factors/regimes
DMD/Koopman              → linear dynamics in lifted features
SINDy                    → sparse nonlinear factor dynamics
control                  → portfolio/risk/rebalance policy
model validation         → walk-forward backtest + regime stress test
```

### Warning

Markets are adaptive, nonstationary, strategic, and reflexive. Do not assume physical-law stability. Use Brunton-style tools for structure discovery and falsification, not as proof of immutable laws.

### Practical workflow

```text
1. Build state vector: returns, volume, funding, order-book imbalance, volatility.
2. Check low-rank/factor structure with SVD/PCA.
3. Use DMD for regime-local linear dynamics.
4. Use sparse regression to search for interpretable nonlinear relationships.
5. Validate with walk-forward splits.
6. Stress-test under liquidity/volatility regimes.
7. Use the model only if it improves decisions after costs.
```

---

## Example 9 — “Picture → Equation → Code” Teaching Template

When explaining any method:

```markdown
## Picture
What geometry should the user imagine?

## Equation
What mathematical object captures that picture?

## Data Matrix
What are the rows, columns, states, and snapshots?

## Algorithm
What are the computational steps?

## Code
What minimal implementation runs?

## Diagnostics
How do we know it worked?

## Failure Modes
How can it fool us?
```

This is the fastest way to preserve both intuition and implementation detail.
