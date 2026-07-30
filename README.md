# TCM Immuno-AntiTumor Screening

**Traditional Chinese Medicine Multi-Dimensional Data Analysis for Screening Immunomodulatory Anti-Tumor Active Components**

A systematic research framework integrating in vitro pharmacology screening, LC-MS/MS chemical profiling, and multivariate data analysis to discover and validate immune-activating anti-tumor lead compounds from Traditional Chinese Medicine (TCM).

## Research Background

Cancer immunotherapy has revolutionized oncology, but therapeutic resistance and limited response rates remain challenges. Traditional Chinese Medicine offers a rich reservoir of bioactive compounds with immunomodulatory properties. This project systematically screens 19 candidate TCM herbs for immune-activating anti-tumor activity through a multi-layered experimental pipeline.

## Core Methodology

### Triple In Vitro Screening System

| Level | Model | Purpose |
|-------|-------|---------|
| **Primary** | MC38 murine colon cancer + mouse splenocyte co-culture | Initial immune activation screening |
| **Secondary** | B16-F10 murine melanoma + mouse splenocyte co-culture | Cross-validation in another tumor model |
| **Tertiary** | PMA/Ionomycin-activated Jurkat T cells + HCT116 co-culture | Human-relevant immune activation assessment |

### Activity-Guided Fractionation

1. Crude extraction (water / ethanol)
2. Sequential solvent partitioning: Petroleum ether (PE) → Ethyl acetate (EA) → n-Butanol (n-BuOH) → Aqueous residue
3. Lyophilization and activity re-testing of each fraction
4. UPLC-MS/MS analysis of active fractions
5. PCA / OPLS-DA multivariate modeling
6. VIP score-based discriminant marker identification
7. Database matching for active monomer identification

### Candidate TCM Library (19 herbs)

*Caesalpinia sappan* (Sappanwood), *Taraxacum mongolicum* (Dandelion), *Lonicera japonica* (Honeysuckle), *Houttuynia cordata* (Fish Mint), *Prunella vulgaris* (Selfheal), *Portulaca oleracea* (Purslane), *Magnolia officinalis*, *Rubia cordifolia* (Indian Madder), *Paeonia lactiflora* (Chinese Peony), *Platycodon grandiflorus* (Balloon Flower), *Chelidonium majus* (Greater Celandine), *Zanthoxylum nitidum*, *Lindera aggregata*, *Sanguisorba officinalis* (Burnet), *Vitex trifolia*, *Morus alba* (Mulberry), *Bidens bipinnata* (Spanish Needles), *Morinda citrifolia* (Noni), *Callicarpa nudiflora*.

## Project Structure

```
├── 25-26/                        # Research literature, progress & reports (2025-2026)
│   ├── 2025Q4/                   # Q4 2025 literature, meeting notes
│   ├── 26Q1/                     # Q1 2026 experimental plans & literature
│   ├── 26Q2/                     # Q2 2026 experimental results & data
│   ├── 报告/                     # AI-generated reports (Gemini, Kimi)
│   └── 绘图等/                   # Diagrams and visualizations
│
├── supplement/                   # Knowledge base (10 comprehensive guides)
│   ├── RESOURCES_GUIDE.md        # 40+ database & tool quick reference
│   ├── LITERATURE_REVIEW.md      # TCM immunomodulation literature review
│   ├── COMPOUND_IMMUNO_ACTIVITY.md # 19-herb compound activity database
│   ├── IMMUNE_CHECKPOINT_TCM.md  # PD-1/PD-L1 natural inhibitor research
│   ├── MOLECULAR_DOCKING_PROTOCOL.md # Vina/GNINA docking protocol
│   ├── NETWORK_PHARMACOLOGY_PROTOCOL.md # Network pharmacology pipeline
│   ├── BIOINFORMATICS_PIPELINE.md # PCA/OPLS-DA analysis code
│   ├── TCM_SERUM_PHARMACOCHEMISTRY.md # Serum pharmacochemistry guide
│   ├── IMMUNE_CELL_SIGNALING.md  # Immune cell & pathway reference
│   └── REFERENCES.md             # Core reference collection
│
├── ai中药分析/                   # AI-assisted TCM analysis
│   ├── 中药多维数据分析筛选免疫激活抗肿瘤药物全流程操作手册/
│   │                             # Complete operation manual (v6/v8)
│   ├── 苏木对CNE-2细胞增殖抑制率及IC₅₀测定全流程操作手册/
│   │                             # Caesalpinia sappan IC50 assay SOP
│   ├── 中药入血/                 # TCM serum pharmacochemistry (6 herbs)
│   │   └── session_archive/     
│   │       └── writing_outputs/
│   │           ├── final/        # Chapter1 full manuscript + scripts
│   │           ├── figures/      # Publication-quality diagrams
│   │           ├── PEER_REVIEW.md # Peer review report (A- 88/100)
│   │           └── SUMMARY.md    # Project deliverable summary
│   └── 分类/                     # Classified analysis docs
│
├── LLM/                          # LLM/AI toolkits for drug discovery
│   ├── Biomni/                   # Biomedical LLM reasoning & RAG planning
│   ├── DeepDR/                   # Deep learning drug response prediction
│   └── LLM机器学习深度学习/       # Machine learning & deep learning resources
│
├── 在研中/                       # Ongoing research projects
│   └── 26/
│       ├── science_one/          # NPC immune-activating TCM virtual screening
│       │   └── 鼻咽癌免疫激活抗肿瘤中药活性成分虚拟筛选/
│       │       ├── 重大战略分析报告.md   # Strategic analysis
│       │       ├── 重大需求分析报告.md   # Demand analysis
│       │       ├── 指标先进性分析报告.md # Technical benchmarking
│       │       ├── 前沿问题分析报告.md   # Frontier issues
│       │       └── 出口管制分析报告.md   # Export control assessment
│       └── 新/
│           ├── 0302/             # New project: TCM immune screening
│           └── 0304/             # New project: operation manual v2.0
│
└── 安捷伦液质联用/               # Agilent LC-MS technical docs
    └── 官方手册/                 # Official manuals (Q-TOF)
        (部分目录仅保留本地副本)
```

