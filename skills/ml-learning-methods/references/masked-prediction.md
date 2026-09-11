# Masked prediction: from cloze tasks to BERT and MAE

A cloze task removes content and asks a learner to recover it. “She put the letter in the ___ and added a stamp” supplies a target without a separate annotator: start with a complete sentence, hide “envelope,” and learn to recover it. The example is simple; across varied data, successful prediction can require grammar, category knowledge, spatial structure, or temporal relationships.

BERT and masked autoencoders share that construction. The important design choices are **what is hidden, what remains visible, what must be predicted, and which part of the model will be reused**.[^1][^2]

## Contents

- [The general objective](#the-general-objective)
- [Original BERT](#original-bert)
- [Original MAE](#original-mae)
- [Why the masking ratios differ](#why-the-masking-ratios-differ)
- [A target is a choice about information](#a-target-is-a-choice-about-information)
- [The family of masked methods](#the-family-of-masked-methods)
- [Strengths and failure modes](#strengths-and-failure-modes)
- [When masking becomes generation](#when-masking-becomes-generation)

## The general objective

Let $x=(x_1,\ldots,x_n)$ be a sequence of tokens or patches. Sample a set $M$ of prediction positions and construct corrupted input $\tilde x=c_M(x)$. A general masked loss is

$$
\mathcal L_{\mathrm{mask}}=
\mathbb E_{x,M}\left[\frac{1}{|M|}\sum_{i\in M}
\ell\big(h_\theta(\tilde x)_i,t_i(x)\big)\right].
$$

$h_\theta$ produces predictions, and $t_i(x)$ supplies the target at position $i$. Cross-entropy is appropriate for a categorical target; squared or absolute error can compare continuous values. Random masking, contiguous spans, and spatial blocks change the available context. The older denoising-autoencoder idea supplies the broader principle: reconstruct clean information from a corrupted observation.[^71]

Three distinct “masks” matter:

| Mask | What it changes | Example |
| --- | --- | --- |
| Input corruption | Which values the model observes | Replace a token or omit a patch |
| Attention mask | Which positions can exchange information | Prevent attending to future tokens |
| Loss mask | Which output positions count in the objective | Score only selected target positions |

A causal language model can use an attention mask without replacing any input token with a special mask symbol. A denoising model can use bidirectional attention over an input containing corrupted values. Keep these mechanisms separate when reading code or comparing objectives.[^38][^5]

## Original BERT

BERT uses a bidirectional Transformer encoder. Its original masked-language-model recipe selects 15% of token positions for prediction. Among selected positions, 80% become `[MASK]`, 10% become a random token, and 10% remain unchanged. Cross-entropy predicts the original token at selected positions. Original BERT also trained a next-sentence-prediction objective.[^1]

```text
Original:  she mailed the letter yesterday
Input:     she mailed the [MASK] yesterday
Target:                  letter
```

In the unmodified subset of selected positions, a prediction target is still present even though the token was not visibly corrupted. Therefore “15% selected” does not mean “15% replaced by `[MASK]`.” The expected special-mask fraction is $0.15\times0.80=0.12$, or 12% of eligible positions. This is arithmetic from the recipe, not another hyperparameter.

A contextual token representation answers a different need from a single vector whose distances reliably express sentence similarity. Pooling a general encoder can provide a baseline; retrieval quality may benefit from a contrastive objective tailored to sentence or document pairs. Architecture alone does not establish that geometry.[^24][^20]

RoBERTa showed that the surrounding training recipe matters: it removed next-sentence prediction, changed masking and data/training choices, and improved language-understanding results. Thus next-sentence prediction is part of original BERT's history, not a requirement of masked language modeling.[^3]

## Original MAE

MAE divides an image into patches, hides a large random subset, and encodes only visible patches. A smaller decoder receives encoded visible patches together with mask tokens and positional information. It predicts pixel values at missing patches; squared reconstruction error is computed on masked patches. The decoder is used for pretraining and the encoder is reused for downstream tasks.[^2]

```text
Image patches:      A B C D E F G H
Visible to encoder: A . . D . . . .
Decoder task:       predict B C E F G H
```

For a toy image with 196 patches and a 75% masking rate, the encoder sees 49 patches. Full self-attention has a pairwise interaction term proportional to the square of sequence length, so that term falls to $(49/196)^2=1/16$. This calculation concerns only that term. Patch embedding, feed-forward layers, decoding, memory transfers, and fixed overhead prevent interpreting it as a sixteenfold end-to-end speedup.

The bottleneck encourages the encoder to retain information that helps explain unseen content. It does not specify that the retained information must align with our labels. SimMIM independently demonstrates that direct pixel regression with a simple head can learn useful image representations; a complex visual tokenizer is not universally necessary.[^8]

## Why the masking ratios differ

The original BERT recipe uses 15% selected positions, whereas MAE uses a representative 75% image-patch masking rate. VideoMAE reports useful results with 90–95% masking and a video-specific tube-masking strategy.[^1][^2][^9]

A useful interpretation is **conditional predictability**. An image's nearby pixels often contain substantial redundant information. Light masking may leave an easy interpolation task. Video adds temporal redundancy: adjacent frames can reveal what was hidden spatially. Language can lose useful context rapidly when several content-bearing tokens disappear.

This is an intuition about those settings, not a proof that images always need more masking. Patch size, tokenization, target type, model capacity, domain, and the loss all change the problem. T5's study also varied corruption rate and span length rather than treating BERT's choices as universal.[^4]

Consider three masking strategies on a surveillance clip. Independent pixels can often be recovered from nearby pixels. Independent patches can sometimes be recovered from an adjacent frame. A spatial tube hidden across frames removes that shortcut but may also remove the only evidence of a small moving object. “Harder” is useful only while enough relevant information remains.

A practical masking experiment compares downstream usefulness at similar compute, not just reconstruction error. A high masking rate might save encoder compute while requiring more training steps, or improve fine-tuning while weakening frozen-feature performance. The intended adaptation protocol determines which result matters.

## A target is a choice about information

| Target | What the learner must preserve | Advantage | Main tradeoff |
| --- | --- | --- | --- |
| Original token identity | Distinctions made by a discrete vocabulary | Clear classification target | Tokenization controls granularity |
| Raw pixels or samples | Detailed local signal | No learned target model required | May devote capacity to unpredictable or irrelevant detail |
| Discrete learned code | Distinctions retained by a tokenizer or clustering stage | Can abstract away some raw detail | Inherits the target generator's errors and information loss |
| Contextual teacher features | Information encoded by another model and its context | Can focus prediction on reusable features | Moving targets and collapse prevention complicate learning |
| A span or whole sequence | Dependencies within missing content | Supports structured conditional generation | Decoder cost and sequence modeling matter |

BEiT predicts visual-token identities produced by an image tokenizer. MAE and SimMIM instead show effective direct pixel targets. data2vec predicts contextual teacher representations across language, speech, and vision. I-JEPA predicts representations of target image regions from a context region.[^7][^8][^10][^11]

A target is an information filter. Suppose we want to recognize a bird species. Predicting pixels might preserve plumage texture, lighting, branch texture, and sensor noise. Predicting a teacher embedding might remove some of that variation, but it might also erase the small color distinction separating two species. “More abstract” is not automatically “more useful.” The downstream task decides which distinctions must survive.

With squared error, the unconstrained best point prediction for a random target $Y$ given context $C=c$ is its conditional mean:

$$
\arg\min_a\mathbb E[(Y-a)^2\mid C=c]=\mathbb E[Y\mid C=c].
$$

One can derive this by differentiating the conditional risk: $2(a-\mathbb E[Y\mid C=c])=0$. If two very different completions are plausible, their mean may look unlike either one. This explains why low reconstruction error need not imply realistic sampling. It also explains why a distributional predictor and a point regressor solve different problems.

## The family of masked methods

| Method | What is predicted | Distinguishing choice | Useful comparison |
| --- | --- | --- | --- |
| BERT | Original identities at selected text positions | Bidirectional contextual encoder | Causal next-token modeling |
| RoBERTa | Masked text tokens | Revised BERT training recipe | Objective versus recipe improvements |
| T5 | Missing spans, generated as a sequence | A sentinel marks each removed span; decoder emits removed spans | Per-position MLM versus sequence denoising |
| BART | Original text after corruption | Bidirectional encoder and autoregressive decoder | Conditional generation from corrupted input |
| ELECTRA | Whether each observed token matches the original | A small generator supplies replacements; discriminator gets dense supervision | Detection versus reconstruction |
| BEiT | Discrete visual-token identities | Learned visual tokenizer constructs targets | Code prediction versus raw pixels |
| MAE | Missing image-patch pixels | Encoder skips missing patches | Asymmetric versus full-input encoding |
| SimMIM | Masked pixels | Simple regression head and masking design | Which architectural machinery is necessary? |
| VideoMAE | Hidden video content | Temporal structure changes masking | Spatial and temporal shortcuts |
| HuBERT | Offline cluster assignments at masked speech positions | Pseudo-discrete speech units | Learned units versus raw waveform |
| wav2vec 2.0 | Correct quantized latent among distractors | Masked context plus a contrastive loss | Masking and contrastive learning can combine |
| data2vec | Contextual teacher features | Similar target construction across modalities | Raw targets versus learned targets |
| I-JEPA | Target-region features | Predict in representation space | Latent prediction versus pixel reconstruction |

The rows describe representative recipes, not interchangeable implementations.[^3][^4][^5][^6][^7][^8][^9][^22][^21][^10][^11]

ELECTRA's discriminator terminology invites a mistaken GAN analogy. Its usual generator is trained through masked-token likelihood rather than adversarially to fool the discriminator. A sampled replacement equal to the original token counts as original for the discriminator's target. The benefit is a different and denser prediction problem, not merely a different name for MLM.[^6]

## Strengths and failure modes

**Why masking can work.** Complete data provides many artificial input–target pairs. The task can use context from either side. A prediction head used only during training can absorb detail that is unnecessary at deployment. Missing-data structure can also match real applications such as imputation or inpainting.

**Why it can fail.** An easy corruption leaves local shortcuts. Excessive corruption removes the evidence needed for useful prediction. A target can emphasize noise, background texture, or domain-specific artifacts. A learned teacher can omit needed information. Dataset duplicates and neighboring observations can make evaluation misleading.

**Missingness is part of the distribution.** Randomly hiding entries in a complete training table does not simulate every real missing-data process. A sensor may fail exactly under extreme conditions, or a field may be absent because the unobserved value is unusual. Test the missingness patterns expected in use; a random-mask benchmark alone does not establish reliable imputation.

**Reconstruction and representation are distinct products.** Evaluate reconstruction if restoration is the goal. Evaluate retrieval if nearest-neighbor search is the goal. Evaluate a frozen head if the encoder must stay frozen. Evaluate fine-tuning if adaptation is allowed. MAE's published comparisons make clear that rankings can change with the adaptation protocol.[^2]

## When masking becomes generation

Ordinary masked pretraining learns conditionals under a corruption scheme. It does not automatically supply a consistent joint distribution and an effective procedure for sampling complete examples. Multiplying simultaneous masked-token predictions is not generally the same thing as autoregressive factorization.

MaskGIT builds a generative procedure around iterative prediction and refinement of masked image tokens. Masked diffusion methods add a specified forward corruption process and a learned reverse process. MDLM derives a weighted mixture of masked-language-model losses in a probabilistic generative framework; LLaDA demonstrates a large language model trained with a related masking-and-reversal construction.[^31][^32][^33]

The bridge is therefore concrete: **corruption supplies training examples; the probabilistic formulation and reverse procedure supply generation**. Read [generative learning](generative-learning.md) for the differences between that procedure, autoregression, diffusion with continuous noise, and flow matching.

## Sources

[^1]: Jacob Devlin; Ming-Wei Chang; Kenton Lee; et al. [BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding](https://arxiv.org/abs/1810.04805). 2018-10-11.

[^2]: Kaiming He; Xinlei Chen; Saining Xie; et al. [Masked Autoencoders Are Scalable Vision Learners](https://arxiv.org/abs/2111.06377). 2021-11-11.

[^71]: Pascal Vincent; Hugo Larochelle; Isabelle Lajoie; et al. [Stacked Denoising Autoencoders: Learning Useful Representations in a Deep Network with a Local Denoising Criterion](https://www.jmlr.org/papers/v11/vincent10a.html). 2010.

[^38]: Ashish Vaswani; Noam Shazeer; Niki Parmar; et al. [Attention Is All You Need](https://arxiv.org/abs/1706.03762). 2017-06-12.

[^5]: Mike Lewis; Yinhan Liu; Naman Goyal; et al. [BART: Denoising Sequence-to-Sequence Pre-training for Natural Language Generation, Translation, and Comprehension](https://arxiv.org/abs/1910.13461). 2019-10-29.

[^24]: Aaron van den Oord; Yazhe Li; Oriol Vinyals. [Representation Learning with Contrastive Predictive Coding](https://arxiv.org/abs/1807.03748). 2018-07-10.

[^20]: Alec Radford; Jong Wook Kim; Chris Hallacy; et al. [Learning Transferable Visual Models From Natural Language Supervision](https://arxiv.org/abs/2103.00020). 2021-02-26.

[^3]: Yinhan Liu; Myle Ott; Naman Goyal; et al. [RoBERTa: A Robustly Optimized BERT Pretraining Approach](https://arxiv.org/abs/1907.11692). 2019-07-26.

[^8]: Zhenda Xie; Zheng Zhang; Yue Cao; et al. [SimMIM: A Simple Framework for Masked Image Modeling](https://arxiv.org/abs/2111.09886). 2021-11-18.

[^9]: Zhan Tong; Yibing Song; Jue Wang; et al. [VideoMAE: Masked Autoencoders are Data-Efficient Learners for Self-Supervised Video Pre-Training](https://arxiv.org/abs/2203.12602). 2022-03-23.

[^4]: Colin Raffel; Noam Shazeer; Adam Roberts; et al. [Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer](https://arxiv.org/abs/1910.10683). 2019-10-23.

[^7]: Hangbo Bao; Li Dong; Songhao Piao; et al. [BEiT: BERT Pre-Training of Image Transformers](https://arxiv.org/abs/2106.08254). 2021-06-15.

[^10]: Alexei Baevski; Wei-Ning Hsu; Qiantong Xu; et al. [data2vec: A General Framework for Self-supervised Learning in Speech, Vision and Language](https://arxiv.org/abs/2202.03555). 2022-02-07.

[^11]: Mahmoud Assran; Quentin Duval; Ishan Misra; et al. [Self-Supervised Learning from Images with a Joint-Embedding Predictive Architecture](https://arxiv.org/abs/2301.08243). 2023-01-19.

[^6]: Kevin Clark; Minh-Thang Luong; Quoc V. Le; et al. [ELECTRA: Pre-training Text Encoders as Discriminators Rather Than Generators](https://arxiv.org/abs/2003.10555). 2020-03-23.

[^22]: Wei-Ning Hsu; Benjamin Bolte; Yao-Hung Hubert Tsai; et al. [HuBERT: Self-Supervised Speech Representation Learning by Masked Prediction of Hidden Units](https://arxiv.org/abs/2106.07447). 2021-06-14.

[^21]: Alexei Baevski; Henry Zhou; Abdelrahman Mohamed; et al. [wav2vec 2.0: A Framework for Self-Supervised Learning of Speech Representations](https://arxiv.org/abs/2006.11477). 2020-06-20.

[^31]: Huiwen Chang; Han Zhang; Lu Jiang; et al. [MaskGIT: Masked Generative Image Transformer](https://arxiv.org/abs/2202.04200). 2022-02-08.

[^32]: Subham Sekhar Sahoo; Marianne Arriola; Yair Schiff; et al. [Simple and Effective Masked Diffusion Language Models](https://arxiv.org/abs/2406.07524). 2024-06-11.

[^33]: Shen Nie; Fengqi Zhu; Zebin You; et al. [Large Language Diffusion Models](https://arxiv.org/abs/2502.09992). 2025-02-14.
