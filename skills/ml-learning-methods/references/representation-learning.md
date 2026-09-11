# Representation learning

A representation is a transformation $z=f_\theta(x)$ that makes useful properties of an input easier to access. A good representation for nearest-neighbor retrieval may organize distance well. A good representation for segmentation must preserve where things are. A useful control representation must retain what changes under actions. Those are different requirements.

Representation learning is an intended result, not a single supervision regime. A supervised classifier, a masked autoencoder, a contrastive learner, and a generative model can all produce reusable features. This chapter compares the self-supervised mechanisms most closely connected to masked prediction.

## Contents

- [Contrastive learning](#contrastive-learning)
- [Learning without explicit negatives](#learning-without-explicit-negatives)
- [Redundancy reduction and clustering](#redundancy-reduction-and-clustering)
- [Latent prediction and JEPA](#latent-prediction-and-jepa)
- [Multimodal and temporal signals](#multimodal-and-temporal-signals)
- [What a representation keeps](#what-a-representation-keeps)

## Contrastive learning

Construct a compatible pair of observations, such as two transformed views of one image. Increase their similarity relative to incompatible pairs. A representative loss for an anchor $i$ and its positive $j$ is

$$
\ell_{i,j}=-\log\frac{\exp(s(z_i,z_j)/\tau)}
{\sum_{k\ne i}\exp(s(z_i,z_k)/\tau)}.
$$

Here $s$ is a similarity such as normalized dot product, $\tau>0$ is temperature, and the denominator includes the positive and the competing examples in the candidate set. The task is classification over matches. Its meaning depends on how positives and negatives were constructed.[^24][^14]

**SimCLR** creates augmented image views, applies an encoder and nonlinear projection head, and uses other views in a batch as negatives. Its experiments show that augmentation composition, projection heads, batch size, and training duration materially affect results. **MoCo** instead maintains a queue of encoded examples and a slowly updated key encoder, providing many negatives without requiring all of them in one simultaneous batch.[^14][^15]

A projection head can let the loss enforce constraints in a space different from the representation exported for downstream use. When evaluating a published method, establish whether its reported features come before or after that head; comparing the wrong layer can change the question.

**Useful when:** semantic search, duplicate detection, image–text retrieval, matching identities across views, and transfer settings where the chosen invariances fit the task. **Weaknesses:** false negatives can push genuinely related examples apart; views can remove label-relevant information; sampling and hard-negative selection change what the model learns. A contrastive objective cannot repair a consistently wrong definition of “similar.”

For example, cropping two parts of a bird photograph may produce compatible views for bird recognition. Cropping the bird out of one view makes the match ambiguous. In a defect-detection task, a crop that removes the defect can teach the model to ignore exactly what matters. These are design consequences of the positive-pair definition.

## Learning without explicit negatives

If the loss merely minimizes $\|f(x_1)-f(x_2)\|^2$, outputting the same vector for every input makes it zero. This is **representation collapse**. A low objective value can therefore mean the learner has discarded all useful distinctions.

BYOL learns to predict a target network's representation of another view. It uses an online encoder with a predictor, a stop-gradient target branch, and an exponential-moving-average target update:

$$
\xi\leftarrow m\xi+(1-m)\theta.
$$

$\theta$ denotes online parameters, $\xi$ target parameters, and $m$ the averaging coefficient. BYOL demonstrates useful representations without explicit negative pairs. Its objective still admits collapsed solutions; the complete learning dynamics and architecture matter. “Add stop-gradient” is not a universal proof that any proposed system avoids collapse.[^16]

DINO trains a student to match a teacher's output distribution across image views. Its centering, sharpening, teacher update, and view construction are part of the recipe. “Self-distillation” describes the source of its targets; it does not mean a pretrained external expert supplies labels.[^17]

**Strengths:** these approaches avoid explicit negative sampling and can supply strong transferable features. **Weaknesses:** stability can depend on interacting architectural and statistical choices; teacher targets are moving; a successful global representation may still be poor at small spatial details. Their benefits must be tested under the actual feature-use protocol.

Ordinary knowledge distillation is related but distinct. A student approximates a teacher's predictions or features, often to compress a larger model or ensemble. Self-distillation constructs the teacher within the learning system. A teacher does not need to be larger in every distillation setup.[^59]

## Redundancy reduction and clustering

**VICReg** separates three pressures: match two views, maintain variation across examples in each embedding dimension, and reduce covariance between different dimensions. The variance term resists constant representations; the covariance term discourages duplicated coordinates. This gives a more explicit decomposition of collapse prevention than an agreement-only objective.[^18]

**Barlow Twins** pushes the cross-correlation matrix between embeddings of two views toward the identity: corresponding coordinates should agree, while different coordinates should not redundantly carry the same signal. It shares the broad idea of preserving information while enforcing view agreement, with a different loss construction.[^19]

**DeepCluster** alternates clustering current features and predicting those cluster assignments. The cluster assignments become pseudo-labels that improve the representation used for the next clustering round. This links conventional unsupervised clustering with neural representation learning.[^65]

| Mechanism | How it prevents the simplest collapse | What still needs attention |
| --- | --- | --- |
| Contrastive matching | Different examples compete | False negatives and sampling |
| Teacher–student methods | Asymmetry, target updates, normalization and distribution controls | Stability depends on the actual recipe |
| VICReg/Barlow Twins | Explicit variation or correlation constraints | Batch statistics, feature scale, suitable views |
| Clustering-based learning | Assignment structure discourages a single undifferentiated output when properly controlled | Empty/dominant clusters and self-reinforcing assignments |
| Raw reconstruction | Different inputs have different fixed targets | Copying shortcuts and irrelevant detail |

Non-collapsed features are only a prerequisite. An encoder that assigns every training example an arbitrary unique code avoids constant output but may generalize badly. Check transfer, not just feature variance.

## Latent prediction and JEPA

Masked prediction can target a representation of the hidden content rather than the content itself. In an illustrative formulation,

$$
\mathcal L=\mathbb E\left[
\left\|p_\theta(f_\theta(x_{\mathrm{context}}),u)
-\operatorname{sg}(f_\xi(x)_{\mathrm{target}})\right\|^2\right],
$$

where $u$ describes the target location, $p$ is a predictor, $\operatorname{sg}$ stops gradients through the target, and the teacher $f_\xi$ supplies contextual target features. This is a family-level sketch; exact losses and normalization differ among methods.

I-JEPA predicts target-region representations from an image context region. Its target and context sampling are consequential: target regions should carry meaningful content, and context should remain informative. Learning in latent space can reduce the need to predict every pixel, but it introduces a learned target whose quality and stability must be managed.[^11]

A **joint-embedding architecture** matches representations of compatible observations. A **joint-embedding predictive architecture** adds a predictor between a context representation and a target representation, often conditioned on location or time. The latter construction permits the model to represent predictable relationships without requiring the two observations themselves to be identical.

Predicting a compressed state can be useful when details are intrinsically uncertain. Imagine a scene after a person opens a door: the door's new position may matter, while the exact sensor noise does not. But if the target representation also discards the hinge location, the prediction may be useless for fine-grained control. Feature-space prediction does not guarantee causal understanding or planning ability.

V-JEPA 2 separates large-scale observational pretraining from subsequent training of an action-conditioned latent world model for planning. The action data and planner matter to the robotics result; it is inaccurate to attribute action-conditioned control to passive video alone. V-JEPA 2.1, a 2026 preprint, extends the representation recipe with dense prediction losses over visible and masked tokens and supervision at intermediate layers.[^12][^82]

DINOv2 and DINOv3 illustrate another branch: reusable visual features through large-scale self-supervised training, data curation, and teacher–student methods. DINOv3 introduces Gram anchoring to address deterioration of dense features during long training. These developments reinforce that training duration and global recognition scores alone do not characterize spatial feature quality.[^23][^13]

## Multimodal and temporal signals

**CLIP** learns which image and text belong together. Image and text encoders create vectors in a shared matching space; a contrastive objective compares paired examples with alternatives. Text descriptions can then define candidate categories for zero-shot classification. The paired captions supply semantic information, so “no manually curated category labels” should not be rewritten as “no semantic supervision.”[^20]

**Contrastive predictive coding** uses a context representation to identify future latent observations among alternatives. Predicting forward in time supplies structure different from making two simultaneous crops agree. Its usefulness depends on the horizon and what remains predictable.[^24]

**wav2vec 2.0** combines masking with contrastive selection of quantized speech latents. **HuBERT** predicts cluster-based speech targets. **data2vec** predicts contextual teacher features. These examples show that masking, contrastive learning, discrete target construction, and self-distillation are components that can be combined.[^21][^22][^10]

## What a representation keeps

Three questions make comparisons concrete:

1. **Invariance:** what changes should leave the representation unchanged? Lighting might be irrelevant for object identity but informative for estimating illumination.
2. **Equivariance:** what changes should alter it in a predictable way? Moving an object should usually move a spatial feature map rather than erase its location.
3. **Sufficiency:** does it retain the information needed for the downstream target? Compression is useful only if it discards the right distinctions.

Do not infer these properties from a method's name. Test the transformations and target tasks. Unsupervised disentanglement research provides a related warning: recovering uniquely meaningful latent factors requires assumptions or inductive biases; an unlabeled dataset does not identify the desired factorization by itself.[^61]

For frozen retrieval, compare embedding geometry directly. For segmentation, inspect dense predictions. For adaptation, measure performance across realistic label budgets. For a world model, test predictions and the decisions they support. The representation is good relative to those uses.

## Sources

[^24]: Aaron van den Oord; Yazhe Li; Oriol Vinyals. [Representation Learning with Contrastive Predictive Coding](https://arxiv.org/abs/1807.03748). 2018-07-10.

[^14]: Ting Chen; Simon Kornblith; Mohammad Norouzi; et al. [A Simple Framework for Contrastive Learning of Visual Representations](https://arxiv.org/abs/2002.05709). 2020-02-13.

[^15]: Kaiming He; Haoqi Fan; Yuxin Wu; et al. [Momentum Contrast for Unsupervised Visual Representation Learning](https://arxiv.org/abs/1911.05722). 2019-11-13.

[^16]: Jean-Bastien Grill; Florian Strub; Florent Altché; et al. [Bootstrap your own latent: A new approach to self-supervised Learning](https://arxiv.org/abs/2006.07733). 2020-06-13.

[^17]: Mathilde Caron; Hugo Touvron; Ishan Misra; et al. [Emerging Properties in Self-Supervised Vision Transformers](https://arxiv.org/abs/2104.14294). 2021-04-29.

[^59]: Geoffrey Hinton; Oriol Vinyals; Jeff Dean. [Distilling the Knowledge in a Neural Network](https://arxiv.org/abs/1503.02531). 2015-03-09.

[^18]: Adrien Bardes; Jean Ponce; Yann LeCun. [VICReg: Variance-Invariance-Covariance Regularization for Self-Supervised Learning](https://arxiv.org/abs/2105.04906). 2021-05-11.

[^19]: Jure Zbontar; Li Jing; Ishan Misra; et al. [Barlow Twins: Self-Supervised Learning via Redundancy Reduction](https://arxiv.org/abs/2103.03230). 2021-03-04.

[^65]: Mathilde Caron; Piotr Bojanowski; Armand Joulin; et al. [Deep Clustering for Unsupervised Learning of Visual Features](https://arxiv.org/abs/1807.05520). 2018-07-15.

[^11]: Mahmoud Assran; Quentin Duval; Ishan Misra; et al. [Self-Supervised Learning from Images with a Joint-Embedding Predictive Architecture](https://arxiv.org/abs/2301.08243). 2023-01-19.

[^12]: Mido Assran; Adrien Bardes; David Fan; et al. [V-JEPA 2: Self-Supervised Video Models Enable Understanding, Prediction and Planning](https://arxiv.org/abs/2506.09985). 2025-06-11.

[^82]: Lorenzo Mur-Labadia; Matthew Muckley; Amir Bar; et al. [V-JEPA 2.1: Unlocking Dense Features in Video Self-Supervised Learning](https://arxiv.org/abs/2603.14482). 2026-03-15.

[^23]: Maxime Oquab; Timothée Darcet; Théo Moutakanni; et al. [DINOv2: Learning Robust Visual Features without Supervision](https://arxiv.org/abs/2304.07193). 2023-04-14.

[^13]: Oriane Siméoni; Huy V. Vo; Maximilian Seitzer; et al. [DINOv3](https://arxiv.org/abs/2508.10104). 2025-08-13.

[^20]: Alec Radford; Jong Wook Kim; Chris Hallacy; et al. [Learning Transferable Visual Models From Natural Language Supervision](https://arxiv.org/abs/2103.00020). 2021-02-26.

[^21]: Alexei Baevski; Henry Zhou; Abdelrahman Mohamed; et al. [wav2vec 2.0: A Framework for Self-Supervised Learning of Speech Representations](https://arxiv.org/abs/2006.11477). 2020-06-20.

[^22]: Wei-Ning Hsu; Benjamin Bolte; Yao-Hung Hubert Tsai; et al. [HuBERT: Self-Supervised Speech Representation Learning by Masked Prediction of Hidden Units](https://arxiv.org/abs/2106.07447). 2021-06-14.

[^10]: Alexei Baevski; Wei-Ning Hsu; Qiantong Xu; et al. [data2vec: A General Framework for Self-supervised Learning in Speech, Vision and Language](https://arxiv.org/abs/2202.03555). 2022-02-07.

[^61]: Francesco Locatello; Stefan Bauer; Mario Lucic; et al. [Challenging Common Assumptions in the Unsupervised Learning of Disentangled Representations](https://arxiv.org/abs/1811.12359). 2018-11-29.
