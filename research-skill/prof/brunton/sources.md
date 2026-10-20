# sources.md — Curated Source Map for Steven L. Brunton Skill Pack

> This is a curated source map. It does not claim to include every message, interview, lecture, book, paper, or opinion ever made by Prof. Steven L. Brunton. It focuses on the strongest public and primary sources for reconstructing his skill stack.

---

## 1. Official / Primary Profiles

### University of Washington Mechanical Engineering profile
- URL: https://www.me.washington.edu/facultyfinder/steve-brunton
- Why it matters: official role, education, research statement, applications, selected publications.
- Extracted themes:
  - dimensionality reduction,
  - sparse sensing,
  - machine learning,
  - data-driven discovery and control,
  - low-rank coherent patterns,
  - optimal sensor/actuator placement,
  - adaptive equation-free controllers.

### Brunton Lab / Eigensteve
- URL: https://www.eigensteve.com/
- Why it matters: central hub for publications, books, videos, CV, and research activity.

### Brunton Lab publications
- URL: https://www.eigensteve.com/publications
- Why it matters: source trail for SINDy, DMD, Koopman, sparse sensing, ML for fluids, reduced-order modeling, model predictive control, PySINDy, and modern extensions.

### Brunton Lab books
- URL: https://www.eigensteve.com/copy-of-publications
- Why it matters: lists the major books that anchor Brunton’s pedagogy and research synthesis.

### NSF AI Institute in Dynamic Systems — Steven Brunton leadership page
- URL: https://dynamicsai.org/leadership/brunton/
- Why it matters: frames the modern AI + dynamics + control mission and Brunton’s role in the institute.

---

## 2. Core Books

### Data-Driven Science and Engineering: Machine Learning, Dynamical Systems, and Control
- Authors: Steven L. Brunton and J. Nathan Kutz
- Cambridge page: https://www.cambridge.org/highereducation/books/data-driven-science-and-engineering/6F9A730B7A9A9F43F68CF21A24BEC339
- Book/course site: https://databookuw.com/
- Course materials: https://databookuw.com/page-5/page-24/
- Main themes:
  - SVD,
  - Fourier and wavelet transforms,
  - sparsity and compressed sensing,
  - regression and model selection,
  - neural networks and deep learning,
  - DMD,
  - SINDy,
  - Koopman operator theory,
  - linear control,
  - balanced models for control,
  - data-driven control,
  - reduced-order models,
  - reinforcement learning,
  - physics-informed machine learning.

### Dynamic Mode Decomposition: Data-Driven Modeling of Complex Systems
- Authors: J. Nathan Kutz, Steven L. Brunton, Bingni W. Brunton, Joshua L. Proctor
- SIAM page: https://epubs.siam.org/doi/book/10.1137/1.9781611974508
- SIAM News article: https://www.siam.org/publications/siam-news/articles/data-driven-modeling-of-dynamic-systems/
- Main themes:
  - DMD as data-driven discovery of dynamical systems,
  - coherent structures,
  - high-dimensional systems,
  - connection to Koopman theory,
  - forecasting and control.

### Machine Learning Control — Taming Nonlinear Dynamics and Turbulence
- Authors: Thomas Duriez, Steven L. Brunton, Bernd R. Noack
- Springer page: https://link.springer.com/book/10.1007/978-3-319-40624-4
- Main themes:
  - machine learning control,
  - nonlinear dynamics,
  - turbulence,
  - genetic programming for feedback laws,
  - control law discovery.

### Data-Driven Fluid Mechanics: Combining First Principles and Machine Learning
- Editors: Miguel A. Mendez, Andrea Ianiro, Bernd R. Noack, Steven L. Brunton
- Cambridge page: https://www.cambridge.org/core/books/datadriven-fluid-mechanics/0327A1A43F7C67EE88BB13743FD9DC8D
- Book site: https://www.datadrivenfluidmechanics.com/index.php/about
- Main themes:
  - model-order reduction,
  - system identification,
  - flow control,
  - data-driven turbulence closures,
  - combining first principles and ML.

---

## 3. Landmark Papers and Research Threads

