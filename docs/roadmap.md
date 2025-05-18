## **Actionable Research and Development Roadmap for FEDOR**

Developing FEDOR requires a structured, phased approach, building upon the pluribus-poker-AI foundation and progressively integrating Deep MCCFR components and GPU optimizations.

### **Phase 1: Game Engine Finalization & Baseline MCCFR (Python-first)**

The initial phase focuses on establishing a robust game environment and validating the core regret minimization logic with a simpler, tabular MCCFR.

* **Task 1.1: Extend pluribus-poker-AI Game Engine:**  
  * **Objective:** Implement comprehensive 6-max NLH game logic.  
  * **Details:** This involves extending the existing Python game engine in pluribus-poker-AI 6 to fully support all rules of 6-player No-Limit Hold'em. This includes correct handling of preflop, flop, turn, and river betting rounds; accurate pot calculations, especially with multiple raises and re-raises; robust side-pot logic for all-in scenarios involving multiple players with varying stack sizes; and correct determination of winners at showdown. The game state representation must be meticulously designed to capture all necessary information for an agent, and the generation of information sets for each of the six players must be accurate and efficient. OpenSpiel's NLH implementations 24 and RLCard's NLH game logic 23 can serve as references for rule validation and standardized practices.  
* **Task 1.2: Implement Tabular MCCFR for Small Games:**  
  * **Objective:** Validate the core CFR traversal and regret update logic.  
  * **Details:** Before tackling Deep MCCFR, implement a standard tabular MCCFR algorithm. This should initially target simpler poker variants like 2-player Kuhn Poker or Leduc Poker, as suggested in the pluribus-poker-AI roadmap.1 External sampling MCCFR 9 is recommended. Regrets will be stored in Python dictionaries or simple arrays mapping information set strings/hashes to regret arrays. The primary goal is to verify that the MCCFR traversals correctly explore the game tree (as per the sampling scheme) and that regret updates lead to convergence towards a Nash equilibrium. Exploitability calculations for these small games will be feasible and should be used to confirm correctness.

### **Phase 2: Neural Network Integration & Deep MCCFR Prototype (PyTorch & 4070ti)**

This phase transitions from tabular methods to neural network-based function approximation for Deep MCCFR.

* **Task 2.1: Develop PyTorch Neural Networks:**  
  * **Objective:** Implement the advantage/value network architectures.  
  * **Details:** Based on the designs outlined in Section 4 (Table 4), implement the advantage network(s) using PyTorch. This will likely be an MLP architecture, potentially incorporating residual connections inspired by PokerRL's FLAT2 22 or the model from dberweger2017.26 Implement the feature engineering pipeline to convert raw game state information (Section 4, Table 3\) into the fixed-length vector input required by these networks.  
* **Task 2.2: Implement Deep MCCFR (SD-CFR style) Training Loop:**  
  * **Objective:** Create the core training pipeline for FEDOR.  
  * **Details:**  
    1. **Advantage Memory:** Implement memory buffers (e.g., using Python lists with a maximum size or NumPy arrays) to store experience tuples: (info\_set\_vector, sampled\_action\_regrets, iteration\_weight). Employ reservoir sampling 2 to manage buffer capacity.  
    2. **Training Loop:**  
       * **Data Generation:** Perform MCCFR traversals (using external sampling) on the 6-max NLH game engine. For each information set encountered by the traverser, calculate the instantaneous counterfactual regrets for all actions.  
       * **Memory Storage:** Store the (info\_set\_vector, sampled\_action\_regrets, iteration\_weight) tuples in the advantage memory. The iteration\_weight could be the iteration number, as in Linear CFR 2, to give more importance to recent samples.  
       * **Network Training:** Periodically, sample mini-batches from the advantage memory. Train the PyTorch advantage network by minimizing a weighted Mean Squared Error (MSE) loss between the network's predicted advantages and the sampled regrets from the buffer.2  
       * **Optimizer:** Use Adam or AdamW \[Loshchilov and Hutter, 2019\] with an appropriate learning rate and potentially a learning rate schedule (e.g., linear decay).  
    3. **Strategy Generation:**  
       * **Current Iteration Strategy:** Derive the strategy for the current MCCFR iteration directly from the positive predicted advantages of the *current* advantage network using regret matching.  
       * **Average Strategy (SD-CFR Style):** The final converged strategy is an average of policies. In an SD-CFR approach 11, this average strategy is implicitly represented by or derived from the historical sequence of advantage network parameters (or their outputs on a representative set of information sets) rather than training a separate explicit average strategy network.  
