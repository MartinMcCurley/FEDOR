# **Developing FEDOR: A Deep Monte Carlo CFR Poker AI for 6-Max No-Limit Hold'em**

## **1\. Introduction**

The development of superhuman artificial intelligence for complex imperfect information games, such as No-Limit Texas Hold'em (NLH) poker, has been a significant benchmark for AI research. Pluribus, a notable achievement in this domain, demonstrated superhuman performance in 6-player NLH.1 This report outlines a strategic approach to develop 'FEDOR', a next-generation poker AI based on Deep Monte Carlo Counterfactual Regret Minimization (Deep MCCFR), specifically tailored for 6-player NLH. The project aims to enhance existing open-source frameworks, notably the pluribus-poker-AI repository, by integrating advanced Deep MCCFR techniques, detailing practical implementation for GPU acceleration on an NVIDIA 4070ti, and providing actionable research and development steps.

The core challenge in 6-max NLH lies in its vast state space and the imperfect information, where players have private cards and must infer opponents' holdings and strategies from observable actions. Counterfactual Regret Minimization (CFR) and its variants have been the leading algorithms for tackling such games.2 Deep learning extensions, such as Deep CFR, obviate the need for manual abstraction by using neural networks to approximate regret values across the enormous game tree.2 FEDOR will leverage these principles, focusing on Monte Carlo sampling versions of CFR (MCCFR) due to their scalability.

This document details the foundational open-source resources, the algorithmic core of Deep MCCFR for 6-max NLH, neural network architecture design, practical GPU-accelerated training methodologies, and a phased development roadmap. The objective is to provide a comprehensive guide for building a state-of-the-art 6-player NLH AI.

## **2\. Foundational Open-Source Resources for FEDOR**

The development of FEDOR will strategically build upon existing open-source poker AI projects and libraries. This approach accelerates development by leveraging established codebases for game engines, AI algorithms, and evaluation frameworks.

### **2.1. Primary Repository: pluribus-poker-AI (tanker-fund/develop fork)**

The pluribus-poker-AI repository, particularly the develop branch of the tanker-fund fork 4, serves as the primary foundation for FEDOR. This Python-based repository 6 is a community effort to implement key ideas from the original Pluribus paper. Its existing structure for game logic, AI algorithms, and utility functions provides a solid starting point. The roadmap outlined in the original fedden/pluribus-poker-AI repository 6 includes implementing MCCFR and extending to No-Limit Texas Hold'em, aligning well with FEDOR's objectives.

The choice of the tanker-fund/develop branch is predicated on its recent activity (commits on Oct 22, 2023 4), suggesting it is the most up-to-date and actively maintained Python-based Pluribus implementation available. This recency is crucial for incorporating contemporary bug fixes and community enhancements. While the original Pluribus was implemented in C++ 1, a Python foundation offers faster prototyping and easier integration with popular deep learning libraries like PyTorch.

The following table outlines key components within the tanker-fund/pluribus-poker-AI (develop branch) and their proposed adaptation for FEDOR, based on the structure described for the fedden/pluribus-poker-AI 6 from which it was forked.

**Table 1: pluribus-poker-AI (tanker-fund/develop) Components for FEDOR Adaptation**

| Module/Directory | Original Purpose | Proposed Use/Modification for FEDOR | Key Files (Anticipated) |
| :---- | :---- | :---- | :---- |
| pluribus/games | Implementations of poker games as node-based objects (e.g., Kuhn Poker). | Extend/Refine for full 6-max NLH rules, including complex betting rounds, all-in scenarios, and side-pot logic. Ensure accurate game state and information set generation for six players. | poker\_game.py (or similar) |
| pluribus/ai | Stub functions for AI algorithms, potentially including basic CFR. | Implement Deep MCCFR algorithms, specifically SD-CFR style. House the neural network models (advantage/value networks) and their training logic. Manage memory buffers for regret/advantage samples. | cfr.py, deep\_mccfr\_agent.py |
| pluribus/poker | General code for managing a hand of poker (cards, hand evaluation, etc.). | Enhance hand evaluation for efficiency. Ensure robust handling of 6-player game flow, including player actions, pot management, and showdowns. | card.py, hand\_evaluator.py |
| pluribus/utils | Utility code like seed setting, general helper functions. | Expand with utilities for data serialization, logging, GPU management, and potentially performance profiling. | utils.py, logging\_utils.py |
| research/ | Directory for research/development scripts. | Utilize for experimental scripts, hyperparameter tuning, and evaluation result analysis. | Various experimental scripts |
| scripts/ | Scripts to help develop the main library. | Adapt or create new scripts for launching training runs, managing distributed workers (if future-scaled), and running evaluations. | train\_fedor.py, eval\_fedor.py |
| test/ | Python tests (functional and unit). | Significantly expand test coverage for 6-max NLH game logic, Deep MCCFR components, and neural network interactions. Implement tests for GPU-specific functionalities. | New test files for NLH 6-max |

