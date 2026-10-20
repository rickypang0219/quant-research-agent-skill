---
name: strang
description: Use for quant research problems involving linear algebra, projections, vector spaces, PCA, SVD, least squares, numerical modeling, Hilbert-space geometry, factor models, residualization, and making abstract mathematical structure intuitive and computable.
---


> **Scope note.** This file is a practical synthesis of publicly available Gilbert Strang materials, not an exhaustive archive and not authored by Prof. Strang. It consolidates recurring methods from his MIT linear algebra, computational science, differential equations, matrix methods, and learning-from-data materials into an agent-usable skill.

---

## 1. Skill Identity

**Name:** `strang-linear-algebra-modeling-learning`

**Purpose:**  
Use this skill to reason about mathematical, computational, modeling, data-analysis, optimization, and deep-learning problems through the lens of applied linear algebra.

**Core style:**  
Geometric first, algebra second, computation third, application always visible.

**Best used for:**

- Explaining linear algebra intuitively and rigorously.
- Turning a real-world problem into matrices, vectors, operators, and constraints.
- Diagnosing systems `Ax = b`, least squares, projections, PCA/SVD, eigenvalue problems, graph/network matrices, and ODE/PDE discretizations.
- Connecting linear algebra to machine learning, signal processing, optimization, numerical methods, and deep neural networks.
- Teaching difficult topics with simple examples, pictures, dimensions, and physical meaning.

---

## 2. Source Map

The skill is synthesized mainly from the following public sources:

1. Gilbert Strang’s MIT homepage  
   https://math.mit.edu/~gs/

2. MIT OpenCourseWare 18.06 Linear Algebra  
   https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/

3. MIT OpenCourseWare 18.065 Matrix Methods in Data Analysis, Signal Processing, and Machine Learning  
   https://ocw.mit.edu/courses/18-065-matrix-methods-in-data-analysis-signal-processing-and-machine-learning-spring-2018/

4. `Linear Algebra and Learning from Data` book page  
   https://math.mit.edu/~gs/learningfromdata/

5. Wellesley-Cambridge Press catalog  
   https://wellesleycambridge.com/

6. Gilbert Strang bibliography  
   https://math.mit.edu/~gs/papers/papers.html

7. MIT OCW / MathWorks differential equations series with Gilbert Strang and Cleve Moler  
   https://ocw.mit.edu/courses/res-18-009-learn-differential-equations-up-close-with-gilbert-strang-and-cleve-moler-fall-2015/

8. MIT News: final lecture / career overview  
   https://news.mit.edu/2023/gilbert-strang-made-linear-algebra-fun-0531

9. SIAM News career reflection  
   https://www.siam.org/publications/siam-news/articles/gilbert-strang-reflects-on-his-rich-academic-career-and-lifelong-friendship-with-linear-algebra-and-siam/

10. MIT OCW podcast: “Making Deep Learning Human with Prof. Gilbert Strang”  
    https://ocw.mit.edu/courses/18-065-matrix-methods-in-data-analysis-signal-processing-and-machine-learning-spring-2018/resources/making-deep-learning-human-with-prof-gilbert-strang/

---

## 3. Core Doctrine

### 3.1 Linear algebra is the language of applied mathematics

Almost every applied problem can be expressed as one or more of:

```text
Ax = b
Ax ≈ b
Aq = λq
A = CR
A = QR
A = UΣVᵀ
minimize f(x)
x_{t+1} = A x_t
du/dt = A u
```

The first task is not to compute.  
The first task is to understand **what the matrix means**.

Ask:

1. What are the unknowns?
2. What are the equations?
3. What is the shape of the matrix?
4. What are the columns?
5. What are the rows?
6. What subspaces does the problem create?
7. What does rank say?
8. What geometry is hiding inside the algebra?

---

## 4. Master Mental Models

### 4.1 Columns create the output

For `Ax = b`, view `b` as a linear combination of the columns of `A`.

```text
Ax = x₁a₁ + x₂a₂ + ... + xₙaₙ
```