* **Task 2.3: Initial Training Runs on 4070ti:**  
  * **Objective:** Debug the pipeline and test initial learning.  
  * **Details:** Begin training with small-scale experiments. This could involve using heavily abstracted versions of 6-max NLH (e.g., very few bet sizes, simplified game tree) or a 6-player version of Leduc Poker to ensure the entire pipeline (data generation, memory storage, network training, strategy extraction) functions correctly. Focus on achieving stable loss convergence and verifying basic GPU utilization on the RTX 4070ti, applying the setup principles from Section 5\.

### **Phase 3: Scaling, Optimization, and Evaluation**

The final phase focuses on training FEDOR on the full game, optimizing performance, and rigorously evaluating its strength.

* **Task 3.1: GPU Optimization and Profiling:**  
  * **Objective:** Maximize training throughput on the RTX 4070ti.  
  * **Details:** Implement Automatic Mixed Precision (AMP) using torch.cuda.amp and GradScaler to accelerate training and reduce memory footprint.30 Leverage torch.compile (with modes like "reduce-overhead" or "max-autotune") for further speedups.30 Use nvidia-smi and the PyTorch Profiler (torch.profiler) to identify and resolve CPU or GPU bottlenecks, paying close attention to data loading, CPU-GPU transfers, and kernel execution times.  
* **Task 3.2: Full-Scale 6-Max NLH Training:**  
  * **Objective:** Train FEDOR on the unabstracted or minimally abstracted version of 6-max NLH.  
  * **Details:** This will be a computationally intensive process, potentially requiring days or weeks of training on the RTX 4070ti. Careful monitoring of training metrics (loss, regret convergence if measurable indirectly) is essential.  
* **Task 3.3: Implement Robust Evaluation Methods:**  
  * **Objective:** Accurately assess FEDOR's performance.  
  * **Details:** Exact exploitability calculation is intractable for 6-max NLH. Implement approximate evaluation methods:  
    * **Local Best Response (LBR):** As used in PokerRL 22, LBR provides an estimate of exploitability by computing best responses in subgames or against fixed opponent strategies.  
    * **RL Best Response (RL-BR):** Train a separate deep reinforcement learning agent (e.g., a DQN) to find the best response against FEDOR's fixed strategy. The performance of this RL-BR agent provides an exploitability estimate.31  
    * **Head-to-Head (H2H) Play:** Evaluate FEDOR by playing it against other strong open-source poker AIs (if available for 6-max NLH) or against previous iterations of itself. Track metrics like win rate (mbb/hand \- milli-big blinds per hand), showdown winnings, etc.  
* **Task 3.4: Iterative Refinement and Potential C++ Porting:**  
  * **Objective:** Continuously improve FEDOR's strategy.  
  * **Details:** Based on evaluation results and training dynamics, iteratively refine the neural network architecture, feature engineering, and training hyperparameters. If profiling (Task 3.1) reveals persistent CPU bottlenecks in Python code that significantly hinder GPU utilization (e.g., in the MCCFR traversal logic or state updates), consider porting these specific, performance-critical modules to C++ and creating Python bindings (as discussed in Section 2.2).