This structured adaptation allows for a systematic development process, leveraging the existing Python framework while integrating the more advanced Deep MCCFR capabilities required for FEDOR. The initial focus on a Python implementation facilitates rapid iteration, which is crucial for research-oriented projects.

### **2.2. C++ for Performance Bottlenecks**

While Python offers development speed, computationally intensive parts of a poker AI, such as game tree traversals in MCCFR or extensive hand evaluations, can become performance bottlenecks. The original Pluribus was implemented in C++ 1, highlighting the performance benefits of systems-level languages. The pluribus-poker-AI repository roadmap also notes the intention to "write in a systems level language like C++ and optimise for performance" once a working prototype exists.6

For FEDOR, a hybrid approach is recommended:

1. **Initial Development in Python:** Leverage Python and PyTorch for the entire system, including the game engine and Deep MCCFR logic. This allows for faster iteration and easier integration with PyTorch's GPU capabilities.  
2. **Profiling:** Once a working prototype is established and training on the NVIDIA 4070ti begins, use profiling tools (e.g., PyTorch Profiler, cProfile) to identify critical performance bottlenecks.  
3. **Selective C++ Porting:** Rewrite identified bottlenecks (e.g., core game state updates, high-frequency utility calculations within MCCFR traversals) in C++. These C++ modules can then be exposed to Python using bindings like Pybind11. This strategy balances development agility with execution speed, ensuring that the most computationally demanding parts benefit from C++ performance while maintaining a Python-centric high-level architecture. This mirrors the approach seen in frameworks like OpenSpiel, which has a C++ core with Python bindings.7

This pragmatic approach addresses the inherent trade-off between development speed and runtime performance. Early Python development accelerates the implementation of complex AI logic and neural network integration, while the option for later C++ optimization ensures that FEDOR can achieve the necessary performance for large-scale training and potentially real-time decision-making.

## **3\. Deep MCCFR for 6-Max No-Limit Hold'em: Algorithmic Core**

The heart of FEDOR will be a Deep Monte Carlo Counterfactual Regret Minimization (Deep MCCFR) algorithm. This section details the principles of MCCFR, the transition to its deep learning counterpart, and a comparative analysis to select the most suitable variant for 6-max NLH.

### **3.1. Core Principles of Monte Carlo CFR (MCCFR)**

Counterfactual Regret Minimization (CFR) is an iterative algorithm that converges to a Nash equilibrium in two-player zero-sum games by minimizing regret at each information set.2 For games as large as 6-max NLH, traversing the entire game tree at each iteration, as done in vanilla CFR, is computationally infeasible. Monte Carlo CFR (MCCFR) addresses this by sampling actions and chance outcomes, updating regrets only along the sampled paths.9 This makes MCCFR suitable for extremely large games.

Key aspects of MCCFR include:

* **Sampling:** Instead of full tree traversals, MCCFR samples paths through the game tree. The specific way sampling is performed defines different MCCFR variants.  
* **Regret Updates:** Regrets are updated for actions within information sets encountered along the sampled paths. The average strategy over iterations converges to an approximate Nash equilibrium.

Several sampling strategies exist within the MCCFR family 9:

