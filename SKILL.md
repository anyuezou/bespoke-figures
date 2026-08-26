---
name: bespoke-figures
description: >
  非模板定制科研插图工作流:Bespoke (non-template) publication-figure workflow.
  When no standard chart template fits the data, design and implement a custom
  matplotlib figure from scratch — choose the coordinate system,
  value-to-geometry mapping (linear / log / broken two-scale), layout,
  dividers and annotation scheme, build a parameterized script, verify the
  render visually, and deliver PNG + SVG. Ships with the worked example of a
  broken two-scale radial chart. Use when the user needs a NON-standard /
  custom figure (radial or rose layout, broken axis, threshold reference
  circles, bespoke composition) or when standard templates fail to show the
  data; ordinary template charts (line/bar/heatmap...) are out of scope and
  better served by existing tools. 适用于"非标准化/定制/非常规科研图"绘制需求。
metadata:
  version: "1.0.0"
  license: "MIT"
---

# 非模板定制科研图工作流 (bespoke-figures)

**定位:本 skill 不提供"模板图库"——常见三十多种模板图(折线/柱状/热图/箱线…)
已有大量现成工具可画。我们专攻"没有模板可用"的定制图:从数据出发,从零设计、
实现一张标准模板画不了或画不好的图。** 断轴双刻度径向图是本 skill 的第一个完整案例。

## 何时使用 / 何时不用

- ✅ **用**:数据有特殊诉求——量级悬殊需要断轴双刻度、环形/径向布局、阈值参考体系、
  多级标注与分区、非常规构成图……标准模板画不了或画出来失真
- ❌ **不用**:普通折线/散点/柱状/热图等**模板图**——建议直接用现成工具,
  本 skill 不重复造轮子

## 数据契约(定制图的通用输入)

| 列 | 角色 |
|---|---|
| 第 1 列 | 类别标签(点位/时间/样本),行数 = 分区数 |
| 中间列 | 数值系列(非负;允许整列全 0,图例保留、图中不出现) |
| 最后一列(可选) | 总计;列名含 "sum"(不分大小写)才被识别为总计 |

## 非模板制图方法(六步,任何定制图都照此)

1. **理解数据与阅读目标**——列角色、数值范围(数量级差)、零值/缺失、系列数与行数;
   明确"读者要一眼看出什么":排序?热点?超阈值?构成?
2. **从零设计图的骨架**(不是选模板,是设计):
   - **坐标系**:直角 / 极坐标 / 环形 / 其他;角度起始与方向
   - **数值→几何映射**:线性 / 对数 / **断轴双刻度** / 份额切分——**"小值可见"优先考虑**
   - **分区与引导线**:扇区虚线、网格、参考圆/参考线(阈值)
   - **标签系统**:类别标签、刻度值、图例、中心标题、断口/注记
3. **落地为参数化脚本** `scripts/chart_<name>.py`:
   - 数据文件与输出名入参;文案可参数化;**不硬编码用户数据、路径、具体系列名**
   - 色板按列顺序分配;风格遵循下方通用规范
4. **渲染并视觉核查(必做,亲眼看图)**:
   - 完整度:所有标签/系列/图例齐全、顺序正确
   - 无遮挡:标注、标题、刻度互不压盖
   - 正确性:映射与数据一致(抽查数值)、断点/阈值位置正确
   - 一致性:图例颜色与图中一致
5. **交付**:PNG(预览)+ SVG(矢量,`fonttype='path'`)+ 生成脚本(可复现);
   **不覆盖已交付物,新需求新文件名**
6. **迭代**:用户反馈 → 改脚本重渲染 → 再核查,直至确认;
   必要时文字模型做逻辑审计、视觉模型做渲染目检,结论写成报告文件

## 通用风格规范(默认科研论文风,可覆盖)

| 项 | 默认 |
|---|---|
| 字体 | **Times New Roman**;数学符号 STIX;缺失时脚本警告并回退 |
| 配色 | **N+1 高区分度纯色**(各系列 + 总计),按列顺序分配;超过色板数时循环复用并提示 |
| 参考阈值 | 常用 0.1 / 1(如风险商);**仅当阈值在轴范围内才绘制并写进注记** |
| 分隔 | 多分区/多组用**浅灰虚线**引导归组 |
| 输出 | PNG(200 dpi)+ SVG(路径文字);需改字时出 `fonttype='none'` 可编辑版 |
| 尺寸 | 默认约 11×9.5 in;投稿按期刊栏宽(89/183 mm)、300–600 dpi 重出 |

## 案例:断轴双刻度径向图(首个完整案例)

背景:22 类别 × 12 系列,数值跨 4~5 个数量级、一半为 0 → 任何模板堆叠图都让
中小值缩成看不见的细线。**设计理由、脚本用法与 QA 见 `recipes/broken-radial.md`。**

```sh
python3 ${SKILL_DIR}/scripts/chart_broken_radial.py <数据.xlsx> <输出名> ["标题行1|行2|行3"]
```

## 新定制图怎么入库

按六步方法设计实现 → 把**设计理由 + 用法 + 专属 QA**写进 `recipes/<name>.md` →
脚本放 `scripts/chart_<name>.py` → 用真实数据验收、视觉核查通过后成为新案例。

## 依赖

Python 3.10+;`pandas`、`openpyxl`、`numpy`、`matplotlib`;建议 `MPLCONFIGDIR` 指向可写目录。

## 隐私约定

本 skill 所有说明与脚本**不包含任何用户个人信息**(无姓名、无机器路径、无具体数据值);
路径与文案由调用方以参数传入,示例仅用通用占位。