The key question is:

> Is `b` inside the column space of `A`?

If yes, the system is solvable.  
If no, project `b` onto the column space and solve least squares.

---

### 4.2 Elimination is factorization

Gaussian elimination is not just a procedure. It is a matrix decomposition.

```text
A = LU
PA = LU
```

Use elimination to understand:

- pivots
- rank
- invertibility
- numerical stability
- triangular solves
- sparse systems
- computational cost

---

### 4.3 Rank is the true size of the problem

Rank tells you how many independent directions are present.

Use rank to diagnose:

- how many equations are independent
- how many unknowns are determined
- whether a solution exists
- whether a solution is unique
- whether data has low-dimensional structure
- whether a model is overparameterized

Core identities:

```text
rank(A) = dimension of column space
rank(A) = dimension of row space
nullity(A) = n - rank(A)
```

---

### 4.4 The four fundamental subspaces are the central map

For an `m × n` matrix `A`:

```text
Column space C(A)          lives in R^m
Left nullspace N(Aᵀ)       lives in R^m
Row space C(Aᵀ)            lives in R^n
Nullspace N(A)             lives in R^n
```

Orthogonality:

```text
C(A) ⟂ N(Aᵀ)
C(Aᵀ) ⟂ N(A)
```

Interpretation:

- Column space = reachable outputs.
- Left nullspace = constraints on outputs.
- Row space = determined part of the input.
- Nullspace = invisible/free directions of the input.

When confused, draw these four spaces.

---

### 4.5 Projection is the bridge from impossible to best possible

When `Ax = b` has no exact solution, solve:

```text
minimize ||Ax - b||²
```

The residual must be orthogonal to the column space:

```text
Aᵀ(b - A x_hat) = 0
AᵀA x_hat = Aᵀb
```

Use projection to interpret:

- least squares
- regression
- conditional expectation
- denoising
- PCA
- factor models
- estimation
- model fitting

---

### 4.6 Orthogonality simplifies everything

Whenever possible, move to an orthonormal basis.

If `QᵀQ = I`, then:

```text
projection = QQᵀb
least squares = R x = Qᵀb
norms are preserved
coordinates are clean
```

Use `QR` when stability matters.

---

### 4.7 Eigenvectors reveal repeated action

Eigenvectors are directions that a matrix does not turn:

```text
Aq = λq
```

Use eigenvalues/eigenvectors to understand:

- powers of matrices
- stability
- Markov chains
- oscillations
- differential equations
- graph Laplacians
- covariance matrices
- principal components
- positive definite matrices

Repeated dynamics:

```text
x_t = A^t x_0
```

If `A = QΛQ⁻¹`, then:

```text
A^t = QΛ^tQ⁻¹
```

The behavior is controlled by eigenvalues.

---

### 4.8 SVD is the best coordinate system for any matrix

Every matrix can be decomposed as:

```text
A = UΣVᵀ
```

Interpretation:

- `V` gives input directions.
- `Σ` gives stretching strengths.
- `U` gives output directions.

Use SVD for:

- low-rank approximation
- PCA
- compression
- denoising
- recommender systems
- pseudoinverse
- ill-conditioning diagnosis
- data matrix geometry

Best rank-`k` approximation:

```text
A_k = U_k Σ_k V_kᵀ
```

---

### 4.9 Positive definite matrices are energy

A symmetric matrix `S` is positive definite if:

```text
xᵀSx > 0 for all x ≠ 0
```

Interpret as energy, curvature, covariance, or squared length.

Use positive definiteness for:

- optimization
- least squares
- covariance matrices
- stability
- finite element stiffness matrices
- kernel methods
- Newton methods

---

### 4.10 Graphs are matrices

For a graph:

- incidence matrix `B`
- graph Laplacian `L = BᵀB`
- flows live on edges
- potentials live on nodes
- conservation laws appear as matrix equations

Use graph matrices for:

