# Supervision and classical methods

Choose the supervision setup before assuming a particular model architecture. A table with reliable labels, a collection of unlabeled images, and a stream of rewards contain different kinds of information. Neural pretraining is one way to use that information; classical statistical methods remain useful for prediction, structure discovery, and baselines.

This chapter gives mechanisms and practical decision rules. A “good fit” identifies a plausible starting point, not a guaranteed winner.

## Contents

- [Supervised learning](#supervised-learning)
- [Classical predictive models](#classical-predictive-models)
- [Semi-supervised learning](#semi-supervised-learning)
- [Weak and positive-unlabeled supervision](#weak-and-positive-unlabeled-supervision)
- [Active learning](#active-learning)
- [Unsupervised structure discovery](#unsupervised-structure-discovery)
- [Anomaly detection and ranking](#anomaly-detection-and-ranking)
- [Why these methods still matter](#why-these-methods-still-matter)

## Supervised learning

Supervised learning observes input–target pairs. Classification predicts a category or probability; regression predicts a numerical quantity; structured prediction predicts an object such as a sequence, segmentation mask, or graph. The labels can come from humans, sensors, transactions, or later outcomes.

For multiclass classification, cross-entropy rewards assigning probability to the observed class:

$$
\mathcal L=-\sum_k y_k\log p_\theta(y=k\mid x).
$$

For numerical targets, squared error emphasizes large residuals, absolute error is less sensitive to them, and quantile loss estimates a specified conditional quantile. The appropriate loss depends on the error costs and required output, not only on whether a target is “continuous.”[^84]

**Strength:** the training target can directly match the application. **Weakness:** labels may encode an imperfect measurement process, a selection bias, or a policy that will change. A model trained to predict past decisions learns those decisions; it does not automatically learn which decision was best.

Label quantity alone is insufficient. Ten thousand repeated measurements of ten objects contain a different amount of independent evidence from ten thousand different objects. The split should reflect the unit on which the model must generalize.

## Classical predictive models

| Method | Mechanism | Good fits | Main weaknesses |
| --- | --- | --- | --- |
| Linear/ridge regression | Weighted feature sum; ridge penalizes coefficient magnitude | Numerical baselines, sparse or engineered features | Misses interactions unless represented |
| Lasso/elastic net | Penalize coefficients to encourage sparse or stabilized solutions | Many potentially irrelevant predictors | Correlated features complicate selection and interpretation |
| Logistic regression | Linear score mapped to class probabilities | Classification with sparse features or embeddings | Linear boundary in supplied feature space |
| Generalized additive model | Sum learned functions of individual features | Smooth nonlinear effects with inspectable components | Interactions require explicit extensions |
| Naive Bayes | Class-conditional feature model with conditional-independence assumptions | Sparse text and fast probabilistic baselines | Correlated evidence can produce poor probability estimates |
| k-nearest neighbors | Predict from nearby stored examples | Strong existing metric, local patterns | Scaling, irrelevant dimensions, and serving cost |
| Support vector machine | Optimize a margin, optionally through a kernel | Moderate-size datasets with useful similarity | Kernel and regularization choice; scaling of kernel methods |
| Decision tree | Recursively split feature space | Readable small models, nonlinear feature interactions | Individual trees are unstable and can overfit |
| Random forest | Average randomized trees | Tabular nonlinear prediction with limited preprocessing | Large ensembles are less interpretable; extrapolation is limited |
| Gradient-boosted trees | Add trees to reduce an objective iteratively | Heterogeneous tabular prediction and ranking | Tuning, leakage, temporal shift, and weak extrapolation |
| Gaussian process | Prior over functions updated by observations | Small-data regression and uncertainty-aware optimization | Kernel assumptions and costly exact inference |

The mechanics are documented in the official linear-model, ensemble, SVM, nearest-neighbor, and Naive Bayes references; the GP text develops the probabilistic formulation.[^84][^85][^86][^87][^92][^73]

**Bagging versus boosting.** Bagging averages models trained on resampled data to reduce variance. Random forests add randomized feature selection when building trees. Boosting combines learners sequentially to improve a loss; gradient boosting builds on loss gradients. XGBoost adds a scalable regularized tree-boosting implementation. More trees do not make a system “deep learning” in the neural-representation sense.[^85][^36]

**Interpretability is conditional.** A logistic coefficient describes an association holding the other represented features fixed; correlated features can make that association unstable. A deep tree or hundreds of trees are difficult to inspect as a whole. An explanation method can describe a model without establishing a causal explanation of the world.

**Features still matter.** Linear regression on a well-chosen nonlinear feature expansion can represent nonlinear relationships in the original variables. Conversely, a powerful model cannot recover information that was never collected. A simple head on pretrained embeddings combines classical supervised fitting with learned neural features.

## Semi-supervised learning

Semi-supervised learning combines labeled and unlabeled data. A common objective is

$$
\mathcal L=\mathcal L_{\mathrm{labeled}}+lambda\mathcal L_{\mathrm{unlabeled}}.
$$

The unlabeled term can enforce consistency across transformations, fit pseudo-labels, or exploit a graph connecting nearby examples. The central assumption is that the unlabeled distribution constrains the desired labeling in a useful way. More unlabeled examples need not help if they come from irrelevant classes or a different domain.

FixMatch makes a prediction on a weakly augmented unlabeled image and uses a sufficiently confident prediction as a pseudo-label for a strongly augmented view. This combines self-training and consistency regularization. Its strong results depend on the overall recipe, including augmentations and confidence filtering.[^34]

**Use when:** labels are scarce, unlabeled examples resemble the target population, and permissible transformations preserve class identity. **Risks:** erroneous confident predictions can reinforce themselves; minority classes may receive fewer pseudo-labels; unlabeled out-of-class examples can be forced into known categories.

Compare with supervised transfer first. A pretrained representation plus a small labeled head can be simpler and stronger than a new semi-supervised training loop. That is a practical baseline choice, not a theorem about either family.

## Weak and positive-unlabeled supervision

Weak supervision uses imperfect labels: keyword rules, distant database matches, coarse document tags, heuristic annotators, or noisy clicks. The source can be plentiful but systematically biased. Several agreeing rules may merely repeat the same underlying signal.

Snorkel combines labeling functions that may abstain or conflict, estimates a label model, and uses probabilistic labels to train a discriminative model. The pattern separates cheap labeling logic from the final predictor. It is useful when experts can write informative heuristics more cheaply than they can annotate a large dataset; correlation and coverage of the heuristics remain important.[^35]

**Positive–unlabeled learning** observes known positives and an unlabeled mixture of positives and negatives. A missing positive label is not a negative label. Non-negative PU learning modifies a risk estimator to prevent a flexible model from exploiting negative empirical risk and overfitting. Class-prior and positive-selection assumptions are part of the statistical setup.[^69]

**Multiple-instance learning** assigns labels to bags of instances, such as a document containing an unknown relevant paragraph. The familiar “a positive bag contains at least one positive instance” assumption is one formulation, not a law for every bag-labeling task. Choose aggregation to match how bag labels were produced.[^100]

Weak supervision and self-supervision can be combined. A model might first learn language structure from raw text, then train on heuristic labels, then adapt to a smaller reviewed set. Keep the supervision sources visible so errors can be attributed to the appropriate stage.

## Active learning

An active learner chooses which unlabeled examples to ask an annotator about. Common strategies consider uncertainty, disagreement among models, coverage of the input space, expected model change, or estimated reduction in error. Pool-based learning selects from a fixed candidate collection; stream-based learning decides whether to query arriving examples.[^74]

**Why it helps:** annotation effort is a resource the algorithm can allocate. **Why it fails:** an uncertain example may be an outlier, unanswerable, redundant, or expensive to label. Batch selections can all describe the same small boundary region. An already biased model can overlook important regions where it is confidently wrong.

A practical loop needs a representative evaluation set independent of acquisition. Compare error reduction per labeling dollar or hour, including rejected and ambiguous examples. Random acquisition is an important baseline; uncertainty-based selection should earn its added complexity.

Active learning is not reinforcement learning merely because it “chooses” examples. The acquisition policy can be hand-designed or learned; the final predictor can remain supervised.

## Unsupervised structure discovery

Without task labels, the objective encodes the kind of structure worth finding.

### Compression and components

**PCA** finds a low-dimensional linear subspace preserving maximum variance, equivalently minimizing squared reconstruction error under the appropriate centered orthogonal projection. High variance need not mean task relevance. A rare decisive feature may contribute little to total variance.[^89]

A linear autoencoder with a rank bottleneck and squared reconstruction loss has a close relationship to PCA at a global optimum. Its internal coordinates are not uniquely the principal components: equivalent rotations or transformations can represent the same reconstruction subspace. Nonlinear autoencoders extend the function family but lose PCA's simple geometry.[^99]

**Non-negative matrix factorization** constrains factors to nonnegative values, often encouraging additive parts. **Independent component analysis** seeks statistically independent components under its mixing assumptions. PCA decorrelates second-order statistics; independence is a stronger property. These methods answer different questions and may find different decompositions.[^89]

### Clustering

| Method | Structure it favors | Failure to watch |
| --- | --- | --- |
| k-means | Compact groups around Euclidean centroids | Feature scaling, chosen cluster count, non-spherical groups |
| Gaussian mixture | Probabilistic clusters with specified covariance structure | Local optima, model misspecification, poorly estimated components |
| Hierarchical clustering | Nested merges or splits under a linkage rule | Linkage choice changes the hierarchy; scale can be costly |
| DBSCAN | Density-connected regions plus noise | Density thresholds and varying-density clusters |
| Spectral clustering | Partition a similarity graph using its eigenstructure | Graph construction can determine the answer; large graphs cost memory |

Gaussian-mixture fitting commonly uses EM: estimate membership responsibilities, update component parameters, and repeat. Spectral clustering connects graph cuts and matrix eigenvectors; it is not just k-means with a different name.[^88][^90][^81]

Clustering does not discover uniquely correct categories without a definition of similarity and scale. The same collection can cluster by subject, writing style, language, or source website. If we care about subject, we must test whether the representation and distance actually express it.

### Visualization

**t-SNE** and **UMAP** create low-dimensional representations emphasizing neighborhood structure in different ways. They are useful for exploration, but separated islands are not sufficient evidence of real classes. Initialization, neighborhood parameters, preprocessing, and distortion affect the display. Quantify the original-space structure before turning a plot into a scientific claim.[^72][^96]

## Anomaly detection and ranking

Anomaly detection can use isolation, neighborhood density, one-class boundaries, or reconstruction. Isolation Forest exploits how readily observations can be isolated by random partitions; local outlier methods compare neighborhood density; one-class methods estimate a boundary around reference data. Novelty detection assumes a suitable reference set; unsupervised outlier detection may operate on already contaminated data.[^91]

An anomaly score answers “unusual according to this model,” not necessarily “bad.” A rare legitimate transaction and a common fraudulent pattern can break the naive equation of rarity with risk. Reconstruction models may also reconstruct unwanted inputs well. Evaluate against the operational errors and alert budget.

Ranking predicts an ordering rather than an isolated label. Pointwise objectives score items separately, pairwise objectives compare items, and listwise objectives consider a collection. Click labels carry exposure and position effects; unclicked does not necessarily mean irrelevant. Tree boosting, neural matching models, and contrastive embeddings can all participate in a ranking pipeline.[^101][^20]

## Why these methods still matter

Grinsztajn and colleagues' tabular benchmark found strong tree performance and investigated biases that favor trees on its medium-sized datasets. That evidence supports including trees in a serious comparison, not an eternal rule that neural approaches lose on tables.[^37]

The 2025 TabPFN study instead learns a tabular prediction algorithm across synthetic datasets and applies it through in-context inference. It reports strong results in a bounded small-to-medium-data regime; its principal benchmark collections were restricted to at most 10,000 samples, 500 features, and 10 classes. Those results change the comparison set without establishing universal dominance outside the evaluated regime.[^78]

For a new table, a useful sequence is a regularized linear model, a strong tree ensemble, and a suitable pretrained tabular or representation-based model when available. Compare on the actual group or time split, with realistic tuning and inference costs. The winner depends on the data and constraints.

## Sources

[^84]: scikit-learn contributors. [1.1. Linear Models](https://scikit-learn.org/stable/modules/linear_model.html). Living documentation; accessed 2026-09-11.

[^85]: scikit-learn contributors. [1.11. Ensembles: Gradient boosting, random forests, bagging, voting, stacking](https://scikit-learn.org/stable/modules/ensemble.html). Living documentation; accessed 2026-09-11.

[^86]: scikit-learn contributors. [1.4. Support Vector Machines](https://scikit-learn.org/stable/modules/svm.html). Living documentation; accessed 2026-09-11.

[^87]: scikit-learn contributors. [1.6. Nearest Neighbors](https://scikit-learn.org/stable/modules/neighbors.html). Living documentation; accessed 2026-09-11.

[^92]: scikit-learn contributors. [1.9. Naive Bayes](https://scikit-learn.org/stable/modules/naive_bayes.html). Living documentation; accessed 2026-09-11.

[^73]: Carl Edward Rasmussen; Christopher K. I. Williams. [Gaussian Processes for Machine Learning](https://gaussianprocess.org/gpml/). 2006.

[^36]: Tianqi Chen; Carlos Guestrin. [XGBoost: A Scalable Tree Boosting System](https://arxiv.org/abs/1603.02754). 2016-03-09.

[^34]: Kihyuk Sohn; David Berthelot; Chun-Liang Li; et al. [FixMatch: Simplifying Semi-Supervised Learning with Consistency and Confidence](https://arxiv.org/abs/2001.07685). 2020-01-21.

[^35]: Alexander Ratner; Stephen H. Bach; Henry Ehrenberg; et al. [Snorkel: Rapid Training Data Creation with Weak Supervision](https://arxiv.org/abs/1711.10160). 2017-11-28.

[^69]: Ryuichi Kiryo; Gang Niu; Marthinus C. du Plessis; et al. [Positive-Unlabeled Learning with Non-Negative Risk Estimator](https://arxiv.org/abs/1703.00593). 2017-03-02.

[^100]: Thomas G. Dietterich; Richard H. Lathrop; Tomás Lozano-Pérez. [Solving the multiple instance problem with axis-parallel rectangles](https://lis.csail.mit.edu/pubs/tlp/multiple-instance-aij.pdf). 1997.

[^74]: Burr Settles. [Active Learning Literature Survey](https://burrsettles.com/pub/settles.activelearning.pdf). 2009; revised 2010.

[^89]: scikit-learn contributors. [2.5. Decomposing signals in components (matrix factorization problems)](https://scikit-learn.org/stable/modules/decomposition.html). Living documentation; accessed 2026-09-11.

[^99]: Pierre Baldi; Kurt Hornik. [Neural Networks and Principal Component Analysis: Learning from Examples Without Local Minima](https://www.igb.uci.edu/~pfbaldi/publications/journals/1989/NN_and_PCA.pdf). 1989.

[^88]: scikit-learn contributors. [2.3. Clustering](https://scikit-learn.org/stable/modules/clustering.html). Living documentation; accessed 2026-09-11.

[^90]: scikit-learn contributors. [2.1. Gaussian mixture models](https://scikit-learn.org/stable/modules/mixture.html). Living documentation; accessed 2026-09-11.

[^81]: Ulrike von Luxburg. [A Tutorial on Spectral Clustering](https://arxiv.org/abs/0711.0189). 2007-11-01.

[^72]: Laurens van der Maaten; Geoffrey Hinton. [Visualizing Data using t-SNE](https://www.jmlr.org/papers/v9/vandermaaten08a.html). 2008.

[^96]: Leland McInnes; John Healy; James Melville. [UMAP: Uniform Manifold Approximation and Projection for Dimension Reduction](https://arxiv.org/abs/1802.03426). 2018-02-09.

[^91]: scikit-learn contributors. [2.7. Novelty and Outlier Detection](https://scikit-learn.org/stable/modules/outlier_detection.html). Living documentation; accessed 2026-09-11.

[^101]: XGBoost contributors. [Learning to Rank](https://xgboost.readthedocs.io/en/stable/tutorials/learning_to_rank.html). Living documentation; accessed 2026-09-11.

[^20]: Alec Radford; Jong Wook Kim; Chris Hallacy; et al. [Learning Transferable Visual Models From Natural Language Supervision](https://arxiv.org/abs/2103.00020). 2021-02-26.

[^37]: Léo Grinsztajn; Edouard Oyallon; Gaël Varoquaux. [Why do tree-based models still outperform deep learning on tabular data?](https://arxiv.org/abs/2207.08815). 2022-07-18.

[^78]: Noah Hollmann; Samuel Müller; Lennart Purucker; et al. [Accurate predictions on small data with a tabular foundation model](https://www.nature.com/articles/s41586-024-08328-6). 2025-01-08.
