# **Design and Implementation of FEDOR.ppl: A Solver-Based Shanky Profile for 5-Max No-Limit Texas Hold'em (2-30bb)**

**Executive Summary** This report outlines a comprehensive methodology for developing FEDOR.ppl, a production-ready, solver-based Shanky/OpenHoldem profile for 5-max No-Limit Texas Hold'em, optimized for effective stack depths of 2 bb to 30 bb. The project leverages credible public GTO resources, including charts, push/fold tables, and existing profile fragments. Where GTO coverage is lacking, new strategies will be generated using Deep Monte Carlo Counterfactual Regret Minimization (MCCFR) or Single Deep CFR (SD-CFR) via the PokerRL framework, targeting convergence on a single NVIDIA RTX 4070 Ti (12 GB VRAM) within a 7-day training cycle per segment. A rich bet-sizing menu (1/3P, 1/2P, 2/3P, P, 2P, jam) will be modeled, with unlimited re-raises handled recursively until the stack-to-pot ratio (SPR) is less than 1\. Board abstraction techniques will be employed to manage VRAM usage, aiming for peak GPU memory below 11 GB. The final profile will convert probabilistic solver outputs into deterministic OpenPPL logic, utilizing custom C/C++ helper DLLs for enhanced functionality. The project is structured into eight weekly sprints, culminating in a validated FEDOR.ppl profile demonstrating near-oracle level performance (≥ \-1 bb/100 vs. the MCCFR oracle over 1 million hands). Key deliverables include a detailed asset inventory, bet-tree design, board abstraction research, MCCFR training protocols, merge/quantisation algorithms, code generation blueprints, a validation plan, and a complete project roadmap with risk assessment.

## **1\. Asset Inventory**

A thorough audit of publicly available GTO assets is crucial for constructing FEDOR.ppl. The following table catalogues relevant resources for 5-max NLH (≤ 30 bb effective stacks), assessing their coverage, licensing, and ease of parsing.

| Source | Street(s) | Coverage Depth | Licence | Parse Method |
| :---- | :---- | :---- | :---- | :---- |
| GTO Wizard Snapshots/Blog | Preflop, Postflop | 6-max NL10 (20-30bb) cash game solutions (General & Simple). Free eBook with quizzes. GTO Reports for preflop cash. | Commercial (free access to some solutions/tools) | Web scrape (if public), API (if available), manual data entry from viewer, potential UPI export for custom solutions |
| ConsciousPoker Push/Fold Charts | Preflop | Push/Fold charts, stack depths up to 30bb (implied). | Free (publicly linked) | Web scrape, PDF parse |
| FloatTheTurn Push/Fold App | Preflop | Push/Fold decisions. | Free (publicly linked) | Web scrape, manual data entry from app UI |
| SnapShove | Preflop | Push/Fold decisions, variable parameters. | Freemium | Web scrape, manual data entry from app UI |
| SimpleNash | Preflop, Postflop | GTO solver for various situations, including short stacks. Output format not detailed but likely text-based. | Free | Direct output parsing (if CLI/batch mode exists), screen scrape from UI |
| ICMIZER3 Outputs (e.g., Fig 1 in ) | Preflop | Open-shoving ranges, EV calculations (e.g., 16bb BTN shove). | Commercial (subscription) | Screenshot OCR, manual data entry if public examples are images |
| Upswing Poker Charts/Quizzes | Preflop | Short stack shove/fold quizzes (5-13bb). General preflop charts (may need adaptation). | Commercial (free content mixed with paid) | Web scrape, PDF parse (if available), manual entry from quiz answers |
| PokerCoaching.com Preflop Charts | Preflop | 6-max RFI, vs RFI, vs 3-bet charts (various stack depths implied by general nature). Specific raise sizing guidelines. | Commercial (free charts available) | Web scrape, manual data entry |
| Scribd GTO Charts (e.g., 25bb-gto-charts) | Preflop | 25bb 5-max charts (RFI, vs RFI, BvB). Also 15bb charts. | User-uploaded (check individual licence) | PDF parse, manual data entry |
| Cepheus Preflop Strategy | Preflop (Limit HE) | Heads-Up Limit Hold'em preflop (solved). Not directly NLH short-stack but foundational. | Academic/Public | Web scrape from interactive viewer, direct data download (if offered) |
| Libratus/DeepStack Papers | Conceptual | Principles of abstraction, subgame solving, bet sizing. Not direct charts. | Academic | N/A (conceptual) |
| GTOBase Free Solutions | Preflop, Postflop | Free 6-max Cash (100bb default, may have adaptable elements), FreeMTT (various stacks). Spin\&Go (5-30bb). | Commercial (free tiers) | Web interface, potential export if supported by free tier. |
| RangeConverter Preflop Charts | Preflop | 8-max MTT charts (e.g., 40bb), simplified GTO (actions rounded to nearest 50%). | Commercial (free PDFs available) | PDF parse, manual data entry from viewer. |
| Existing OpenHoldem.ppl Fragments | All Streets | Variable, often heuristic or simplified GTO. | Open Source / User-created | Direct PPL text parsing. |

