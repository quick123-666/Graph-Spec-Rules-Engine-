# Graph-Spec Rules Engine

> 图谱演化可视化 — 追踪知识图谱从探索到实现的全生命周期

## 🎯 项目简介

Graph-Spec Rules Engine 是一个用于**知识图谱演化追踪**的可视化工具。它将技术主题的完整生命周期（探索 → 设计 → 实现）以图谱和时间线的形式呈现，让知识演进过程变得可见、可追溯。

## 📊 核心功能

- **知识图谱可视化** — 基于 AntV G6 的交互式知识网络
- **演化时间线** — Mermaid 驱动的版本演进追踪
- **多主题支持** — 10+ 技术主题的并行追踪
- **三元组关联** — 实体-关系-实体的细粒度知识表示

## 🖥️ 在线演示

- [知识图谱](https://quick123-666.github.io/Graph-Spec-Rules-Engine-/)
- [演化时间线](https://quick123-666.github.io/Graph-Spec-Rules-Engine-/evolution-timeline.html)

## 📁 项目结构

```
Graph-Spec-Rules-Engine-/
├── index.html              # 主知识图谱可视化
├── evolution-timeline.html # 演化时间线
├── data.json               # 图谱数据
├── REPORT.md               # 技术报告
├── kg-plan.md              # 规划方案
└── kg_rules/               # 规则引擎源码
    └── base.py
```

## 🔧 技术栈

| 组件 | 技术 |
|------|------|
| 图谱渲染 | AntV G6 |
| 时间线 | Mermaid |
| 数据格式 | JSON |

## 📈 数据统计

- **10** 技术主题
- **30** 版本（每主题 3 阶段）
- **118** 问题追踪
- **30+** 演化三元组

## 🚀 本地运行

```bash
# 直接用浏览器打开
open index.html

# 或使用任意静态服务器
python -m http.server 8080
```

## 📖 文档

- [技术报告](./REPORT.md) — GraphSpec Rules Engine 的设计与实现
- [规划方案](./kg-plan.md) — 最细颗粒度知识图谱设计

---

Built with [Hermes Agent](https://github.com/NousResearch/hermes-agent)