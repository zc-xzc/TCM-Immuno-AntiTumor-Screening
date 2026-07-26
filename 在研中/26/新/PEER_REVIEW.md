# Peer Review: TCM Multi-Dimensional Data Analysis Drug Screening Operation Manual

**Document:** 中药多维数据分析筛选免疫激活抗肿瘤药物全流程可落地操作手册
**Version:** 2.0
**Date of Review:** 2026-03-04
**Reviewer Role:** External Expert Peer Reviewer (Computational Pharmacology / TCM Systems Biology)
**Document Length:** ~74 pages, 9 modules, LaTeX source (~3,037 lines)

---

## Executive Summary

This manual is a well-structured, operationally detailed standard operating procedure (SOP) guide for conducting TCM drug screening research targeting nasopharyngeal carcinoma (NPC) with dual endpoints of direct anti-tumor activity and immune activation. It demonstrates commendable ambition in bridging computational (network pharmacology, molecular docking, multi-omics) and experimental (CCK-8, ELISA, qRT-PCR, Western Blot) methodologies within a single cohesive workflow. The document's principal strengths are its granular, step-by-step instructions and its consistent quality-control (QC) framework embedded at every module boundary. However, several methodological concerns — particularly around TCGA/NPC data limitations, the use of contaminated cell lines, SwissTargetPrediction as sole target predictor, and the absence of in vivo validation — warrant attention before this manual is used as a definitive scientific reference. The document scores **7.5 / 10** overall.

---

## 1. Scientific Rigor

### 1.1 PICO Framework and Research Design (Module 1)

The PICO framework is applied correctly at lines 415–421. The dual-endpoint design (anti-tumor IC50 ≤ 50 μmol/L AND immune activation ≥ 20% increase, p < 0.05) is scientifically appropriate and differentiates this approach from conventional single-endpoint TCM screening. However, the 50 μmol/L IC50 threshold is too permissive for clinical relevance. The manual itself correctly notes (lines 487–489) that cisplatin's IC50 in CNE1 is ~2–8 μmol/L; a cut-off ten times higher than the positive control is not a meaningful filter. The advisory warning is good, but the threshold in the formal endpoint definition (line 478) should be tightened or the rationale for the permissive value stated explicitly.

**Issue (line 478):** The primary endpoint threshold of IC50 ≤ 50 μmol/L stands in tension with the advisory note that cisplatin achieves ~2–8 μmol/L in the same cell line. Consider replacing the absolute threshold with a relative criterion (e.g., IC50 ≤ 2× the cisplatin IC50 measured in the same experimental batch).

### 1.2 ADME Filtering Thresholds (Module 2)

The OB ≥ 30% and DL ≥ 0.18 thresholds (lines 471, 798–799) are correctly attributed to Ru et al. 2014 (TCMSP). The manual's tip box (lines 815–816) correctly explains the origin of these values. One scientific concern is that these thresholds were derived from the TCMSP database's internal computational models, not from experimentally measured pharmacokinetic data. The manual should note that these are computational proxies and that candidates identified should still be cross-checked against the DCABM-TCM database (a reference already present in the bibliography, `wang2023dcabm`) for blood-absorbed compound confirmation. The reference is cited in the `.bib` file but never called out in the main text of Module 2 — this is an oversight.

**Issue (line 879):** The QC criterion "if < 20 compounds remain, lower DL to 0.15" is presented as a fallback without scientific justification. Arbitrarily relaxing a filtering threshold to increase candidate pool size introduces methodological circularity and should be replaced by a recommendation to expand the TCM herb list rather than relax quality filters.

### 1.3 Target Identification Strategy (Module 3)

The triple-intersection Venn approach (TCM targets ∩ NPC targets ∩ immune targets) is a well-established network pharmacology paradigm. The selection of GeneCards Score ≥ 2.0 (line 951) and DisGeNET Score ≥ 0.1 (line 960) as filters is reasonable and appropriately cited.

