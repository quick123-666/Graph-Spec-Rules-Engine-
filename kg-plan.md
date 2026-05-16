# 最细颗粒度知识图谱规划方案

## 一、现状分析

| 数据对象 | 当前数量 | 问题 |
|----------|----------|------|
| Documents | 66 | 只有文档级别的元信息 |
| Chunks | 436 | 文本片段，没有结构化实体 |
| Topics | 12 | 只有 12 个高层主题 |
| Facts | 714 | 实际是文本片段，不是三元组 |
| Edges | 9 | 主题间关系，很稀疏 |

**核心问题**：数据是"文档分块"，不是"知识图谱"。

---

## 二、最细颗粒度图谱设计

### 2.1 节点类型体系

```
Knowledge Graph Node Types (最细粒度)
│
├── ENTITY (实体) - 可独立存在的事物
│   ├── PERSON (人物)
│   │   ├── 创始人: Michael Truell (Cursor), Evan You (Vue/Vite)
│   │   ├── 贡献者: 具体人名
│   │   └── 用户: 匿名用户
│   │
│   ├── ORGANIZATION (组织)
│   │   ├── COMPANY: Anthropic, Microsoft, Vercel, NousResearch
│   │   ├── OSS_ORG: facebook, microsoft, sindresorhus
│   │   └── COMMUNITY: freeCodeCamp, Vue.js
│   │
│   ├── SOFTWARE (软件实体)
│   │   ├── PROJECT: React, Vue, Vite, LangChain, AutoGPT
│   │   ├── FRAMEWORK: LangChain, LlamaIndex, CrewAI
│   │   ├── TOOL: Cursor, VS Code, GitHub CLI
│   │   ├── LIBRARY: lodash, axios, requests
│   │   └── PLUGIN: ESLint, Prettier
│   │
│   ├── CONCEPT (概念)
│   │   ├── TECH: Transformer, RAG, Embedding, Token
│   │   ├── PATTERN: Singleton, Factory, Observer
│   │   └── DOMAIN: Knowledge Graph, Self-Improving Agent
│   │
│   └── EVENT (事件)
│       ├── RELEASE: v1.0.0, 2024-05-15
│       ├── CONF: React Conf, JSConf
│       └── MILESTONE: GitHub Stars 100k
│
├── ATTRIBUTE (属性) - 描述实体的特征
│   ├── METRIC: stars (数量), size (大小), latency (延迟)
│   ├── PROPERTY: language (Python/JS), license (MIT), platform (Web)
│   └── QUALITY: fast, scalable, secure, easy-to-use
│
├── RELATION (关系) - 连接实体的边（本身就是节点）
│   ├── FOUNDED_BY: (Company) --[FOUNDED_BY]--> (Person)
│   ├── USES: (Project) --[USES]--> (Library)
│   ├── IMPLEMENTS: (Project) --[IMPLEMENTS]--> (Concept)
│   ├── SIMILAR_TO: (Project) --[SIMILAR_TO]--> (Project)
│   ├── DEPENDS_ON: (Project) --[DEPENDS_ON]--> (Project)
│   ├── SUPPORTS: (Project) --[SUPPORTS]--> (Feature)
│   ├── ALTERNATIVE_TO: (Project) --[ALTERNATIVE_TO]--> (Project)
│   └── POWERED_BY: (App) --[POWERED_BY]--> (Tech)
│
└── VALUE (值) - 具体数值
    ├── NUMBER: 150766 (stars), 3.5 (rating)
    ├── VERSION: v1.0.0, 2024.05
    └── TEXT: "MIT License", "Python"
```

### 2.2 边的类型体系

```
Knowledge Graph Edge Types

1. IS_A (继承关系)
   (React) -[IS_A]-> (UI Framework)
   (Vue) -[IS_A]-> (UI Framework)
   (LangChain) -[IS_A]-> (Agent Framework)

2. PART_OF (组成关系)
   (Vue Router) -[PART_OF]-> (Vue.js)
   (npm) -[PART_OF]-> (Node.js)

3. USES / IMPLEMENTS (使用/实现)
   (Cursor) -[USES]-> (VS Code)
   (LangChain) -[USES]-> (OpenAI API)
   (MetaGPT) -[IMPLEMENTS]-> (SOP Pattern)

4. FOUNDED_BY / CREATED_BY (创建关系)
   (Anthropic) -[FOUNDED_BY]-> (Dario Amodei)
   (Vue) -[CREATED_BY]-> (Evan You)

5. DEPENDS_ON / REQUIRES (依赖关系)
   (Next.js) -[DEPENDS_ON]-> (React)
   (LangChain) -[DEPENDS_ON]-> (OpenAI)

6. COMPETES_WITH / ALTERNATIVE_TO (竞争关系)
   (Cursor) -[COMPETES_WITH]-> (GitHub Copilot)
   (Vite) -[ALTERNATIVE_TO]-> (Webpack)

7. SUPPORTS / ENABLES (支持/使能)
   (MCP) -[ENABLES]-> (Tool Calling)
   (GitHub) -[SUPPORTS]-> (CI/CD)

8. HAS_FEATURE / HAS_PROPERTY (特征/属性)
   (Vite) -[HAS_FEATURE]-> (Hot Reload)
   (React) -[HAS_PROPERTY]-> (Virtual DOM)

9. RELATED_TO (一般关联)
   (Self-Improving Agent) -[RELATED_TO]-> (RAG)
   (Knowledge Graph) -[RELATED_TO]-> (Vector DB)
```

