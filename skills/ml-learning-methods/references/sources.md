# Sources

The numbered references support the method descriptions throughout the resource. Each chapter includes the references it uses; this page collects them in one place. Dates on arXiv entries are initial-submission dates unless otherwise stated. A later conference or journal publication may have a different year, and an unversioned arXiv link may serve a revised manuscript.

## Evidence and scope

The resource covers major learning regimes, objective families, and representative algorithms. It gives extra depth to masked prediction and its relationships with representation learning and generation. It does not enumerate every optimizer, architecture, domain-specific estimator, or biologically motivated learning rule.

Mechanisms and historical recipes are attributed to original papers and official technical references. Textbooks and author-written tutorials supply definitions spanning several algorithms. Application examples, comparison matrices, and recommendations are practical synthesis; they are not claims of universal comparative superiority.

Historical performance statements apply to the source's data, model, training recipe, and evaluation protocol. The older tabular-tree results and the newer TabPFN results concern different methods and bounded benchmark settings. BERT's masking recipe, MAE's reconstruction design, and later latent-prediction recipes are described separately rather than treated as one implementation.

The recent examples include DINOv3, V-JEPA 2, masked diffusion language modeling, LLaDA, and the 2026 V-JEPA 2.1 preprint. These examples illustrate changes in the design space through September 11, 2026; they do not establish a latest-model leaderboard. Abstract-level claims of state-of-the-art performance are not adopted as current recommendations.

## Starting papers

- **Denoising autoencoders → BERT → MAE:** how corruption creates supervision and how target modality changes the problem.
- **SimCLR → BYOL → VICReg:** contrasting negative pairs, teacher dynamics, and explicit anti-collapse constraints.
- **data2vec → I-JEPA → V-JEPA 2:** prediction of learned targets and the additional role of actions in planning.
- **VAE → DDPM/score models → flow matching → MDLM:** probabilistic reconstruction, multi-level corruption, transport, and masked generation.
- **FixMatch/Snorkel → DAgger/RLHF/DPO:** what changes when targets come from pseudo-labels, heuristics, demonstrations, or preferences.
- **Tabular benchmarks → TabPFN:** why practical method recommendations must be revisited when the comparison set changes.

## Bibliography