The primary challenge in utilizing these assets lies in the heterogeneity of formats and the often-restrictive licenses of commercial tools. For FEDOR.ppl, preference will be given to academic sources, verifiably open GTO chart repositories, and outputs from free-tier GTO solvers where parsing is feasible and licensing permits educational, offline use. Web scraping and PDF parsing will be necessary for many static chart resources. Tools like GTO Wizard, while largely commercial, offer some free solutions and an "Elite Tier" custom solver whose output might be parsable if it conforms to standards like UPI. SimpleNash is noted as a free GTO solver, but its output format needs investigation. The Cepheus project provides preflop strategies for Limit Hold'em, which, while not directly applicable to NLH, offers insights into GTO principles.

## **2\. Raise-Tree & Bet-Menu Design**

A robust and tractable bet-tree design is fundamental to modeling No-Limit Hold'em. The FEDOR.ppl profile will employ a recursive betting structure to accommodate unlimited raises, constrained by the Stack-to-Pot Ratio (SPR).  
**Bet-Size Menu:** The base bet-size menu for any decision point (bet or raise) will include: 1/3P, 1/2P, 2/3P, P, 2P, and Jam (all-in). This rich menu provides a good approximation of common NLH bet sizings.  
**Recursion Scheme:** When a player faces a bet or raise, they have the option to fold, call, or re-raise. If a re-raise is chosen, the same base bet-size menu is made available, scaled to the new pot size and remaining effective stacks. This process can repeat. The recursion terminates for a given betting line when:

1. A player chooses to fold or call.  
2. A player goes all-in (jams).  
3. The Stack-to-Pot Ratio (SPR) for the player to act falls below 1.0. Once SPR \< 1.0, the only available raise option becomes Jam. This condition prevents arbitrarily small raises when stacks are very shallow relative to the pot, naturally capping the recursion depth for most practical scenarios.  
4. A pre-defined maximum number of bets/raises per street is reached (e.g., 4 or 5 raises), after which only call/fold options are allowed. This is a common simplification in solvers to keep game trees manageable.

**Estimating Node Counts and Peak VRAM:** Estimating the exact number of nodes in a No-Limit Hold'em game tree with a rich bet menu and recursive raises is complex. The number of decision points (information sets) grows exponentially with stack depth and the number of allowed bet sizings. For short stacks (2-30bb), the game tree is considerably smaller than for deep-stacked play.  
Let B be the number of bet/raise size options (excluding fold, call, check). In our case, B=6 (1/3P, 1/2P, 2/3P, P, 2P, Jam). A simplified estimation for a single betting sequence (e.g., Bet \-\> Raise \-\> Re-raise \-\>...):

* Depth 1 (1 bet/raise): Player 1 has B options. Player 2 responds (fold, call, B raise options). Roughly B \\times (2+B) terminal/transition states from P2's perspective.  
* Depth 2 (2 raises): Player 1 Bets, Player 2 Raises, Player 1 Re-raises. Number of nodes increases significantly.  
* The actual game tree involves multiple players and branching at each decision point.

The number of information sets is a more relevant metric for solver memory. For HULH Limit Hold'em (a much simpler game), there are \\approx 10^{14} information sets. NLH is vastly larger, estimated at \\approx 10^{165} states for 200bb stacks. However, for 2-30bb 5-max, the effective game size is dramatically smaller.  
**Peak VRAM Estimation Factors:** Peak VRAM usage in MCCFR/SD-CFR is influenced by:

1. **Number of Information Sets (Abstract States):** This is the primary driver. Determined by card abstraction (number of buckets for flop, turn, river) and action abstraction (bet tree complexity).  
2. **Neural Network Size:** Number of parameters in the value/policy networks.  
3. **Batch Size:** Larger batch sizes during training consume more VRAM.  
4. **Reservoir Buffer Size (for MCCFR/Deep CFR):** Stores samples of (infoset, regret, strategy).  
5. **Precision (FP32 vs FP16):** FP16 roughly halves memory for parameters, gradients, and activations.

**Table 2.1: Estimated Node Counts and VRAM Impact at Different Recursion Depths (Illustrative)**

| Max Raises per Street | Estimated Relative Node Increase Factor (vs. 1 Raise) | Qualitative Peak VRAM Impact (with fixed abstraction) | Recommendation |
| :---- | :---- | :---- | :---- |
| 1 | 1x | Baseline | Too restrictive, doesn't capture NLH dynamics. |
| 2 | 5-10x | Moderate Increase | Minimum for reasonable NLH. |
| 3 | 20-50x | Significant Increase | Likely feasible for short stacks with good abstraction. This is a common limit in many solver setups. **Recommended Cap.** |
| 4 | 100-200x+ | Very High Increase | Potentially exceeds VRAM budget for the target board abstraction sizes unless action space is severely pruned. May be viable for SPR \< 1 scenarios. |

