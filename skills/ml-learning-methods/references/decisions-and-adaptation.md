# Decisions, feedback, and adaptation

Some learning problems ask which action to take. Others ask how to reuse existing knowledge when a new task, dataset, or environment arrives. These questions overlap, but they are different: reinforcement learning concerns consequences of actions; transfer and continual learning concern the reuse and updating of learned behavior.

## Contents

- [Bandits and reinforcement learning](#bandits-and-reinforcement-learning)
- [Model-free and model-based methods](#model-free-and-model-based-methods)
- [Online, off-policy, and offline](#online-off-policy-and-offline)
- [Imitation and preferences](#imitation-and-preferences)
- [Transfer and fine-tuning](#transfer-and-fine-tuning)
- [Multitask and meta-learning](#multitask-and-meta-learning)
- [In-context, few-shot, and zero-shot](#in-context-few-shot-and-zero-shot)
- [Continual and online learning](#continual-and-online-learning)

## Bandits and reinforcement learning

A contextual bandit observes context, chooses an action, and receives a reward for that action. It normally does not model action-dependent multi-step state transitions. A recommendation example is choosing one item to display and observing feedback; the original LinUCB paper develops contextual-bandit methods for news recommendation.[^95]

Supervised learning would observe correct target labels for sampled inputs. A bandit observes only the consequence of the action taken. It must balance **exploration**, which learns about uncertain alternatives, and **exploitation**, which selects what currently appears best. If an action changes future user behavior materially, a one-step bandit abstraction may omit part of the problem.

Reinforcement learning models the sequence. An agent observes state or observation $s_t$, chooses $a_t$, receives $r_t$, and encounters a new state. In a Markov decision process, state is sufficient for the transition and reward rules; with partial observations, memory or a belief state may be needed.[^75]

A value function summarizes expected future return. One optimal Bellman equation is

$$
Q^*(s,a)=\mathbb E\left[r+\gamma\max_{a'}Q^*(s',a')\mid s,a\right].
$$

It connects the value of acting now with the value of later actions. Learning from such targets is called bootstrapping: the learner's current estimate helps construct another learning target. The word has a different use from bootstrap resampling in statistics.[^75]

**Use RL when** actions affect what happens next and the objective is cumulative consequence. **Use a bandit when** the one-step abstraction captures the important decision. **Use supervised prediction when** the needed outcome is a prediction and intervention is outside the model's scope. These are practical modeling choices, not measures of algorithmic sophistication.

## Model-free and model-based methods

| Family | What it learns | Attraction | Main difficulty |
| --- | --- | --- | --- |
| Value-based | Values of states or state–action pairs | Reuses experience to compare actions | Bootstrapping error and action maximization |
| Policy gradient | Parameters of an action distribution | Directly optimizes behavior; handles continuous actions | Noisy gradient estimates and data demands |
| Actor–critic | Policy plus value estimator | Value estimates help reduce policy-gradient variance | Errors in critic and actor interact |
| Model-based | Transition/reward model plus policy or planner | Uses predictions to evaluate alternatives | Model errors compound and can be exploited |

These families overlap. A model-based system can use an actor–critic algorithm inside imagined trajectories. A value learner can use a model to generate additional data. “Model-free” means it does not explicitly use a learned or known transition model for that algorithmic role; it does not mean the agent has no neural model.[^75][^53]

PPO limits the incentive for large policy changes through a clipped surrogate objective, usually with an actor–critic implementation. It is an optimization recipe for policy improvement, not a new source of supervision. Its popularity does not make it a default solution for every reward-based problem.[^50]

Dreamer learns a world model and improves behavior using imagined experience. This can make observations more useful, but a planner or policy can favor trajectories that are attractive only because the model is wrong. Evaluate decisions in the real target environment or an adequate independent simulator, not solely in the model that proposed them.[^53]

## Online, off-policy, and offline

**On-policy** methods learn using data from the current policy or a suitably close policy. **Off-policy** methods can learn about one policy from data collected by another. **Offline RL** restricts learning to a fixed logged dataset without further environment interaction. Off-policy capability alone does not make an algorithm reliable in the offline setting.

The offline difficulty is coverage. A learned policy may choose actions scarcely represented in the logs, and a value function may assign them overly optimistic values. Conservative Q-learning addresses this by regularizing value estimates toward conservatism on unsupported actions. Its guarantees rely on the paper's assumptions; no offline method can manufacture arbitrary missing outcome evidence.[^52]

**Practical implication:** a historical dataset with only one action in each context may support prediction of that behavior, but not a reliable comparison of many alternative policies. Logged propensities, overlap, and an explicit evaluation design matter. The final system should be compared with a behavior-cloning baseline and the policy that generated the data where appropriate.

Exploration is also a cost. In a game it may consume simulator steps. In an operational system it may expose users to poor actions or consume physical resources. Better reward optimization is not sufficient if data collection is unaffordable or the reward omits the outcome that matters.

## Imitation and preferences

### Imitation learning

Behavior cloning treats demonstrations as supervised state–action examples. It is often a simple route to useful initial behavior. The limitation is distribution shift: a small early mistake can lead the learner into states that the demonstrator data barely covers.

DAgger addresses this by collecting expert actions at states encountered by the learner and aggregating those examples into training. It changes the data-collection loop, not merely the loss on the original demonstrations. Its applicability depends on expert access and the cost of learner rollouts.[^54]

Inverse reinforcement learning instead tries to infer a reward explaining demonstrations, after which a policy can be optimized under that reward. Reward identification is underdetermined without further assumptions: many rewards can explain the same behavior. If the immediate goal is simply to imitate a well-covered behavior, reward inference may add unnecessary complexity.[^102]

### RLHF and preference optimization

Preference data compares alternatives, such as two responses to one prompt. A representative RLHF pipeline first fits a model to demonstrations, then learns a reward model from comparisons, then optimizes a policy against that reward while constraining departure from a reference policy. This is one influential recipe; not every aligned model uses every stage.[^51]

DPO uses pairwise preferences to fit the policy directly under a model relating preference probabilities to relative rewards. For preferred response $y_w$, rejected response $y_l$, prompt $x$, policy $\pi_\theta$, and fixed reference $\pi_{\mathrm{ref}}$, a representative loss is

$$
\mathcal L_{\mathrm{DPO}}=-\mathbb E\log\sigma\left[
\beta\left(
\log\frac{\pi_\theta(y_w\mid x)}{\pi_{\mathrm{ref}}(y_w\mid x)}
-\log\frac{\pi_\theta(y_l\mid x)}{\pi_{\mathrm{ref}}(y_l\mid x)}
\right)\right].
$$

$\sigma$ is the logistic function and $\beta$ controls the reference-relative scaling. Standard DPO uses a fixed preference dataset and does not require an explicit learned reward model or an online RL rollout loop during optimization. Its connection to KL-regularized reward maximization depends on the formulation's assumptions.[^49]

Preference learning inherits the judgment process. An evaluator may favor length, confidence, formatting, or familiar claims over correctness. Pairwise training does not establish calibrated probabilities or truthful answers. Evaluate the capabilities and undesirable shortcuts that matter, not just agreement with a reused preference judge.

### Verifiable rewards and synthetic feedback

When outcomes can be checked, training can use rewards from executable or exact criteria, such as whether a proposed solution passes a specified check. DeepSeek-R1 illustrates reinforcement learning with verifiable tasks and later use of generated data to train other models. Its published pipeline distinguishes an RL exploration setting from a broader multi-stage training recipe.[^68]

A verifier can still be incomplete or exploitable. Passing a weak check is evidence only for what it checks. AI-generated preference labels are another supervision source, with cost advantages and inherited model biases; they do not eliminate the need to understand the evaluator.

## Transfer and fine-tuning

Transfer learning reuses information learned elsewhere. Supervised pretraining can transfer; self-supervised pretraining can transfer; pretraining need not be language modeling. The central question is whether source-task features or parameters are useful for the target.

| Adaptation approach | Updated at target-task training | Why choose it | Main limit |
| --- | --- | --- | --- |
| Frozen features plus head | A small predictor | Cheap, stable, easy baseline | Cannot repair missing information in the features |
| Partial fine-tuning | A subset of layers plus head | Adds adaptation with less training state | Layer choice affects transfer |
| Full fine-tuning | Most or all parameters | Maximum parameter flexibility | More memory, overfitting and forgetting risks |
| Adapters/LoRA | Added or restricted parameter updates | Reduces trainable parameters and optimizer memory | Restricted update family; base model still needed |
| Distillation | Student parameters | Reduces serving cost or transfers teacher behavior | Inherits teacher errors and data coverage |
| Continued pretraining | Base parameters or selected updates on new raw data | Learns domain patterns before task adaptation | Can spend compute without improving the target task |

T5 studies transfer choices in a common framework. LoRA freezes pretrained weights and learns low-rank updates, typically written

$$
W'=W+BA,\qquad \operatorname{rank}(BA)\le r.
$$

It restricts the update's parameterization; it does not define the training objective. LoRA can accompany supervised fine-tuning or other differentiable objectives. Reducing trainable parameters reduces some training state, but does not remove the base model or all activation memory.[^4][^42]

Distillation changes the learned artifact by training a student to reproduce teacher information. It is distinct from parameter-efficient adaptation of the teacher itself.[^59]

**Negative transfer** occurs when reuse hurts the target relative to an appropriate alternative. It can come from mismatched domains, incompatible label meanings, or lost task-relevant detail. A frozen-feature baseline, partial adaptation, and training a smaller model can reveal which constraint is binding.

**Domain adaptation** uses information from a target domain to improve transfer. Domain-adversarial training encourages representations that predict the source task while obscuring the domain. This requires care: if domains differ in task-relevant ways, indiscriminate alignment can remove useful information or match incompatible classes.[^64]

**Domain generalization** trains for unseen domains without using their data during training. Group distributionally robust optimization emphasizes poor-performing predefined training groups, but improvement still depends on generalization and regularization. Training-domain invariance does not guarantee performance under arbitrary new shifts.[^63]

## Multitask and meta-learning

Multitask learning trains related tasks together, often by sharing features or parameters. Sharing can improve statistical efficiency when tasks need similar information. It can also create gradient conflict, let data-rich tasks dominate, or blur incompatible label definitions. The weights among task losses express priorities rather than neutral bookkeeping.

Meta-learning learns across tasks with the explicit aim of adapting to a new task. MAML learns initial parameters that perform well after a small number of updates on new-task data. A schematic objective is

$$
\min_\theta\;\mathbb E_{\mathcal T}
\mathcal L_{\mathcal T}^{\mathrm{query}}
\left(\theta-\alpha\nabla_\theta
\mathcal L_{\mathcal T}^{\mathrm{support}}(\theta)\right).
$$

The support set supplies adaptation examples; the query set evaluates the adapted parameters. This is an illustrative single inner step. The training distribution of tasks must resemble the adaptation demands expected later.[^43]

Prototypical networks instead learn an embedding in which each class can be represented by the mean of a few support examples. Classification compares a query to those prototypes. This is a metric-based route to few-shot learning rather than MAML's learned initialization.[^44]

Meta-learning can have substantial upstream cost. A small adaptation set does not imply that the entire system learned cheaply. Compare it with ordinary transfer using the same upstream data and task access.

## In-context, few-shot, and zero-shot

In-context learning supplies examples as input to a pretrained model. In the usual setup, a forward pass changes activations and predictions but not persistent weights. Few-shot gradient fine-tuning updates weights; few-shot prompting supplies context. Report which protocol produced a result.[^45]

Zero-shot evaluation uses no task-specific labeled training examples under the stated protocol. CLIP can match an image to text descriptions of candidate classes; that is zero-shot transfer built on extensive paired image–text training. Zero-shot does not mean untrained or free of human semantic input.[^20]

Retrieval-augmented generation supplies retrieved information at inference. It is a system design that can use learned retrievers and generators, not by itself a parameter-update rule. Test-time search similarly spends inference compute. Test-time training, in contrast, actually updates parameters using a chosen test-time signal. These mechanisms must be separated when discussing “the model learning during use.”

## Continual and online learning

Online supervised learning updates a model as labeled examples arrive. Incremental SGD is one implementation; it can update a linear or neural predictor without repeatedly refitting the entire history. A streaming update rule alone does not solve changing distributions.[^97]

Continual learning emphasizes sequential experience and retention. Catastrophic forgetting occurs when new training damages previously useful behavior. Approaches include replaying past examples, regularizing changes to important parameters, distilling old predictions, and allocating separate capacity.

Elastic weight consolidation uses an approximate importance-weighted penalty to resist changing parameters important to prior tasks. It offers one stability–adaptation tradeoff, with approximation and capacity limits. Replay and architectural separation solve different parts of the same problem; none grants unlimited retention in fixed resources.[^46]

Measure both new-task acquisition and old-task retention, plus memory and retraining costs. Sometimes forgetting is desirable because an old relationship no longer holds. The objective is to retain useful knowledge while adapting to the present task, not to preserve every historical prediction.

## Sources

[^95]: Lihong Li; Wei Chu; John Langford; et al. [A Contextual-Bandit Approach to Personalized News Article Recommendation](https://arxiv.org/abs/1003.0146). 2010-02-28.

[^75]: Richard S. Sutton; Andrew G. Barto. [Reinforcement Learning: An Introduction, second edition](http://incompleteideas.net/book/the-book-2nd.html). 2018.

[^53]: Danijar Hafner; Jurgis Pasukonis; Jimmy Ba; et al. [Mastering Diverse Domains through World Models](https://arxiv.org/abs/2301.04104). 2023-01-10.

[^50]: John Schulman; Filip Wolski; Prafulla Dhariwal; et al. [Proximal Policy Optimization Algorithms](https://arxiv.org/abs/1707.06347). 2017-07-20.

[^52]: Aviral Kumar; Aurick Zhou; George Tucker; et al. [Conservative Q-Learning for Offline Reinforcement Learning](https://arxiv.org/abs/2006.04779). 2020-06-08.

[^54]: Stephane Ross; Geoffrey J. Gordon; J. Andrew Bagnell. [A Reduction of Imitation Learning and Structured Prediction to No-Regret Online Learning](https://arxiv.org/abs/1011.0686). 2010-11-02.

[^102]: Andrew Y. Ng; Stuart Russell. [Algorithms for Inverse Reinforcement Learning](https://ai.stanford.edu/~ang/papers/icml00-irl.pdf). 2000.

[^51]: Long Ouyang; Jeff Wu; Xu Jiang; et al. [Training language models to follow instructions with human feedback](https://arxiv.org/abs/2203.02155). 2022-03-04.

[^49]: Rafael Rafailov; Archit Sharma; Eric Mitchell; et al. [Direct Preference Optimization: Your Language Model is Secretly a Reward Model](https://arxiv.org/abs/2305.18290). 2023-05-29.

[^68]: DeepSeek-AI; Daya Guo; Dejian Yang; et al. [DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning](https://arxiv.org/abs/2501.12948). 2025-01-22.

[^4]: Colin Raffel; Noam Shazeer; Adam Roberts; et al. [Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer](https://arxiv.org/abs/1910.10683). 2019-10-23.

[^42]: Edward J. Hu; Yelong Shen; Phillip Wallis; et al. [LoRA: Low-Rank Adaptation of Large Language Models](https://arxiv.org/abs/2106.09685). 2021-06-17.

[^59]: Geoffrey Hinton; Oriol Vinyals; Jeff Dean. [Distilling the Knowledge in a Neural Network](https://arxiv.org/abs/1503.02531). 2015-03-09.

[^64]: Yaroslav Ganin; Evgeniya Ustinova; Hana Ajakan; et al. [Domain-Adversarial Training of Neural Networks](https://arxiv.org/abs/1505.07818). 2015-05-28.

[^63]: Shiori Sagawa; Pang Wei Koh; Tatsunori B. Hashimoto; et al. [Distributionally Robust Neural Networks for Group Shifts: On the Importance of Regularization for Worst-Case Generalization](https://arxiv.org/abs/1911.08731). 2019-11-20.

[^43]: Chelsea Finn; Pieter Abbeel; Sergey Levine. [Model-Agnostic Meta-Learning for Fast Adaptation of Deep Networks](https://arxiv.org/abs/1703.03400). 2017-03-09.

[^44]: Jake Snell; Kevin Swersky; Richard S. Zemel. [Prototypical Networks for Few-shot Learning](https://arxiv.org/abs/1703.05175). 2017-03-15.

[^45]: Tom B. Brown; Benjamin Mann; Nick Ryder; et al. [Language Models are Few-Shot Learners](https://arxiv.org/abs/2005.14165). 2020-05-28.

[^20]: Alec Radford; Jong Wook Kim; Chris Hallacy; et al. [Learning Transferable Visual Models From Natural Language Supervision](https://arxiv.org/abs/2103.00020). 2021-02-26.

[^97]: scikit-learn contributors. [1.5. Stochastic Gradient Descent](https://scikit-learn.org/stable/modules/sgd.html). Living documentation; accessed 2026-09-11.

[^46]: James Kirkpatrick; Razvan Pascanu; Neil Rabinowitz; et al. [Overcoming catastrophic forgetting in neural networks](https://arxiv.org/abs/1612.00796). 2016-12-02.