### Discovering governing equations from data by sparse identification of nonlinear dynamical systems
- Authors: Steven L. Brunton, Joshua L. Proctor, J. Nathan Kutz
- PNAS DOI page: https://www.pnas.org/doi/10.1073/pnas.1517384113
- arXiv: https://arxiv.org/abs/1509.03580
- Main themes:
  - sparse regression for nonlinear dynamics,
  - discovering governing equations,
  - parsimony,
  - avoiding overfitting,
  - SINDy.

### Sparse Identification of Nonlinear Dynamics with Control
- Authors: Steven L. Brunton, Joshua L. Proctor, J. Nathan Kutz
- ScienceDirect: https://www.sciencedirect.com/science/article/pii/S2405896316318298
- arXiv: https://arxiv.org/abs/1605.06682
- Main themes:
  - SINDy with inputs/control,
  - forced systems,
  - regression for nonlinear controlled dynamics,
  - links to DMD and Koopman theory.

### Data-driven discovery of partial differential equations
- Authors: Samuel H. Rudy, Steven L. Brunton, Joshua L. Proctor, J. Nathan Kutz
- DOI: https://doi.org/10.1126/sciadv.1602614
- Main themes:
  - PDE discovery,
  - sparse regression over derivative libraries,
  - governing laws from spatiotemporal data.

### Data-driven discovery of coordinates and governing equations
- Authors: Kathleen Champion, Bethany Lusch, J. Nathan Kutz, Steven L. Brunton
- PNAS / PubMed: https://pubmed.ncbi.nlm.nih.gov/31636218/
- Main themes:
  - autoencoders,
  - coordinate discovery,
  - sparse dynamics in learned latent space,
  - nonlinear model discovery.

### Deep learning for universal linear embeddings of nonlinear dynamics
- Authors: Bethany Lusch, J. Nathan Kutz, Steven L. Brunton
- Nature Communications DOI: https://doi.org/10.1038/s41467-018-07210-0
- Main themes:
  - deep learning,
  - Koopman embeddings,
  - linear representations of nonlinear dynamics.

### Machine Learning for Fluid Mechanics
- Authors: Steven L. Brunton, Bernd R. Noack, Petros Koumoutsakos
- Annual Reviews DOI: https://doi.org/10.1146/annurev-fluid-010719-060214
- arXiv: https://arxiv.org/abs/1905.11075
- PDF: https://faculty.washington.edu/sbrunton/ARFM2020.pdf
- Main themes:
  - ML fundamentals for fluids,
  - modeling,
  - optimization,
  - control,
  - strengths and limitations of ML in scientific inquiry.

### Sparse identification of nonlinear dynamics for model predictive control in the low-data limit
- Authors: Eurika Kaiser, J. Nathan Kutz, Steven L. Brunton
- DOI: https://doi.org/10.1098/rspa.2018.0335
- Main themes:
  - SINDy-MPC,
  - control in low-data regimes,
  - efficient nonlinear models for real-time control.

### Ensemble-SINDy: Robust sparse model discovery in the low-data, high-noise limit, with active learning and control
- Authors: Urban Fasel, J. Nathan Kutz, Bingni W. Brunton, Steven L. Brunton
- Proceedings of the Royal Society A: https://royalsocietypublishing.org/doi/10.1098/rspa.2021.0904
- Main themes:
  - ensemble model discovery,
  - robustness under low data / high noise,
  - active learning,
  - control.

### Modern Koopman Theory for Dynamical Systems
- Authors include Steven L. Brunton
- arXiv: https://arxiv.org/abs/2102.12086
- Main themes:
  - Koopman operator theory,
  - observables,
  - nonlinear dynamics through linear operators,
  - data-driven Koopman analysis.

### PySINDy: A comprehensive Python package for robust sparse system identification
- JOSS page: https://joss.theoj.org/papers/10.21105/joss.03994
- GitHub: https://github.com/dynamicslab/pysindy
- Main themes:
  - production software for SINDy,
  - sparse system identification,
  - reusable research tooling.

---

## 4. Lectures, Courses, and Public Pedagogy

