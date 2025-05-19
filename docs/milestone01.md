| Week | Sprint Goal | Key Questions to Answer | Key Tasks | Deliverables (Artefacts) | Definition-of-Done (DoD) | Minimal CI/Local Build Commands |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| **1** | **Foundations & Preflop Data Acquisition** | What is the full inventory of relevant public GTO assets (preflop focus)? How complex is parsing? Initial PokerRL/OH setup. | 1\. Setup Git repo, Conda env for PokerRL, OpenHoldem dev env. 2\. Finalize Asset Inventory (Sec 1), focusing on preflop charts & push/fold tables. 3\. Develop parsers (Python) for PDF, HTML, text-based GTO charts. 4\. Convert all identified preflop data into standardized CSV/JSON: (context, hand\_range, action, frequency, eff\_stack). | data/raw\_gto\_charts/preflop/, data/parsed\_gto\_data/preflop\_compiled.csv, src/parsing/, README.md (initial project setup). | All targeted preflop assets parsed & standardized. Dev environments functional. Git repo initialized. | python \-m unittest discover src/parsing/tests |

## Current Progress (Milestone 1)

### Completed ✅
1. Git repository initialized with proper structure
2. Basic Python environment setup with requirements.txt
3. Project directory structure created according to roadmap
4. Parsing framework developed (base classes, PDF, HTML parsers)
5. Unit tests implemented and passing for parsing framework
6. OpenHoldem setup script created (`scripts/setup_openholdem.py`)
7. README.md with project overview and setup instructions

### Incomplete ❌
1. **Asset Inventory Document** - Need to finalize which specific GTO resources to acquire
2. **Actual GTO Chart Collection** - No chart files in `data/raw_gto_charts/preflop/`
3. **Parsed Data Output** - Missing `preflop_compiled.csv`
4. **PokerRL-specific Setup** - Environment needs PokerRL configuration

## Next Steps (Human Tasks vs. AI Assistance)

### Human Tasks
1. **Source GTO Charts**: Find and download actual preflop GTO charts and push/fold tables from sources mentioned in research.md section 1
   - Consider GTO Wizard free snapshots, ConsciousPoker charts, SnapShove, PokerCoaching.com free charts
   - Place downloaded files in `data/raw_gto_charts/preflop/` and `data/raw_gto_charts/push_fold/`
   - Formats: PDF, HTML, screenshots, or text exports

2. **OpenHoldem Installation**: Download and install OpenHoldem from official sources
   - Run `python scripts/setup_openholdem.py --oh-path=<your-openholdem-path>` to configure the environment

3. **PokerRL Setup**: Determine if PokerRL installation is needed for milestone 1 or can be deferred to later milestones

### AI Assistant Tasks
1. **Create Asset Inventory**: Can help draft a formal inventory document of GTO resources based on research.md
   - Will list specific chart types with sources, licensing, and acquisition strategies

2. **Enhance Parsers**: Can extend current parsers for specific GTO chart formats once examples are provided
   - Implement format-specific extraction logic for different chart layouts

3. **Run Parsing Pipeline**: Can assist with scripts to batch process chart files and generate standardized output
   - Will help create `preflop_compiled.csv` once raw data is available

4. **PokerRL Integration**: Can provide code for PokerRL setup if needed for this milestone

Once these steps are completed, we'll have a fully functional foundation for the subsequent milestones in the project.