**Recommendation for Raise Cap:** A maximum of **3 raises** (i.e., Bet \-\> Raise1 \-\> Raise2 \-\> Raise3) per street is recommended as a starting point. Beyond this, for SPR \> 1, actions could be limited to Call/Fold/Jam. If SPR \< 1, only Call/Fold/Jam are allowed after any initial bet/raise. This cap, combined with the SPR \< 1 rule, should keep the game tree tractable for the 2-30bb stack depth range. The "All-in Threshold %" (e.g., if a raise is \>70% of remaining effective stack, it becomes an all-in) and "Add All-in SPR" (e.g., automatically add all-in if SPR \< 2\) rules from tools like HoldemResources Calculator can further prune the tree. These rules effectively reduce the branching factor at shallow SPRs.  
The actual node count will be heavily influenced by the card abstraction. The goal is to choose abstraction levels (bucket counts) that, when combined with this bet tree structure, fit within the 11 GB VRAM target. Initial experiments in Sprint 3 will be critical to validate this.

## **3\. Board Abstraction R\&D**

Effective board abstraction is critical for making Deep MCCFR training feasible within the 12 GB VRAM limit of an RTX 4070 Ti. The process involves defining features to characterize board textures and then clustering boards based on these features into a manageable number of buckets for the flop, turn, and river.  
**Clustering Features:** The following features will be engineered to represent board states. These features aim to capture strategically relevant aspects of the board texture :

1. **Suit Structure:**  
   * *Monotone*: Boolean (1 if all cards same suit, 0 otherwise).  
   * *Two-Tone*: Boolean (1 if two suits present, with two or three cards of one suit, 0 otherwise).  
   * *Rainbow*: Boolean (1 if all cards different suits, 0 otherwise).  
   * *Number of Flush Cards*: Integer (e.g., 3 on a monotone flop).  
   * *Number of Flush Draws Possible*: Integer (count of suits with 2 cards on flop/turn).  
2. **Pairedness:**  
   * *Board Pair*: Boolean (1 if board is paired, 0 otherwise).  
   * *Two Pair on Board*: Boolean (flop/turn/river).  
   * *Trips on Board*: Boolean (flop/turn/river).  
   * *Full House on Board*: Boolean (river).  
3. **Connectivity:**  
   * *Number of Straight Gaps*: Integer (e.g., T87 has 1 gap for a straight with J9, 0 gaps for 96).  
   * *Number of Open-Enders Possible*: Integer (count of two-card combinations on board that form open-ended straight draws).  
   * *Highest Straight Possible*: Rank (e.g., Ace on A K Q J x).  
   * *Number of Gutshots Possible*: Integer.  
4. **High-Card Tier:**  
   * *Highest Card Rank*: (e.g., Ace=14, King=13,..., Two=2).  
   * *Second Highest Card Rank*:  
   * *Third Highest Card Rank*:  
   * *Number of Broadway Cards*: (A, K, Q, J, T).  
   * *Is Ace Present?*: Boolean.  
5. **Equity Moments (Optional, advanced feature):**  
   * *Mean EHS (Expected Hand Strength)*: Average EHS of a random hand against another random hand on this board.  
   * *Variance/StdDev of EHS*: Captures how "static" or "dynamic" the board is in terms of hand value distribution.  
   * *Skewness/Kurtosis of EHS*: Higher-order moments to describe the shape of the EHS distribution. These can be pre-calculated or sampled. The concept is similar to using EHS distributions for hand abstraction.

**Feature Vector Construction:** Each board (flop, turn, or river) will be transformed into a numerical feature vector based on the features above. For example, a flop like K\\heartsuit 7\\diamond 2\\clubsuit (rainbow, no pairs, K-high, some connectivity) would have a specific vector representation. Categorical features (like suit structure) can be one-hot encoded.  
**Clustering Algorithm:** K-Means clustering will be the primary algorithm used.

* **Distance Metric:** Euclidean distance (L2 norm) for numerical feature vectors. For more complex features like EHS histograms (if used), Earth Mover's Distance (EMD) could be considered, as it's effective for comparing distributions. However, EMD is computationally more expensive than L2 for k-means.  
* **Initialization:** K-Means++ initialization will be used to improve centroid selection and convergence speed.  
* **Determining k (Number of Buckets):**  
  * The Elbow Method (plotting Within-Cluster Sum of Squares vs. k).  
  * Silhouette Analysis.  
  * The primary constraint will be VRAM: k will be the largest value that keeps the estimated VRAM usage for MCCFR training below 11 GB. This involves estimating the number of information sets resulting from k board buckets combined with other state variables (positions, action sequences, stack depths).

**Experiment Design for Selecting k:**

1. Generate all possible canonical flops (^{52}C\_3 / \\text{isomorphisms} \= 1755 unique flops, often simplified to fewer strategic groups like the 184 used by some authors, or even fewer like the "single-broadway-dry" texture example ). For turns and rivers, a representative sample will be used due to the much larger number of possibilities.  
2. For each board in the sample, compute its feature vector.  
3. Run K-Means for a range of k values for flop, turn, and river separately.  
   * Target flop buckets (k\_{flop}): \\le 1000 (e.g., try 100, 200, 500, 1000).  
   * Target turn buckets (k\_{turn}): \\sim 5000 (e.g., try 1000, 2500, 5000).  
   * Target river buckets (k\_{river}): \\sim 15000 (e.g., try 5000, 10000, 15000). These target numbers are based on typical abstraction sizes in poker AI research, adjusted for short-stack NLH.  
