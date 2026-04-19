# Boyd Mental Models

## 1. Modeling Is the Hard Part

The solver is usually not the main problem. The main problem is formulating the objective and constraints honestly.

## 2. Convexity Is a Global-Optimum Certificate

If the problem is convex, local optimum equals global optimum. If not, say what guarantee is lost.

## 3. Constraints Are Research Claims

Every constraint encodes a belief: leverage cap, turnover cap, beta neutrality, liquidity participation, or concentration limit. Make the belief explicit.

## 4. Dual Variables Are Diagnostics

Binding constraints explain why the optimizer chose a portfolio. Use them to debug impossible or overconstrained designs.

## 5. Expected Returns Are Noisy Inputs

Optimizers amplify noisy alpha forecasts. Regularize, constrain, shrink, and perturb.

## 6. Infeasibility Is Information

If constraints are infeasible, the portfolio design is inconsistent with the signal, universe, or market structure.