- networks
- electrical circuits
- ranking
- clustering
- PageRank-like dynamics
- graph signal processing
- discrete differential operators

---

## 5. Modeling Skill

### 5.1 Translate reality into linear algebra

For any modeling problem:

1. Identify state variables.
2. Identify observations.
3. Identify constraints.
4. Identify conservation laws.
5. Identify linear or approximately linear relationships.
6. Build the matrix.
7. Check dimensions.
8. Interpret subspaces.
9. Solve or optimize.
10. Validate residuals.

Template:

```text
Real system
→ variables
→ equations
→ matrix/operator
→ computation
→ interpretation
→ validation
```

---

### 5.2 Choose the correct matrix form

| Situation | Matrix form |
|---|---|
| Exact system | `Ax = b` |
| Overdetermined noisy system | `min ||Ax - b||²` |
| Underdetermined system | minimum norm solution |
| Dynamics | `x_{t+1} = Ax_t` or `du/dt = Au` |
| Vibrations / modes | `Aq = λq` |
| Covariance / PCA | eigenvectors of `AᵀA` or covariance |
| Large data | low-rank approximation |
| Network | incidence matrix / Laplacian |
| PDE discretization | difference / finite element matrix |
| Optimization | gradient, Hessian, KKT system |

---

### 5.3 Model with residuals

A model is not complete until residuals are inspected.

```text
residual = observed - predicted
r = b - Ax
```

Ask:

1. Is the residual small?
2. Is it structured?
3. Is it orthogonal to the fitted space?
4. Does it reveal missing variables?
5. Is the error random or systematic?
6. Does the residual change over time?

In data science, residual structure is often more informative than the fitted model.

---

### 5.4 Conditioning matters

A correct formula can still be numerically dangerous.

Check:

```text
condition number κ(A) = σ_max / σ_min
```

Warning signs:

- tiny singular values
- unstable inverse
- large coefficient changes from small data changes
- multicollinearity
- near-rank deficiency

Prefer:

- QR over normal equations when possible
- SVD for rank-deficient systems
- regularization for ill-conditioned problems
- scaling / normalization before optimization

---

### 5.5 Discretization turns calculus into matrices

Differential equations become matrix equations after discretization.

Examples:

```text
first derivative  → difference matrix
second derivative → tridiagonal matrix
Laplacian         → sparse matrix
boundary condition → modified rows
finite element method → stiffness matrix
```

A continuous operator becomes a matrix.  
The geometry, stability, and accuracy depend on the discretization.

---

## 6. Deep Learning Skill

### 6.1 A neural network is repeated linear algebra plus nonlinearity

Basic layer:

```text
z_l = W_l x_{l-1} + b_l
x_l = σ(z_l)
```

Deep network:

```text
f(x) = W_L σ(W_{L-1} σ(...σ(W_1x + b_1)...))
```

Interpretation:

- weights are matrices
- activations are nonlinear coordinate changes
- training is optimization
- backpropagation is repeated chain rule
- generalization depends on structure, data, and regularization

---

### 6.2 Data begins as a matrix

For `m` samples and `n` features:

```text
X ∈ R^{m×n}
```

Questions:

1. Are columns features?
2. Are rows samples?
3. Are features centered?
4. Are features scaled?
5. What is the rank?
6. Are there dominant singular values?
7. Is the data approximately low-rank?
8. What structure remains after projection?

---

### 6.3 PCA/SVD before deep learning

Before reaching for a neural network, inspect:

```text
X = UΣVᵀ
```

Use singular values to understand:

- intrinsic dimension
- noise floor
- correlated features
- dominant directions
- compression
- whether a simple model may work

A deep model should not be a black box replacement for understanding the data matrix.

---

### 6.4 Optimization is geometry

Training minimizes a loss:

```text
minimize L(W)
```

Gradient descent:

```text
W_{k+1} = W_k - η ∇L(W_k)
```

Key questions:

1. What is the loss surface?
2. What is the gradient?
3. What is the Hessian or curvature?
4. Is the problem convex locally or globally?
5. Is the data matrix ill-conditioned?
6. Is normalization helping the optimization?
7. Is regularization controlling variance?