* **External Sampling:** In this scheme, actions for the "traverser" (the player whose regrets are being updated in the current traversal) are explored exhaustively at decision points they reach, while chance events and opponents' actions are sampled according to their respective probabilities or current strategies. Pluribus reportedly used a form of external sampling.10 Theoretical analysis suggests that external sampling can achieve an order reduction in the cost per iteration with only a constant-factor increase in iterations needed for convergence, leading to an asymptotic improvement in equilibrium computation time.9  
* **Outcome Sampling:** This method samples a single path (a single outcome) through the game tree for all players, including the traverser. An advantage is that it does not require full knowledge of opponents' strategies beyond samples of play, making it potentially suitable for online regret minimization.9  
* **Chance Sampling:** This variant focuses on sampling chance outcomes (e.g., card deals) on each iteration.9

For FEDOR, **External Sampling MCCFR** is recommended as the primary approach. Its proven effectiveness in complex poker AI like Pluribus and its favorable theoretical properties regarding computational cost make it a strong candidate for efficiently exploring the vast game tree of 6-max NLH.

### **3.2. Transitioning from Tabular MCCFR to Deep MCCFR**

While MCCFR reduces the per-iteration computational load compared to full CFR, storing regrets in tabular form for every possible information set remains intractable for 6-max NLH due to the astronomical number of such sets. Deep MCCFR overcomes this by employing function approximation, specifically deep neural networks, to estimate the cumulative regrets (or related quantities like advantages).2

The transition involves these key changes:

* **Neural Network Approximation:** Instead of a table entry for each information set, a neural network takes a feature vector representing an information set as input and outputs estimated regrets or advantage values for each legal action from that state.2 This allows the system to generalize across similar, but not identical, information sets.  
* **Memory Buffers (Replay Buffers):** During MCCFR traversals, samples of (information set, action, instantaneous regret, iteration weight) are collected. These samples are stored in memory buffers, often referred to as replay buffers or advantage memories.2 The neural networks are then trained using batches of data sampled from these buffers. Reservoir sampling is a common technique to manage the size of these buffers, ensuring that older and newer samples are appropriately represented.2

### **3.3. Comparative Analysis of Deep CFR Variants for 6-Max NLH**

Several Deep CFR variants have been proposed, each with nuances in how they use neural networks and manage the learning process.