**Critical issue (lines 975–982):** The manual correctly and prominently flags that TCGA lacks a standalone NPC category and specifies three GEO substitute datasets (GSE12452, GSE53819, GSE61218). However, the three datasets are of heterogeneous platform types (HG-U133A and Agilent arrays) and are analyzed independently before taking a union of DEGs (line 1053). This approach, while common in the literature, does not account for platform-specific expression biases. The manual should recommend a cross-platform meta-analysis (e.g., using the `metafor` R package or the `inSilicoMerging` Bioconductor package) or at minimum state why a union rather than intersection is preferred here, since a union will inflate the NPC target set and potentially introduce false positives.

**Issue (line 1150):** SwissTargetPrediction is designated as the sole tool for TCM compound-target prediction (the target file `03_tcm_predicted_targets.csv` is expected to originate from SwissTargetPrediction). This is methodologically insufficient. SwissTargetPrediction is a structure-similarity-based tool trained primarily on human drug-target data; it consistently underperforms for polyphenols, terpenoids, and saponins — compound classes that dominate TCM. The manual mentions TCMSP, ETCM, and BATMAN-TCM for compound retrieval (Module 2) but does not instruct the user to also retrieve their precomputed target predictions. The BATMAN-TCM database already provides confidence-scored compound-target predictions that should be the primary source here, supplemented by SwissTargetPrediction only for compounds lacking BATMAN-TCM coverage.

### 1.4 Network Pharmacology Analysis (Module 4)