---

### 6.5 Backpropagation is organized chain rule

Backprop is not magic. It is efficient differentiation of matrix products and nonlinearities.

For each layer:

```text
forward:  z_l = W_l x_{l-1} + b_l
          x_l = σ(z_l)

backward: gradients flow through W_l and σ'(z_l)
```

Always track dimensions.

Dimension discipline prevents most errors in deep learning implementation.

---

### 6.6 Deep learning explanation protocol

When explaining neural networks:

1. Start with one neuron.
2. Convert one neuron into a vector equation.
3. Stack neurons into a matrix.
4. Stack layers into function composition.
5. Add nonlinearity.
6. Define loss.
7. Derive gradient idea.
8. Explain SGD.
9. Discuss generalization.
10. Return to geometry.

---

## 7. Teaching Skill

### 7.1 Begin with the simplest nontrivial example

Good examples:

- `2 × 2` system for geometry
- `3 × 3` system for elimination
- rank-one matrix for outer products
- projection onto a line
- tridiagonal matrix for second derivatives
- small graph incidence matrix
- tiny neural network with one hidden layer

Avoid starting with definitions alone.

---

### 7.2 Always include the picture

For any answer, include at least one of:

- column-space picture
- row-reduction picture
- projection picture
- energy/ellipse picture
- eigenvector direction picture
- graph/network picture
- data-cloud/PCA picture
- layer-by-layer neural network picture

If no image is drawn, describe the mental picture.

---

### 7.3 Track dimensions explicitly

Every matrix expression should pass the dimension test.

Example:

```text
A ∈ R^{m×n}
x ∈ R^n
b ∈ R^m
Ax ∈ R^m
AᵀA ∈ R^{n×n}
Aᵀb ∈ R^n
```

Dimension checking is a proof assistant for applied mathematics.

---

### 7.4 Connect formulas to meaning

Do not leave a formula alone.

For each formula, explain:

1. What it computes.
2. Why it is true.
3. What geometry it represents.
4. When it fails.
5. How to compute it safely.
6. What it means in the application.

---

## 8. Agent Operating Procedure

When given a problem, follow this protocol.

### Step 1 — Identify the objects

Write:

```text
Known:
Unknown:
Data:
Matrix:
Vector:
Objective:
Constraints:
```

### Step 2 — Check dimensions

Write all shapes.

```text
A: m × n
x: n × 1
b: m × 1
```

If dimensions do not match, stop and fix the formulation.

### Step 3 — Identify the linear algebra type

Choose one:

```text
solve
least squares
projection
eigenproblem
SVD/PCA
optimization
dynamics
graph/network
ODE/PDE discretization
deep learning layer stack
```

### Step 4 — Interpret the subspaces

Ask:

```text
What is C(A)?
What is N(A)?
What does rank mean?
What does the residual mean?
What is being projected?
```

### Step 5 — Choose stable computation

Prefer:

```text
LU       for square nonsingular systems
QR       for least squares
SVD      for rank-deficient / ill-conditioned systems
Cholesky for symmetric positive definite systems
eigendecomposition for symmetric operators
iterative sparse solvers for huge sparse systems
```

### Step 6 — Explain the result geometrically

Convert the answer back into:

- directions
- projections
- modes
- energy
- rank
- low-rank structure
- residuals
- dynamics
- data geometry

### Step 7 — Validate

Check:

```text
residual norm
orthogonality
rank
conditioning
edge cases
units
interpretability
```

---

## 9. Prompt Templates

### 9.1 Linear algebra explainer

```text
Explain this linear algebra problem in the Gilbert Strang style:
1. Start from the geometry.
2. Define the matrix and vector dimensions.
3. Show the algebra.
4. Explain the column space / nullspace interpretation.
5. Give a small numerical example.
6. Explain how to compute it stably.
Problem: {problem}
```

---

### 9.2 Modeling from a real problem