* **Deep CFR (Brown et al. 2018/2019):** The original Deep CFR framework typically involves two neural networks per player: an *advantage network* that learns to predict the immediate counterfactual regrets for actions in a given information set, and a *strategy network* that learns to approximate the average strategy over all iterations.2 The advantage networks are periodically retrained from scratch using samples from an advantage memory (ℳV), while the strategy network (Π) is trained using samples from a strategy memory (ℳΠ).2 Deep CFR is proven to converge to an ϵ-Nash equilibrium in two-player zero-sum games, where ϵ is related to the network's prediction error.2  
* **Single Deep CFR (SD-CFR) (Steinberger 2019):** SD-CFR simplifies the Deep CFR architecture by eliminating the separate average strategy network.11 Instead, the average strategy is derived directly from the history of advantage (or value) networks trained during the MCCFR iterations.11 The primary motivation is to reduce the overall approximation error by removing one layer of neural network approximation.10 If Deep CFR trains a value network V and a separate strategy network Π, SD-CFR argues that training Π introduces an additional source of error. By directly using the sequence of learned Vt​ networks to compute the average strategy, this error source is avoided. This simplification has shown empirical benefits, with SD-CFR outperforming Deep CFR in terms of exploitability and head-to-head matches in poker benchmarks.10 Theoretically, SD-CFR is also considered more attractive as it more closely aligns with linear CFR under ideal conditions.11  
* **DREAM (Deep Regret minimization with Advantage baselines and Model-free learning) (Steinberger, Lerer, Brown 2020):** DREAM is a model-free deep reinforcement learning algorithm that converges to a Nash Equilibrium in two-player zero-sum games and to an extensive-form coarse correlated equilibrium in other game types.13 It uses one-action sampling (making it model-free, as it doesn't require a perfect game simulator for all aspects of its learning) and incorporates learned advantage baselines to reduce variance in regret estimates.14 While MCCFR is inherently model-based (requiring a simulator for traversals), the variance reduction techniques and model-free learning principles from DREAM could offer valuable insights for enhancing Deep MCCFR, particularly in managing the high variance of Monte Carlo estimates.  
* **ReBeL (Recursive Belief-based Learning) (Brown et al. 2020):** ReBeL introduced the concept of Public Belief States (PBS), where the "state" includes the probabilistic belief distribution over all agents' possible private states given common knowledge.18 It combines self-play reinforcement learning with depth-limited CFR search, using value and policy networks that operate on these PBSs. ReBeL achieved superhuman performance in heads-up NLH.18 While powerful, the complexity of PBS representation and the integration of search within the learning loop for 6-max NLH might be a significant step up from the target pluribus-poker-AI base. It represents a more advanced future research direction.

The evolution from the original Deep CFR to SD-CFR indicates a valuable pattern: reducing the number of independent neural network approximations can lead to more robust and better-performing systems. The dual-network architecture of Deep CFR introduces two potential sources of approximation error—one in estimating current regrets/advantages and another in estimating the average strategy. SD-CFR's approach of deriving the average strategy directly from the sequence of advantage/value networks consolidates these, potentially leading to a more stable learning signal and lower overall error. This suggests that for FEDOR, adopting an SD-CFR-like approach for the Deep MCCFR component is likely to be more effective.

While Deep MCCFR, as implied by the user query, is a model-based approach (requiring a game simulator for MCCFR traversals), the emergence of model-free algorithms like DREAM 13 in the broader deep regret minimization landscape is noteworthy. These algorithms learn from sampled trajectories without necessarily needing a perfect simulator for every aspect of training. For FEDOR, adhering to the Deep MCCFR paradigm aligns with the goal of building upon Pluribus's MCCFR foundations. However, the variance reduction techniques from DREAM could be particularly relevant for stabilizing the training of the Deep MCCFR neural networks, given the inherent variance in Monte Carlo sampling.

**Table 2: Comparison of Deep CFR Algorithm Variants for 6-Max NLH**

| Algorithm | Key Features | Neural Network Requirements | Sampling Strategy Used/Implied | Pros | Cons | Suitability for FEDOR (Initial) |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| **Deep CFR** (Brown et al. 2018/2019) | Two NNs per player (advantage, average strategy); Advantage memory (ℳV), Strategy memory (ℳΠ).2 | 2 per player (Advantage, Average Strategy) | External Sampling MCCFR (typically) | Theoretical convergence guarantees (2p0s) 2; Foundational work. | Higher potential approximation error due to two NNs; More complex memory management. | Medium |
| **Single Deep CFR (SD-CFR)** (Steinberger 2019\) | One NN type per player (advantage/value); Average strategy derived from value network history; Avoids separate average strategy NN.11 | 1 type per player (Advantage/Value) | External Sampling MCCFR (typically) | Lower overall approximation error 11; Better empirical performance than Deep CFR in poker 10; Simpler architecture. | Requires storing or accessing history of value networks (though often manageable 11). | **High** |
| **DREAM** (Steinberger et al. 2020\) | Model-free (one-action sampling); Learned advantage baselines for variance reduction.14 | Value/Advantage Network, Policy Network (implicitly through regret matching) | One-action sampling (model-free) | Does not require perfect simulator for all aspects 16; Strong variance reduction; Good empirical performance.13 | Model-free nature differs from MCCFR's typical model-based sampling; Convergence to EFCCE in N-player general-sum.13 | Medium (Inspirational for VR) |
| **ReBeL** (Brown et al. 2020\) | Public Belief States (PBS); Combines RL with depth-limited CFR search; Value and Policy networks on PBS.18 | Value Network (on PBS), Policy Network (on PBS) | Self-play with embedded CFR search | Superhuman in HU NLH 18; Principled approach to imperfect information. | High complexity for 6-max NLH implementation from pluribus-poker-AI base; PBS representation and management are challenging. | Low (Future Research) |

**Recommendation for FEDOR:** The initial implementation of Deep MCCFR for FEDOR should be based on the **Single Deep CFR (SD-CFR)** methodology. This involves using neural networks to approximate iteration regrets (or advantages) via external sampling MCCFR, and then deriving the average strategy directly from the historical sequence of these advantage network parameters or their outputs. This choice is motivated by SD-CFR's demonstrated empirical performance, theoretical elegance, and reduced architectural complexity compared to the original Deep CFR.11 Techniques for variance reduction inspired by DREAM could be explored as a secondary optimization.

## **4\. Neural Network Architecture and Feature Engineering for FEDOR**

The performance of FEDOR will heavily depend on the quality of its input feature representation and the architecture of its PyTorch-based neural networks. These networks will approximate the advantage functions central to Deep MCCFR.

### **4.1. Input Feature Vector Design for 6-Max NLH**

The input vector must comprehensively encode all strategically relevant information available to a player at any decision point in a 6-max NLH game. This includes:

* **Private Cards (Hole Cards):** Two cards unique to the player. A common representation is a 52-bit one-hot vector for each card, indicating its rank and suit. Alternatively, canonical suit mappings can reduce redundancy.  
* **Public Cards (Community Cards):** Up to five cards (flop, turn, river) shared by all players. These are revealed sequentially and should be encoded similarly to private cards.  
* **Betting History/Sequence:** This is crucial for inferring opponent strategies and game state. It's arguably the most complex part to encode.  
  * A sequence of all actions (fold, check, call, bet, raise) taken by each player in each betting round (preflop, flop, turn, river).  
  * The amounts bet or raised by each player, potentially normalized by pot size or big blind.  
  * Current pot size and the amount required to call.  
  * The PokerRL-Omaha fork's CNN input, which includes a vector of stacks and prior bets 22, and RLCard's NLH state representation, which encodes betting history across rounds 23, offer valuable starting points.  
* **Player Positions:** The acting player's position relative to the button (e.g., Small Blind, Big Blind, Under The Gun, Middle Position, Cutoff, Button). This can be one-hot encoded. The status (active, folded, all-in) of other players is also relevant.  
* **Stack Sizes:** Current stack sizes for all players at the table, often normalized by the big blind or initial tournament stack. RLCard's NLH state includes player chip counts.23  
* **Number of Active Players:** In 6-max, this can change as players are eliminated or fold, affecting strategy.

OpenSpiel's information\_state\_tensor() provides a flat vector that includes cards and betting history for simpler games like Kuhn Poker.24 For NLH, this vector would be significantly larger and more structured. The dberweger2017/deepcfr-texas-no-limit-holdem-6-players project 26 and its associated article 26 are primary references for a 6-max NLH feature set, as they directly address this game variant.

A noteworthy feature engineering technique is **preflop hand bucketing**, as mentioned in the PokerRL-Omaha fork for both Hold'em and Omaha.22 This groups preflop hands that are strategically equivalent (isomorphic, e.g., AsKh vs AdKc, as suits don't matter before the flop unless a flush draw is immediately possible). This reduces the input dimensionality and can improve neural network convergence early in training by leveraging domain-specific knowledge to simplify the learning task for the network.