4. For each k, estimate the peak VRAM required by PokerRL's SD-CFR. A simplified formula for VRAM estimation considers parameters for the neural network and activations: VRAM\_{total} \\approx VRAM\_{params} \+ VRAM\_{activations} \+ VRAM\_{gradients} \+ VRAM\_{optimizer\\\_states} \+ VRAM\_{buffers} VRAM\_{params} \= \\text{Num\_Parameters} \\times \\text{Bytes\_per\_Parameter} VRAM\_{activations} \\approx \\text{Batch\_Size} \\times \\text{Max\_Hidden\_Layer\_Size} \\times \\text{Bytes\_per\_Activation} (simplified for feedforward). The number of input features to the neural network will depend on the total number of abstract states (buckets for cards, actions, stack sizes, etc.). The size of the abstract state space, particularly the number of board buckets (k\_{flop}, k\_{turn}, k\_{river}), directly influences the input layer size and, consequently, the total number of parameters and activations.  
5. Select the largest k\_{flop}, k\_{turn}, k\_{river} values that keep estimated peak VRAM \< 11 GB.

**Dispersion and Exploitability Trade-offs:**

* **Dispersion:** Measured by metrics like average intra-cluster distance or silhouette scores. Higher k generally leads to lower dispersion (more coherent clusters) but increases VRAM.  
* **Exploitability Trade-off:** Coarser abstraction (lower k) saves memory but can lead to higher exploitability because strategically different board states are treated identically. Finer abstraction (higher k) allows for more nuanced strategies but is more computationally expensive. The goal is to find the sweet spot. The impact of abstraction on strategy strength is not always monotonic; sometimes refining an abstraction can paradoxically lead to a weaker strategy if not done carefully, though generally, more detail is better if computationally feasible.

**Table 3.1: Board Abstraction Feature Candidates**

| Feature Category | Specific Feature | Data Type | Quantification Example / Notes | Relevance Citation |
| :---- | :---- | :---- | :---- | :---- |
| Suit Structure | Is Monotone? | Boolean | 1 if yes, 0 if no |  |
|  | Is Two-Tone? | Boolean | 1 if yes, 0 if no |  |
|  | Is Rainbow? | Boolean | 1 if yes, 0 if no |  |
| Pairedness | Is Paired? (any pair) | Boolean | 1 if yes, 0 if no |  |
|  | Number of Pairs | Integer | 0, 1, 2 (for flop/turn with 4/5 cards) |  |
|  | Is Trips? | Boolean | 1 if yes, 0 if no |  |
| Connectivity | Max Straight Length | Integer | e.g., 5 for A K Q J T, 3 for K 8 2 |  |
|  | Num Open-Ended Straight Draw Combos | Integer | Count of 2-card combos on board that make open-enders |  |
| High-Card | Highest Card Rank (2-14) | Integer | Ace \= 14 |  |
|  | Number of Broadway Cards | Integer | Count of A, K, Q, J, T |  |
| Equity Moments | EHS Mean vs Random | Float | Pre-calculated/sampled mean equity |  |
|  | EHS StdDev vs Random | Float | Pre-calculated/sampled equity standard deviation |  |

The selection of k directly impacts the size of the information set space for the MCCFR solver. Fewer buckets mean more game states are mapped to the same abstract state, reducing memory but potentially losing strategic nuance. The 11 GB VRAM target necessitates a careful balance. The features chosen (e.g., simple booleans for pairedness vs. detailed EHS moments) also affect the complexity and discriminative power of the abstraction. Using features like those in ASHE (pairedness, suitedness as probability, connectivity as probability) provides a good starting point.

## **4\. Deep MCCFR Training Protocol**

The Deep Monte Carlo Counterfactual Regret Minimization (MCCFR) training, specifically using the Single Deep CFR (SD-CFR) variant within PokerRL, will be employed to generate strategies for game situations not covered by existing GTO resources or where finer granularity is desired.  
**SD-CFR Hyperparameters:** The PokerRL framework allows configuration of SD-CFR through a TrainingProfile. Key hyperparameters to tune for the RTX 4070 Ti include:

* **Learning Rate (Advantage Networks):** lr\_adv. Start with values common in Deep RL, e.g., 1e-4 to 5e-4. Smaller LRs might be needed for stability with FP16. The Deep CFR paper used Adam optimizer; learning rates are specific to the optimizer chosen.  
* **Batch Size (Advantage Networks):** batch\_size\_adv\_per\_la. Maximize this based on VRAM after accounting for model size and buffers. For a 12GB card, with FP16, try starting with 256 or 512 and adjust. The \_per\_la suffix in PokerRL implies this is per learner actor if distributed training is used, though for a single GPU, it's the effective batch size.  
* **Neural Network Architecture (nn\_type):**  
  * PokerRL offers options like "feedforward" and potentially "recurrent". The diditforlulz273/PokerRL-Omaha fork introduces nn\_type='dense\_residual' (MainPokerModuleFLAT2), described as 2x deeper than the original FLAT but with similar complexity, yielding faster training. This "dense\_residual" option seems promising.  
  * The original Deep CFR paper used a 7-layer network with \~99k parameters. The network structure typically involves separate input branches for cards (processed with embeddings) and betting history, which are then concatenated and fed through further fully connected layers. ReLU or Leaky ReLU activations are common. Leaky ReLU with a negative slope of 0.1 is reported to improve loss decrease speed in the PokerRL-Omaha fork.  
  * Network architecture details (layers, neurons) are often encapsulated within the nn\_type choice in PokerRL, rather than exposed as many individual TrainingProfile parameters. Customization might require modifying PokerRL's neural network module Python files (e.g., AdvantageNetFeedForward.py or similar).  
