## **8\. Sprint Schedule**

The development of FEDOR.ppl is structured into eight one-week sprints, each with specific goals, tasks, deliverables, and definitions of done. This agile approach allows for iterative progress and adaptation.  
**Table 8.1: Eight-Week Sprint Road-Map**

| Week | Sprint Goal | Key Questions to Answer | Key Tasks | Deliverables (Artefacts) | Definition-of-Done (DoD) | Minimal CI/Local Build Commands |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| **1** | **Foundations & Preflop Data Acquisition** | What is the full inventory of relevant public GTO assets (preflop focus)? How complex is parsing? Initial PokerRL/OH setup. | 1\. Setup Git repo, Conda env for PokerRL, OpenHoldem dev env. 2\. Finalize Asset Inventory (Sec 1), focusing on preflop charts & push/fold tables. 3\. Develop parsers (Python) for PDF, HTML, text-based GTO charts. 4\. Convert all identified preflop data into standardized CSV/JSON: (context, hand\_range, action, frequency, eff\_stack). | data/raw\_gto\_charts/preflop/, data/parsed\_gto\_data/preflop\_compiled.csv, src/parsing/, README.md (initial project setup). | All targeted preflop assets parsed & standardized. Dev environments functional. Git repo initialized. | python \-m unittest discover src/parsing/tests |
| **2** | **Bet Tree Design & Initial Board Abstraction Features** | Finalize recursive bet-tree logic (max raises, SPR\<1 rule). Define comprehensive feature set for board abstraction. | 1\. Formalize bet-tree generation algorithm (Sec 2), including all bet sizes and recursive raise logic. 2\. Research & define feature vector for board states (suits, pairedness, connectivity, high-card tiers) for flop, turn, river (Sec 3). 3\. Implement Python functions to extract these features from canonical board representations. | docs/bet\_tree\_design.md, src/abstraction/board\_features.py, src/abstraction/tests/test\_board\_features.py. | Bet-tree logic documented. Board feature extraction functions implemented and unit tested. | python \-m unittest src/abstraction/tests/test\_board\_features.py |
| **3** | **Board Abstraction Clustering & VRAM Validation** | What are the optimal k values for flop, turn, river buckets within 11GB VRAM? How good is cluster separation? | 1\. Generate canonical flop list; sample turn/river boards. 2\. Implement K-Means clustering (using scikit-learn) with K-Means++ init. 3\. Run clustering experiments for various k on flop, turn, river using features from Sprint 2\. 4\. Estimate VRAM for SD-CFR with resulting bucket counts and target NN size. Select final k values. 5\. Save k-means models. | data/board\_abstraction\_models/kflop.joblib, kturn.joblib, kriver.joblib. notebooks/board\_abstraction\_analysis.ipynb. Report on k selection and VRAM estimates. | Optimal k values for flop, turn, river selected and models saved. VRAM estimates confirm \<11GB target. | python src/abstraction/run\_clustering.py \--street flop \--k 500 (example) |
| **4** | **PokerRL SD-CFR Setup & Initial Training Cycle (Small Segment)** | Can PokerRL with SD-CFR be configured for a small NLH segment using custom abstractions? FP16 integration. | 1\. Setup PokerRL TrainingProfile for SD-CFR. 2\. Implement custom PokerRL game environment for a small segment of 5-max NLH (e.g., a specific preflop line, flop only, using 10-20 flop buckets). 3\. Integrate FP16 (autocast, GradScaler) into PokerRL training loop if not native. 4\. Run a short (1-2 day) test training cycle on the RTX 4070 Ti. Monitor convergence, VRAM, speed. | src/mccfr\_training/custom\_game\_env.py, src/mccfr\_training/profiles/test\_profile.py, scripts/run\_poker\_rl\_test.sh. Report on test cycle results. | PokerRL training pipeline functional for a small custom segment with abstractions and FP16. Initial performance metrics gathered. | bash scripts/run\_poker\_rl\_test.sh |
| **5** | **Full MCCFR Training Cycle 1 (Key Postflop Segment)** | Can a significant postflop segment converge adequately within 7 days? Hyperparameter tuning. | 1\. Select a key, complex postflop segment (e.g., BTN vs BB SRP, using full flop/turn buckets from Sprint 3). 2\. Refine SD-CFR hyperparameters (LR, batch size, network architecture choice like dense\_residual) based on Sprint 4\. 3\. Launch a full 7-day training cycle for this segment. 4\. Monitor convergence (exploitability if measurable, loss curves), VRAM, GPU util. | data/mccfr\_solver\_outputs/segment1\_strategy.json, logs/segment1\_training.log. Report on training cycle 1\. | First major postflop segment trained for 7 days. Strategy output saved. Convergence metrics documented. | bash scripts/train\_segment.sh \--segment\_config configs/segment1.json |
| **6** | **Strategy Merging, Quantisation & PPL Generation Core** | Develop algorithms for merging chart/solver data and quantising frequencies. Implement core PPL generator. | 1\. Implement merge logic (Sec 5): rules for chart vs. solver precedence, visit count thresholds. 2\. Implement quantisation logic (Sec 5): 70/30 thresholds, handling multiple mixed actions. 3\. Design and implement the Python PPL generator (Sec 6\) to convert (context, hand, action, freq) rows to basic OpenPPL WHEN clauses. Test with preflop data and segment1\_strategy. | src/merging\_quantisation/merge\_tool.py, src/ppl\_generation/ppl\_writer.py. profiles/FEDOR\_preflop\_segment1.txt (sample PPL). | Merge and quantisation algorithms implemented. Core PPL generator creates valid syntax for tested data. | python src/merging\_quantisation/merge\_tool.py..., python src/ppl\_generation/ppl\_writer.py... |
| **7** | **Helper DLL Development & Full PPL Generation** | Implement and test C++ helper DLL. Generate full FEDOR.txt from all available strategies. | 1\. Implement C++ helper DLL (FEDOR\_Helpers.dll) exposing user\_ variables (Sec 6\) for board buckets, eff\_stack\_cat, spr\_cat, action\_hash. 2\. Unit test DLL functions. Compile DLL. 3\. Integrate DLL variable usage into PPL generator. 4\. Run PPL generator on all parsed charts and all trained MCCFR segments to produce FEDOR.txt. 5\. Implement Perl script for .ppl encryption. Encrypt to FEDOR.ppl. | src/cpp\_dll/FedorHelpers.cpp, src/cpp\_dll/FedorHelpers.dll, profiles/FEDOR.txt, profiles/FEDOR.ppl, scripts/encrypt\_ppl.pl. | Helper DLL compiles and provides correct variables. Full FEDOR.txt and FEDOR.ppl generated. | cd src/cpp\_dll && make && cd../.., python make\_fedor.py \--generate\_ppl \--encrypt\_ppl |
| **8** | **Simulation, Validation & Final Packaging** | Validate FEDOR.ppl against performance targets. Document and package project. | 1\. Conduct full Simulation & Validation Plan (Sec 7): Oracle H2H (or strategy matching), positional stats, archetype testing, timing tell analysis. 2\. Analyze results, iterate on PPL/DLL if minor fixes needed. 3\. Finalize make\_fedor.py script. 4\. Complete all documentation (README, section reports). 5\. Package all project artefacts for delivery. | Final FEDOR.ppl, FEDOR/ folder structure populated. Validation report (docs/validation\_report.md). Final README.md. | FEDOR.ppl meets or exceeds \-1bb/100 vs oracle. All validation tests passed. Project fully documented and packaged. | python make\_fedor.py \--all, python run\_validation\_suite.py |

