---
name: ml-learning-methods
description: Explain, compare, or choose machine-learning objectives and learning regimes, including masked prediction, self-supervision, generative modeling, reinforcement learning, transfer, and classical methods. Use for ML learning-method questions and training-design tradeoffs; not routine model API usage or infrastructure debugging.
metadata:
  category: tools
  keywords:
    - machine-learning
    - self-supervised-learning
    - masked-language-modeling
    - masked-autoencoders
    - representation-learning
    - generative-modeling
    - reinforcement-learning
  blurb: Explains how machine-learning methods work, how they relate, and when to choose them, with a detailed BERT-to-MAE guide and cited research chapters.
---

# ML learning methods

Use the reference chapters to explain mechanisms and make training choices. Start with the relevant chapter; load the full collection only for a broad survey.

## Route the question

| Question | Read |
| --- | --- |
| How do the categories fit together? | [Map of learning](references/map.md) |
| Cloze tasks, BERT, MAE, masking ratios, or prediction targets | [Masked prediction](references/masked-prediction.md) |
| Contrastive learning, collapse, teachers, embeddings, or JEPA | [Representation learning](references/representation-learning.md) |
| Autoregression, VAEs, GANs, diffusion, flows, or masked generation | [Generative learning](references/generative-learning.md) |
| Labels, pseudo-labels, weak supervision, trees, kernels, or clustering | [Supervision and classical methods](references/supervision-and-classical.md) |
| Rewards, imitation, preferences, transfer, LoRA, meta-learning, or forgetting | [Decisions and adaptation](references/decisions-and-adaptation.md) |
| Bayesian, causal, graph, scientific, federated, or distributed learning | [Structured and distributed learning](references/structured-and-distributed.md) |
| Choosing a method, modality examples, evaluation, or learning exercises | [Choosing and evaluating](references/choosing-and-evaluating.md) |
| Original papers and research lineage | [Sources](references/sources.md) |

## Explain a method

Identify its axis first: supervision source, prediction objective, architecture, optimizer, training stage, deployment setting, or evaluation protocol. Many methods occupy several axes; do not force them into exclusive branches.

Connect the visible input, target, loss, and learned artifact to a concrete example. Then explain what the objective encourages, what information it may discard, suitable uses, failure modes, and the nearest alternative. Add equations when they clarify the mechanism; define their symbols.

Distinguish a model's original training recipe from the broader family. BERT's 15% selection rate and MAE's 75% masking rate are recipe choices, not general laws. Distinguish selected prediction positions, corrupted values, and attention masks.

Avoid common category errors: self-supervised does not mean signal-free; masked reconstruction does not by itself specify a generative sampler; federated does not mean private; DPO does not require an online RL loop; in-context examples do not ordinarily update model weights.

## Recommend a method

Use available context to establish the output needed, data modality and independence unit, label or reward availability, pretrained assets, adaptation budget, and inference constraints. State assumptions when a missing constraint changes the recommendation.

Offer the smallest credible baseline and the alternative justified by the bottleneck. Explain why the training signal matches the downstream need, which assumption could fail, and which comparison would change the choice. Do not recommend pretraining from scratch merely because unlabeled data exists.

Compare total costs: obtaining data and labels, training, tuning, adaptation, and serving. Keep reconstruction quality, frozen-feature quality, fine-tuning quality, and sample quality separate. A result on one dataset or compute budget is not a universal ranking.

## Use the evidence

The chapters combine sourced mechanisms with explicitly identified practical synthesis. Follow citations for exact recipes or disputed claims. Refresh current model availability, benchmark rankings, and implementation requirements from primary papers or official documentation before recommending a specific current release.

Use the bundled material as a conceptual resource, not a claim that every ML algorithm is covered or that its representative models are the latest. Preserve limitations and identification assumptions when summarizing causal, privacy, uncertainty, and out-of-distribution results.