* **Advantage Memory Buffer Size:** max\_buffer\_size\_adv. Deep CFR used 10^6 to 10^7 samples. Aim for 10^6 to 5 \\times 10^6 samples, balancing VRAM/RAM and sample diversity. The leduc\_example.py in Deep-CFR repo shows 3e6.  
* **Number of Traversals per Iteration:** n\_traversals\_per\_iter. Higher values provide more samples per iteration. Deep CFR used 100-200. The leduc\_example.py uses 1500\. This needs to be balanced with n\_batches\_adv\_training.  
* **Number of Batches for Advantage Training:** n\_batches\_adv\_training. The number of gradient descent steps on the advantage network per iteration. Deep CFR used 500-1000. The leduc\_example.py uses 750\.  
* **FP16 Mixed Precision:** PokerRL itself does not explicitly document built-in FP16 support in its main README. However, PyTorch (which PokerRL uses) supports Automatic Mixed Precision (AMP) via torch.cuda.amp.autocast and torch.cuda.amp.GradScaler. This would need to be integrated into PokerRL's training loop (within LearnerActor or Driver). The diditforlulz273/PokerRL-Omaha fork mentions GPU-CPU combined schemes but not explicitly FP16 in its README. Some HuggingFace TRL examples show torch\_dtype=torch.float16 during model loading. If PokerRL's TrainingProfile doesn't have a direct use\_fp16 flag, modifications to the training worker code will be needed.  
  * **Implementation:**  
    `# In PokerRL's training loop (conceptual)`  
    `# from torch.cuda.amp import autocast, GradScaler # At module import`  
    `# scaler = GradScaler(enabled=t_prof.use_fp16) # In LearnerActor.__init__`

    `# Inside training step:`  
    `# optimizer.zero_grad()`  
    `# with autocast(enabled=t_prof.use_fp16):`  
    `#   predictions = model(inputs)`  
    `#   loss = loss_fn(predictions, targets)`  
    `# scaler.scale(loss).backward()`  
    `# scaler.step(optimizer)`  
    `# scaler.update()`

* **Discounted CFR (DCFR) Hyperparameters:** If using a DCFR variant (which PokerRL might support or could be integrated), hyperparameters like \\alpha, \\beta, \\gamma for discounting regrets and strategies would need tuning. Recent research suggests hyperparameter schedules (HSs) can significantly speed up DCFR convergence. This is an advanced consideration.

**Stopping Criteria (Logical OR):**

1. **Visit-Count Threshold:** Stop when a minimum average number of visits is achieved for a significant fraction of information sets in the game sub-module being trained. This indicates sufficient exploration.  
2. **Exploitability Target:** Stop if estimated exploitability (e.g., via LBR if feasible to compute periodically, or if PokerRL provides an internal exploitability measure for SD-CFR) drops below a target threshold (e.g., \< 50 mbb/hand or \< 2% of pot for the sub-game). The overall profile target is \-1 bb/100 vs oracle, so sub-components should aim for low exploitability.  
3. **Wall Clock Limit:** Stop after 7 days of continuous training on the RTX 4070 Ti. This is a hard constraint.

**Experiment Schedule / Shell Script Template:** Training will be done in segments (e.g., specific preflop scenarios if not covered by charts, then flop play for various preflop lines, then turn, then river). Each segment is a "training cycle."  
`#!/bin/bash`  
`# train_segment.sh`

`# --- Parameters ---`  
`GAME_MODULE="Flop_BTN_vs_BB_SRP_25bb" # Describes the game segment being trained`  
`PREFLOP_RANGES_OOP="path/to/bb_call_vs_btn_rfi_25bb.json"`  
`PREFLOP_RANGES_IP="path/to/btn_rfi_25bb.json"`  
`BOARD_ABSTRACTION_FLOP="path/to/fedor_flop_buckets_k500.joblib"`  
`# Add paths for turn/river abstractions if training those streets`

`OUTPUT_STRATEGY_PATH="output/strategies/${GAME_MODULE}_strategy.json"`  
`LOG_DIR="logs/${GAME_MODULE}"`  
`mkdir -p $LOG_DIR`

