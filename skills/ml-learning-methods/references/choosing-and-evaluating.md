# Choosing and evaluating a learning method

Start from the output needed and the experience available. “We have unlabeled data” is not enough to choose masked learning. The data must contain relationships that can teach something useful, the target must preserve the relevant information, and the training cost must beat the available alternatives.

The recommendations in this chapter are practical synthesis from the preceding mechanisms. They are starting points for comparison, not a published universal ranking.

## Contents

- [A decision sequence](#a-decision-sequence)
- [Problem-to-method matrix](#problem-to-method-matrix)
- [Choosing among self-supervised objectives](#choosing-among-self-supervised-objectives)
- [Worked project choices](#worked-project-choices)
- [Evaluation that matches the claim](#evaluation-that-matches-the-claim)
- [Cost and evidence](#cost-and-evidence)
- [A learning path with exercises](#a-learning-path-with-exercises)

## A decision sequence

1. **Name the product.** Is it a class, number, embedding, restored observation, generated sample, action policy, or causal estimate?
2. **Name the available information.** Which labels, natural pairs, sequences, demonstrations, action logs, rewards, or equations are present? Which are trustworthy?
3. **Name the generalization unit.** A new row, person, device, document, institution, location, time period, species, or task?
4. **Inspect reusable models and simpler baselines.** A linear head on existing features may solve the actual problem before pretraining is justified.
5. **Match the objective to the missing capability.** Choose masking to exploit missing-content structure, contrastive learning to organize similarities, RL to improve consequences, and so on.
6. **Compare under the intended use.** Match data access, adaptation, compute, and latency assumptions. Change the method when evidence identifies its limiting assumption.

This sequence prevents a common error: choosing a fashionable training task and only later asking which application it might help.

## Problem-to-method matrix

| Situation | First credible comparison | Why it fits | What would justify another method? |
| --- | --- | --- | --- |
| Labeled heterogeneous table | Regularized linear model and boosted trees | Strong simple feature-to-target mappings | A suitable tabular foundation model or other method wins on the real split |
| Few image labels | Frozen pretrained image features plus a head | Reuses existing visual learning | Domain mismatch or missing fine detail warrants adaptation/pretraining |
| Many domain-specific unlabeled images | Existing features, then masked or teacher–student pretraining | Exploits domain structure | Contrastive views or labels target semantics more directly |
| Semantic text/image retrieval | Appropriate pretrained embeddings | Similarity is the output | Domain pairs or hard negatives reveal errors that contrastive tuning can fix |
| Text classification | Sparse text baseline and pretrained encoder | Direct label signal with cheap baselines | Longer context or domain language needs adaptation |
| Missing observations/inpainting | Conditional predictor trained on realistic missingness | Directly models available versus absent information | Need diverse completions rather than a point estimate |
| High-quality image/audio synthesis | Suitable existing conditional generator | Reuses expensive distribution learning | Domain, control, rights, or serving constraints justify training/adaptation |
| Forecasting | Seasonal/persistence baseline and supervised temporal model | Direct future-target evaluation | Masked/latent pretraining transfers across many series or scarce labels |
| Cheap labels for a few examples | Transfer plus active acquisition | Addresses label scarcity directly | Unlabeled consistency improves performance beyond acquisition alone |
| Noisy rules or distant labels | Weak supervision with a reviewed evaluation set | Uses available expertise at scale | Labels are too correlated or biased; collect direct annotations |
| Logged sequential actions | Behavior cloning and conservative offline RL | Uses existing trajectories | Coverage is insufficient; new interaction data is required |
| One-step action with observable reward | Contextual bandit | Matches partial feedback and exploration | Long-term state effects require RL or a richer model |
| New tasks with tiny support sets | Strong transfer baseline; then meta-learning | Reuses cross-task structure | Repeated task distribution makes specialized rapid adaptation pay off |
| Intervention effect | Causal design plus appropriate estimators | The question concerns changing the world | Identification fails; more flexible prediction does not solve it |
| Separate data-owning clients | Federated variant of a suitable objective | Respects data locality | Centralization is feasible and simpler, or client heterogeneity defeats sharing |

The table identifies comparisons, not specific current model releases. Verify current availability and benchmark scope before choosing a release. The contrast between older tabular benchmarks and the bounded TabPFN results is one reason to keep such recommendations conditional.[^37][^78]

## Choosing among self-supervised objectives

| Desired information | Plausible objective | Main question before choosing |
| --- | --- | --- |
| Contextual language features | Masked token or span prediction | Does the task need contextual encoding, generation, or retrieval geometry? |
| Dense spatial information | Masked image or spatial teacher-feature prediction | Are small locations and details preserved? |
| View-invariant global identity | Contrastive or teacher–student view matching | Are the view transformations valid for the task? |
| Shared image–text semantics | Cross-modal contrastive matching | Are pairs accurate and sufficiently descriptive? |
| Predictable dynamics | Temporal or action-conditioned latent prediction | What can observations identify, and which actions are covered? |
| Raw missing-content restoration | Reconstruction under realistic corruption | Is a mean prediction acceptable or are diverse outcomes needed? |
| A complete sample distribution | Autoregressive, variational, adversarial, flow, or diffusion training | Is there a specified distribution and effective sampler? |

These objectives can be combined. wav2vec 2.0 uses masking and contrastive prediction; data2vec combines masking and teacher targets. Choose combinations for a specific information need, not to accumulate methods.[^21][^10]

## Worked project choices

### Unlabeled images and a small annotation budget

Suppose a project has many photographs from a distinctive camera and a few hundred category labels. First compare frozen pretrained features plus a small head with limited fine-tuning. Split by the source object or acquisition session so repeated views do not inflate the result.

If the features fail on the camera's peculiar appearance, domain pretraining is a candidate. Masking exploits image structure without category labels. Contrastive learning becomes plausible when transformations preserve the categories. Teacher features may help when raw pixel detail is a distraction. The decisive outcome is classification or retrieval improvement at the available label and compute budget.

A lower pretraining loss alone would not justify the training expense. If the model misses a tiny color cue, a supposedly stronger invariant representation could worsen the task.

### Searching a specialized document collection

Start with lexical search and a suitable pretrained embedding model, then examine actual failed queries. If terminology causes misses, supervised or weakly supervised query–document pairs may improve contrastive retrieval. If the documents require unusual linguistic structure, domain language pretraining might help, but it solves a less direct objective.

A masked language model predicts missing tokens; it does not automatically place whole documents in the desired nearest-neighbor geometry. A cross-encoder that jointly reads a query and candidate can also rerank a short list, trading more inference work for richer interaction. Compare retrieval recall and ranking relevance, not language-model perplexity alone.

### A time series with gaps and a forecasting requirement

Distinguish interpolation from forecasting. Filling a missing middle value can use later observations; predicting tomorrow cannot. Masked training that sees both sides can be useful pretraining, but its evaluation must not silently become a forecast with future context.

Use a time-based split and include the naive last-value or seasonal forecast. Fit preprocessing within training periods. If pretraining on many related series helps the true future horizon, retain it; otherwise direct supervised forecasting may be sufficient. Missing-data patterns at deployment should also be represented.

### A robot with passive videos and some demonstrations

Passive video can teach visual regularities and predictable motion. Demonstrations can teach actions. A model of how actions change the scene needs relevant action-conditioned information; a planner also needs an objective. V-JEPA 2's separation between observation-based pretraining and action-conditioned world-model training is a concrete example of those roles.[^12]

Compare behavior cloning before adopting a complex RL pipeline. If the learner leaves the demonstration distribution, collecting expert responses in those states may be more valuable than adding model capacity. If offline logs omit useful actions, conservative optimization can limit extrapolation but cannot reveal their outcomes.[^54][^52]

### Improving response preferences

If the project has good example responses, supervised fine-tuning is a direct baseline. If it has meaningful pairwise judgments, DPO is a candidate. If a reliable reward can evaluate newly sampled responses and exploration is valuable, an RL method becomes plausible.[^51][^49]

The evaluation should separately assess preference, correctness, and task completion. A preference judge can prefer eloquent errors; a pass/fail verifier can miss important behavior. Select training feedback that measures the needed improvement.

## Evaluation that matches the claim

### Separate the learned products

| Claim | Suitable measurement | What it does not establish |
| --- | --- | --- |
| “Good reconstruction” | Error on hidden content under realistic corruption | Useful semantic features or diverse samples |
| “Good frozen representation” | Fixed encoder with specified head, k-NN, or retrieval protocol | Best result after updating the encoder |
| “Good for fine-tuning” | Target-task performance after stated adaptation | Quality without labels or adaptation |
| “Good generator” | Conditional correctness, fidelity, diversity, coverage, latency | Accurate beliefs or reliable planning |
| “Good uncertainty” | Calibration/coverage and informativeness on appropriate data | Robustness to arbitrary shift |
| “Good policy” | Expected return and relevant failures in the intended environment | Causal identification from unsupported logs |
| “Good causal estimate” | Identification assumptions, design, estimator diagnostics, sensitivity | Causality inferred from prediction accuracy alone |

**Linear probing** freezes the representation and trains a linear head. **Full fine-tuning** updates the representation. These answer different questions; the original MAE comparisons demonstrate that their rankings can differ.[^2]

### Prevent leakage at the right boundary

Split before fitting preprocessing and before constructing any training resource that must not observe held-out data. Deduplicate across splits. Keep related measurements together when the target is a new object or person. For forecasting, use the past to predict the future. Hyperparameter selection needs validation data separate from the final test.[^80]

Self-supervised pretraining can also leak evaluation content. Using unlabeled test inputs may be legitimate in a declared transductive protocol, but it differs from generalizing to genuinely unseen inputs. Foundation-model comparisons should disclose known upstream overlap and acknowledge when it cannot be fully audited.

### Pick metrics with the right costs

For imbalanced classification, accuracy can reward predicting the majority. Inspect precision and recall at a useful operating point, ranking metrics where appropriate, probability calibration when probabilities drive decisions, and subgroup outcomes. A threshold belongs to the application's cost tradeoff.

For regression, distinguish typical error, rare large error, and interval quality. For retrieval, evaluate actual relevant candidates and query types. For generation, consider fidelity and coverage together: excellent samples from a narrow subset can conceal mode dropping. For control, report outcomes over meaningful seeds, starting states, and conditions.

### Inspect distribution shift and shortcuts

Evaluate changes that are plausible in use: a camera, lighting condition, source website, vocabulary, season, or population. A model can exploit easy associations that hold in random splits but fail in new environments. Shortcut-learning research motivates testing such failures directly.[^60]

Worst-group performance can matter even when average performance improves. Group DRO research shows that changing the optimization target is not enough if the model overfits the groups' training examples; regularization and generalization still matter.[^63]

Conformal intervals illustrate another boundary: marginal coverage under exchangeability does not promise equally good coverage for every subgroup or after distribution shift. Evaluate the condition under which the guarantee will be used.[^62]

## Cost and evidence

Compare the entire chain:

$$
\text{total cost}=\text{data acquisition}+\text{labels}+\text{pretraining}
+\text{adaptation/tuning}+\text{serving over expected use}.
$$

This is an accounting identity, not a universal numerical cost model. The same pretrained checkpoint can be economical for its user and expensive to create. A technique with fewer trainable parameters can still require large activations and an expensive base-model forward pass. A generator with parallel updates can still require many refinement steps.

When comparing papers, check the dataset and duplicate policy, upstream labels or paired data, model size, training duration, image/text resolution, adaptation head, augmentation, evaluation split, and tuning budget. A recipe change can look like an objective breakthrough if these differ. RoBERTa is a useful example of how revisiting training choices changed the comparison.[^3]

Treat small differences cautiously when there are few independent evaluation cases or high training variance. Repeat only where uncertainty could change the choice. Practical measurements should answer a decision, such as whether to spend annotation budget or deploy a more expensive model.

## A learning path with exercises

These are optional experiments, not prerequisites for using the resource.

| Exercise | Change one thing | Prediction to examine |
| --- | --- | --- |
| Small text cloze task | Hide one token, then a span | Which contexts become ambiguous? |
| Masked image reconstruction | Vary patch size and corruption pattern | Does a harder task improve useful features or merely error? |
| Contrastive toy images | Add a transformation that erases the label cue | Does enforcing the wrong invariance hurt? |
| Fixed features | Fit a linear head, then allow adaptation | Do method rankings change? |
| Tabular prediction | Compare linear and tree baselines on random versus time/group splits | Was apparent performance driven by leakage or stationary assumptions? |
| Pseudo-labeling | Inspect confident wrong predictions before retraining | Which classes amplify errors? |
| Simple bandit | Compare greedy and exploratory policies | What is the cost of never testing alternatives? |
| Sequential tasks | Learn task A, then B, with and without replay | How much new learning and forgetting occur? |

A paper-reading sequence follows the conceptual relationships: denoising autoencoders → BERT → MAE → SimCLR/BYOL/VICReg → I-JEPA/data2vec → VAE/DDPM/flow matching → masked diffusion. For breadth, pair this with the supervised/classical chapter and the RL/adaptation chapter. The [source bibliography](sources.md) links the original work.

For each method, write four lines in your own words: the visible input, the target, the loss, and what survives for downstream use. Then name one task it should help and one assumption that could make it fail. That exercise is more informative than memorizing the acronym.

## Sources

[^37]: Léo Grinsztajn; Edouard Oyallon; Gaël Varoquaux. [Why do tree-based models still outperform deep learning on tabular data?](https://arxiv.org/abs/2207.08815). 2022-07-18.

[^78]: Noah Hollmann; Samuel Müller; Lennart Purucker; et al. [Accurate predictions on small data with a tabular foundation model](https://www.nature.com/articles/s41586-024-08328-6). 2025-01-08.

[^21]: Alexei Baevski; Henry Zhou; Abdelrahman Mohamed; et al. [wav2vec 2.0: A Framework for Self-Supervised Learning of Speech Representations](https://arxiv.org/abs/2006.11477). 2020-06-20.

[^10]: Alexei Baevski; Wei-Ning Hsu; Qiantong Xu; et al. [data2vec: A General Framework for Self-supervised Learning in Speech, Vision and Language](https://arxiv.org/abs/2202.03555). 2022-02-07.

[^12]: Mido Assran; Adrien Bardes; David Fan; et al. [V-JEPA 2: Self-Supervised Video Models Enable Understanding, Prediction and Planning](https://arxiv.org/abs/2506.09985). 2025-06-11.

[^54]: Stephane Ross; Geoffrey J. Gordon; J. Andrew Bagnell. [A Reduction of Imitation Learning and Structured Prediction to No-Regret Online Learning](https://arxiv.org/abs/1011.0686). 2010-11-02.

[^52]: Aviral Kumar; Aurick Zhou; George Tucker; et al. [Conservative Q-Learning for Offline Reinforcement Learning](https://arxiv.org/abs/2006.04779). 2020-06-08.

[^51]: Long Ouyang; Jeff Wu; Xu Jiang; et al. [Training language models to follow instructions with human feedback](https://arxiv.org/abs/2203.02155). 2022-03-04.

[^49]: Rafael Rafailov; Archit Sharma; Eric Mitchell; et al. [Direct Preference Optimization: Your Language Model is Secretly a Reward Model](https://arxiv.org/abs/2305.18290). 2023-05-29.

[^2]: Kaiming He; Xinlei Chen; Saining Xie; et al. [Masked Autoencoders Are Scalable Vision Learners](https://arxiv.org/abs/2111.06377). 2021-11-11.

[^80]: scikit-learn contributors. [3.1. Cross-validation: evaluating estimator performance](https://scikit-learn.org/stable/modules/cross_validation.html). Living documentation; accessed 2026-09-11.

[^60]: Robert Geirhos; Jörn-Henrik Jacobsen; Claudio Michaelis; et al. [Shortcut Learning in Deep Neural Networks](https://arxiv.org/abs/2004.07780). 2020-04-16.

[^63]: Shiori Sagawa; Pang Wei Koh; Tatsunori B. Hashimoto; et al. [Distributionally Robust Neural Networks for Group Shifts: On the Importance of Regularization for Worst-Case Generalization](https://arxiv.org/abs/1911.08731). 2019-11-20.

[^62]: Anastasios N. Angelopoulos; Stephen Bates. [A Gentle Introduction to Conformal Prediction and Distribution-Free Uncertainty Quantification](https://arxiv.org/abs/2107.07511). 2021-07-15.

[^3]: Yinhan Liu; Myle Ott; Naman Goyal; et al. [RoBERTa: A Robustly Optimized BERT Pretraining Approach](https://arxiv.org/abs/1907.11692). 2019-07-26.
