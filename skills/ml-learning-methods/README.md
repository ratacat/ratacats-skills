# ML learning methods

A research guide to how machines learn: what supplies the signal, what is predicted, what the model retains, and when each approach is useful. It starts from cloze tasks and connects BERT's masked language modeling to masked autoencoders, contrastive learning, latent prediction, generative models, and the wider ML landscape.

The skill helps an agent explain a technique, compare alternatives, or choose a training approach. The reference chapters are also written to read directly: intuition first, then equations, examples, strengths, weaknesses, and links to original work.

## Read the resource

| Chapter | What it answers |
| --- | --- |
| [1. Map of learning](references/map.md) | Which terms describe supervision, objectives, architectures, or training settings? How do they combine? |
| [2. Masked prediction](references/masked-prediction.md) | How do BERT and MAE work? Why different mask ratios? What changes when predicting pixels, tokens, or features? |
| [3. Representation learning](references/representation-learning.md) | How do contrastive methods, self-distillation, redundancy reduction, and JEPA learn useful features? |
| [4. Generative learning](references/generative-learning.md) | How do autoregressive models, VAEs, GANs, normalizing flows, diffusion, and flow matching differ? |
| [5. Supervision and classical methods](references/supervision-and-classical.md) | How do labeled, partly labeled, weakly labeled, and unlabeled data change the choice? Where do trees, kernels, and clustering fit? |
| [6. Decisions and adaptation](references/decisions-and-adaptation.md) | When do rewards, imitation, preference learning, transfer, meta-learning, and continual learning help? |
| [7. Structured and distributed learning](references/structured-and-distributed.md) | What do Bayesian, causal, scientific, graph, federated, and distributed approaches add? |
| [8. Choosing and evaluating](references/choosing-and-evaluating.md) | What should I try for a real problem, and what would show that it works? |
| [Sources](references/sources.md) | Where are the original papers, official references, and evidence limits? |

For the BERT/MAE connection, read **2 → 3 → 4**. For the whole landscape, read **1 → 5 → 2 → 3 → 4 → 6 → 7 → 8**. For a project decision, start at **8** and follow the relevant chapters.

This is a map of major families with representative algorithms, not an enumeration of every ML technique. It includes classical statistical learning and selected developments through September 2026. Methods are compared by their assumptions and use cases; historical benchmark winners are not presented as current defaults.

## Good fits

- “Explain masked language modeling, MAE, and JEPA using the same example.”
- “We have many unlabeled images and a few hundred labels. Compare plausible approaches.”
- “Is diffusion another kind of denoising autoencoder?”
- “Show how supervised learning, Transformers, LoRA, and DPO fit into one training pipeline.”
- “Help me choose between trees, pretrained embeddings, and training a neural model.”

## Install

From this local checkout, point a compatible agent at [SKILL.md](SKILL.md).

Install through either supported route:

```text
/plugin marketplace add ratacat/ratacats-skills
/plugin install ml-learning-methods@ratacats-skills
```

```sh
npx skills add ratacat/ratacats-skills --skill ml-learning-methods
```

The bundled resource needs no API keys, scripts, or model runtime. Fresh comparisons need web access to primary sources. This skill does not train or deploy models by itself.