`# --- PokerRL TrainingProfile Parameters (passed to a Python script) ---`  
`TRAINING_PROFILE_NAME="FEDOR_${GAME_MODULE}"`  
`NN_TYPE="dense_residual" # Or 'feedforward'`  
`MAX_BUFFER_SIZE_ADV="3000000" # 3e6`  
`N_TRAVERSALS_PER_ITER="1500"`  
`N_BATCHES_ADV_TRAINING="750"`  
`BATCH_SIZE_ADV_PER_LA="512" # Effective batch size for single GPU`  
`LR_ADV="0.0002" # 2e-4`  
`USE_FP16="True"`  
`MAX_TRAIN_TIME_SECONDS=$((7 * 24 * 60 * 60)) # 7 days in seconds`  
`EXPLOITABILITY_TARGET_MBBH="50" # Target mbb/hand`

`# --- PokerRL Game Definition Parameters ---`  
`GAME_NAME="NLH_5MAX_CUSTOM_SEGMENT" # Internal PokerRL game name`  
`EFFECTIVE_STACK_BB_MIN="20" # Example for a 20-30bb segment`  
`EFFECTIVE_STACK_BB_MAX="30"`  
`# Other game_kwargs for PokerRL's game_cls`

`echo "Starting MCCFR training for segment: ${GAME_MODULE}"`  
`echo "Log directory: ${LOG_DIR}"`

`# Activate Conda environment if necessary`  
`# source /opt/conda/bin/activate poker_rl_env`

`# Set OMP_NUM_THREADS=1 if using older PyTorch that has issues with Ray`  
`export OMP_NUM_THREADS=1`

`# --- Run PokerRL Training Script ---`
`# This assumes a main Python script \`run_poker_rl_training.py\` that accepts these as args`
`python run_poker_rl_training.py \\`
    `--training_profile_name "$TRAINING_PROFILE_NAME" \\`
    `--game_name "$GAME_NAME" \\`
    `--game_module_id "$GAME_MODULE" \\`
    `--nn_type "$NN_TYPE" \\`
    `--max_buffer_size_adv "$MAX_BUFFER_SIZE_ADV" \\`
    `--n_traversals_per_iter "$N_TRAVERSALS_PER_ITER" \\`
    `--n_batches_adv_training "$N_BATCHES_ADV_TRAINING" \\`
    `--batch_size_adv_per_la "$BATCH_SIZE_ADV_PER_LA" \\`
    `--lr_adv "$LR_ADV" \\`
    `--use_fp16 "$USE_FP16" \\`
    `--max_train_time_seconds "$MAX_TRAIN_TIME_SECONDS" \\`
    `--exploitability_target_mbbh "$EXPLOITABILITY_TARGET_MBBH" \\`
    `--eff_stack_bb_min "$EFFECTIVE_STACK_BB_MIN" \\`
    `--eff_stack_bb_max "$EFFECTIVE_STACK_BB_MAX" \\`
    `--preflop_ranges_oop "$PREFLOP_RANGES_OOP" \\`
    `--preflop_ranges_ip "$PREFLOP_RANGES_IP" \\`
    `--board_abstraction_flop "$BOARD_ABSTRACTION_FLOP" \\`
    `--output_strategy_path "$OUTPUT_STRATEGY_PATH" \\`
    `--log_dir "$LOG_DIR" \\`
    `# Potentially --num_players 5 for 5-max setup in PokerRL game class`
    `# PokerRL's game_cls might take dicts for bet_sizes, stack_depths etc.`

`echo "Training for segment ${GAME_MODULE} complete or stopped."`  
`echo "Strategy saved to: ${OUTPUT_STRATEGY_PATH}"`