```text
Convert this real-world problem into an applied linear algebra model:
1. Define variables and observations.
2. Build the matrix/operator.
3. State whether it is Ax=b, least squares, eigenproblem, dynamics, or optimization.
4. Explain the physical meaning of each matrix.
5. Discuss rank, residuals, and conditioning.
6. Suggest a computational method.
Problem: {problem}
```

---

### 9.3 Deep learning explanation

```text
Explain this deep learning concept using matrix methods:
1. Represent the data as a matrix.
2. Represent each layer as affine map + nonlinearity.
3. Track dimensions.
4. Explain the loss function.
5. Explain gradients/backprop as chain rule.
6. Connect to SVD/PCA/conditioning where relevant.
Concept: {concept}
```

---

### 9.4 Debugging a numerical model

```text
Debug this numerical/modeling pipeline:
1. Check matrix dimensions.
2. Check rank and conditioning.
3. Check residuals.
4. Identify whether the problem is underdetermined, overdetermined, or ill-conditioned.
5. Recommend stable decompositions.
6. Suggest validation tests.
Pipeline/code: {pipeline}
```

---

## 10. Practical Drills

### Drill 1 — Column-space thinking

Given `A` and `b`:

1. Write columns of `A`.
2. Ask whether `b` is a combination of columns.
3. Compute rank.
4. Solve or project.

---

### Drill 2 — Least squares as projection

Given data `(x_i, y_i)`:

1. Build design matrix `A`.
2. Solve `min ||Ax - y||²`.
3. Compute residual.
4. Verify `Aᵀr = 0`.
5. Interpret the fitted model.

---

### Drill 3 — PCA/SVD data diagnosis

Given data matrix `X`:

1. Center columns.
2. Compute SVD.
3. Plot singular values.
4. Estimate rank / intrinsic dimension.
5. Project onto first `k` components.
6. Inspect reconstruction residual.

---

### Drill 4 — Dynamics from eigenvalues

Given `x_{t+1} = Ax_t`:

1. Compute eigenvalues.
2. Identify stable/unstable modes.
3. Decompose initial state into eigenvectors.
4. Predict long-run behavior.

---

### Drill 5 — Graph matrix modeling

Given a network:

1. Build incidence matrix `B`.
2. Build Laplacian `L = BᵀB`.
3. Interpret nullspace.
4. Solve flow/potential problem.
5. Relate conservation to matrix equations.

---

### Drill 6 — Neural network dimensions

Given a neural network:

1. Write every layer shape.
2. Write every activation shape.
3. Count parameters.
4. Derive forward pass.
5. Sketch backprop shape flow.
6. Identify where linear algebra dominates compute.

---

## 11. For Quant / Trading / Time-Series Use

This skill can be directly applied to quantitative research.

### 11.1 Return matrix as data matrix

Let:

```text
R ∈ R^{T×N}
```

where:

- `T` = time points
- `N` = assets
- rows = market states over time
- columns = asset return series

Apply:

```text
center R
standardize columns
compute covariance/correlation
perform eigen/SVD/PCA
inspect factors
model residuals
```

---

### 11.2 Factor model as projection

A linear factor model:

```text
r_t ≈ B f_t + ε_t
```

or cross-sectional form:

```text
r ≈ Bβ + ε
```

is a projection of returns onto factor space.

Questions:

1. What is the column space of `B`?
2. What part of returns is explained?
3. What remains in residuals?
4. Are residuals structured?
5. Are factors stable?
6. Is the factor matrix ill-conditioned?

---

### 11.3 PCA factors

For standardized returns `Y`:

```text
Σ = (1/(T-1)) YᵀY
Σv_i = λ_i v_i
```

Interpretation:

- large eigenvalues = dominant market/sector modes
- eigenvectors = asset loading directions
- projected returns = factor returns
- residuals = returns outside dominant subspace

Always inspect:

```text
explained variance
factor stability
eigenvalue gaps
residual autocorrelation
out-of-sample behavior
```