**Table 3: Feature Engineering Specification for 6-Max NLH Input Vector (Proposed for FEDOR)**

| Feature Category | Encoding Method | Vector Size/Dimension (Approx.) | Rationale/Notes |
| :---- | :---- | :---- | :---- |
| **Player Private Cards** | 2x (52-bit one-hot or canonical suit \+ rank) | 104 (one-hot) or smaller | Unambiguous representation of player's hand. Consider preflop bucketing input.22 |
| **Public Cards (Board)** | 5x (52-bit one-hot or canonical suit \+ rank); Padded for pre-flop/flop/turn. | 260 (one-hot) or smaller | Represents community cards. Padding needed for consistent input size across betting rounds. |
| **Betting Sequence** | For each of 4 rounds (preflop, flop, turn, river): Sequence of (player\_idx, action\_type, bet\_amount\_norm) tuples. | Variable, requires fixed max seq len \+ padding or RNN. E.g., 6 players \* max\_actions\_per\_round \* feature\_per\_action. | Critical for strategy. action\_type (fold, check, call, bet, raise) one-hot encoded. bet\_amount\_norm normalized by pot or BB. Inspired by.22 |
| **Current Pot Size** | Normalized value (e.g., by sum of initial stacks or average stack). | 1 | Key game state variable. |
| **Amount to Call** | Normalized value (e.g., by current pot size or BB). | 1 | Immediate decision context. |
| **Player Stack Sizes** | 6x Normalized values (for each seat, normalized by initial BB or current BB). | 6 | Effective stack sizes are crucial..23 |
| **Player Positions** | Current player's position (one-hot, 6 values: SB, BB, UTG, MP, CO, BTN). | 6 | Positional advantage is fundamental in NLH. |
| **Active Player Mask** | 6-bit boolean vector indicating which players are still in the hand. | 6 | Tracks active opponents. |
| **Current Betting Round** | One-hot encoded (4 values: Preflop, Flop, Turn, River). | 4 | Indicates current stage of the game. |
| **Relative Player Positions** | Optional: Vector encoding relative positions of other active players to current player. | \~5\*k features | Can help model interactions with specific opponents. |
| **Is All-In Mask** | 6-bit boolean vector indicating if a player is all-in. | 6 | Important for end-of-action scenarios. |