### Eigensteve YouTube channel
- URL: https://www.youtube.com/@Eigensteve
- Why it matters: large public teaching archive on data science, dynamics, control, SINDy, DMD, optimization, and ML.

### Eigensteve YouTube playlists
- URL: https://www.youtube.com/c/Eigensteve/playlists
- Search result themes:
  - Data-Driven Science and Engineering,
  - Dynamical Systems with Machine Learning,
  - Data-Driven Control with Machine Learning,
  - Optimization,
  - Probability and statistics,
  - SINDy,
  - DMD and Koopman theory.

### Data-Driven Science and Engineering course materials
- URL: https://databookuw.com/page-5/page-24/
- Why it matters: maps the textbook into lecture materials and course structure.

### Dynamical Systems with Machine Learning playlist
- URL: https://www.youtube.com/playlist?list=PLMrJAkhIeNNR6DzT17-MM1GHLkuYVjhyt
- Main themes:
  - data-driven dynamical systems,
  - Lorenz system,
  - SINDy,
  - Koopman,
  - DMD,
  - modeling and simulation.

### Deep Learning in Fluid Mechanics course page
- URL: https://databookuw.com/page-5/page-24/
- Main themes:
  - turbulence closures,
  - time-stepping and flow maps,
  - dimensionality reduction,
  - spatiotemporal systems,
  - reinforcement learning for flow control,
  - model predictive control.

---

## 5. Interviews / Podcasts / Public Conversations

### inControl podcast episode: Steve Brunton — DMD, Koopman, SINDy, Eigensteve Channel, HydroGym, Optimization
- URL: https://www.incontrolpodcast.com/1632769/episodes/18960945-ep43-steve-brunton-dmd-koopman-sindy-eigensteve-channel-hydrogym-optimization-and-much-more
- Main themes:
  - origin story,
  - DMD and Koopman,
  - teaching and Eigensteve,
  - SINDy,
  - explainable AI,
  - HydroGym,
  - optimization.

### UW Mechanical Engineering article: “Eigensteve” Brunton: YouTubing math for engineers
- URL: https://www.me.washington.edu/news/article/2020-10-27/eigensteve-brunton
- Main themes:
  - teaching style,
  - online education,
  - mathematical visualization,
  - lightboard lectures.

### GeekWire article: Do the math with Steve Brunton
- URL: https://www.geekwire.com/2020/steve-brunton/
- Main themes:
  - public mathematical teaching,
  - YouTube pedagogy,
  - communication style.

---

## 6. Software and Code Ecosystem

### PySINDy
- URL: https://github.com/dynamicslab/pysindy
- Purpose: sparse identification of nonlinear dynamical systems.

### PyDMD
- URL: https://github.com/PyDMD/PyDMD
- Purpose: dynamic mode decomposition algorithms.

### PyKoopman
- URL: https://github.com/dynamicslab/pykoopman
- Purpose: data-driven Koopman modeling.

### HydroGym
- URL: https://github.com/dynamicslab/hydrogym
- Purpose: reinforcement-learning benchmarks for fluid flow control.

### Data book code resources
- URL: https://databookuw.com/
- Purpose: code and examples accompanying Data-Driven Science and Engineering.

---

## 7. Consolidated Skill Themes

From the sources above, the major skill clusters are:

1. **Linear algebra as the computational backbone**
   - SVD, matrix factorizations, low-rank approximation, projections, modes.

2. **Dynamical-systems-first machine learning**
   - Fit dynamics, not only static mappings.

3. **Sparse discovery**
   - Identify the few active terms that govern the system.

4. **Coordinate discovery**
   - Find variables in which the model becomes simple.

5. **Koopman/DMD thinking**
   - Use linear operators on measurements or observables to study nonlinear systems.

6. **Data-driven control**
   - Learn models that support feedback, actuation, and closed-loop design.

7. **Hybrid physics + ML**
   - Use first principles, dimensional analysis, constraints, and ML together.

8. **High-dimensional physical systems**
   - Extract coherent patterns and reduced-order models from large measurements.

9. **Sparse sensing**
   - Select small, informative measurements for reconstruction/classification/control.

10. **Pedagogical clarity**
    - Explain through geometry, equations, algorithms, and code.
