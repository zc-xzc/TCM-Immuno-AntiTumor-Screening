# 中药多维数据分析筛选免疫激活抗肿瘤药物全流程可落地操作手册
## 交付摘要 / Delivery Summary

**文件版本 / Version:** 2.0
**完成日期 / Date:** 2026-03-04
**输出格式 / Format:** LaTeX to PDF
**总页数 / Pages:** 74 页

---

## 主要交付文件 / Primary Deliverables

| 文件 | 路径 | 说明 |
|------|------|------|
| **最终 PDF** | `final/v1_final.pdf` | 74页完整操作手册 |
| **LaTeX 源文件** | `drafts/v1_final.tex` | 可编辑 LaTeX 源码（3000+ 行） |
| **参考文献库** | `references/references.bib` | 28条实验室验证 BibTeX 条目 |
| **图形摘要** | `figures/graphical_abstract.png` | 9模块全流程摘要图 |
| **同行评审报告** | `PEER_REVIEW.md` | 专家级评审，综合评分 7.5/10 |

## 手册内容结构 / Manual Structure

### 9大核心模块
| 模块 | 标题 | 关键内容 |
|------|------|---------|
| 一 | 研究设计与前期准备 | PICO框架、NPC研究问题定义 |
| 二 | 中药多维数据库构建 | TCMSP/ETCM/BATMAN-TCM检索、ADME筛选 |
| 三 | 双维度靶点集筛选 | GeneCards/DisGeNET/OMIM、GEO差异基因、ImmPort免疫靶点 |
| 四 | 虚拟筛选 | Cytoscape网络分析、STRING PPI、分子对接、多维评分 |
| 五 | 多组学公共数据验证 | GEO差异表达、KM生存、scRNA-seq、CIBERSORT |
| 六 | 湿实验验证全流程 | CNE1/CNE2细胞培养、CCK-8 IC50、流式凋亡、ELISA |
| 七 | 数据分析与可视化 | 统计方法、ggplot2可视化 |
| 八 | 成果输出 | SCI论文、专利申请、NSFC课题申报 |
| 九 | 全流程质控与风险管控 | 52周研究时间轴、5大风险规避预案 |

### 核心实验参数
- ADME筛选: OB >= 30%, DL >= 0.18
- STRING置信度: >= 0.700
- 分子对接强结合: <= -8.0 kcal/mol
- GEO差异基因: FDR < 0.05, |log2FC| >= 1
- CCK-8 IC50拟合: Variable Slope, R2 >= 0.95

### 核心工具文献
- Ru et al. (2014) — TCMSP
- Liu et al. (2024) — BATMAN-TCM 2.0
- Szklarczyk et al. (2021) — STRING
- Trott & Olson (2010) — AutoDock Vina
- Mai et al. (2021) — Toripalimab JUPITER-02

*由 K-Dense Web 研究团队 AI 辅助生成 | Version 2.0 | 2026-03-04*