The exact dimensions will depend on choices like maximum sequence lengths for betting history. The total input vector size will likely be several hundred to over a thousand elements.

### **4.2. PyTorch-based Neural Network Architecture(s) for Advantage/Policy Networks**

For FEDOR's Deep MCCFR, the neural networks will primarily serve as advantage networks (also called value networks in some contexts), predicting the counterfactual regret for each action given an information set. If an SD-CFR approach is used, a separate policy network is not explicitly trained; the policy is derived from the advantage network's outputs.

* **General Structure:** Multi-Layer Perceptrons (MLPs) are a common choice for poker due to the tabular/vector nature of the information state. The PokerRL framework provides nn\_type options such as "feedforward" (likely a standard MLP), "FLAT" (another MLP variant), and "dense\_residual".22 The MainPokerModuleFLAT2 from the PokerRL-Omaha fork is a deeper residual network that showed good performance.22 The dberweger2017 project for 6-max NLH also implements a specific PyTorch model 26, which should be a key reference.  
* **Layers and Units:**  
  * The number of hidden layers can range from 2 to 8, with units per layer typically between 256 and 1024\. Deeper networks with residual connections, like PokerRL's MainPokerModuleFLAT2 22, can capture more complex relationships without suffering from vanishing gradients.  
  * The input layer will match the dimension of the feature vector.  
  * The output layer will have a dimension equal to the number of possible actions. In NLH, the action space can be large (fold, call, check, various bet/raise sizes). Action abstraction (e.g., discretizing bet sizes into a few options like 0.5x pot, 1x pot, all-in) is often necessary to keep the output dimension manageable.  
* **Activation Functions:**  
  * ReLU (Rectified Linear Unit) is a standard choice and was used in early function approximation CFR.29  
  * Leaky ReLU, as used in PokerRL-Omaha's FLAT2 and CNN architectures 22, can prevent "dying ReLU" problems and reportedly improved loss decrease. A negative slope of 0.01 or 0.1 is common.  
  * GELU (Gaussian Error Linear Unit) is another effective activation function popular in Transformer models, but also applicable to MLPs.  
* **Output Head (Advantage Network):**  
  * The final layer outputs the estimated counterfactual regret (or advantage) for each legal action. These are raw values, not probabilities.  
  * During inference, the policy for the current iteration is derived using regret matching: σ(I,a)=∑a′∈A(I)​max(0,R(I,a′))max(0,R(I,a))​. If the sum of positive regrets is zero, a uniform random policy over legal actions is used.

The existence of specialized neural network modules within frameworks like PokerRL (e.g., "FLAT", "FLAT2") 22 and custom-designed models in successful projects such as dberweger2017 26 strongly suggests that off-the-shelf, generic MLP architectures may not be sufficient for the demanding task of learning strong poker strategies. Poker involves a unique interplay of public and private information, sequential decision-making, and opponent modeling, which benefits from network designs that are either empirically found to work well or incorporate structural priors (like residual connections for deeper learning). Therefore, when developing FEDOR, it is advisable to start with architectures that have a proven track record in poker AI, such as those found in PokerRL or the dberweger2017 implementation, rather than designing a completely novel architecture from scratch.