This script template is illustrative. The actual \`run_poker_rl_training.py\` would need to be developed to interface with PokerRL's Driver and TrainingProfile, and to set up the custom game environment based on the segment being trained (e.g., specific starting ranges from preflop charts, specific board abstraction model). The 7-day training limit per cycle necessitates careful selection of game segments; it's unlikely the entire 5-max 2-30bb game can be solved monolithically to high precision. Instead, key strategic situations (e.g., BTN RFI \\-> BB Call \\-> Flop play with X buckets) will be solved.  
The choice of SD-CFR over Deep CFR is motivated by its reported lower approximation error, more efficient training by not requiring an average strategy network, and better empirical performance in poker. This aligns well with the VRAM and time constraints. The use of FP16 is critical for maximizing batch sizes and network depth on the RTX 4070 Ti, potentially offering significant speedups and memory savings.

## **5\. Merge & Quantisation Algorithm**

Once strategies are obtained from public GTO assets and Deep MCCFR/SD-CFR solver runs, they must be merged into a cohesive strategy and then quantised into deterministic rules suitable for an OpenPPL profile.  
**Merging MCCFR Frequencies with Chart Priors:** A hierarchical approach will be used to combine strategies from different sources:

1. **Preflop Strategy:**  
   * **Direct Chart Coverage:** For common preflop situations (e.g., Raise First In (RFI) from Button at 25bb effective stack), if a high-quality, specific GTO chart is available (e.g., from Scribd GTO charts or GTO Wizard free solutions ), its prescribed ranges and frequencies will generally take precedence. This is because these charts are often derived from extensive solver runs with highly refined bet trees for these specific common spots.  
   * **Push/Fold Tables:** For very short stack situations (e.g., \<10-12bb), dedicated push/fold charts (e.g., ConsciousPoker , SnapShove ) will be the primary source for all-in or fold decisions.  
   * **MCCFR Augmentation:** For preflop scenarios not directly or reliably covered by charts (e.g., complex multi-way spots, unusual 3-bet/4-bet lines at specific stack depths within the 2-30bb range, or if chart data is too simplified), the MCCFR-generated strategy will be used. This requires the MCCFR strategy for the specific information set (defined by position, effective stack, action history) to have achieved a HIGH\_PREFLOP\_VISIT\_THRESHOLD (e.g., 10^5 visits) to ensure stability.  
2. **Postflop Strategy:**  
   * Postflop play will predominantly rely on MCCFR-generated strategies. Publicly available, comprehensive postflop GTO solutions for 5-max short-stack NLH across numerous textures and lines are scarce.  
   * The MCCFR strategy for a given postflop information set (defined by street, board bucket ID, positions, effective stack, SPR, prior actions) will be used if its visit count exceeds POSTFLOP\_VISIT\_THRESHOLD (e.g., 10^4 visits).  
3. **Heuristic for Overlap (Advanced):**  
   * In rare cases where a chart prior and a well-converged MCCFR strategy both exist for the exact same narrow context, a decision rule is needed. A simple heuristic is to prefer the MCCFR strategy if its estimated exploitability for that sub-tree is demonstrably lower than what can be inferred for the chart (difficult to quantify for static charts), or if the MCCFR strategy has been trained for a very high number of iterations/visits (e.g., \>10^6 visits) and shows significantly different frequencies, suggesting a more nuanced solution. Given the project constraints, defaulting to MCCFR for postflop and specific chart coverage for preflop is a more practical initial approach.

**Frequency-to-Deterministic Mapping (Quantisation):** The probabilistic outputs (action frequencies) from the chosen strategy source must be converted into deterministic rules for OpenPPL, which uses WHEN random \<= n clauses for mixed strategies. The user query specifies the following quantisation thresholds:

* If an action's frequency f \\ge 0.70 (70%), it is mapped to ALWAYS (i.e., the action is taken unconditionally for that hand in that context, or it's the default action if no other WHEN condition for that hand is met first).  
* If 0.30 \< f \< 0.70 (30% to 70%, exclusive of 70%), it is mapped to WHEN random \<= n, where n \= \\lfloor f \\times 100 \\rfloor.  
* If f \\le 0.30 (30%), the action is mapped to NEVER (i.e., it is omitted from the PPL for that hand in that context, or potentially grouped into a low-frequency "otherwise" block if multiple sub-30% actions exist that sum to a relevant frequency).

**Handling Multiple Mixed Actions:** If a hand in a specific context has multiple actions with frequencies between 30% and 70%, or a mix of ALWAYS and RANDOM\_N, they must be ordered correctly in the PPL. Example: Hand XY in context C: Bet 60%, Call 35%, Fold 5%.

* WHEN hand\_is\_XY AND context\_is\_C AND random \<= 60 Bet Pot FORCE  
* WHEN hand\_is\_XY AND context\_is\_C AND random \<= 95 Call FORCE (60 for Bet \+ 35 for Call)  
* (Fold is implicit if random \> 95, or can be WHEN hand\_is\_XY AND context\_is\_C Fold FORCE as the last rule for this hand/context). The 5% Fold action would typically be omitted due to the \\le 30\\% NEVER rule, unless it's the only remaining action. If Bet was 75%, Call 20%, Fold 5%:  
* WHEN hand\_is\_XY AND context\_is\_C Bet Pot FORCE (Call and Fold are omitted as they are \\le 30\\%).

This quantisation approach simplifies the strategy for PPL implementation. However, it's important to recognize that these hard thresholds (30%/70%) introduce a degree of information loss compared to the original mixed strategy. The impact of this simplification is one reason why the final PPL profile's performance against the MCCFR oracle is a key validation metric; a \-1 bb/100 margin is relatively tight and implies that such quantisation must not significantly degrade EV. The simplification in RangeConverter charts, rounding to the nearest 50% , is another example of such quantisation, highlighting that this is a common practice for practical play.  
The choice of visit-count thresholds (HIGH\_PREFLOP\_VISIT\_THRESHOLD, POSTFLOP\_VISIT\_THRESHOLD) is critical. If set too low, the MCCFR strategies might be noisy and unconverged. If too high, MCCFR might not contribute significantly in areas where chart coverage is sparse but MCCFR exploration is also limited. These thresholds may need empirical tuning based on observed convergence rates during training.  
**Table 5.1: Merge & Quantisation Parameters**

| Parameter Name | Proposed Value(s) | Rationale |
| :---- | :---- | :---- |
| HIGH\_PREFLOP\_VISIT\_THRESHOLD | 10^5 \- 10^6 | Ensures MCCFR preflop strategies are stable before overriding or filling gaps in established GTO charts. Higher confidence needed for preflop. |
| PUSH\_FOLD\_VISIT\_THRESHOLD | 5 \\times 10^4 | Push/fold decisions are often simpler; moderate visit count may suffice if dedicated charts are unavailable. |
| POSTFLOP\_VISIT\_THRESHOLD | 10^4 \- 5 \\times 10^4 | Balances need for converged strategy with the vastness of postflop states. Some infosets will naturally have fewer visits. |
| Quantisation Low Cutoff | 0.30 | Actions with frequency \\le 30\\% are considered infrequent enough to be omitted or grouped, simplifying the PPL. User-specified. |
| Quantisation High Cutoff | 0.70 | Actions with frequency \\ge 70\\% are considered dominant enough to be played always, simplifying the PPL. User-specified. |

The merging process must also carefully consider potential mismatches in game tree assumptions (e.g., slightly different bet sizings used in a public chart versus those in the MCCFR solver). When preflop ranges from charts are used as input to an MCCFR postflop solve, this consistency is better managed.

## **6\. Code Generation & Helper DLL**

This section outlines the blueprint for converting the merged and quantised strategic data into a functional OpenPPL profile (FEDOR.txt, later encrypted to FEDOR.ppl) and specifies the interface for a custom C/C++ helper DLL (FEDOR\_Helpers.dll) to provide dynamic game state information not readily available or efficiently computable within OpenPPL.  
**Schema for PPL Generation:** The core data structure for PPL generation will be rows or records, each representing a specific strategic decision. Each row will contain:

* street: Enum (Preflop, Flop, Turn, River)  
* board\_bucket\_id: Integer (ID from k-means clustering for Flop, Turn, River; 0 for Preflop)  
* hero\_position: Enum (UTG, MP, CO, BTN, SB, BB)  
* num\_players\_remaining: Integer (2-5)  
* effective\_bb\_category: Integer (e.g., 1 for 2-5bb, 2 for 6-10bb,..., 6 for 26-30bb)  
* spr\_category: Integer (e.g., 1 for SPR \<1, 2 for 1≤SPR\<2, etc.)  
* action\_sequence\_hash: Integer/String (A compact representation of the betting actions on the current street leading to this decision point)  
* hero\_hand\_range\_id: String or Integer (e.g., "AA", "KQs", "Preflop\_RFI\_BTN\_Bucket\_5", or a specific hand category ID)  
* action\_to\_take: Enum (Fold, Check, Call, Bet, Raise)  
* bet\_raise\_size\_frac\_pot: Float (e.g., 0.33, 0.5, 1.0, 2.0; 0 if not a bet/raise; \-1 for Jam)  
* play\_type: Enum (ALWAYS, RANDOM\_N, where N is 0-99 for random \<= N)

A Python script will process these rows, grouped by street and then by common conditions (e.g., position, eff\_bb\_cat, spr\_cat, action\_sequence\_hash, board\_bucket\_id), to generate OpenPPL code. OpenPPL's WHEN conditions will be constructed using equality checks against variables provided by the helper DLL and built-in OpenHoldem symbols.  
**PPL Generation Logic (Python Pseudocode Snippet):**  
`def generate_ppl_for_street(street_data, street_name):`  
    `ppl_lines = [f"##f${street_name}##"]`  
    `# Group data by common context first (eff_stack, spr, position, board_bucket, action_sequence)`  
    `# to leverage OpenPPL's open-ended WHEN clauses for efficiency.`  
    `# For example:`  
    `# WHEN dll$eff_bb_cat == 3 AND dll$spr_cat == 2 AND dll$board_bucket_id == 123...`  
    `#   WHEN hand$AA AND dll$action_seq_hash == HASH_X AND random <= 75 BetValue 0.5 FORCE`  
    `#   WHEN hand$KK AND dll$action_seq_hash == HASH_X Call FORCE`  
    `#  ...`  
    `#   WHEN Others Fold FORCE // Default for this specific detailed context`  
    `# WHEN Others Fold FORCE // Default for broader context (e.g. only eff_bb and spr)`  
      
    `# Simplified example for one specific context block:`  
    `current_context_conditions = # e.g., ["dll$eff_bb_cat == 3", "dll$board_bucket_id == 123"]`  
    `if current_context_conditions:`  
        `ppl_lines.append("WHEN " + " AND ".join(current_context_conditions))`

    `# Within this context, iterate through hand-specific rules`  
    `cumulative_random_threshold = 0`  
    `# Sort strategy rows by hand, then by play_type (ALWAYS first, then RANDOM_N ascending)`  
    `for row in sorted_street_data_for_context:`  
        `hand_cond = f"hand${row.hero_hand_range_id}" # Needs mapping for hand categories`  
        `action_str = format_action(row.action_to_take, row.bet_raise_size_frac_pot)`

        `if row.play_type == "ALWAYS":`  
            `ppl_lines.append(f"  WHEN {hand_cond} {action_str} FORCE")`  
        `elif row.play_type.startswith("RANDOM_"):`  
            `# Assumes actions for a given hand are mutually exclusive and probabilities sum to <=100`  
            `# For multiple random actions for the SAME hand, need careful ordering and cumulative random`  
            `# This example assumes one random action or a sequence of them properly ordered.`  
            `rand_val = int(row.play_type.split("_")) # e.g. RANDOM_65 -> 65`  
            `