## Technical Stack

| Domain | Technologies |
|--------|-------------|
| **Cell Biology** | Co-culture assays, flow cytometry, ELISA, Griess assay, Western blot |
| **Analytical Chemistry** | UPLC-MS/MS, PCA, OPLS-DA multivariate analysis |
| **Molecular Biology** | NF-κB pathway (p-p65, IκBα), apoptosis markers (Bax/Bcl-2, Caspase-3) |
| **Computational** | LLM-assisted analysis (Claude, DeepDR, Biomni), Python data processing |
| **AI/Drug Discovery** | DeepDR (drug response), Biomni (biomedical LLM), virtual screening |

## Supplement Knowledge Base

The `supplement/` directory contains 10 systematically organized reference guides covering the full research pipeline:

| File | Focus | Target Audience |
|------|-------|----------------|
| `RESOURCES_GUIDE.md` | 40+ database & tool references with URLs | New researchers |
| `LITERATURE_REVIEW.md` | TCM immune pathways, checkpoint regulation, TIME review | Paper introduction writers |
| `COMPOUND_IMMUNO_ACTIVITY.md` | 19-herb compound activity database (SMILES, IC50) | Experimental design |
| `IMMUNE_CHECKPOINT_TCM.md` | PD-1/PD-L1/CTLA-4 natural compound inhibitors | Target screening |
| `MOLECULAR_DOCKING_PROTOCOL.md` | AutoDock Vina/GNINA full pipeline with code | Computational chemists |
| `NETWORK_PHARMACOLOGY_PROTOCOL.md` | Python network pharmacology with Cytoscape | Bioinfo beginners |
| `BIOINFORMATICS_PIPELINE.md` | PCA/OPLS-DA/VIP analysis in Python & R | LC-MS data analysis |
| `TCM_SERUM_PHARMACOCHEMISTRY.md` | Medicated serum prep & LC-MS methods | In vivo pharmacology |
| `IMMUNE_CELL_SIGNALING.md` | Flow cytometry panel & signaling pathway maps | Wet-lab experimenters |
| `REFERENCES.md` | Core reference collection with BibTeX | Citation verification |

## Recent Progress

- **[2026-04]** Established triple screening system validation
- **[2026-05]** Completed 19-herb library preliminary screening
- **[2026-06]** Active fraction isolation and UPLC-MS/MS profiling in progress
- **[2026-07]** Released supplement knowledge base (10 guides), TCM serum pharmacochemistry chapter, NPC virtual screening reports (5 analyses)
- **[2026-07]** Repository cleanup: removed 32+ redundant images and duplicate files, reducing image count from 116 to 90

## Getting Started

```bash
git clone https://github.com/zc-xzc/TCM-Immuno-AntiTumor-Screening.git
cd TCM-Immuno-AntiTumor-Screening
```

For researchers interested in the experimental protocol, refer to the comprehensive operation manual under `ai中药分析/中药多维数据分析筛选免疫激活抗肿瘤药物全流程操作手册/`.

For a quick overview of available resources, start with `supplement/RESOURCES_GUIDE.md`.

## License

This project is intended for **academic research purposes only**.

## Notes

- This repository has been sanitized for public release — all personal identifiers have been removed.
- Large binary files (.pdf, .pptx, .docx) are excluded from version control via `.gitignore`.
- Third-party code in `LLM/` directories retains its original licenses.