1. Jacob Devlin; Ming-Wei Chang; Kenton Lee; et al. [BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding](https://arxiv.org/abs/1810.04805). 2018-10-11.

2. Kaiming He; Xinlei Chen; Saining Xie; et al. [Masked Autoencoders Are Scalable Vision Learners](https://arxiv.org/abs/2111.06377). 2021-11-11.

3. Yinhan Liu; Myle Ott; Naman Goyal; et al. [RoBERTa: A Robustly Optimized BERT Pretraining Approach](https://arxiv.org/abs/1907.11692). 2019-07-26.

4. Colin Raffel; Noam Shazeer; Adam Roberts; et al. [Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer](https://arxiv.org/abs/1910.10683). 2019-10-23.

5. Mike Lewis; Yinhan Liu; Naman Goyal; et al. [BART: Denoising Sequence-to-Sequence Pre-training for Natural Language Generation, Translation, and Comprehension](https://arxiv.org/abs/1910.13461). 2019-10-29.

6. Kevin Clark; Minh-Thang Luong; Quoc V. Le; et al. [ELECTRA: Pre-training Text Encoders as Discriminators Rather Than Generators](https://arxiv.org/abs/2003.10555). 2020-03-23.

7. Hangbo Bao; Li Dong; Songhao Piao; et al. [BEiT: BERT Pre-Training of Image Transformers](https://arxiv.org/abs/2106.08254). 2021-06-15.

8. Zhenda Xie; Zheng Zhang; Yue Cao; et al. [SimMIM: A Simple Framework for Masked Image Modeling](https://arxiv.org/abs/2111.09886). 2021-11-18.

9. Zhan Tong; Yibing Song; Jue Wang; et al. [VideoMAE: Masked Autoencoders are Data-Efficient Learners for Self-Supervised Video Pre-Training](https://arxiv.org/abs/2203.12602). 2022-03-23.

10. Alexei Baevski; Wei-Ning Hsu; Qiantong Xu; et al. [data2vec: A General Framework for Self-supervised Learning in Speech, Vision and Language](https://arxiv.org/abs/2202.03555). 2022-02-07.

11. Mahmoud Assran; Quentin Duval; Ishan Misra; et al. [Self-Supervised Learning from Images with a Joint-Embedding Predictive Architecture](https://arxiv.org/abs/2301.08243). 2023-01-19.

12. Mido Assran; Adrien Bardes; David Fan; et al. [V-JEPA 2: Self-Supervised Video Models Enable Understanding, Prediction and Planning](https://arxiv.org/abs/2506.09985). 2025-06-11.

13. Oriane Siméoni; Huy V. Vo; Maximilian Seitzer; et al. [DINOv3](https://arxiv.org/abs/2508.10104). 2025-08-13.

14. Ting Chen; Simon Kornblith; Mohammad Norouzi; et al. [A Simple Framework for Contrastive Learning of Visual Representations](https://arxiv.org/abs/2002.05709). 2020-02-13.

15. Kaiming He; Haoqi Fan; Yuxin Wu; et al. [Momentum Contrast for Unsupervised Visual Representation Learning](https://arxiv.org/abs/1911.05722). 2019-11-13.

16. Jean-Bastien Grill; Florian Strub; Florent Altché; et al. [Bootstrap your own latent: A new approach to self-supervised Learning](https://arxiv.org/abs/2006.07733). 2020-06-13.

17. Mathilde Caron; Hugo Touvron; Ishan Misra; et al. [Emerging Properties in Self-Supervised Vision Transformers](https://arxiv.org/abs/2104.14294). 2021-04-29.

18. Adrien Bardes; Jean Ponce; Yann LeCun. [VICReg: Variance-Invariance-Covariance Regularization for Self-Supervised Learning](https://arxiv.org/abs/2105.04906). 2021-05-11.

19. Jure Zbontar; Li Jing; Ishan Misra; et al. [Barlow Twins: Self-Supervised Learning via Redundancy Reduction](https://arxiv.org/abs/2103.03230). 2021-03-04.

20. Alec Radford; Jong Wook Kim; Chris Hallacy; et al. [Learning Transferable Visual Models From Natural Language Supervision](https://arxiv.org/abs/2103.00020). 2021-02-26.

21. Alexei Baevski; Henry Zhou; Abdelrahman Mohamed; et al. [wav2vec 2.0: A Framework for Self-Supervised Learning of Speech Representations](https://arxiv.org/abs/2006.11477). 2020-06-20.

22. Wei-Ning Hsu; Benjamin Bolte; Yao-Hung Hubert Tsai; et al. [HuBERT: Self-Supervised Speech Representation Learning by Masked Prediction of Hidden Units](https://arxiv.org/abs/2106.07447). 2021-06-14.

23. Maxime Oquab; Timothée Darcet; Théo Moutakanni; et al. [DINOv2: Learning Robust Visual Features without Supervision](https://arxiv.org/abs/2304.07193). 2023-04-14.

24. Aaron van den Oord; Yazhe Li; Oriol Vinyals. [Representation Learning with Contrastive Predictive Coding](https://arxiv.org/abs/1807.03748). 2018-07-10.

25. Diederik P Kingma; Max Welling. [Auto-Encoding Variational Bayes](https://arxiv.org/abs/1312.6114). 2013-12-20.

26. Ian J. Goodfellow; Jean Pouget-Abadie; Mehdi Mirza; et al. [Generative Adversarial Networks](https://arxiv.org/abs/1406.2661). 2014-06-10.

27. Jonathan Ho; Ajay Jain; Pieter Abbeel. [Denoising Diffusion Probabilistic Models](https://arxiv.org/abs/2006.11239). 2020-06-19.

28. Yang Song; Jascha Sohl-Dickstein; Diederik P. Kingma; et al. [Score-Based Generative Modeling through Stochastic Differential Equations](https://arxiv.org/abs/2011.13456). 2020-11-26.

29. Yaron Lipman; Ricky T. Q. Chen; Heli Ben-Hamu; et al. [Flow Matching for Generative Modeling](https://arxiv.org/abs/2210.02747). 2022-10-06.

30. Laurent Dinh; Jascha Sohl-Dickstein; Samy Bengio. [Density estimation using Real NVP](https://arxiv.org/abs/1605.08803). 2016-05-27.

31. Huiwen Chang; Han Zhang; Lu Jiang; et al. [MaskGIT: Masked Generative Image Transformer](https://arxiv.org/abs/2202.04200). 2022-02-08.

32. Subham Sekhar Sahoo; Marianne Arriola; Yair Schiff; et al. [Simple and Effective Masked Diffusion Language Models](https://arxiv.org/abs/2406.07524). 2024-06-11.

33. Shen Nie; Fengqi Zhu; Zebin You; et al. [Large Language Diffusion Models](https://arxiv.org/abs/2502.09992). 2025-02-14.

34. Kihyuk Sohn; David Berthelot; Chun-Liang Li; et al. [FixMatch: Simplifying Semi-Supervised Learning with Consistency and Confidence](https://arxiv.org/abs/2001.07685). 2020-01-21.

35. Alexander Ratner; Stephen H. Bach; Henry Ehrenberg; et al. [Snorkel: Rapid Training Data Creation with Weak Supervision](https://arxiv.org/abs/1711.10160). 2017-11-28.

36. Tianqi Chen; Carlos Guestrin. [XGBoost: A Scalable Tree Boosting System](https://arxiv.org/abs/1603.02754). 2016-03-09.

37. Léo Grinsztajn; Edouard Oyallon; Gaël Varoquaux. [Why do tree-based models still outperform deep learning on tabular data?](https://arxiv.org/abs/2207.08815). 2022-07-18.

38. Ashish Vaswani; Noam Shazeer; Niki Parmar; et al. [Attention Is All You Need](https://arxiv.org/abs/1706.03762). 2017-06-12.

39. Kaiming He; Xiangyu Zhang; Shaoqing Ren; et al. [Deep Residual Learning for Image Recognition](https://arxiv.org/abs/1512.03385). 2015-12-10.

40. Alexey Dosovitskiy; Lucas Beyer; Alexander Kolesnikov; et al. [An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale](https://arxiv.org/abs/2010.11929). 2020-10-22.

41. William L. Hamilton; Rex Ying; Jure Leskovec. [Inductive Representation Learning on Large Graphs](https://arxiv.org/abs/1706.02216). 2017-06-07.

42. Edward J. Hu; Yelong Shen; Phillip Wallis; et al. [LoRA: Low-Rank Adaptation of Large Language Models](https://arxiv.org/abs/2106.09685). 2021-06-17.

43. Chelsea Finn; Pieter Abbeel; Sergey Levine. [Model-Agnostic Meta-Learning for Fast Adaptation of Deep Networks](https://arxiv.org/abs/1703.03400). 2017-03-09.

44. Jake Snell; Kevin Swersky; Richard S. Zemel. [Prototypical Networks for Few-shot Learning](https://arxiv.org/abs/1703.05175). 2017-03-15.

45. Tom B. Brown; Benjamin Mann; Nick Ryder; et al. [Language Models are Few-Shot Learners](https://arxiv.org/abs/2005.14165). 2020-05-28.

46. James Kirkpatrick; Razvan Pascanu; Neil Rabinowitz; et al. [Overcoming catastrophic forgetting in neural networks](https://arxiv.org/abs/1612.00796). 2016-12-02.

47. H. Brendan McMahan; Eider Moore; Daniel Ramage; et al. [Communication-Efficient Learning of Deep Networks from Decentralized Data](https://arxiv.org/abs/1602.05629). 2016-02-17.

48. Martín Abadi; Andy Chu; Ian Goodfellow; et al. [Deep Learning with Differential Privacy](https://arxiv.org/abs/1607.00133). 2016-07-01.

49. Rafael Rafailov; Archit Sharma; Eric Mitchell; et al. [Direct Preference Optimization: Your Language Model is Secretly a Reward Model](https://arxiv.org/abs/2305.18290). 2023-05-29.

50. John Schulman; Filip Wolski; Prafulla Dhariwal; et al. [Proximal Policy Optimization Algorithms](https://arxiv.org/abs/1707.06347). 2017-07-20.

51. Long Ouyang; Jeff Wu; Xu Jiang; et al. [Training language models to follow instructions with human feedback](https://arxiv.org/abs/2203.02155). 2022-03-04.

52. Aviral Kumar; Aurick Zhou; George Tucker; et al. [Conservative Q-Learning for Offline Reinforcement Learning](https://arxiv.org/abs/2006.04779). 2020-06-08.

53. Danijar Hafner; Jurgis Pasukonis; Jimmy Ba; et al. [Mastering Diverse Domains through World Models](https://arxiv.org/abs/2301.04104). 2023-01-10.

54. Stephane Ross; Geoffrey J. Gordon; J. Andrew Bagnell. [A Reduction of Imitation Learning and Structured Prediction to No-Regret Online Learning](https://arxiv.org/abs/1011.0686). 2010-11-02.

55. Jonas Peters; Peter Bühlmann; Nicolai Meinshausen. [Causal inference using invariant prediction: identification and confidence intervals](https://arxiv.org/abs/1501.01332). 2015-01-06.

56. Maziar Raissi; Paris Perdikaris; George Em Karniadakis. [Physics Informed Deep Learning (Part I): Data-driven Solutions of Nonlinear Partial Differential Equations](https://arxiv.org/abs/1711.10561). 2017-11-28.

57. Zongyi Li; Nikola Kovachki; Kamyar Azizzadenesheli; et al. [Fourier Neural Operator for Parametric Partial Differential Equations](https://arxiv.org/abs/2010.08895). 2020-10-18.

58. Diederik P. Kingma; Jimmy Ba. [Adam: A Method for Stochastic Optimization](https://arxiv.org/abs/1412.6980). 2014-12-22.

59. Geoffrey Hinton; Oriol Vinyals; Jeff Dean. [Distilling the Knowledge in a Neural Network](https://arxiv.org/abs/1503.02531). 2015-03-09.

60. Robert Geirhos; Jörn-Henrik Jacobsen; Claudio Michaelis; et al. [Shortcut Learning in Deep Neural Networks](https://arxiv.org/abs/2004.07780). 2020-04-16.

61. Francesco Locatello; Stefan Bauer; Mario Lucic; et al. [Challenging Common Assumptions in the Unsupervised Learning of Disentangled Representations](https://arxiv.org/abs/1811.12359). 2018-11-29.

62. Anastasios N. Angelopoulos; Stephen Bates. [A Gentle Introduction to Conformal Prediction and Distribution-Free Uncertainty Quantification](https://arxiv.org/abs/2107.07511). 2021-07-15.

63. Shiori Sagawa; Pang Wei Koh; Tatsunori B. Hashimoto; et al. [Distributionally Robust Neural Networks for Group Shifts: On the Importance of Regularization for Worst-Case Generalization](https://arxiv.org/abs/1911.08731). 2019-11-20.

64. Yaroslav Ganin; Evgeniya Ustinova; Hana Ajakan; et al. [Domain-Adversarial Training of Neural Networks](https://arxiv.org/abs/1505.07818). 2015-05-28.

65. Mathilde Caron; Piotr Bojanowski; Armand Joulin; et al. [Deep Clustering for Unsupervised Learning of Visual Features](https://arxiv.org/abs/1807.05520). 2018-07-15.

66. Ricky T. Q. Chen; Yulia Rubanova; Jesse Bettencourt; et al. [Neural Ordinary Differential Equations](https://arxiv.org/abs/1806.07366). 2018-06-19.

67. Steven L. Brunton; Joshua L. Proctor; J. Nathan Kutz. [Discovering governing equations from data: Sparse identification of nonlinear dynamical systems](https://arxiv.org/abs/1509.03580). 2015-09-11.

68. DeepSeek-AI; Daya Guo; Dejian Yang; et al. [DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning](https://arxiv.org/abs/2501.12948). 2025-01-22.

69. Ryuichi Kiryo; Gang Niu; Marthinus C. du Plessis; et al. [Positive-Unlabeled Learning with Non-Negative Risk Estimator](https://arxiv.org/abs/1703.00593). 2017-03-02.

70. Michael Gutmann; Aapo Hyvärinen. [Noise-contrastive estimation: A new estimation principle for unnormalized statistical models](https://proceedings.mlr.press/v9/gutmann10a.html). 2010.

71. Pascal Vincent; Hugo Larochelle; Isabelle Lajoie; et al. [Stacked Denoising Autoencoders: Learning Useful Representations in a Deep Network with a Local Denoising Criterion](https://www.jmlr.org/papers/v11/vincent10a.html). 2010.

72. Laurens van der Maaten; Geoffrey Hinton. [Visualizing Data using t-SNE](https://www.jmlr.org/papers/v9/vandermaaten08a.html). 2008.

73. Carl Edward Rasmussen; Christopher K. I. Williams. [Gaussian Processes for Machine Learning](https://gaussianprocess.org/gpml/). 2006.

74. Burr Settles. [Active Learning Literature Survey](https://burrsettles.com/pub/settles.activelearning.pdf). 2009; revised 2010.

75. Richard S. Sutton; Andrew G. Barto. [Reinforcement Learning: An Introduction, second edition](http://incompleteideas.net/book/the-book-2nd.html). 2018.

76. scikit-learn contributors. [1. Supervised learning](https://scikit-learn.org/stable/supervised_learning.html). Living documentation; accessed 2026-09-11.

77. scikit-learn contributors. [2. Unsupervised learning](https://scikit-learn.org/stable/unsupervised_learning.html). Living documentation; accessed 2026-09-11.

78. Noah Hollmann; Samuel Müller; Lennart Purucker; et al. [Accurate predictions on small data with a tabular foundation model](https://www.nature.com/articles/s41586-024-08328-6). 2025-01-08.

79. Keith Bonawitz; Vladimir Ivanov; Ben Kreuter; et al. [Practical Secure Aggregation for Privacy-Preserving Machine Learning](https://research.google/pubs/practical-secure-aggregation-for-privacy-preserving-machine-learning/). 2017.

80. scikit-learn contributors. [3.1. Cross-validation: evaluating estimator performance](https://scikit-learn.org/stable/modules/cross_validation.html). Living documentation; accessed 2026-09-11.

81. Ulrike von Luxburg. [A Tutorial on Spectral Clustering](https://arxiv.org/abs/0711.0189). 2007-11-01.

82. Lorenzo Mur-Labadia; Matthew Muckley; Amir Bar; et al. [V-JEPA 2.1: Unlocking Dense Features in Video Self-Supervised Learning](https://arxiv.org/abs/2603.14482). 2026-03-15.

83. Miguel A. Hernán; James M. Robins. [Causal Inference: What If](https://miguelhernan.org/whatifbook). 2020; current online edition accessed 2026-09-11.

84. scikit-learn contributors. [1.1. Linear Models](https://scikit-learn.org/stable/modules/linear_model.html). Living documentation; accessed 2026-09-11.

85. scikit-learn contributors. [1.11. Ensembles: Gradient boosting, random forests, bagging, voting, stacking](https://scikit-learn.org/stable/modules/ensemble.html). Living documentation; accessed 2026-09-11.

86. scikit-learn contributors. [1.4. Support Vector Machines](https://scikit-learn.org/stable/modules/svm.html). Living documentation; accessed 2026-09-11.

87. scikit-learn contributors. [1.6. Nearest Neighbors](https://scikit-learn.org/stable/modules/neighbors.html). Living documentation; accessed 2026-09-11.

88. scikit-learn contributors. [2.3. Clustering](https://scikit-learn.org/stable/modules/clustering.html). Living documentation; accessed 2026-09-11.

89. scikit-learn contributors. [2.5. Decomposing signals in components (matrix factorization problems)](https://scikit-learn.org/stable/modules/decomposition.html). Living documentation; accessed 2026-09-11.

90. scikit-learn contributors. [2.1. Gaussian mixture models](https://scikit-learn.org/stable/modules/mixture.html). Living documentation; accessed 2026-09-11.

91. scikit-learn contributors. [2.7. Novelty and Outlier Detection](https://scikit-learn.org/stable/modules/outlier_detection.html). Living documentation; accessed 2026-09-11.

92. scikit-learn contributors. [1.9. Naive Bayes](https://scikit-learn.org/stable/modules/naive_bayes.html). Living documentation; accessed 2026-09-11.

93. Jasper Snoek; Hugo Larochelle; Ryan P. Adams. [Practical Bayesian Optimization of Machine Learning Algorithms](https://arxiv.org/abs/1206.2944). 2012-06-13.

94. Tim Salimans; Jonathan Ho; Xi Chen; et al. [Evolution Strategies as a Scalable Alternative to Reinforcement Learning](https://arxiv.org/abs/1703.03864). 2017-03-10.

95. Lihong Li; Wei Chu; John Langford; et al. [A Contextual-Bandit Approach to Personalized News Article Recommendation](https://arxiv.org/abs/1003.0146). 2010-02-28.

96. Leland McInnes; John Healy; James Melville. [UMAP: Uniform Manifold Approximation and Projection for Dimension Reduction](https://arxiv.org/abs/1802.03426). 2018-02-09.

97. scikit-learn contributors. [1.5. Stochastic Gradient Descent](https://scikit-learn.org/stable/modules/sgd.html). Living documentation; accessed 2026-09-11.

98. David E. Rumelhart; Geoffrey E. Hinton; Ronald J. Williams. [Learning representations by back-propagating errors](https://doi.org/10.1038/323533a0). 1986-10-09.

99. Pierre Baldi; Kurt Hornik. [Neural Networks and Principal Component Analysis: Learning from Examples Without Local Minima](https://www.igb.uci.edu/~pfbaldi/publications/journals/1989/NN_and_PCA.pdf). 1989.

100. Thomas G. Dietterich; Richard H. Lathrop; Tomás Lozano-Pérez. [Solving the multiple instance problem with axis-parallel rectangles](https://lis.csail.mit.edu/pubs/tlp/multiple-instance-aij.pdf). 1997.

101. XGBoost contributors. [Learning to Rank](https://xgboost.readthedocs.io/en/stable/tutorials/learning_to_rank.html). Living documentation; accessed 2026-09-11.

102. Andrew Y. Ng; Stuart Russell. [Algorithms for Inverse Reinforcement Learning](https://ai.stanford.edu/~ang/papers/icml00-irl.pdf). 2000.
