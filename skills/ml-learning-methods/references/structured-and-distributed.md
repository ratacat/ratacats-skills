# Structured, probabilistic, and distributed learning

Some methods add assumptions about the world; others change how computation or data are organized. Bayesian inference, graph learning, causal estimation, physics constraints, and federated training can combine with the objectives in the other chapters. Treating them as mutually exclusive types of ML hides their usefulness.

## Contents

- [Bayesian and probabilistic learning](#bayesian-and-probabilistic-learning)
- [Causal learning](#causal-learning)
- [Graphs and relational structure](#graphs-and-relational-structure)
- [Scientific learning and symbolic models](#scientific-learning-and-symbolic-models)
- [Federated and distributed learning](#federated-and-distributed-learning)
- [Other cross-cutting techniques](#other-cross-cutting-techniques)

## Bayesian and probabilistic learning

Bayesian inference updates uncertainty through

$$
p(\theta\mid D)=\frac{p(D\mid\theta)p(\theta)}{p(D)}.
$$

The prior $p(\theta)$ expresses assumptions before observing $D$, the likelihood expresses how parameters generate observations, and the posterior combines them. Prediction averages over posterior uncertainty:

$$
p(y_*\mid x_*,D)=\int p(y_*\mid x_*,\theta)p(\theta\mid D)\,d\theta.
$$

This differs from using one fitted parameter vector, although point-estimate approximations such as maximum a posteriori estimation are common. Bayesian and supervised are compatible labels: one describes inference, the other the available targets.[^73]

**Epistemic uncertainty** concerns uncertainty about the model or parameters. **Aleatoric uncertainty** concerns variability remaining in outcomes under the observation model. Their division depends on the model and information available. Collecting better measurements can make what looked irreducible become predictable.

A Gaussian process places a prior over functions through a mean and covariance kernel. Conditioning provides predictions and uncertainties informed by similarity to observed inputs. Exact dense GP regression usually requires cubic work in the number of observations for a matrix factorization and quadratic storage; sparse or structured approximations change these costs. The kernel's assumptions matter as much as the presence of error bars.[^73]

Probabilistic graphical models factor a joint distribution using a graph of dependencies. Hidden-state and mixture models introduce latent explanations of observations. EM, variational inference, and sampling methods offer different ways to fit or infer those explanations. A Gaussian mixture's soft assignments, for example, quantify component membership under a model rather than proving natural categories exist.[^90][^25]

**Use when:** uncertainty is part of the decision, data are limited, prior structure is valuable, or latent variables express a meaningful scientific model. **Weaknesses:** posterior inference may be expensive or approximate; priors and likelihoods can be wrong; a concentrated posterior can be confidently wrong under misspecification.

Bayesian optimization uses a probabilistic surrogate and an acquisition rule to choose the next expensive evaluation. Expected improvement and related rules balance predicted value with uncertainty. It is useful for small-budget optimization of costly experiments or hyperparameters, not usually a replacement for gradient descent over millions of network weights.[^93]

Conformal prediction is a different route to uncertainty sets. Under an appropriate exchangeability setup, a calibration procedure can provide marginal coverage without requiring a correct parametric model. The guarantee is not automatically conditional on each subgroup or valid after arbitrary distribution shift. Set width and subgroup performance remain operational questions.[^62]

## Causal learning

Prediction asks what is associated with an outcome given observed information. Causal inference asks what would happen under an intervention. In general,

$$
p(y\mid x)\ne p(y\mid\operatorname{do}(x)).
$$

Seeing an umbrella predicts rain; making someone carry an umbrella does not cause rain. A high-accuracy predictor of historical outcomes can therefore be a poor tool for deciding which intervention to perform.

A causal estimate needs a defined intervention, target population, outcome, and identification strategy. Randomization can support identification. Observational approaches rely on assumptions such as adequate confounder measurement, consistency, and positivity or overlap for the comparison. Flexible ML can estimate components of a causal procedure; it does not remove these requirements.[^83]

**Causal discovery** attempts to infer aspects of causal structure from data plus assumptions. Conditional independences can leave several graphs observationally equivalent. Time order, interventions, non-Gaussianity, functional restrictions, or multiple environments can supply additional information. State which assumptions identify which part of the structure.

Invariant causal prediction uses stability across environments to identify causal predictors under specified assumptions. The useful idea is that certain causal mechanisms remain stable when other parts of a system change. It does not imply that every empirically invariant predictor is causal or that every causal relationship is constant under every intervention.[^55]

**Use when:** the intended question changes the world—policy, experiment, treatment, operational intervention—rather than only predicting it. **Weaknesses:** unmeasured confounding, unsupported interventions, measurement error, and wrong structural assumptions can dominate prediction accuracy.

A latent world model and a causal model are not synonyms. Passive observations can support good forecasts without identifying how a particular action changes the system. Action-conditioned data and carefully designed evaluation are needed when the result will guide intervention.

## Graphs and relational structure

Graph learning represents entities and their relationships. A message-passing layer updates a node from its own state and aggregated neighbor information:

$$
h_v^{(l+1)}=\phi\left(h_v^{(l)},
\operatorname{AGG}_{u\in\mathcal N(v)}\psi(h_v^{(l)},h_u^{(l)},e_{uv})\right).
$$

$e_{uv}$ represents edge information, and aggregation commonly respects permutation of neighbors. GraphSAGE learns aggregation functions for inductive representation of nodes rather than merely storing a separate embedding for every training node.[^41]

Graph tasks include node classification, link prediction, whole-graph prediction, and masked attribute or subgraph reconstruction. Their supervision may be explicit labels, observed edges, or artificial masking. Molecular property prediction and community-link prediction share graph structure but need different assumptions and splits.

**Strength:** the architecture can express relations that a flat feature table would obscure. **Weaknesses:** neighbors may be misleading; repeated aggregation can blur distinct node features; many distant signals can bottleneck through a small representation. Missing edges and sampled neighborhoods change what the model sees.

Distinguish **transductive** evaluation, where unlabeled test nodes can be part of the available graph, from **inductive** evaluation on genuinely new nodes or graphs. For temporal links, prevent future edges from appearing in the context. A random edge split can answer a much easier question than predicting future relationships.

## Scientific learning and symbolic models

A physics-informed neural network combines data fitting with residuals of governing equations and boundary or initial conditions. For a differential operator $\mathcal N$ and solution model $u_\theta$, a schematic loss is

$$
\mathcal L=\lambda_d\mathcal L_{\mathrm{data}}
+\lambda_p\|\mathcal N[u_\theta]\|^2
+\lambda_b\mathcal L_{\mathrm{boundary}}.
$$

This embeds knowledge in the objective. It can help when observations are sparse and the equations are appropriate. The original PINN work develops data-driven PDE solution and discovery; the mere use of an equation penalty does not guarantee an accurate or efficient numerical solution.[^56]

Neural operators learn maps between functions, such as an input coefficient field and a solution field. Fourier Neural Operators parameterize operations in Fourier space to learn across a family of PDE instances. This is different from fitting one coordinate-to-solution function. Training-data generation and out-of-family generalization belong in the total cost.[^57]

**Symbolic regression** searches for explicit formulas fitting observations. SINDy uses sparsity over a library of candidate terms to recover compact dynamical equations. Its value comes from a suitable function library, measurements, and sparse structure. Noise in derivative estimates or a missing term in the library can break the inference.[^67]

**Neuro-symbolic learning** combines learned representations with explicit logical, algebraic, or program structure. The benefit depends on where the structure constrains the model: in data generation, the architecture, a loss, inference, or a solver. The label alone does not identify a single algorithm or guarantee interpretability.

For scientific use, compare against the appropriate numerical or statistical method. Check residuals, boundary behavior, extrapolation, and the desired physical quantity. A visually plausible field can violate conservation, and an equation with a small fitted residual can still be wrong outside the observed regime.

## Federated and distributed learning

**Distributed training** divides computation among workers. Data parallelism gives workers different examples and aggregates gradients; model parallelism divides parameters or layers; other schemes partition optimizer state. These choices affect resource use and synchronization, not the supervision source.

**Federated learning** addresses decentralized data owners. In a representative FedAvg round, a server sends model parameters to selected clients, clients train locally, and the server aggregates their updates. Data can remain local while a shared model improves. Heterogeneous client distributions, varying participation, and communication cost become core statistical and systems constraints.[^47]

**Federated does not mean private.** Model updates can contain information about local examples. Secure aggregation protects individual contributions from direct inspection by an aggregator under its threat model, while still revealing the permitted aggregate. Differential privacy bounds how much the released computation can depend on one protected unit. They address different risks.[^79][^48]

DP-SGD clips per-example gradients and adds calibrated noise, with privacy accounting across training. The privacy unit—example or user—must be stated. Clipping, sampling, noise, number of steps, and accounting assumptions affect both privacy and utility. Aggregation alone supplies no differential-privacy guarantee.[^48]

| Setting | Why consider it | Main added cost |
| --- | --- | --- |
| Centralized training | Data can be pooled and managed together | Data movement and central governance |
| Distributed centralized training | Compute or memory exceeds one device | Communication and coordination |
| Federated training | Raw data should remain with separate owners | Client heterogeneity, participation, aggregation |
| Secure aggregation | Aggregator should not inspect individual updates | Cryptographic protocol and failure handling |
| Differentially private training | Need a bounded influence/privacy guarantee | Accuracy tradeoff and privacy accounting |

A federated system can train supervised classifiers, self-supervised encoders, or other compatible objectives. Privacy and distribution are orthogonal to whether the target is a label, a missing patch, or a preference.

## Other cross-cutting techniques

| Technique | What changes | Appropriate use and limit |
| --- | --- | --- |
| Regularization | Penalizes or restricts fitted solutions | Helps generalization; must match the relevant complexity |
| Data augmentation | Changes training examples under assumed invariances | Useful only if transformations preserve what the target needs |
| Curriculum learning | Changes order or difficulty of experience | May ease optimization; can hide data-selection advantages |
| Self-play | Learner generates experience through interactions with versions of itself | Useful in games and competitive domains; training opponents can narrow behavior |
| Adversarial robustness | Trains or evaluates under constrained input perturbations | Robustness is relative to the allowed perturbation set |
| Multi-agent learning | Several decision-makers adapt or interact | Other learners make the environment change during training |
| Evolutionary optimization | Searches populations of parameter or program candidates | Works without useful gradients; can require many evaluations |
| Hyperparameter search | Selects among training procedures | Must use validation data; tuning effort belongs in comparisons |
| Test-time adaptation | Updates a model using deployment-time signals | May help shift; a bad self-supervised signal can degrade the model |

Evolution strategies demonstrate black-box optimization of policy parameters through perturbed evaluations. They supply an alternative optimizer for some RL tasks; they do not make the reward source disappear. Bayesian optimization likewise chooses expensive trials, whereas gradient methods update a model within a trial.[^94][^93]

The useful question for every cross-cutting technique is which assumption or constraint it changes. If that constraint is not the bottleneck in the application, adding the technique can increase complexity without improving the result.

## Sources

[^73]: Carl Edward Rasmussen; Christopher K. I. Williams. [Gaussian Processes for Machine Learning](https://gaussianprocess.org/gpml/). 2006.

[^90]: scikit-learn contributors. [2.1. Gaussian mixture models](https://scikit-learn.org/stable/modules/mixture.html). Living documentation; accessed 2026-09-11.

[^25]: Diederik P Kingma; Max Welling. [Auto-Encoding Variational Bayes](https://arxiv.org/abs/1312.6114). 2013-12-20.

[^93]: Jasper Snoek; Hugo Larochelle; Ryan P. Adams. [Practical Bayesian Optimization of Machine Learning Algorithms](https://arxiv.org/abs/1206.2944). 2012-06-13.

[^62]: Anastasios N. Angelopoulos; Stephen Bates. [A Gentle Introduction to Conformal Prediction and Distribution-Free Uncertainty Quantification](https://arxiv.org/abs/2107.07511). 2021-07-15.

[^83]: Miguel A. Hernán; James M. Robins. [Causal Inference: What If](https://miguelhernan.org/whatifbook). 2020; current online edition accessed 2026-09-11.

[^55]: Jonas Peters; Peter Bühlmann; Nicolai Meinshausen. [Causal inference using invariant prediction: identification and confidence intervals](https://arxiv.org/abs/1501.01332). 2015-01-06.

[^41]: William L. Hamilton; Rex Ying; Jure Leskovec. [Inductive Representation Learning on Large Graphs](https://arxiv.org/abs/1706.02216). 2017-06-07.

[^56]: Maziar Raissi; Paris Perdikaris; George Em Karniadakis. [Physics Informed Deep Learning (Part I): Data-driven Solutions of Nonlinear Partial Differential Equations](https://arxiv.org/abs/1711.10561). 2017-11-28.

[^57]: Zongyi Li; Nikola Kovachki; Kamyar Azizzadenesheli; et al. [Fourier Neural Operator for Parametric Partial Differential Equations](https://arxiv.org/abs/2010.08895). 2020-10-18.

[^67]: Steven L. Brunton; Joshua L. Proctor; J. Nathan Kutz. [Discovering governing equations from data: Sparse identification of nonlinear dynamical systems](https://arxiv.org/abs/1509.03580). 2015-09-11.

[^47]: H. Brendan McMahan; Eider Moore; Daniel Ramage; et al. [Communication-Efficient Learning of Deep Networks from Decentralized Data](https://arxiv.org/abs/1602.05629). 2016-02-17.

[^79]: Keith Bonawitz; Vladimir Ivanov; Ben Kreuter; et al. [Practical Secure Aggregation for Privacy-Preserving Machine Learning](https://research.google/pubs/practical-secure-aggregation-for-privacy-preserving-machine-learning/). 2017.

[^48]: Martín Abadi; Andy Chu; Ian Goodfellow; et al. [Deep Learning with Differential Privacy](https://arxiv.org/abs/1607.00133). 2016-07-01.

[^94]: Tim Salimans; Jonathan Ho; Xi Chen; et al. [Evolution Strategies as a Scalable Alternative to Reinforcement Learning](https://arxiv.org/abs/1703.03864). 2017-03-10.