This sprint schedule is ambitious but achievable given the constraints. The critical path items involve successful board abstraction within VRAM limits (Sprint 3\) and achieving meaningful convergence in MCCFR training cycles (Sprint 4-5). Parallel work on data parsing/PPL generation (Sprints 1, 6\) and DLL development (Sprint 7\) can occur alongside these core solver tasks. Continuous, albeit minimal, integration (compiling, unit testing) is vital for catching errors early.

## **9\. Open Questions & Risk Register**

This section outlines unresolved technical questions and potential risks associated with the FEDOR.ppl project. Proactive identification and mitigation are key to successful completion.  
**Table 9.1: Open Questions & Risk Register**

| ID | Type | Description | Potential Impact (Severity/Likelihood) | Proposed Experiment / Mitigation Strategy | Owner | Status |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| QN-01 | Question | Optimal SD-CFR hyperparameters (LR, batch size, network architecture details beyond nn\_type) for 5-max short-stack NLH on RTX 4070 Ti with FP16. | Suboptimal convergence speed or final strategy quality. (High/Medium) | Literature review for similar setups. Small-scale hyperparameter sweeps in early training cycles (Sprint 4). Start with values from Deep CFR paper and PokerRL examples , adjust based on VRAM and stability. | MCCFR Lead | Open |
| RSK-01 | Risk | **VRAM Exhaustion:** Chosen board abstraction buckets (k\_{flop}, k\_{turn}, k\_{river}) \+ NN size \+ batch size exceed 11GB VRAM on RTX 4070 Ti. | Training fails or requires drastically smaller NN/batch, impacting quality/speed. (High/High) | **Mitigation:** Rigorous VRAM estimation in Sprint 3\. Use FP16. Start with conservative k values and NN size, profile memory, and scale up. Prioritize simpler NN architecture if dense\_residual is too large. Reduce batch size as a last resort. Consider techniques like gradient accumulation if batch size becomes too small for stable learning. | Abstraction Lead | Open |
| RSK-02 | Risk | **MCCFR Convergence Time:** SD-CFR may not converge to a sufficiently low exploitability level for complex game segments within the 7-day training cycle per segment. | Resulting strategy is weak. Project timeline overrun if multiple re-trains needed. (High/Medium) | **Mitigation:** Prioritize dense\_residual NN type. Optimize PokerRL for speed (OMP\_NUM\_THREADS=1 ). Use FP16. Focus training on most impactful game segments. Accept slightly higher exploitability for less critical/frequent spots if time-constrained. Explore DCFR with Hyperparameter Schedules if convergence is a major issue and integration is feasible. | MCCFR Lead | Open |
| RSK-03 | Risk | **PPL Quantisation EV Loss:** The 70%/30% quantisation thresholds for ALWAYS/RANDOM\_N/NEVER cause significant EV loss compared to the true mixed strategy from MCCFR. | FEDOR.ppl fails to meet \\ge \-1 bb/100 benchmark against oracle. (Medium/Medium) | **Experiment:** During validation (Sprint 8), if EV loss is high, test alternative quantisation schemes (e.g., more RANDOM\_N bins, or rounding to nearest 10% like some commercial tools). **Mitigation:** Ensure MCCFR strategies are well-converged. The current thresholds are user-specified; if problematic, they can be adjusted, though this adds PPL complexity. | PPL Gen Lead | Open |
| RSK-04 | Risk | **Licence Ambiguity of GTO Assets:** Using data derived from commercial GTO tools (even free snapshots or outputs from custom solves if terms are restrictive) for building FEDOR.ppl, even for offline educational use, might violate terms of service. | Legal issues or inability to share/use the profile as intended. (Low/Medium, given offline/edu context) | **Mitigation:** Prioritize academic sources (Cepheus ), fully open-source GTO charts, or self-generated data. Clearly document sources. If using GTOWizard custom solves, review their ToS for data ownership/usage of *solver outputs*. For "educational purposes," this risk is lower. | Project Lead | Open |
| RSK-05 | Risk | **Helper DLL Detection (if used online):** While specified for offline use, if any component were ever used online, custom DLLs can be a detection vector for poker site security. | Account suspension on poker sites. (Medium/Low \- for this project's scope) | **Mitigation:** Adhere strictly to offline, educational use. If any online application considered in future, DLL would need extreme caution (e.g., non-invasive memory reading only, or different integration). This is largely out of scope for current project. | N/A (Offline) | Resolved (for current scope) |
| RSK-06 | Risk | **PokerRL FP16 Integration Issues:** Difficulties in seamlessly integrating PyTorch AMP (autocast, GradScaler) into the PokerRL training loop if not natively supported or if conflicts arise with PokerRL's existing Ray-based parallelism or older PyTorch version dependencies. | Loss of FP16 benefits (speed, VRAM capacity), jeopardizing RSK-01 and RSK-02. (Medium/Medium) | **Experiment:** Test FP16 integration thoroughly in Sprint 4 on a small segment. **Mitigation:** Refer to PyTorch AMP documentation and examples. If PokerRL's PyTorch version (0.4.1 mentioned in some docs ) is too old for native AMP, an upgrade of PyTorch within the PokerRL environment might be needed, which carries its own compatibility risks. The diditforlulz273/PokerRL-Omaha fork might offer insights if it uses a newer PyTorch. | MCCFR Lead | Open |
| RSK-07 | Risk | **Complexity of Action Sequence Hashing:** Defining a robust and compact hash/ID for previous\_action\_sequence that effectively distinguishes strategic situations without causing excessive PPL rule granularity. | PPL file becomes too large or too complex, or strategically different lines are incorrectly merged. (Medium/Medium) | **Mitigation:** Start with simpler action sequence features (e.g., number of bets, last action type/size). Incrementally add complexity. The DLL should handle this. Analyze frequency of different action sequences to guide hashing strategy. | DLL Lead / PPL Gen Lead | Open |
| RSK-08 | Risk | **Perl Converter for.ppl Encryption:** Legacy tool, potential compatibility or operational issues in a modern environment. | Inability to encrypt the final FEDOR.txt for Shanky bot use. (Low/Low) | **Mitigation:** Test the Perl converter early (e.g., Sprint 6 or 7 with a sample PPL). Ensure Perl environment is correctly set up. If it fails, seek alternative PPL encryption methods or confirm if Shanky can use unencrypted .txt profiles (unlikely for distribution). | PPL Gen Lead | Open |

The single RTX 4070 Ti represents a significant constraint. While 12GB VRAM is decent, modern Deep RL can be memory-hungry. The 7-day training cycle per segment also limits the depth of convergence achievable for any single part of the game tree. This necessitates a modular approach, solving different parts of the game (e.g., specific preflop scenarios leading to different postflop SPRs, then specific flop textures) independently if full-game solves are too slow. This modularity, however, can introduce issues at the seams where different solved components meet, which the merging logic must try to smooth out. The "educational and offline" use context is crucial for mitigating risks associated with using GTO data from various public and semi-public sources.

## **10\. Folder Layout & Rebuild Command**

A well-organized project structure and an automated build process are essential for reproducibility and manageability, particularly in an educational context.  
**Proposed Folder Structure (FEDOR/):**  
`FEDOR/`  
`├── data/`  
`│   ├── raw_gto_charts/             # PDFs, web scrapes, images of GTO charts`  
`│   │   ├── preflop/`  
`│   │   └── push_fold/`  
`│   ├── parsed_gto_data/            # Standardized CSV/JSON from parsing raw_gto_charts`  
`│   │   ├── preflop_rfi.csv`  
`│   │   ├── preflop_vs_rfi.csv`  
`│   │   └── push_fold_sb.csv`  
`│   ├── board_abstraction_models/   # Saved k-means models and feature scalers`  
`│   │   ├── flop_kmeans_k500.joblib`  
`│   │   ├── turn_kmeans_k2500.joblib`  
`│   │   ├── river_kmeans_k10000.joblib`  
`│   │   └── board_feature_scaler.joblib`  
`│   └── mccfr_solver_outputs/       # Raw strategy dumps from PokerRL (JSON/CSV)`  
`│       ├── segment_btn_vs_bb_srp_flop/`  
`│       │   └── strategy_epoch_final.json`  
`│       └──... (other segments)`  
`├── src/`  
`│   ├── parsing/                    # Python scripts to parse raw_gto_charts`  
`│   │   └── parse_gto_wizard_pdf.py`  
`│   ├── abstraction/                # Python scripts for board abstraction`  
`│   │   ├── board_feature_extractor.py`  
`│   │   └── run_board_clustering.py`  
`│   ├── mccfr_training/             # PokerRL TrainingProfile configs, custom game defs`  
`│   │   ├── fedor_game_env.py`  
`│   │   └── training_profiles/`  
`│   │       └── segment_btn_vs_bb_srp_profile.py`  
`│   ├── merging_quantisation/       # Python scripts for merging strategies and quantising frequencies`  
`│   │   └── merge_and_quantise.py`  
`│   ├── ppl_generation/             # Python script to generate.txt PPL from merged data`  
`│   │   └── generate_fedor_ppl.py`  
`│   └── cpp_dll/                    # C++ source for FEDOR_Helpers.dll`  
`│       ├── FedorHelpers.cpp`  
`│       ├── FedorHelpers.h`  
`│       └── Makefile (or build script)`  
`├── profiles/`  
`│   ├── FEDOR.txt                   # Intermediate unencrypted OpenPPL profile`  
`│   └── FEDOR.ppl                   # Final encrypted Shanky profile`  
`├── notebooks/                      # Jupyter notebooks for analysis, visualization, R&D`  
`│   ├── 01_preflop_data_analysis.ipynb`  
`│   └── 02_board_abstraction_eda.ipynb`  
`├── scripts/                        # Utility scripts, CI scripts, training launchers`  
`│   ├── run_mccfr_training_cycle.sh`  
`│   └── encrypt_ppl.pl              # Perl script for PPL encryption`  
`├── make_fedor.py                   # Master Python build script for the entire pipeline`  
`├── requirements.txt                # Python dependencies (e.g., PokerRL, scikit-learn, pandas)`  
`├── Dockerfile                      # Optional: For containerized build/run environment`  
`└── README.md                       # Project README with setup, build, and usage instructions`

**Key Artefacts for Rebuild:**

* **Raw Data:** All original GTO chart files, PDF documents, web page saves.  
* **Parsing Scripts:** Python scripts to convert raw data into a structured format.  
* **Board Abstraction:** Python scripts for feature engineering and k-means clustering; saved k-means model files (.joblib).  
* **MCCFR Training:** PokerRL TrainingProfile configurations, any custom PokerRL game environment Python files, and the final trained neural network weights/strategy files from PokerRL.  
* **Merging & Quantisation Scripts:** Python scripts implementing the logic from Section 5\.  
* **PPL Generation Script:** Python script to convert merged/quantised data into FEDOR.txt.  
* **C++ DLL Source:** All .cpp and .h files for FEDOR\_Helpers.dll.  
* **Build/Encryption Scripts:** make\_fedor.py, encrypt\_ppl.pl, and any Makefiles.

**Master Rebuild Command (make\_fedor.py):** A single Python script, make\_fedor.py, will orchestrate the entire build process. This script will use Python's subprocess module to call other scripts and tools. It should support incremental builds (i.e., only re-running steps whose inputs have changed, if feasible, though a full rebuild is acceptable for simplicity).  
**Signature and Behavior:** python make\_fedor.py \[options\]  
**Options:**

* \--all: (Default) Perform all steps from parsing raw data to generating the final encrypted FEDOR.ppl.  
* \--parse\_gto: Only run the GTO chart parsing stage.  
* \--run\_abstraction: Only run the board abstraction (feature extraction and clustering) stage. Requires parsed GTO data if used for defining game segments.  
* \--train\_mccfr \[--segment \<segment\_name\>\]\[--force\_retrain\]: Run MCCFR training. Can specify a segment or train all defined segments. \--force\_retrain ignores existing solver outputs.  
* \--merge\_strategies: Run the strategy merging and quantisation stage. Requires parsed GTO data and MCCFR outputs.  
* \--generate\_ppl\_txt: Generate the unencrypted FEDOR.txt. Requires merged strategies.  
* \--compile\_dll: Compile FEDOR\_Helpers.dll. Requires C++ source.  
* \--encrypt\_ppl: Encrypt FEDOR.txt to FEDOR.ppl. Requires FEDOR.txt and encrypt\_ppl.pl.  
* \--clean: Remove all generated intermediate files and outputs, leaving only source files and raw data.  
* \--config \<config\_file.json\>: Specify a configuration file for paths, parameters, etc.

**Example make\_fedor.py Structure (Conceptual):**  
`import subprocess`  
`import os`  
`import argparse`

`# Define paths to scripts, data, models, etc. (ideally from a config file)`

`def run_command(command_list):`  
    `print(f"Executing: {' '.join(command_list)}")`  
    `process = subprocess.Popen(command_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE)`  
    `stdout, stderr = process.communicate()`  
    `if process.returncode!= 0:`  
        `print(f"Error running command: {' '.join(command_list)}")`  
        `print(f"STDOUT: {stdout.decode()}")`  
        `print(f"STDERR: {stderr.decode()}")`  
        `raise Exception("Command failed")`  
    `print(stdout.decode())`

`def parse_gto_data():`  
    `print("--- Parsing GTO Charts ---")`  
    `# run_command(["python", "src/parsing/parse_all_charts.py", "--output_dir", "data/parsed_gto_data"])`

`def run_board_abstraction():`  
    `print("--- Running Board Abstraction ---")`  
    `# run_command(["python", "src/abstraction/run_board_clustering.py", "--output_dir", "data/board_abstraction_models"])`

`def train_mccfr_segment(segment_name):`  
    `print(f"--- Training MCCFR Segment: {segment_name} ---")`  
    `# script_path = "scripts/run_mccfr_training_cycle.sh"`  
    `# config_path = f"src/mccfr_training/training_profiles/{segment_name}_profile.py" # Or a JSON/YAML config`  
    `# run_command(["bash", script_path, "--segment_config", config_path]) # Pass relevant args`

`def merge_quantise_strategies():`  
    `print("--- Merging and Quantising Strategies ---")`  
    `# run_command(["python", "src/merging_quantisation/merge_and_quantise.py",...])`

`def generate_ppl_txt():`  
    `print("--- Generating FEDOR.txt ---")`  
    `# run_command(["python", "src/ppl_generation/generate_fedor_ppl.py",...])`

`def compile_dll():`  
    `print("--- Compiling FEDOR_Helpers.dll ---")`  
    `# original_dir = os.getcwd()`  
    `# os.chdir("src/cpp_dll")`  
    `# run_command(["make"]) # Assuming a Makefile exists`  
    `# os.chdir(original_dir)`

`def encrypt_ppl():`  
    `print("--- Encrypting FEDOR.ppl ---")`  
    `# run_command()`

`if __name__ == "__main__":`  
    `parser = argparse.ArgumentParser(description="FEDOR.ppl Build Script")`  
    `# Add arguments as defined above`  
    `#...`  
    `args = parser.parse_args()`

    `if args.all or args.parse_gto:`  
        `parse_gto_data()`  
    `if args.all or args.run_abstraction:`  
        `run_board_abstraction()`  
    `#... and so on for other steps, handling dependencies implicitly by order or explicitly`  
    `# For MCCFR training, might iterate over defined segments`  
    `# if args.all or args.train_mccfr:`  
    `#     for segment in ["segment1", "segment2"]: # Defined elsewhere`  
    `#         train_mccfr_segment(segment)`  
    `#...`  
    `print("Build process finished.")`

This structure ensures that the entire process, from raw data to the final encrypted profile, is automated and reproducible. The make\_fedor.py script serves as the single point of entry for building FEDOR.ppl, which is crucial for verifying the methodology and for any future iterations or modifications. Storing large intermediate files like MCCFR reservoir samples or numerous neural network checkpoints needs careful consideration for disk space; the .gitignore file should be configured to exclude these if they are easily reproducible by the build script. The primary goal is reproducibility of the *final* FEDOR.ppl from the core source code and initial raw data.  
This comprehensive plan addresses all tasks outlined in the user query, providing a clear path toward the development of the FEDOR.ppl profile.