The hub gene selection using CytoHubba MCC algorithm (lines 1334–1345) is scientifically justified; MCC has been shown superior to other centrality measures for identifying biologically relevant hub nodes in PPI networks (the manual's own note at line 1341 correctly states this). The STRING confidence score threshold of 0.700 (line 1330) is appropriately set at "high confidence."

**Issue (lines 1305–1307):** The core compound selection criterion "Degree ≥ 2 × median AND Betweenness Centrality ≥ 2 × median" is heuristic and arbitrary. A more rigorous approach would use statistical thresholds derived from a null-model network (e.g., random network of the same size and degree distribution) to define significance. At minimum, the manual should cite a precedent paper using this same 2× median criterion, or acknowledge that it is a heuristic.

### 1.5 Molecular Docking (Module 4)

The docking workflow is generally sound. The use of AutoDock Vina 1.2.3 with `exhaustiveness = 32` (double the default of 8; line 1603) is a good practice for improved sampling. The threshold classification (≤ −8.0 kcal/mol = strong binding; lines 1674–1681) is aligned with published norms for fragment-sized compounds.

**Important technical error (line 1567–1573):** The `prepare_receptor4.py` command includes the flag `-e` described as "保留电荷计算" (preserve charge calculation). This is not a valid flag for `prepare_receptor4.py` in AutoDockTools 1.5.7; the correct flag for preserving existing charges is `-C`. Using an invalid flag may silently fail or produce incorrectly protonated receptors. This should be corrected.

**Issue (PDB structure table, lines 1527–1538):** The recommended PDB IDs for certain targets appear outdated or non-optimal:
- TP53 (2OCJ, 2.05 Å) — This structure is of the p53 core domain in an apo form. For small-molecule docking, co-crystal structures such as 3ZME or 6WRH (with ligands at the Y220C hotspot) would be more appropriate.
- VEGFA (3QTK, 2.20 Å) — VEGFA lacks a conventional small-molecule binding pocket; this choice is highly questionable for molecular docking against a TCM small molecule. The manual should either exclude VEGFA from docking targets or provide context about the specific binding site targeted.

### 1.6 Multi-Omics Validation (Module 5)

The scRNA-seq workflow using Seurat follows the standard pipeline and the QC parameters (nFeature_RNA 200–6000, percent.mt < 20; lines 1963–1967) are broadly appropriate, though the upper nFeature_RNA threshold of 6000 may be dataset-dependent and should be adapted after inspecting data distributions.

**Issue (lines 1938–1940):** GSE150825 is proposed as the reference NPC scRNA-seq dataset. The manual should verify this accession exists (GSE150825 at time of writing is a study of COVID-19; the correct NPC scRNA-seq datasets as of 2025 would include GSE150430 [Chen et al., 2020, *Nature Genetics*] or GSE162025). This appears to be an error in the accession number.

**Issue (lines 2039–2040):** The CIBERSORT workflow uses the `immunedeconv` package with `method = "timer"` as a substitute for CIBERSORT. TIMER and CIBERSORT are fundamentally different deconvolution methods (reference-free vs. reference-based); using TIMER as a "replacement" for CIBERSORT without acknowledgment of the methodological difference is misleading. The manual should either use CIBERSORT (via its licensed implementation) or clearly state that TIMER is being used as an alternative with its own limitations.

### 1.7 Wet Lab Protocols (Module 6)

The cell culture and assay SOPs are detailed and practical. The CCK-8 protocol is standard and correctly specifies 6 replicate wells per concentration with ≥ 3 independent biological repeats.

**Issue (lines 2099–2105, CNE1/CNE2 cell identity):** The manual prominently and appropriately flags in the disclaimer (line 288–289) and in the warning box (lines 514–516) that CNE1 and CNE2 have been confirmed to harbor HeLa contamination (ICLAC-00596). This is a critical cell line integrity issue. Continuing to use these cell lines as the primary experimental model while only noting it in a warning box is insufficient for a manual targeting publication-quality science. The manual should more strongly recommend alternative authenticated NPC cell lines (HK-1, 6-10B, C666-1) as the primary model and relegate CNE1/CNE2 to supplementary or comparative use only, given that journals such as *Cancer Research*, *Oncogene*, and *Cell* now require cell line authentication and may reject manuscripts based on ICLAC-listed contaminated cell lines.

**Issue (lines 2265–2268, THP-1 M1 polarization):** The LPS (100 ng/mL) + IFN-γ (20 ng/mL) M1 protocol is standard. However, the manual proposes treating cells with candidate compounds at "IC50/4 concentration to avoid cytotoxicity." This is a reasonable heuristic but should be supplemented by a cell viability check (e.g., CCK-8 on THP-1) at each drug concentration used in the immune activation assay, as IC50 derived from NPC cells does not translate directly to THP-1 toxicity.

### 1.8 Statistical Analysis (Module 7)

The statistical guidance is sound: BH-corrected FDR for bioinformatics (line 2701), Shapiro-Wilk normality testing before ANOVA (line 2537), Tukey HSD for multiple comparisons, and the correct note to analyze ΔCt (not ΔΔCt) for statistical testing of qRT-PCR data (line 2414).

**Minor issue (line 2356):** The manual states β-actin (ACTB) or GAPDH as internal reference genes with Ct values expected at 18–24. While this is a common practice, neither ACTB nor GAPDH is reliably stable across all treatment conditions. The manual should recommend validating reference gene stability using geNorm, NormFinder, or BestKeeper with at least two reference genes, especially since drug treatments may alter housekeeping gene expression.

---

## 2. Completeness

### 2.1 Missing Critical Steps

1. **No normalization QC step for microarray data (Module 3):** The limma workflow (lines 988–1048) begins with `exprs()` directly without first checking whether the array data requires normalization (e.g., RMA for Affymetrix, quantile normalization for Agilent). The boxplot at line 1012–1015 is added for visual inspection, but no branch for "if not normalized, apply normalization" is provided. For a manual targeting graduate students, this is a significant gap.

2. **No inter-dataset batch correction for multi-GEO meta-analysis (Module 3):** As noted above, taking the union of DEGs from three different array platforms without batch correction is a methodological gap.

3. **No Power Analysis / Sample Size Calculation (Module 1/6):** The manual specifies n ≥ 3 biological replicates throughout but never discusses statistical power or how to determine whether 3 replicates is adequate for a given effect size. A basic power analysis guidance (e.g., using G*Power or the `pwr` R package) should be included, particularly for the immune activation experiments where the effect size threshold (20% increase, p < 0.05) is pre-specified.

4. **No in vivo validation guidance:** The manual transitions from cell-line validation directly to paper writing. A comment or supplementary note on xenograft model validation (e.g., BALB/c nude mouse NPC xenograft) or patient-derived organoid (PDO) use would strengthen the scientific completeness and is increasingly expected by reviewers at mid-to-high IF journals.

5. **No protocol for validating molecular docking results by Surface Plasmon Resonance (SPR) or Isothermal Titration Calorimetry (ITC):** The manual acknowledges (line 2765) that docking false-positive rates can reach 30–50%, yet does not provide any binding affinity validation protocol beyond cellular experiments. SPR or microscale thermophoresis (MST) are standard binding validation methods that should be mentioned.

6. **Absence of RNA-seq pipeline:** The manual relies exclusively on Affymetrix/Agilent microarray GEO datasets for transcriptomic analysis. An increasing proportion of NPC GEO datasets are RNA-seq based (e.g., GSE102349 for survival, which the manual itself references). A brief DESeq2 or edgeR workflow for RNA-seq data would improve completeness.

### 2.2 Template Placeholders Not Filled

The document contains numerous `【模板替换位】` (template placeholder) annotations (e.g., lines 417, 425, 462, 742–750) that are intentionally left for the end-user to fill in. While this design choice is explicitly acknowledged, several of these placeholders appear in critical decision points where leaving them blank might cause confusion for a graduate student. The placeholder at line 425 (the standardized scientific question statement) is the most important one to at least demonstrate with a complete filled example.

---

## 3. Reproducibility

Overall, the reproducibility level of this manual is **high relative to the field standard**, which typically provides only brief Methods sections in published papers. The click-level instructions for Cytoscape (lines 1285–1320), the fully executable R and Python code blocks throughout Modules 2–7, and the QC checkboxes at each module boundary are genuine strengths.

### 3.1 Code Quality

The R and Python code is clean, well-commented, and functional. Specific reproducibility concerns:

- **Line 1109:** `read_csv("data/03_immport_immune_genes.txt", col_names = c("gene_symbol", "category"))` — ImmPort gene list files use a different column structure than implied (they have multiple columns including "Gene Name," "Gene Symbol," "Category"). The column names will not map correctly. The manual should show the actual ImmPort file header and the correct column selection.

- **Lines 1823–1824:** `feature_data[, c("ID", "Gene Symbol")]` — The GPL570 annotation file (GSE12452 uses GPL570) does not have a column literally named "Gene Symbol"; it uses `Gene Symbol` as part of a multi-value field. For many probes, multiple gene symbols are concatenated with ` /// `. The code does not handle this ambiguity, which would produce incorrect probe-gene mappings for a significant fraction of rows.

- **Line 2034:** `read_csv("data/GEO/GSE12452_expr_matrix.csv", row.names = 1)` — `read_csv` from `readr` does not support `row.names = 1`; this is a `read.csv` base R syntax. The code would throw an error for a student following it exactly. The correct `readr` approach would be: `column_to_rownames(var = "...ID")`.

- **Lines 2055–2056:** The CIBERSORT code groups samples by `ifelse(grepl("NPC", colnames(expr_matrix)), "NPC", "Normal")`, but the GSE12452 matrix column names are GSM identifiers (e.g., GSM312895), not strings containing "NPC." This grouping logic would incorrectly classify all samples as "Normal."

- **Line 2957:** `url = "http://www.swisstargetprediction.ch/predict.php"` — SwissTargetPrediction uses HTTPS, not HTTP. The API endpoint URL format should be verified; the current URL appears to be incorrect for the API.

### 3.2 Software Version Compatibility

- The manual pins R 4.3.3 and Bioconductor 3.18 (lines 351, 625). Seurat (line 2942) has since been updated to v5.x, which has breaking API changes from v4.x; the manual should specify `Seurat >= 4.4.0, < 5.0` or update to Seurat v5 syntax.
- `immunedeconv` (line 2920) requires CIBERSORT source code to be manually installed from cibersort.stanford.edu under an academic license; the installation script in Appendix A (line 2920) lists `immunedeconv` in `BiocManager::install(bioc_packages)`, but `immunedeconv` is a CRAN package that requires external setup. This will fail for students who simply run the script.
- AutoDock Vina 1.2.3 is correctly specified, but the `prepare_receptor4.py` script (line 1567) is part of the legacy MGLTools/ADT suite, not the standalone Vina 1.2.x distribution. Students should be directed to the updated `meeko` Python package or `prepare_receptor` from the ADFR suite for Vina 1.2+ compatibility.

---

## 4. Citations

### 4.1 Strengths

The bibliography (`references.bib`, 22 entries) includes the key foundational references:
- TCMSP: Ru et al. 2014 — correctly cited
- BATMAN-TCM 2.0: Liu et al. 2024 — correctly cited
- AutoDock Vina: both Trott & Olson 2010 (original) and Eberhardt et al. 2021 (1.2.0 version) are present
- STRING: Szklarczyk et al. 2021 — correctly cited
- limma: Ritchie et al. 2015 — correctly cited
- JUPITER-02 trial: Mai et al. 2021 — correctly cited for NPC clinical context

### 4.2 Missing Key References

1. **clusterProfiler** — Used extensively in Module 4 (lines 1354–1411) but never formally cited. The correct citation is: Yu G, Wang LG, Han Y, He QY. clusterProfiler: an R Package for Comparing Biological Themes Among Gene Clusters. *OMICS.* 2012;16(5):284–287.

2. **Seurat** — Used in Module 5 (line 1942) without citation. Cite: Hao Y et al. Integrated analysis of multimodal single-cell data. *Cell.* 2021;184(13):3573–3587.

3. **CytoHubba** — Used in Module 4 (line 1338) for hub gene identification, uncited. Cite: Chin CH et al. cytoHubba: identifying hub objects and sub-networks from complex interactome. *BMC Systems Biology.* 2014;8(Suppl 4):S11.

4. **VennDiagram R package** — Used in Module 3 (line 1141) without citation. Cite: Chen H, Boutros PC. VennDiagram: a package for the generation of highly-customizable Venn and Euler diagrams in R. *BMC Bioinformatics.* 2011;12:35.

5. **GEPIA2** — Referenced in Module 5 (line 1884) without citation. Cite: Tang Z et al. GEPIA2: enhanced gene expression profiling analysis in cancer. *Nucleic Acids Research.* 2019;47(W1):W556–W560.

6. **ICLAC / CNE1/CNE2 contamination** — The warning box (line 515) cites ICLAC-00596 but provides no formal reference for the original characterization of CNE1/CNE2 HeLa contamination. Recommend citing: Lin C et al. Characterization of contamination by HeLa cells in nasopharyngeal carcinoma cell lines. *Int J Oncol.* 2013.

7. **ImmPort** — Used as a primary gene source (line 1059) without citation. Cite: Bhatt DL et al. *Immunology.* 2018 or the original ImmPort publication: Bhatt DL et al. ImmPort, toward repurposing of open access immunological assay data for translational and clinical research. *Scientific Data.* 2018;5:180015.

8. **DisGeNET** — Used in Module 3 (line 955) without citation in the text (though referenced in a generic way). Cite: Piñero J et al. DisGeNET: a comprehensive platform integrating information on human disease-associated genes and variants. *Nucleic Acids Research.* 2017;45(D1):D833–D839.

9. **GeneCards** — Used throughout Module 3 but never formally cited. Cite: Stelzer G et al. The GeneCards Suite: From Gene Data Mining to Disease Genome Sequence Analyses. *Current Protocols in Bioinformatics.* 2016;54:1.30.1–1.30.33.

10. **DCABM-TCM** — Present in `references.bib` (`wang2023dcabm`) but never cited in the main text despite being directly relevant to Module 2 activity.

### 4.3 Citation Format Issues

- Line 112 in `references.bib`: The PMID for `fan2021npc_methylation` is listed as `PMC7778547` in the `pmid` field, which is a PMC accession, not a PMID. Similarly, `jiang2019cck8_comparison` (line 124) and `zhang2024npc_hub` (line 219) have PMC IDs in the PMID field. These should be corrected.
- The `zhang2024npc_hub` entry (lines 214–221) has the journal year listed as 2025 but the entry key is `zhang2024npc_hub`. The `pages` field contains a PMC ID rather than page numbers, suggesting the article may not yet have definitive publication details at time of writing.

---

## 5. Technical Accuracy

### 5.1 Database URLs

| Database | URL in Manual | Assessment |
|---|---|---|
| TCMSP | tcmsp-e.com | Correct (though tcmsp-e.com is a mirror; official is tcmsp.ac.cn) |
| ETCM | etcm.alihealth.cn | Correct |
| BATMAN-TCM | bionet.ncpsb.org.cn/batman-tcm | Correct |
| TCMID | bidd.nus.edu.sg/tcmid | Correct |
| HIT 2.0 | hit2.badd-cadd.cn | Correct |
| ImmPort | immport.org | Correct |
| TIMER 2.0 | timer.cistrome.org | Correct |
| GEPIA2 | gepia2.cancer-pku.cn | Correct |
| SwissTargetPrediction | swisstargetprediction.ch | Uses http:// in API code (line 2957); should be https:// |

### 5.2 Software and Version Accuracy

| Software | Version in Manual | Assessment |
|---|---|---|
| Cytoscape | 3.10.1 | Current as of early 2026 — correct |
| AutoDock Vina | 1.2.3 | Correct (1.2.3 is the current release) |
| R | 4.3.3 | Correct (4.3.3 "Angel Food Cake" is stable) |
| RDKit | 2023.09.1 | Slightly dated (2024.03.x is current as of 2025) but functional |
| PyMOL | 2.5 | Open-source 2.5 or Incentive 3.x — version exists but clarification between open-source and commercial versions would help |
| GraphPad Prism | 9.0 | Correct, though 10.x is available; 9.0 syntax is compatible |
| Bioconductor | 3.18 | Correct for R 4.3.x |
| RStudio | 2024.04 | Correct (Posit RStudio 2024.04) |
| FlowJo | 10.9 | Correct |
| Seurat | Not explicitly versioned | Should specify v4.4.0 vs v5.x due to API changes |

### 5.3 Parameter and Threshold Accuracy

- **STRING score ≥ 0.700:** Correctly categorized as "high confidence" per STRING documentation.
- **limma FDR correction using BH:** Correct; BH is standard and is the default in `topTable`.
- **exhaustiveness = 32:** Appropriate upgrade from default 8 for screening; accepted practice.
- **PDB 5J89 for PD-L1:** Valid choice — 1.50 Å resolution co-crystal with BMS-202 inhibitor at the dimer interface. Coordinates in the config file (center_x = 15.024, center_y = 5.176, center_z = 22.831; lines 1593–1595) appear to correspond to the BMS-202 binding site. While plausible, these coordinates should be provided with a note that users must independently verify them against the actual PDB structure in PyMOL, as coordinate systems depend on how the file was downloaded and oriented.
- **OD260/280 target 1.8–2.1 for RNA (line 2333):** Correct.
- **qPCR internal control Ct range 18–24 (line 2356):** Correct for typical cell line total RNA.

---

## 6. Strengths

**Strength 1: Unprecedented Operational Granularity for Graduate-Level Audiences**
The manual breaks every computational and experimental procedure down to the individual click, command, and pipette step. This level of detail — specifying exact software menu paths (e.g., "File → Import → Network from File," line 1289), exact centrifuge parameters (300 × g, 5 min, line 2115), and exact catalog numbers for reagents (CCK-8: Dojindo CK04, line 2178; IFN-γ ELISA: Invitrogen BMS228, line 2292) — is rarely found in published literature and substantially reduces the gap between a written protocol and a successfully executed experiment. This is the document's defining virtue.

**Strength 2: Integrated, Consistent Quality Control Framework**
The placement of a dedicated QC checkpoint box (qcbox) at the end of every module, with specific quantitative pass/fail criteria (e.g., R² ≥ 0.95 for dose-response curves; STR authentication within passage 5; Gene ID conversion ≥ 90%), is methodologically mature. This QC architecture mimics GLP/GMP practices adapted for academic research and will meaningfully improve reproducibility for users of this manual.

**Strength 3: Dual-Endpoint Scientific Design for Immuno-Oncology**
The explicit dual-endpoint framework (anti-tumor cytotoxicity AND immune activation) is scientifically forward-looking and aligned with the contemporary understanding that effective cancer therapeutics, including TCM-derived compounds, should modulate the tumor immune microenvironment. Incorporating THP-1 M1 polarization, Jurkat T-cell IL-2 secretion, and CIBERSORT immune deconvolution as co-primary endpoints goes well beyond standard TCM network pharmacology papers.

**Strength 4: Proactive Risk Management and Caveat Communication**
The manual's warning boxes (warningbox) demonstrate intellectual honesty unusual for a prescriptive SOP: the TCMSP SMILES error rate (2–5%, line 2741), the molecular docking false-positive rate (30–50%, line 2765), the CNE1/CNE2 HeLa contamination (lines 514–516), and the absence of independent NPC TCGA data (lines 975–982) are all explicitly flagged rather than glossed over. The disclaimer about AI-generated content (lines 1721–1743) is commendably specific about verification requirements.

**Strength 5: Complete Research Output Lifecycle Coverage (Module 8)**
The inclusion of Module 8 (paper writing, patent application, and grant writing) within the same document as the experimental SOP is unusual and genuinely valuable. The IMRaD section table (lines 2558–2576), target journal recommendations with 2024 impact factors (lines 2580–2596), and the NSFC grant writing framework (lines 2623–2641) provide actionable academic career support that transforms this from a technical manual into a comprehensive research capacity-building tool.

---

## 7. Recommendations

**Recommendation 1: Replace or Supplement CNE1/CNE2 with an Authenticated NPC Cell Line as Primary Model**
Given the ICLAC-confirmed HeLa contamination of CNE1 and CNE2, the manual should formally designate C666-1, HK-1, or 6-10B as the primary experimental cell line(s) and reposition CNE1/CNE2 as a historical comparator. The protocol in Module 6 should be duplicated (or adapted with note differences) for C666-1, which is the most widely used EBV-positive NPC cell line and accepted by major journals. Keeping CNE1/CNE2 as the sole primary model risks manuscript rejection at target journals (Journal of Ethnopharmacology IF ~5.4, Biomedicine & Pharmacotherapy IF ~7.2) that have adopted ICLAC policies.

**Recommendation 2: Replace SwissTargetPrediction as Sole Target Predictor with a Multi-Database Approach**
Module 3 should instruct users to obtain compound-target predictions from three sources and take a confidence-weighted union: (a) BATMAN-TCM 2.0 (already used for compound retrieval in Module 2 — its precomputed target predictions should be downloaded simultaneously); (b) SwissTargetPrediction for compounds not covered by BATMAN-TCM; and (c) HERB database (herb.ac.cn, already listed in Table 1) for its integrated target predictions. This three-source approach is now the field standard for TCM target prediction and would substantially improve the quality and coverage of the compound-target network.

**Recommendation 3: Add Microarray Normalization QC and Cross-Platform Batch Correction to Module 3**
Before executing the limma differential analysis, the manual should include a step to: (a) verify that the downloaded GEO expression matrix is already normalized (common for GSEMatrix = TRUE downloads from non-single-channel arrays) or apply RMA/quantile normalization as needed; and (b) if combining data from multiple GEO datasets with different platforms, apply batch effect correction using `ComBat` (from the `sva` Bioconductor package) or perform a proper meta-analysis. Example code block should be added after line 1048.

**Recommendation 4: Correct Multiple Code Bugs Before Distribution**
The following code errors (detailed in Section 3.1) should be corrected to prevent student confusion:
- Line 2034: Replace `read_csv(..., row.names = 1)` with correct `readr` syntax.
- Lines 2043–2045: Fix CIBERSORT sample grouping logic (currently groups by column name substring, which will fail for GSM IDs).
- Line 2957: Change `http://` to `https://` in SwissTargetPrediction API URL.
- Lines 1823–1824: Add code to handle multi-gene probe annotations in GPL570 (split `///` delimited fields).
- Lines 1567–1573: Correct the `-e` flag in `prepare_receptor4.py` to the valid receptor preparation syntax.

**Recommendation 5: Add Missing Key Citations for All Software Tools Used**
At minimum, add formal in-text citations for: clusterProfiler (used in Module 4, lines 1354+), Seurat (Module 5, line 1942), CytoHubba (Module 4, line 1338), GEPIA2 (Module 5, line 1884), VennDiagram R package (Module 3, line 1141), ImmPort (Module 3, line 1059), GeneCards (Module 3, line 945), and DisGeNET (Module 3, line 955). Also integrate the DCABM-TCM reference (`wang2023dcabm`) that is already in the bibliography but is never cited in the main text.

---

## 8. Minor/Editorial Issues

1. **Line 625, Bioconductor version:** Bioconductor is listed as version 3.18, which corresponds to R 4.3.x — consistent with the specified R 4.3.3. However, the appendix package installation script (line 2908) uses `BiocManager::install(version = "3.18")`, which will fail on systems running a newer R version without a warning. Add a note to check the correct Bioconductor version using `BiocManager::version()`.

2. **Line 2244, FlowJo model:** "Dean-Jett-Fox or Watson (polynomial) model" — both names are slightly off. The correct names in FlowJo 10.9 are "Dean-Jett-Fox" (correct) and "Watson (Pragmatic)" model. Minor but should be corrected for students trying to locate these options in the software.

3. **Lines 2582–2595, Journal impact factors:** Impact factors listed as "2024" values include Frontiers in Pharmacology at ~5.6. The 2024 JCR IF for Frontiers in Pharmacology was 4.4, following a downward revision. These values should be verified and a note added that IF values change annually.

4. **Line 2879, bibliography style:** `\bibliographystyle{unsrtnat}` is used. For SCI submission, numbered or author-year styles depend on the journal. The manual should note that the bibliography style must be changed to match the target journal's requirements before submission.

5. **Line 288, ChP 2025:** The Chinese Pharmacopoeia 2025 edition is referenced throughout. As of the document date (2026-03-04), the 2025 edition should be officially available. This is appropriate and up-to-date.

6. **Line 2592, Chinese journal:** The Chinese journal "中国中药杂志" is listed without an ISSN or DOI format guidance. For completeness, the manual should include its Peking University PKU Core classification or CSCD database status.

---

## 9. Overall Rating

| Dimension | Score (1–10) | Notes |
|---|---|---|
| Scientific Rigor | 7 | Strong framework; docking errors, CNE1/2 concerns, TCGA/NPC data gaps |
| Completeness | 7 | Excellent experimental coverage; missing normalization, power analysis, in vivo |
| Reproducibility | 7.5 | Click-level detail is excellent; several code bugs would trip up students |
| Citations | 6.5 | Core tools cited; 8+ missing software citations; some bib metadata errors |
| Technical Accuracy | 8 | Largely accurate; AutoDockTools flag error and Seurat versioning are notable |

**Overall Score: 7.5 / 10**

This is a high-quality, operationally mature SOP manual that substantially exceeds the documentation standard typical of published TCM network pharmacology papers. With the recommended corrections — particularly addressing cell line contamination, multi-source target prediction, cross-platform batch correction, code bug fixes, and missing software citations — this document could serve as an excellent reference resource for graduate students and young investigators entering the field of TCM computational pharmacology. The authors are commended for their transparency regarding methodological limitations and their commitment to reproducibility through QC checkboxes and code provision.

---

*Peer review conducted by automated expert analysis. All findings reference specific line numbers in `/app/sandbox/session_20260304_150739_f885c9831e98/writing_outputs/drafts/v1_final.tex` and `/app/sandbox/session_20260304_150739_f885c9831e98/writing_outputs/references/references.bib`.*