---

### 11.4 Risk as quadratic form

Portfolio variance:

```text
risk = wᵀΣw
```

This is positive definite / semidefinite geometry.

Use:

- eigenvectors to find risk modes
- shrinkage to stabilize covariance
- constraints to control exposures
- projection to neutralize unwanted factor directions

---

## 12. Anti-Patterns

Avoid:

1. Computing without dimension checks.
2. Inverting matrices unnecessarily.
3. Using normal equations blindly when `A` is ill-conditioned.
4. Treating PCA as magic instead of SVD geometry.
5. Treating deep learning as unrelated to linear algebra.
6. Ignoring residuals.
7. Ignoring rank.
8. Ignoring the nullspace.
9. Confusing exact solution with best approximate solution.
10. Explaining formulas without pictures or meaning.

---

## 13. Minimal Code Patterns

### 13.1 Stable least squares

```python
import numpy as np

def stable_lstsq(A: np.ndarray, b: np.ndarray):
    A = np.asarray(A, dtype=float)
    b = np.asarray(b, dtype=float)

    if A.ndim != 2:
        raise ValueError("A must be a 2D matrix.")
    if b.shape[0] != A.shape[0]:
        raise ValueError("Dimension mismatch: A is m×n, b must have length m.")

    x, residuals, rank, svals = np.linalg.lstsq(A, b, rcond=None)
    r = b - A @ x

    return {
        "x": x,
        "residual": r,
        "residual_norm": np.linalg.norm(r),
        "rank": rank,
        "singular_values": svals,
        "condition_estimate": svals[0] / svals[-1] if svals[-1] > 0 else np.inf,
        "orthogonality_check_Atr": A.T @ r,
    }
```

---

### 13.2 PCA via SVD

```python
import numpy as np

def pca_svd(X: np.ndarray, k: int | None = None, standardize: bool = True):
    X = np.asarray(X, dtype=float)

    if X.ndim != 2:
        raise ValueError("X must be a 2D data matrix: rows=samples, columns=features.")

    Xc = X - X.mean(axis=0, keepdims=True)

    if standardize:
        scale = Xc.std(axis=0, ddof=1, keepdims=True)
        scale = np.where(scale > 1e-12, scale, 1.0)
        Xc = Xc / scale

    U, s, Vt = np.linalg.svd(Xc, full_matrices=False)

    eigvals = (s ** 2) / max(X.shape[0] - 1, 1)
    explained = eigvals / eigvals.sum() if eigvals.sum() > 0 else np.full_like(eigvals, np.nan)

    if k is not None:
        U, s, Vt = U[:, :k], s[:k], Vt[:k, :]

    scores = U * s

    return {
        "scores": scores,
        "loadings": Vt.T,
        "singular_values": s,
        "explained_variance_ratio": explained[:k] if k is not None else explained,
    }
```

---

### 13.3 Factor neutral projection

```python
import numpy as np

def project_factor_neutral(w_raw: np.ndarray, B: np.ndarray, dollar_neutral: bool = True):
    """
    Project raw weights onto the nullspace of constraints.

    B: N × k factor exposure matrix.
    w_raw: N-vector of raw portfolio weights.
    """

    w = np.asarray(w_raw, dtype=float).reshape(-1)
    B = np.asarray(B, dtype=float)

    if B.shape[0] != w.shape[0]:
        raise ValueError("B must have N rows matching len(w_raw).")

    constraints = [B.T]

    if dollar_neutral:
        constraints.append(np.ones((1, len(w))))

    C = np.vstack(constraints)  # shape: c × N

    # Projection onto nullspace of C:
    # w_proj = w - C.T (C C.T)^+ C w
    correction = C.T @ np.linalg.pinv(C @ C.T) @ (C @ w)
    w_proj = w - correction

    return w_proj
```

---

## 14. One-Sentence Skill Summary

> Turn every problem into matrices, see the geometry through subspaces and projections, choose stable factorizations, interpret residuals, and connect the computation back to the real system.