### 2.3 最细颗粒度示例

```json
{
  "entities": [
    {
      "id": "entity_001",
      "name": "Cursor",
      "type": "SOFTWARE.PROJECT",
      "aliases": ["Cursor IDE", "getcursor/cursor"],
      "properties": {
        "language": "TypeScript",
        "license": "MIT",
        "github": "getcursor/cursor",
        "stars": 15000,
        "platform": "Electron"
      }
    },
    {
      "id": "entity_002", 
      "name": "Anthropic",
      "type": "ORGANIZATION.COMPANY",
      "aliases": ["Anthropic PBC"],
      "properties": {
        "founded": "2021",
        "headquarters": "San Francisco",
        "founders": ["Dario Amodei", "Daniela Amodei"]
      }
    },
    {
      "id": "entity_003",
      "name": "Michael Truell",
      "type": "PERSON.FOUNDER",
      "properties": {
        "role": "CEO",
        "company": "Cursor"
      }
    }
  ],
  "triples": [
    {"head": "entity_001", "relation": "FOUNDED_BY", "tail": "entity_003"},
    {"head": "entity_002", "relation": "FOUNDED_BY", "tail": "entity_003"},
    {"head": "entity_001", "relation": "USES", "tail": "software:vscode"},
    {"head": "entity_001", "relation": "HAS_FEATURE", "tail": "feature:cmd_k"},
    {"head": "entity_001", "relation": "COMPETES_WITH", "tail": "software:github_copilot"},
    {"head": "entity_002", "relation": "CREATED", "tail": "software:mcp_protocol"},
    {"head": "software:mcp_protocol", "relation": "ENABLES", "tail": "concept:tool_calling"}
  ]
}
```

---

## 三、实现路径

### 阶段1: 实体抽取 (Entity Extraction)

```
输入: Documents / Chunks (436 条文本)
      ↓
NER 工具: spaCy / LLM 抽取
      ↓
输出: 实体列表 (目标: 500+ 实体)
```

**抽取规则**:
- GitHub 项目名 (user/repo 格式)
- 组织/公司名 (驼峰+大写)
- 技术术语 (AI, LLM, RAG, Agent...)
- 人物名 (从 README 中)
- 国家/地区

### 阶段2: 关系抽取 (Relation Extraction)

```
输入: 实体列表 + 原文
      ↓
关系规则 + LLM 推断
      ↓
输出: 三元组列表 (目标: 2000+ 三元组)
```

**关系模式**:
- `X uses Y` → USES
- `X built by Y` → CREATED_BY
- `X is a Y` → IS_A
- `X depends on Y` → DEPENDS_ON
- `X vs Y` → COMPETES_WITH

### 阶段3: 属性填充 (Property Filling)

```
输入: 实体列表
      ↓
GitHub API / Wikipedia 补充
      ↓
输出: 带属性的完整实体
```

---

## 四、目标规模

| 指标 | 当前 | 目标 |
|------|------|------|
| 节点数 | 12 (Topics) | 1000+ |
| 边数 | 9 | 5000+ |
| 实体类型 | 1 (Topic) | 8 |
| 关系类型 | 5 | 20+ |
| 属性覆盖 | 无 | 80%+ |

---

## 五、数据模型设计

### 5.1 新建表结构