This phased development approach is essential for managing the inherent complexity of building a sophisticated AI system like FEDOR. Attempting to construct the full-scale, highly optimized system from the outset would be fraught with risk. Each phase builds upon the validated successes of the previous one, allowing for incremental development, testing, and refinement. This iterative cycle is standard in large-scale AI research and software engineering.

A critical consideration, especially for N-player games like 6-max NLH, is the difficulty of evaluation. Unlike two-player zero-sum games where direct exploitability is a clear and often computable measure of strength, assessing an N-player strategy is far more complex. The computational cost of finding a true best response against a 6-player strategy profile is prohibitive. This necessitates reliance on approximate methods like LBR or RL-BR, as employed by frameworks such as PokerRL 31, and empirical evaluations through head-to-head play. The development and refinement of these approximate evaluation techniques are, therefore, as crucial as the development of the AI agent itself, as they are the primary means by which progress and strategic nuances can be measured.

**Table 5: FEDOR Development Roadmap Milestones and Key Tasks**

| Phase | Milestone | Key Tasks | Estimated Effort | Relevant Open-Source/Snippets |
| :---- | :---- | :---- | :---- | :---- |
| **1** | **6-Max NLH Engine Complete** | Extend pluribus-poker-AI for full 6-max NLH rules, state/info set generation. | Medium-Large | pluribus-poker-AI 6, OpenSpiel NLH 35, RLCard NLH 23 |
| **1** | **Tabular MCCFR Validated** | Implement tabular external sampling MCCFR for Kuhn/Leduc poker; verify convergence. | Medium | pluribus-poker-AI roadmap 1, MCCFR theory 9 |
| **2** | **PyTorch NN & Feature Eng. Implemented** | Develop advantage NNs (Table 4\) and feature vector (Table 3\) in PyTorch. | Medium | PokerRL NNs 22, dberweger2017 model 26, RLCard features 23 |
| **2** | **Deep MCCFR (SD-CFR) Training Loop Operational** | Implement advantage memory, training loop (data gen, NN training, SD-CFR style strategy). | Large | Deep CFR 2, SD-CFR 11, dberweger2017 trainer 33 |
| **2** | **Initial Small-Scale Training Debugged** | Conduct training on abstracted 6-max NLH or Leduc 6P; verify loss convergence, basic GPU use. | Medium | PyTorch docs 30 |
| **3** | **GPU Optimizations Applied** | Implement AMP, torch.compile; Profile and resolve CPU/GPU bottlenecks. | Medium | PyTorch AMP/compile 30, nvidia-smi |
| **3** | **Full-Scale 6-Max NLH Training Initiated** | Scale training to full (or near-full) 6-max NLH on 4070ti. | Large (Ongoing) | \- |
| **3** | **Robust Evaluation Suite Implemented** | Develop LBR, RL-BR, and H2H evaluation frameworks. | Medium-Large | PokerRL evaluation 22 |
| **3** | **Iterative Refinement & C++ Porting (If Needed)** | Continuously tune based on evaluations; Port Python bottlenecks to C++ if identified. | Ongoing | Profiling tools, Pybind11 |

## **Leveraging Open-Source Libraries and Tools**

The development of FEDOR will extensively utilize and adapt code from several key open-source projects. This strategy accelerates progress by building on proven components.

