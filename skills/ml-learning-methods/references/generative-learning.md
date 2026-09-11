# Generative learning

A generative model represents a distribution over data, possibly conditioned on a prompt, class, previous observation, or action. A usable generator also specifies how to draw samples. Different families make different compromises between density evaluation, training, latent structure, and sampling cost.

Generating examples and learning reusable features are related goals, but their evaluations differ. A model can produce convincing pictures while dropping rare modes. Another can estimate useful probabilities without producing the most visually appealing samples. This chapter compares mechanisms; its use-case recommendations are practical synthesis.

## Contents

- [Autoregressive modeling](#autoregressive-modeling)
- [Autoencoders and variational autoencoders](#autoencoders-and-variational-autoencoders)
- [Adversarial generation](#adversarial-generation)
- [Normalizing flows](#normalizing-flows)
- [Diffusion and score learning](#diffusion-and-score-learning)
- [Flow matching](#flow-matching)
- [Masked generation](#masked-generation)
- [Energy-based learning](#energy-based-learning)
- [Comparing the families](#comparing-the-families)

## Autoregressive modeling

The probability chain rule decomposes a sequence distribution:

$$
p_\theta(x_1,\ldots,x_T)=\prod_{t=1}^{T}p_\theta(x_t\mid x_{<t}).
$$

Training minimizes the sum of negative log probabilities of observed tokens. During teacher-forced training, the previous tokens come from the data. With an appropriate causal mask, a Transformer can compute losses for many positions in parallel. Conventional sampling then produces one token after another, conditioning each decision on generated history.[^38][^45]

**Useful when:** variable-length sequences, language, code, and tasks where exact conditional likelihood and prefix-based generation fit the application. **Strengths:** a straightforward normalized factorization; dense training targets; a clear sampling procedure. **Weaknesses:** sequential decoding dependencies; mistakes can change the future context; conditioning naturally favors a chosen order.

The token need not be a word. It can represent an image code, audio segment, action, or structured record. The architecture and tokenization decide which sequences are tractable. Parallel training and sequential sampling are not contradictory: training knows the previous tokens, while sampling must obtain them.

An infilling task can use an encoder–decoder model: the encoder sees available content on both sides, and the decoder generates the missing output sequentially. BART demonstrates that bidirectional input processing and autoregressive generation can coexist in one denoising model.[^5]

## Autoencoders and variational autoencoders

A basic autoencoder maps $x$ to a code $z$ and reconstructs $x$ from $z$. Compression, corruption, or other constraints keep the task from being trivial copying. But an arbitrary point sampled in that code space need not decode to realistic data: ordinary reconstruction does not automatically organize a usable sampling distribution.[^71]

A VAE adds a probabilistic latent model. Choose a prior $p(z)$, learn a decoder $p_\theta(x\mid z)$, and approximate posterior inference with $q_\phi(z\mid x)$. A standard evidence lower bound is

$$
\log p_\theta(x)\ge
\mathbb E_{q_\phi(z\mid x)}[\log p_\theta(x\mid z)]
-\operatorname{KL}(q_\phi(z\mid x)\|p(z)).
$$

The first term rewards explaining observations; the second controls how much the inferred latent distribution departs from the prior. The reparameterization trick permits low-variance gradient estimation in common continuous-latent cases. Generation samples $z$ from the prior, then decodes.[^25]

**Useful when:** latent-variable modeling, probabilistic compression, simulation, and learning a structured latent space. **Tradeoffs:** posterior approximation can be restrictive; a strong decoder may ignore the latent variable; a simple Gaussian observation model can average ambiguous outputs. Blurry images are associated with particular likelihoods and architectures, not a theorem about every VAE.

A masked autoencoder and a VAE both contain encoders and decoders, but those roles do not establish the same probabilistic model. Check for an explicit prior, posterior approximation, and probabilistic objective before calling a reconstruction model variational.

## Adversarial generation

A GAN trains a generator against a discriminator. In the original formulation,

$$
\min_G\max_D\;
\mathbb E_{x\sim p_{\mathrm{data}}}\log D(x)
+\mathbb E_{z\sim p(z)}\log(1-D(G(z))).
$$

$G$ maps noise to samples; $D$ learns to distinguish generated data from observed data. Common practical variants change these losses. The original non-saturating generator update, for example, differs from directly minimizing the displayed minimax generator term.[^26]

**Useful when:** the sample distribution matters more than explicit likelihood, and fast feed-forward generation is valuable. **Strengths:** the discriminator learns a comparison signal in data space; sampling can require a single generator pass. **Weaknesses:** two interacting learners complicate optimization; the generator may cover only part of the data distribution; visual fidelity can conceal missing diversity.

“Adversarial” also appears elsewhere. Domain-adversarial learning tries to remove domain-predictive information from a representation. Adversarial robustness trains against input perturbations. Neither implies that the final product is a GAN image generator.[^64]

## Normalizing flows

A normalizing flow transforms a simple random variable through an invertible mapping. If $x=f_\theta(z)$, the change-of-variables formula gives

$$
\log p_X(x)=\log p_Z(f_\theta^{-1}(x))
+\log\left|\det J_{f_\theta^{-1}}(x)\right|.
$$

The Jacobian term accounts for local expansion and contraction of volume. Real NVP uses structured invertible transformations to make density evaluation and sampling tractable. This differs from a plain autoencoder, whose encoder and decoder need not be inverses.[^30]

**Useful when:** density estimation, invertible transformations, or latent inference are central. **Tradeoffs:** tractable invertibility constrains architecture; transformations and Jacobians can be expensive; high density does not automatically imply semantic typicality or good anomaly detection.

Continuous normalizing flows describe transformations through an ordinary differential equation. Neural ODEs provide one construction, with numerical solvers and a divergence calculation replacing a sequence of discrete invertible layers. Numerical tolerances and solver cost become part of the method.[^66]

## Diffusion and score learning

A diffusion process gradually corrupts data. A common Gaussian formulation is

$$
x_t=\sqrt{\bar\alpha_t}\,x_0+\sqrt{1-\bar\alpha_t}\,\epsilon,
\qquad \epsilon\sim\mathcal N(0,I).
$$

Train a network to predict noise or an equivalent parameterization at sampled times:

$$
\mathcal L_{\epsilon}=\mathbb E_{x_0,t,\epsilon}
\|\epsilon-\epsilon_\theta(x_t,t)\|^2.
$$

The schedule $\bar\alpha_t$ controls signal and noise. Sampling starts from noise and follows a learned denoising process. The commonly used simple noise-prediction loss is related to a variational formulation, but its weighting should not be casually equated with exact maximum-likelihood training.[^27]

Score models learn $\nabla_x\log p_t(x)$, the gradient of the log density of corrupted data at time $t$. Score-based SDE theory connects forward noising, reverse stochastic dynamics, and a probability-flow ODE. The latter shows why a model trained through noisy examples can also admit deterministic sampling dynamics.[^28]

**Useful when:** high-quality conditional samples, image or audio synthesis, and inverse problems. **Tradeoffs:** repeated network evaluations can dominate serving cost; results depend on the scheduler and guidance; quality, diversity, and speed can move in different directions. Faster sampling techniques exist, so “diffusion always needs hundreds of steps” is not a durable definition.

A denoising objective alone is insufficient. A generative diffusion model specifies corruption across noise levels and a reverse procedure linked to a distribution. An autoencoder trained to remove one fixed noise level does not automatically supply that machinery.

## Flow matching

Flow matching trains a vector field that transports a simple distribution into the data distribution. A simple illustrative path pairs noise $x_0$ with data $x_1$:

$$
x_t=(1-t)x_0+t x_1,\quad u_t=x_1-x_0,
$$

$$
\mathcal L_{\mathrm{FM}}=\mathbb E\|v_\theta(x_t,t)-u_t\|^2.
$$

Here the endpoints are named differently from the diffusion section: $x_0$ is noise and $x_1$ is data. Conditional regression learns the marginal velocity field through averaging over sampled endpoint pairs. Generation numerically integrates $dx/dt=v_\theta(x,t)$.[^29]

The displayed straight path is one choice, not the definition of all flow matching. Couplings, probability paths, and time schedules can differ. The original framework also accommodates diffusion paths. Thus diffusion and flow matching overlap mathematically; “stochastic versus deterministic” is too crude a division because diffusion also has ODE formulations.[^29][^28]

**Useful when:** training a continuous transport generator through vector-field regression. **Tradeoffs:** numerical integration still costs compute; a simple training path does not guarantee accurate one-step sampling; transport geometry and model approximation affect the required solver effort. Discrete normalizing flows and flow matching share distribution transport, but use different parameterizations and training mechanics.

## Masked generation

MaskGIT predicts masked discrete image tokens, then iteratively revises which positions remain uncertain. It connects bidirectional token prediction to a sampling algorithm. Its iterative refinement is not the same as conventional one-token-at-a-time decoding.[^31]

Masked discrete diffusion turns tokens into a special masked state under a corruption schedule and learns the reverse process. MDLM derives a weighted MLM objective within this framework. LLaDA uses a diffusion formulation for language pretraining and supervised fine-tuning. These results establish viable alternatives to autoregressive language modeling in the studied settings, not universal speed or quality superiority.[^32][^33]

Parallel prediction at one refinement step does not mean generation finishes in one step. Length handling, the number of refinement steps, re-masking, confidence decisions, and caching affect practical latency. Compare actual end-to-end generation under a specified quality target.

## Energy-based learning

An energy-based model assigns a scalar compatibility score. In a normalized probabilistic formulation,

$$
p_\theta(x)=\frac{\exp(-E_\theta(x))}{Z_\theta},
\qquad Z_\theta=\int\exp(-E_\theta(x))\,dx.
$$

Low energy means relatively high probability. The partition function $Z_\theta$ may be hard to compute; both training and sampling can therefore require approximations. Noise-contrastive estimation learns an unnormalized model by distinguishing observed data from a specified noise distribution. Its “contrastive” terminology should not be confused with the complete SimCLR recipe.[^70]

Score learning offers a useful connection: the gradient with respect to input removes a partition function that is constant in that input. Learning a score can therefore avoid explicitly evaluating the normalization, although sampling and statistical estimation remain substantive problems.[^28]

Energy models are flexible for compatibility and structured prediction, but a useful scalar score is not by itself an efficient sampler. Some joint-embedding systems also use the language of energy to describe compatibility without claiming a normalized data-density model. State which meaning is intended.

## Comparing the families

| Family | Training target | Sampling | Principal attraction | Principal difficulty |
| --- | --- | --- | --- | --- |
| Autoregressive | Next element given previous elements | Sequential conditional draws | Explicit factorization and flexible sequences | Serial dependencies |
| VAE | Reconstruction likelihood plus posterior regularization | Prior latent, then decoder | Probabilistic latent representation | Approximate posterior and latent usage |
| GAN | Learned real/generated comparison | Usually feed-forward generation | Fast samples and learned perceptual comparison | Instability and mode coverage |
| Discrete normalizing flow | Exact transformed density | Invertible transform | Tractable likelihood and latent inversion | Architectural constraints |
| Diffusion/score | Denoising or score at noise levels | Reverse SDE or related solver | Flexible high-quality conditional generation | Iterative compute and solver choices |
| Flow matching | Velocity along probability paths | ODE integration | Direct vector-field regression | Integration accuracy versus cost |
| Masked token generator | Missing tokens under a masking scheme | Iterative fill/refinement | Bidirectional context and parallel updates | Schedule, consistency, length, latency |

Likelihood, sample fidelity, diversity, conditional accuracy, and representation quality are separate criteria. Choose the criterion the application consumes, then compare suitable models using the same data access and inference budget. See [choosing and evaluating](choosing-and-evaluating.md).

## Sources

[^38]: Ashish Vaswani; Noam Shazeer; Niki Parmar; et al. [Attention Is All You Need](https://arxiv.org/abs/1706.03762). 2017-06-12.

[^45]: Tom B. Brown; Benjamin Mann; Nick Ryder; et al. [Language Models are Few-Shot Learners](https://arxiv.org/abs/2005.14165). 2020-05-28.

[^5]: Mike Lewis; Yinhan Liu; Naman Goyal; et al. [BART: Denoising Sequence-to-Sequence Pre-training for Natural Language Generation, Translation, and Comprehension](https://arxiv.org/abs/1910.13461). 2019-10-29.

[^71]: Pascal Vincent; Hugo Larochelle; Isabelle Lajoie; et al. [Stacked Denoising Autoencoders: Learning Useful Representations in a Deep Network with a Local Denoising Criterion](https://www.jmlr.org/papers/v11/vincent10a.html). 2010.

[^25]: Diederik P Kingma; Max Welling. [Auto-Encoding Variational Bayes](https://arxiv.org/abs/1312.6114). 2013-12-20.

[^26]: Ian J. Goodfellow; Jean Pouget-Abadie; Mehdi Mirza; et al. [Generative Adversarial Networks](https://arxiv.org/abs/1406.2661). 2014-06-10.

[^64]: Yaroslav Ganin; Evgeniya Ustinova; Hana Ajakan; et al. [Domain-Adversarial Training of Neural Networks](https://arxiv.org/abs/1505.07818). 2015-05-28.

[^30]: Laurent Dinh; Jascha Sohl-Dickstein; Samy Bengio. [Density estimation using Real NVP](https://arxiv.org/abs/1605.08803). 2016-05-27.

[^66]: Ricky T. Q. Chen; Yulia Rubanova; Jesse Bettencourt; et al. [Neural Ordinary Differential Equations](https://arxiv.org/abs/1806.07366). 2018-06-19.

[^27]: Jonathan Ho; Ajay Jain; Pieter Abbeel. [Denoising Diffusion Probabilistic Models](https://arxiv.org/abs/2006.11239). 2020-06-19.

[^28]: Yang Song; Jascha Sohl-Dickstein; Diederik P. Kingma; et al. [Score-Based Generative Modeling through Stochastic Differential Equations](https://arxiv.org/abs/2011.13456). 2020-11-26.

[^29]: Yaron Lipman; Ricky T. Q. Chen; Heli Ben-Hamu; et al. [Flow Matching for Generative Modeling](https://arxiv.org/abs/2210.02747). 2022-10-06.

[^31]: Huiwen Chang; Han Zhang; Lu Jiang; et al. [MaskGIT: Masked Generative Image Transformer](https://arxiv.org/abs/2202.04200). 2022-02-08.

[^32]: Subham Sekhar Sahoo; Marianne Arriola; Yair Schiff; et al. [Simple and Effective Masked Diffusion Language Models](https://arxiv.org/abs/2406.07524). 2024-06-11.

[^33]: Shen Nie; Fengqi Zhu; Zebin You; et al. [Large Language Diffusion Models](https://arxiv.org/abs/2502.09992). 2025-02-14.

[^70]: Michael Gutmann; Aapo Hyvärinen. [Noise-contrastive estimation: A new estimation principle for unnormalized statistical models](https://proceedings.mlr.press/v9/gutmann10a.html). 2010.