```sql
-- 最细粒度实体表
CREATE TABLE kg_entities (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT NOT NULL,           -- PERSON.COMPANY, SOFTWARE.PROJECT, etc.
    aliases TEXT,                  -- JSON数组 ["别名1", "别名2"]
    properties TEXT,               -- JSON对象 {key: value}
    source_doc_id TEXT,
    confidence REAL DEFAULT 1.0,
    created_at TIMESTAMP
);

-- 三元组表 (head, relation, tail)
CREATE TABLE kg_triples (
    id TEXT PRIMARY KEY,
    head_id TEXT NOT NULL,        -- 头实体
    relation TEXT NOT NULL,       -- 关系类型
    tail_id TEXT NOT NULL,        -- 尾实体
    weight REAL DEFAULT 1.0,       -- 置信度
    source TEXT,                  -- 来源
    created_at TIMESTAMP
);

-- 实体类型枚举
CREATE TABLE kg_entity_types (
    category TEXT,                 -- PERSON, ORGANIZATION, SOFTWARE, CONCEPT, EVENT
    subcategory TEXT,              -- COMPANY, PROJECT, FRAMEWORK, etc.
    description TEXT
);

-- 关系类型枚举  
CREATE TABLE kg_relation_types (
    relation TEXT PRIMARY KEY,
    inverse TEXT,                 -- 反向关系 USES → USED_BY
    description TEXT
);
```

### 5.2 关系类型定义

| Relation | Inverse | Description |
|----------|---------|-------------|
| IS_A | HAS_INSTANCE | 继承关系 |
| PART_OF | HAS_PART | 组成关系 |
| USES | USED_BY | 使用关系 |
| FOUNDED_BY | FUNDS | 创建关系 |
| DEPENDS_ON | REQUIRED_BY | 依赖关系 |
| COMPETES_WITH | COMPETES_WITH | 竞争关系 |
| SIMILAR_TO | SIMILAR_TO | 相似关系 |
| SUPPORTS | SUPPORTED_BY | 支持关系 |
| ENABLES | ENABLED_BY | 使能关系 |
| HAS_FEATURE | FEATURE_OF | 特征关系 |
| HAS_PROPERTY | PROPERTY_OF | 属性关系 |
| LOCATED_IN | CONTAINS | 位置关系 |
| CREATED_BY | CREATED | 创建关系 |
| RELATES_TO | RELATES_TO | 一般关联 |

---

## 六、可视化设计

### 6.1 节点视觉分层

```
第一层: 核心实体 (高亮显示)
   - 大节点 (60px+)
   - 亮边框
   - 显示名称
   
第二层: 关联实体 (正常显示)
   - 中节点 (40-60px)
   - 正常边框
   
第三层: 弱相关 (淡化显示)
   - 小节点 (30px)
   - 灰色边框
   - 可折叠
```

### 6.2 边视觉分层

```
强关系 (IS_A, PART_OF)
   - 粗线 (3px)
   - 实线
   - 标签清晰

中关系 (USES, CREATED)
   - 中线 (2px)
   - 带箭头
   
弱关系 (RELATED_TO)
   - 细线 (1px)
   - 虚线
   - 灰色
```

---

## 七、执行计划

### Phase 1: 基础设施 (1小时)
- [ ] 创建 kg_entities 表
- [ ] 创建 kg_triples 表
- [ ] 创建类型枚举表

### Phase 2: 实体抽取 (2小时)
- [ ] 编写 NER 抽取脚本
- [ ] 从 Documents 抽取实体
- [ ] 从 Chunks 抽取实体
- [ ] 去重合并

### Phase 3: 关系抽取 (3小时)
- [ ] 编写关系规则引擎
- [ ] 基于共现推断关系
- [ ] LLM 辅助关系推断
- [ ] 人工校验高置信度

### Phase 4: 属性填充 (1小时)
- [ ] GitHub API 补充项目信息
- [ ] 补充实体描述
- [ ] 链接 external IDs

### Phase 5: 可视化 (2小时)
- [ ] 重建 G6 图谱
- [ ] 支持节点类型筛选
- [ ] 支持关系类型筛选
- [ ] 搜索和跳转

### Phase 6: 集成 (1小时)
- [ ] 与现有 AskDB 集成
- [ ] 支持增量更新
- [ ] 性能优化

---

## 八、工具选型

| 阶段 | 工具 | 理由 |
|------|------|------|
| 实体抽取 | LLM (MiniMax) | 通用性强，成本低 |
| 关系抽取 | LLM + 规则 | 结构化输出 |
| 图数据库 | SQLite (初期) | 简单，集成方便 |
| 可视化 | G6 | 已有，成熟 |
| 实体消歧 | Levenshtein + 向量 | 简单有效 |

---

## 九、预期产出

```
最终知识图谱规模:
├── 实体: 800-1200 个
├── 三元组: 3000-5000 条
├── 实体类型: 8 个大类，30+ 子类
├── 关系类型: 15+ 种
└── 覆盖文档: 66 篇 (100%)
```