* **pluribus-poker-AI** 4**:** This repository will serve as the **primary codebase** for FEDOR. Its Python structure 6 for game logic (pluribus/games/poker\_game.py), poker utilities (pluribus/poker/), and AI stubs (pluribus/ai/) will be adapted and extended for 6-max NLH and Deep MCCFR as detailed in Table 1\.  
* **PokerRL** 11**:**  
  * **Neural Network Architectures:** PokerRL's PyTorch neural network modules, such as MainPokerModuleFLAT and the optimized MainPokerModuleFLAT2 (a deeper residual network using Leaky ReLU from the PokerRL-Omaha fork 22), and feedforward networks from DeepCFR examples 28, are strong candidates for FEDOR's advantage networks.  
  * **Observation Encoding:** While specific NoLimitHoldem encoder files were not directly accessible in the provided search results 36, the general concepts for input representation in PokerRL, particularly the preflop hand bucketing for Hold'em and the CNN input structure from the PLO fork (vector of stacks and bets) 22, will inform FEDOR's feature engineering.  
  * **Evaluation Tools:** Methodologies for Local Best Response (LBR), RL Best Response (RL-BR), and Head-to-Head (H2H) play detailed in PokerRL 22 will be adapted for evaluating FEDOR.  
  * **Distributed Training (Future Reference):** PokerRL's integration with Ray for distributed computing 31 provides a valuable blueprint if FEDOR's training needs to scale beyond a single machine.  
* **OpenSpiel** 7**:**  
  * **Game Logic Validation:** OpenSpiel's implementations of poker variants like Kuhn Poker and Leduc Poker 24 can be used to cross-validate the game engine developed from pluribus-poker-AI. If a robust 6-max NLH game is available in OpenSpiel, it can also serve as a reference.  
  * **Information State Representation:** The concept and structure of OpenSpiel's information\_state\_tensor() 24, which provides a flat vector representation of a player's knowledge, will influence the design of FEDOR's input feature vector.  
  * **Deep CFR Implementations:** OpenSpiel contains examples of Deep CFR in both TensorFlow 39 and PyTorch.41 These implementations, particularly their replay buffer mechanisms (e.g., reservoir sampling) and network designs, offer algorithmic insights, even if FEDOR uses a custom PyTorch implementation.  
* **dberweger2017/deepcfr-texas-no-limit-holdem-6-players** 13**:** This repository is a **critical and highly relevant resource** as it specifically implements Deep CFR for 6-player NLH using PyTorch.  
  * **Feature Engineering:** Its feature\_utils.py (or equivalent) 43 will provide direct examples of card encoding and betting history representation for 6-max NLH.  
  * **PyTorch Model:** The model.py file 44 contains the neural network architecture used, which is invaluable.  
  * **Training Loop:** The CFRtrainer.py 33 details the experience replay, loss functions, optimizer, and stabilization techniques employed.  
  * The accompanying Medium article 19 offers high-level explanations of these components.  
* **PyPoks** 34**:**  
  * **DRL Concepts:** While FEDOR focuses on Deep MCCFR, PyPoks' implementations of Policy Gradient, Actor-Critic, and PPO in PyTorch for poker 34 can offer general insights into deep reinforcement learning for this domain.  
  * **Parallel Processing:** Its approach to asynchronous self-play using multiprocessing and multi-GPU support 34 can inform the design of an efficient data generation pipeline for FEDOR, even on a single powerful GPU like the 4070ti (by maximizing CPU core utilization for traversals).

The successful development of advanced AI systems like FEDOR is often accelerated by building upon the collective knowledge and efforts encapsulated in open-source projects. Frameworks such as PokerRL and OpenSpiel provide well-tested modules and algorithmic blueprints, while specific project implementations like dberweger2017/deepcfr-texas-no-limit-holdem-6-players offer solutions tailored to the exact problem domain (6-max NLH Deep CFR). This "standing on the shoulders of giants" approach allows the FEDOR project to bypass redundant foundational work and focus on targeted enhancements and novel contributions.

Furthermore, no single existing framework may perfectly align with all of FEDOR's specific requirements (6-max NLH, Deep MCCFR with an SD-CFR philosophy, PyTorch, and optimization for a specific GPU). Thus, a strategy of judiciously selecting and integrating the most relevant components and ideas from each—for instance, using pluribus-poker-AI as the base game engine, adapting neural network architectures from PokerRL or dberweger2017, drawing on OpenSpiel for standardized game concepts and information state representations, and learning from PyPoks' parallel processing techniques—is likely to yield the most robust and performant system. This cross-pollination of ideas is a hallmark of dynamic research and development environments.