Furthermore, the significant impact of feature engineering, such as preflop hand bucketing in PokerRL-Omaha 22, underscores that even with advanced deep learning models, domain-specific input processing is critical. Such techniques reduce the complexity of the learning problem by encoding invariances (like suit irrelevance preflop) directly, allowing the neural network to focus on more nuanced strategic aspects. This synergy between thoughtful feature engineering and tailored neural network design is essential for achieving high performance in FEDOR.

**Table 4: Proposed PyTorch Neural Network Architecture for FEDOR (Advantage Network \- SD-CFR Style)**

| Network Name | Component | Layer Type(s) | Units/Filters | Activation | Input Shape | Output Shape | Notes |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| **AdvantageNet\_FEDOR** | Input Processing | Optional: Embedding layers for categorical features | Varies | \- | (batch\_size, feature\_dim) | (batch\_size, embed\_dim) | For high-cardinality discrete features if not fully one-hot encoded. |
|  | Core Layers | Sequence of torch.nn.Linear \+ torch.nn.ReLU (or LeakyReLU) \<br/\> Potentially with Residual Blocks (2x Linear \+ ReLU, add input to output) | 512 \-\> 1024 \-\> 1024 \-\> 512 (example) | ReLU or LeakyReLU 22 | (batch\_size, feature\_dim or embed\_dim) | (batch\_size, last\_hidden\_dim) | Inspired by PokerRL FLAT2 (deep residual) 22 or dberweger2017 model.26 Number of layers and units are hyperparameters to be tuned. |
|  | Output Head | torch.nn.Linear | num\_actions | Linear | (batch\_size, last\_hidden\_dim) | (batch\_size, num\_actions) | Outputs raw advantage values for each (abstracted) legal action. |

This architecture provides a flexible yet robust starting point, drawing inspiration from successful existing models. Hyperparameter tuning (number of layers, units, learning rate, etc.) will be crucial.

## **5\. Practical Implementation: GPU-Accelerated Training on NVIDIA 4070ti**

Efficiently utilizing the NVIDIA GeForce RTX 4070ti is critical for training FEDOR within a reasonable timeframe. This GPU, based on the Ada Lovelace architecture, offers significant computational power, 12GB of GDDR6X VRAM, and advanced features like third-generation RT Cores and fourth-generation Tensor Cores.

### **5.1. Setting up the PyTorch Environment for Optimal 4070ti Performance**

* **PyTorch Version:** The latest stable release of PyTorch (e.g., 2.x at the time of writing) is highly recommended. PyTorch 2.x introduced torch.compile, a feature that can significantly accelerate model training and inference by JIT-compiling parts of the model into optimized kernels.30 While older frameworks like PokerRL initially used PyTorch 0.4.1 or 1.0 31, modern PyTorch versions offer superior performance and compatibility with newer GPU architectures.  
* **CUDA and cuDNN:** Ensure that the installed NVIDIA drivers, CUDA Toolkit version, and cuDNN library version are compatible with the chosen PyTorch version and the RTX 4070ti. The official PyTorch website provides installation commands that bundle appropriate CUDA versions.  
* **Environment Management:** Utilize Conda or Python virtual environments (venv) to create isolated environments for the project. This helps manage dependencies and avoid conflicts. pip install \-r requirements.txt from a well-defined requirements file is standard practice.

### **5.2. Techniques for Efficient Data Loading and Batching to the GPU**

The Deep MCCFR training loop involves generating experience tuples (info\_set, action\_regrets, iteration\_weight) during game traversals (primarily CPU-bound) and then using these tuples to train the neural network (GPU-bound).

* **PyTorch DataLoader:** Use PyTorch's DataLoader class for batching training data. Setting num\_workers to a value greater than 0 in the DataLoader enables multi-process data loading, which can prefetch data in parallel and prevent the CPU from becoming a bottleneck for the GPU.  
* **Pin Memory:** When creating the DataLoader, set pin\_memory=True. This allocates the data in pinned (page-locked) memory on the CPU, which allows for faster asynchronous data transfers to the GPU via Direct Memory Access (DMA).  
* **Batch Size:** The batch size is a critical hyperparameter. It should be set as large as possible to maximize GPU parallelism without exceeding the 12GB VRAM of the RTX 4070ti. Starting points can be derived from existing Deep CFR implementations (e.g., mini\_batch\_size\_adv=2048 in a PokerRL Leduc example 28, though this was for a smaller game). The dberweger2017 project's settings for 6-max NLH would be a more relevant reference.32

