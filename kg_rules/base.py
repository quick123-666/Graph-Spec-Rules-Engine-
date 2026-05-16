"""
Graph Rule Programming Framework
图谱规则编程框架

核心思想：
- 规则驱动，而非过程驱动
- 模式匹配触发规则
- 向前链式推理直到饱和
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Set, Dict, List, Optional, Callable
from enum import Enum
import hashlib
import json
import re


class EntityType(Enum):
    """实体类型"""
    PERSON = "PERSON"
    ORGANIZATION = "ORGANIZATION" 
    SOFTWARE = "SOFTWARE"
    CONCEPT = "CONCEPT"
    EVENT = "EVENT"
    ATTRIBUTE = "ATTRIBUTE"
    VALUE = "VALUE"
    UNKNOWN = "UNKNOWN"


class RelationType(Enum):
    """关系类型"""
    IS_A = "IS_A"
    PART_OF = "PART_OF"
    USES = "USES"
    USED_BY = "USED_BY"
    FOUNDED_BY = "FOUNDED_BY"
    CREATED_BY = "CREATED_BY"
    DEPENDS_ON = "DEPENDS_ON"
    REQUIRED_BY = "REQUIRED_BY"
    COMPETES_WITH = "COMPETES_WITH"
    SIMILAR_TO = "SIMILAR_TO"
    SUPPORTS = "SUPPORTS"
    ENABLES = "ENABLES"
    HAS_FEATURE = "HAS_FEATURE"
    HAS_PROPERTY = "HAS_PROPERTY"
    RELATED_TO = "RELATED_TO"
    CO_OCCURS_WITH = "CO_OCCURS_WITH"  # 共现关系
    CONTEXT_OF = "CONTEXT_OF"         # 上下文关系


@dataclass
class Entity:
    """实体"""
    id: str
    name: str
    entity_type: EntityType
    aliases: Set[str] = field(default_factory=set)
    properties: Dict = field(default_factory=dict)
    confidence: float = 1.0
    source: str = ""
    
    def matches(self, name: str) -> bool:
        """检查是否匹配某个名称"""
        name_lower = name.lower()
        return (self.name.lower() == name_lower or 
                name_lower in [a.lower() for a in self.aliases])


@dataclass  
class Triple:
    """三元组 (head, relation, tail)"""
    id: str
    head_id: str
    relation: RelationType
    tail_id: str
    weight: float = 1.0
    source: str = ""
    
    def __hash__(self):
        return hash((self.head_id, self.relation.value, self.tail_id))


@dataclass
class GraphState:
    """图谱状态"""
    entities: Dict[str, Entity] = field(default_factory=dict)
    triples: Set[Triple] = field(default_factory=set)
    
    def add_entity(self, entity: Entity) -> bool:
        """添加实体，返回是否新增"""
        if entity.id in self.entities:
            # 合并
            existing = self.entities[entity.id]
            existing.aliases.update(entity.aliases)
            existing.properties.update(entity.properties)
            existing.confidence = max(existing.confidence, entity.confidence)
            return False
        self.entities[entity.id] = entity
        return True
    
    def add_triple(self, triple: Triple) -> bool:
        """添加三元组，返回是否新增"""
        if triple in self.triples:
            return False
        self.triples.add(triple)
        return True
    
    def find_entity(self, name: str) -> Optional[Entity]:
        """按名称查找实体"""
        name_lower = name.lower()
        for e in self.entities.values():
            if e.matches(name):
                return e
        return None
    
    def get_neighbors(self, entity_id: str, relation: Optional[RelationType] = None) -> List[tuple]:
        """获取邻居实体 [(neighbor, relation), ...]"""
        neighbors = []
        for t in self.triples:
            if t.head_id == entity_id:
                if relation is None or t.relation == relation:
                    neighbors.append((t.tail_id, t.relation))
            elif t.tail_id == entity_id:
                if relation is None:
                    neighbors.append((t.head_id, t.relation))
        return neighbors


@dataclass
class RuleContext:
    """规则执行上下文"""
    state: GraphState
    working_memory: List  # 未处理的事实
    trace: List[str] = field(default_factory=list)  # 推理轨迹
    
    def log(self, msg: str):
        self.trace.append(msg)


class GraphRule(ABC):
    """图谱规则基类"""
    
    def __init__(self, name: str, priority: int = 0):
        self.name = name
        self.priority = priority  # 优先级，数字越大越先执行
    
    @abstractmethod
    def condition(self, ctx: RuleContext) -> bool:
        """条件：检查规则是否应该触发"""
        pass
    
    @abstractmethod
    def action(self, ctx: RuleContext) -> None:
        """动作：规则触发后执行的操作"""
        pass
    
    def execute(self, ctx: RuleContext) -> bool:
        """执行规则，返回是否触发"""
        if self.condition(ctx):
            ctx.log(f"🔥 规则触发: {self.name}")
            self.action(ctx)
            return True
        return False
    
    def __lt__(self, other):
        return self.priority > other.priority  # 优先级高的先执行


@dataclass
class Pattern:
    """图模式"""
    entity_type: Optional[EntityType] = None
    name_pattern: Optional[str] = None  # regex
    has_property: Optional[tuple] = None  # (key, value)
    related_to: Optional[tuple] = None  # (entity_id, relation)


class RuleEngine:
    """规则引擎"""
    
    def __init__(self):
        self.rules: List[GraphRule] = []
        self.state = GraphState()
        self.working_memory: List = []
        self.max_iterations = 100
        self.trace_enabled = True
    
    def add_rule(self, rule: GraphRule):
        self.rules.append(rule)
        self.rules.sort()  # 按优先级排序
    
    def add_fact(self, fact: any):
        """添加原始事实到工作内存"""
        self.working_memory.append(fact)
    
    def add_entity(self, entity: Entity):
        self.state.add_entity(entity)
    
    def add_triple(self, triple: Triple):
        self.state.add_triple(triple)
    
    def run(self) -> GraphState:
        """运行规则引擎直到饱和"""
        iteration = 0
        changed = True
        
        while changed and iteration < self.max_iterations:
            changed = False
            iteration += 1
            
            if self.trace_enabled:
                print(f"\n{'='*50}")
                print(f"迭代 {iteration}")
                print(f"{'='*50}")
            
            ctx = RuleContext(
                state=self.state,
                working_memory=self.working_memory,
                trace=[]
            )
            
            for rule in self.rules:
                if rule.execute(ctx):
                    changed = True
            
            if self.trace_enabled:
                print(f"实体数: {len(self.state.entities)}, 三元组数: {len(self.state.triples)}")
        
        return self.state
    
    def get_trace(self) -> str:
        return "\n".join(self.state.entities.get('_trace', []))