## **Conclusion and Future Directions**

### **Summary of Proposed Path for FEDOR**

The development of FEDOR, a Deep Monte Carlo CFR agent for 6-max No-Limit Hold'em, will proceed by enhancing the tanker-fund/pluribus-poker-AI repository. The core AI algorithm will be a Deep MCCFR implemented in a style similar to Single Deep CFR (SD-CFR), utilizing PyTorch-based neural networks to approximate advantage values from data generated via external sampling. Feature engineering will focus on creating a comprehensive information state vector for 6-max NLH, drawing inspiration from successful projects like dberweger2017/deepcfr-texas-no-limit-holdem-6-players and frameworks like PokerRL and OpenSpiel. Training will be optimized for an NVIDIA RTX 4070ti using techniques such as Automatic Mixed Precision and torch.compile. The development will follow a phased roadmap, starting with game engine completion and tabular MCCFR, progressing to a Deep MCCFR prototype, and culminating in scaled-up training, rigorous evaluation, and iterative refinement.

### **Potential Advanced Research Avenues**

Once a strong baseline FEDOR agent is established, several advanced research directions can be pursued to further enhance its capabilities:

* **Advanced Action and State Abstraction:** While Deep MCCFR aims to learn without explicit abstraction, the sheer scale of 6-max NLH might still benefit from more sophisticated, potentially learnable, abstraction techniques. Research into methods like RL-CFR, which dynamically learns action abstractions 46, could reduce the computational burden or improve generalization.  
* **Incorporating Ideas from ReBeL and DREAM:**  
  * **Public Belief States (ReBeL):** For more nuanced opponent modeling, especially in a 6-player dynamic, exploring the integration of Public Belief States (PBS) 18 into the Deep MCCFR framework could be a long-term goal. This would involve training value/advantage networks that operate on these belief states, a significant architectural evolution.  
  * **Model-Free Learning and Variance Reduction (DREAM):** While FEDOR's MCCFR is model-based, the variance reduction techniques from model-free algorithms like DREAM 14, particularly its use of learned advantage baselines, could be adapted to further stabilize and accelerate the training of Deep MCCFR's neural networks.  
* **Automated Hyperparameter Optimization:** The performance of deep learning models is highly sensitive to hyperparameters. Employing systematic hyperparameter optimization tools like Optuna (related context in 47) for tuning neural network architectures, learning rates, buffer sizes, and other training parameters could lead to significant performance gains.  
* **Multi-Agent Training Dynamics and Curriculum Learning:** Training in a 6-player self-play environment presents unique challenges in terms of non-stationarity and convergence. Investigating more sophisticated opponent selection strategies during self-play, or employing curriculum learning (starting with simpler versions of the game or weaker opponents and gradually increasing complexity) could improve training stability and final performance.  
* **Explainability and Strategy Analysis:** Developing tools and techniques to interpret FEDOR's learned strategies is crucial for understanding its decision-making process, identifying potential biases or weaknesses, and building trust in its capabilities. Visualizing action probabilities in key situations, or analyzing network activations, could provide insights. PokerRL's PokerViz tool for visualizing strategies in tiny games 31 is a rudimentary example; more advanced methods would be needed for 6-max NLH.  
* **Exploration of Alternative Neural Architectures:** While MLPs are standard, continued exploration of architectures like Graph Neural Networks (GNNs) for relational reasoning over game elements (players, cards, betting actions) or Transformer models for processing sequential betting information could yield breakthroughs.

The development of FEDOR represents a challenging but rewarding endeavor at the intersection of game theory, deep learning, and high-performance computing. By systematically leveraging existing open-source resources and focusing on principled algorithmic enhancements and practical implementation strategies, it is feasible to create a formidable 6-max No-Limit Hold'em AI. The outlined future research directions offer pathways to push the boundaries of AI performance in complex multi-agent imperfect information games even further.