### **5.3. Mixed-Precision Training (AMP)**

The RTX 4070ti's Tensor Cores provide substantial speedups for operations using lower precision, such as FP16 (half-precision).

* **torch.cuda.amp:** PyTorch's Automatic Mixed Precision (AMP) module allows for training in mixed FP16 and FP32 precision with minimal code changes.30 This can lead to significant training speedups (e.g., 51% faster on A100s reported for PyTorch 2.0 30) and reduced memory consumption, allowing for larger batch sizes or models.  
* **GradScaler:** When using AMP, a torch.cuda.amp.GradScaler should be used to scale loss values before the backward pass and unscale gradients before the optimizer step. This helps prevent gradient underflow, which can occur with small FP16 gradients.

### **5.4. torch.compile for Performance Boost**

PyTorch 2.0's torch.compile(model) function is a powerful tool for optimizing model performance.30 It uses TorchDynamo to capture PyTorch programs, then backends like TorchInductor to compile these into highly optimized kernels for the target hardware.

* **Modes:** Different modes like "default", "reduce-overhead" (good for smaller models or reducing framework overhead), or "max-autotune" (longer compile time, potentially fastest inference) can be used. For training FEDOR, "reduce-overhead" or experimenting with "max-autotune" during stable phases could yield benefits.  
* This feature can provide substantial speedups on Ada Lovelace GPUs like the 4070ti with minimal code changes.

### **5.5. Parallelizing MCCFR Traversals and Neural Network Updates**

A common pattern in deep reinforcement learning for games is the interplay between data generation and model training.

* **Data Generation (CPU):** MCCFR traversals simulate game play to generate training samples. These simulations are often CPU-intensive. Frameworks like PokerRL utilize Ray for distributing these worker tasks across multiple CPU cores or even multiple machines.31 PyPoks also mentions using multiprocessing for its asynchronous self-play.34 For FEDOR on a single machine with an RTX 4070ti, multiple CPU cores should be dedicated to parallel game traversals.  
* **Neural Network Training (GPU):** The forward and backward passes of the neural network, along with optimizer steps, occur on the GPU.  
* **Asynchronous Pipeline:** The system should be designed so that data generation on the CPU can occur concurrently with neural network training on the GPU. A producer-consumer pattern, where CPU workers fill a replay buffer from which the GPU trainer samples batches, is effective. This ensures the GPU is not kept waiting for data.

The capabilities of modern GPUs like the NVIDIA 4070ti, with its Ada Lovelace architecture and specialized Tensor Cores, are best realized when paired with contemporary software features. PyTorch 2.0's torch.compile and Automatic Mixed Precision (AMP) are prime examples.30 Simply possessing powerful hardware is insufficient; software-level optimizations are paramount to unlock its full potential. Thus, for FEDOR, a naive PyTorch implementation would likely underutilize the 4070ti. Adopting AMP and torch.compile from the outset is a crucial step towards achieving efficient training.

Moreover, in complex game AI training scenarios like Deep MCCFR, the process of data generation (simulating game traversals, which is often CPU-bound) can become a significant bottleneck for GPU-based neural network training if not managed effectively. Frameworks that explicitly support distributed or parallel data generation, such as PokerRL with Ray 31 or PyPoks with Python's multiprocessing 34, directly address this challenge. This implies that FEDOR's training architecture must be designed to facilitate asynchronous data generation on CPU cores while the GPU is concurrently training the model, thereby maximizing overall throughput and minimizing GPU idle time.

### **5.6. Monitoring GPU Utilization**

* **nvidia-smi:** The NVIDIA System Management Interface command-line utility provides real-time monitoring of GPU utilization, memory usage, temperature, and power draw.  
* **PyTorch Profiler (torch.profiler):** This tool can be integrated into the PyTorch training script to get detailed performance breakdowns of CPU and GPU operations, identify time-consuming kernels, and pinpoint data loading or transfer bottlenecks.

By implementing these practical considerations, the training of FEDOR on an NVIDIA 4070ti can be made significantly more efficient, enabling more extensive experimentation and faster convergence.
