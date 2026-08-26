# bespoke-figures · 非模板定制科研图工作流

**Bespoke (non-template) publication-chart workflow for DeepSeek Harness (DSH):**
when no standard chart template fits your data, design and implement a custom
matplotlib chart from scratch — coordinate system, value-to-geometry mapping
(linear / log / broken two-scale), dividers, annotations — then verify the
render visually and deliver reproducible PNG + SVG.

> **定位 / Positioning**:三十多种常见模板图(折线、柱状、热图、箱线…)已有大量现成工具。
> 本 skill **不重复造轮子**,专攻**没有模板可用**的定制图——从数据出发,设计并实现一张
> 标准模板画不了或画不好的图。

## 包含内容 / What's inside

| 路径 | 内容 |
|---|---|
| `SKILL.md` | 核心:**非模板制图六步法** + 通用风格规范 + QA 清单 + 隐私约定 |
| `recipes/broken-radial.md` | 首个完整案例:断轴双刻度径向图(含 **8 条设计理由**) |
| `scripts/chart_broken_radial.py` | 参数化脚本(通用:任意"标签列+系列列(+总计列)"表格) |

## 何时使用 / When to use

- ✅ 数据有特殊诉求:**量级悬殊要断轴双刻度、径向/环形布局、阈值参考体系、多级标注、
  非常规构成图**……模板画不了或画出来失真
- ❌ 普通折线/散点/柱状/热图等模板图 → 用现成工具即可

## 安装 / Install

```bash
# 安装为 DSH skill(以 DSH_HOME 为例,默认为 ~/.dsh)
cp -r bespoke-figures "$DSH_HOME/skills/bespoke-figures"
```

安装后,DSH 会话的 skill 目录中即可见 `bespoke-figures`,按需加载使用。

## 用法 / Usage

**六步法**(详见 SKILL.md):

1. 理解数据与阅读目标(范围 / 零值 / 系列数 → 读者要一眼看出什么)
2. 从零设计骨架:坐标系 → 数值映射(线性 / 对数 / **断轴双刻度**)→ 分区引导线 → 标签系统
3. 落地为参数化脚本(`scripts/chart_<name>.py`,不硬编码数据 / 路径)
4. 渲染后**亲眼看图核查**(完整 / 无遮挡 / 映射正确 / 一致)
5. 交付 PNG + SVG + 脚本(可复现;新需求新文件)
6. 迭代直至确认(可选:文字模型逻辑审计 + 视觉模型渲染目检)

**断轴径向图示例**:

```sh
python3 "${SKILL_DIR}/scripts/chart_broken_radial.py" data.xlsx out_stem "Risk|Quotient|(RQ)"
# -> out_stem.png (200 dpi 预览) + out_stem.svg (矢量,插入论文)
```

## 案例:断轴双刻度径向图 / Worked example

22 类别 × 12 系列、数值跨 4~5 个数量级、一半为 0 → 任何模板堆叠图都会把中小值压成
看不见的细线。解决方案与设计理由(为什么断轴、为什么断点自适应、为什么非堆叠分组柱
等 8 条)记录在 `recipes/broken-radial.md`。

## 风格规范 / Conventions(默认,可覆盖)

- 字体 **Times New Roman**,数学符号 STIX;缺失时警告并回退
- **N+1 高区分度纯色**(各系列 + 总计),按列顺序分配
- 参考阈值(默认 0.1 / 1)仅在轴范围内绘制并写进注记
- 多分区用浅灰虚线引导归组;中心小字标题
- 输出 PNG(200 dpi)+ SVG(路径文字;需改字时出可编辑文字版)
- 投稿可按期刊栏宽(89 / 183 mm)、300–600 dpi 重出

## 依赖 / Dependencies

Python 3.10+;`pandas`、`openpyxl`、`numpy`、`matplotlib`。
建议设置 `MPLCONFIGDIR` 指向可写目录。

## 隐私 / Privacy

本 skill 所有说明与脚本**不含任何用户个人信息**(无姓名、无机器路径、无具体数据值);
数据路径与文案由调用方以参数传入,示例仅用通用占位。

## 支持 / Support

⭐ 如果这个 skill 对你有帮助,欢迎点个 Star,或把它推荐给需要的人。

## 许可 / License

[MIT](LICENSE)
