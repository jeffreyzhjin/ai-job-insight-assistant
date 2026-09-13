from __future__ import annotations

import re
from enum import Enum
from typing import Iterable

from pydantic import BaseModel, Field


class MatchLevel(str, Enum):
    STRONG = "Strong Match"
    PARTIAL = "Partial Match"
    GAP = "Capability Gap"


class PositionOverview(BaseModel):
    company: str
    title: str
    category: str
    summary: str


class RequirementMatch(BaseModel):
    requirement: str
    requirement_type: str
    match_level: MatchLevel
    resume_evidence: str
    gap: str
    recommendation: str


class InterviewQuestion(BaseModel):
    question: str
    question_type: str
    preparation_hint: str


class AnalysisResult(BaseModel):
    position: PositionOverview
    responsibilities: list[str] = Field(default_factory=list)
    required_qualifications: list[str] = Field(default_factory=list)
    preferred_qualifications: list[str] = Field(default_factory=list)
    business_keywords: list[str] = Field(default_factory=list)
    technical_skills: list[str] = Field(default_factory=list)
    matches: list[RequirementMatch] = Field(default_factory=list)
    interview_questions: list[InterviewQuestion] = Field(default_factory=list)
    recommended_actions: list[str] = Field(default_factory=list)
    verification_note: str


ROLE_KEYWORDS: dict[str, tuple[str, ...]] = {
    "Product Management": (
        "产品经理",
        "产品规划",
        "需求分析",
        "用户需求",
        "product manager",
        "product roadmap",
        "prd",
        "prototype",
    ),
    "Product Operations": (
        "产品运营",
        "行业运营",
        "用户运营",
        "活动运营",
        "转化",
        "渗透",
        "留存",
        "kpi",
        "product operations",
        "growth",
        "retention",
    ),
    "Business Analysis": (
        "商业分析",
        "经营分析",
        "业务分析",
        "商业模式",
        "business analysis",
        "business model",
        "market analysis",
        "competitive landscape",
    ),
    "Strategy Analysis": (
        "战略分析",
        "战略规划",
        "行业研究",
        "市场趋势",
        "竞争环境",
        "strategy",
        "industry research",
        "market trend",
    ),
}


CANONICAL_TERMS: dict[str, tuple[str, ...]] = {
    "data analysis": ("数据分析", "数据挖掘", "data analysis", "analytics"),
    "Excel": ("excel", "数据透视表", "vlookup"),
    "Python": ("python", "pandas", "numpy"),
    "SQL": ("sql",),
    "user research": ("用户研究", "用户需求", "问卷", "访谈", "user research"),
    "business analysis": ("商业分析", "经营分析", "业务分析", "business analysis"),
    "industry research": ("行业研究", "行业分析", "市场分析", "industry research"),
    "product thinking": ("产品设计", "产品规划", "需求分析", "prd", "prototype"),
    "operations": ("运营", "活动执行", "活动策划", "增长", "转化", "operations"),
    "KPI": ("kpi", "指标体系", "经营指标", "metrics"),
    "project management": ("项目管理", "项目推进", "统筹", "分工", "协调", "project management"),
    "communication": ("沟通", "协调", "对接", "汇报", "communication"),
    "leadership": ("领导力", "负责人", "带领", "团队管理", "leadership"),
    "AI": ("人工智能", "大模型", "chatgpt", "codex", "ai", "llm"),
    "machine learning": ("机器学习", "xgboost", "shap", "machine learning"),
    "English": ("英语", "cet-4", "cet-6", "english"),
    "bachelor degree": ("本科", "学士", "bachelor"),
}


BUSINESS_KEYWORDS = (
    "industry",
    "market",
    "business model",
    "competition",
    "customer",
    "user",
    "growth",
    "conversion",
    "retention",
    "strategy",
    "risk",
    "行业",
    "市场",
    "商业模式",
    "竞争",
    "客户",
    "用户",
    "增长",
    "转化",
    "留存",
    "战略",
    "风险",
)


TECHNICAL_KEYWORDS = (
    "Python",
    "R",
    "SQL",
    "Excel",
    "Power BI",
    "Tableau",
    "XGBoost",
    "SHAP",
    "ChatGPT",
    "Codex",
    "ArcGIS",
)


EXAMPLE_JD = """行业运营实习生

岗位职责：
1. 扫描行业市场，关注行业前沿动态，分析产业结构、商业模式变化趋势和潜在机会；
2. 分析目标客户特征、客户需求和应用场景，协助形成产品与解决方案建议；
3. 协调销售、产品及外部合作伙伴，推动项目执行与业务目标达成；
4. 协助建立经营指标体系，分析KPI完成情况、业务机会和潜在风险。

岗位要求：
1. 本科及以上学历，对互联网行业和AI应用有兴趣；
2. 具备信息整合、数据分析、逻辑组织和问题解决能力；
3. 熟练使用Excel，具备良好的沟通协作能力；
4. 有Python、SQL、行业研究或产品分析经验者优先。"""


EXAMPLE_RESUME = """教育背景：本科，具备城市规划与公共管理交叉背景。
数据分析：使用Python、pandas、NumPy、R和Excel完成多源数据清洗、统计分析和可视化。
研究经历：独立完成行业资料整理、用户需求分析、467份问卷处理和15,298条设施数据分析。
建模经历：使用XGBoost和SHAP识别关键影响因素并形成差异化建议。
项目管理：担任15人团队第一负责人，负责目标拆解、任务分工、政府与合作方沟通以及成果交付。
AI应用：使用ChatGPT和Codex辅助Python脚本编写、调试和批量数据处理。"""


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip().lower()


def _split_items(text: str) -> list[str]:
    raw_items = re.split(r"[\n\r]+|(?<=[。；;])", text)
    items: list[str] = []
    for raw in raw_items:
        item = re.sub(r"^\s*[\d一二三四五六七八九十]+[.、)）:]?\s*", "", raw).strip(" -•\t。；;")
        if len(item) >= 8 and item not in items:
            items.append(item)
    return items


def _unique_matches(text: str, candidates: Iterable[str]) -> list[str]:
    normalized = _normalize(text)
    found: list[str] = []
    for candidate in candidates:
        if candidate.lower() in normalized and candidate not in found:
            found.append(candidate)
    return found


def classify_role(jd_text: str) -> str:
    normalized = _normalize(jd_text)
    scores = {
        role: sum(normalized.count(keyword.lower()) for keyword in keywords)
        for role, keywords in ROLE_KEYWORDS.items()
    }
    best_role, best_score = max(scores.items(), key=lambda item: item[1])
    return best_role if best_score else "General Business Role"


def _infer_title(items: list[str], category: str) -> str:
    for item in items[:4]:
        if any(token in item.lower() for token in ("实习", "intern", "经理", "分析", "运营")):
            return item[:80]
    return category


def _extract_sections(jd_text: str) -> tuple[list[str], list[str], list[str]]:
    items = _split_items(jd_text)
    responsibilities: list[str] = []
    required: list[str] = []
    preferred: list[str] = []

    responsibility_markers = (
        "负责",
        "分析",
        "协助",
        "推动",
        "协调",
        "建立",
        "扫描",
        "洞察",
        "develop",
        "analyze",
        "coordinate",
        "support",
    )
    requirement_markers = (
        "要求",
        "学历",
        "具备",
        "熟练",
        "能力",
        "experience",
        "degree",
        "proficient",
        "required",
    )
    preferred_markers = ("优先", "加分", "preferred", "plus")

    for item in items:
        normalized = item.lower()
        if any(marker in normalized for marker in preferred_markers):
            preferred.append(item)
        elif any(marker in normalized for marker in requirement_markers):
            required.append(item)
        elif any(marker in normalized for marker in responsibility_markers):
            responsibilities.append(item)

    if not responsibilities:
        responsibilities = items[:4]
    if not required:
        required = items[4:8] or items[:3]

    return responsibilities[:8], required[:8], preferred[:6]


def _canonical_terms(text: str) -> set[str]:
    normalized = _normalize(text)
    return {
        canonical
        for canonical, variants in CANONICAL_TERMS.items()
        if any(variant.lower() in normalized for variant in variants)
    }


def _best_resume_evidence(requirement: str, resume_text: str) -> tuple[str, int, set[str]]:
    requirement_terms = _canonical_terms(requirement)
    requirement_words = set(re.findall(r"[a-zA-Z]{3,}", requirement.lower()))
    best_sentence = ""
    best_score = 0
    best_terms: set[str] = set()

    for sentence in _split_items(resume_text):
        sentence_terms = _canonical_terms(sentence)
        shared_terms = requirement_terms & sentence_terms
        sentence_words = set(re.findall(r"[a-zA-Z]{3,}", sentence.lower()))
        shared_words = requirement_words & sentence_words
        score = min(100, len(shared_terms) * 38 + len(shared_words) * 7)
        if score > best_score:
            best_sentence = sentence
            best_score = score
            best_terms = shared_terms

    return best_sentence, best_score, best_terms


def _recommendation(requirement: str, level: MatchLevel, shared_terms: set[str]) -> str:
    if level == MatchLevel.STRONG:
        return "Quantify the result and prepare a concise STAR example for interviews."
    if level == MatchLevel.PARTIAL:
        focus = ", ".join(sorted(shared_terms)) if shared_terms else "the related experience"
        return f"Strengthen {focus} with a clearer action, metric, and business outcome."
    if "sql" in requirement.lower():
        return "Complete a small SQL analysis project and add query results to the portfolio."
    if "excel" in requirement.lower():
        return "Add a business dashboard demonstrating formulas, pivot tables, and KPI analysis."
    return "Build a small portfolio case that provides direct, verifiable evidence for this requirement."


def _build_matches(requirements: list[str], resume_text: str) -> list[RequirementMatch]:
    if not resume_text.strip():
        return []

    matches: list[RequirementMatch] = []
    for requirement in requirements:
        evidence, score, shared_terms = _best_resume_evidence(requirement, resume_text)
        if score >= 70:
            level = MatchLevel.STRONG
        elif score >= 35:
            level = MatchLevel.PARTIAL
        else:
            level = MatchLevel.GAP
            evidence = "No direct evidence found in the provided resume."

        gap = (
            "No material gap identified in the provided text."
            if level == MatchLevel.STRONG
            else "The evidence is related but does not fully demonstrate this requirement."
            if level == MatchLevel.PARTIAL
            else "Direct evidence is missing from the provided resume."
        )
        matches.append(
            RequirementMatch(
                requirement=requirement,
                requirement_type="Required or preferred qualification",
                match_level=level,
                resume_evidence=evidence,
                gap=gap,
                recommendation=_recommendation(requirement, level, shared_terms),
            )
        )
    return matches


def _interview_questions(category: str, responsibilities: list[str]) -> list[InterviewQuestion]:
    questions = [
        InterviewQuestion(
            question="Tell me about a time you used data to identify a problem and recommend an action.",
            question_type="Behavioral",
            preparation_hint="Use STAR and quantify the data volume, your action, and the final outcome.",
        ),
        InterviewQuestion(
            question="How would you evaluate whether a new product or operation strategy is working?",
            question_type="Business Case",
            preparation_hint="Define the objective, north-star metric, leading indicators, segments, and risks.",
        ),
        InterviewQuestion(
            question="How do you verify an AI-generated analysis before using it in a decision?",
            question_type="AI Product",
            preparation_hint="Discuss evidence tracing, structured output, test cases, human review, and privacy.",
        ),
    ]
    if responsibilities:
        questions.append(
            InterviewQuestion(
                question=f"How would you approach this responsibility: {responsibilities[0]}",
                question_type=f"{category} Deep Dive",
                preparation_hint="Break the task into objective, information, analysis, stakeholders, execution, and measurement.",
            )
        )
    return questions


def analyze_locally(jd_text: str, resume_text: str = "") -> AnalysisResult:
    items = _split_items(jd_text)
    category = classify_role(jd_text)
    responsibilities, required, preferred = _extract_sections(jd_text)
    requirements = required + preferred
    matches = _build_matches(requirements, resume_text)

    actions: list[str] = []
    if not resume_text.strip():
        actions.append("Add resume content to generate evidence-based matching and gap analysis.")
    else:
        gaps = [match for match in matches if match.match_level == MatchLevel.GAP]
        partials = [match for match in matches if match.match_level == MatchLevel.PARTIAL]
        if gaps:
            actions.append(f"Prioritize direct evidence for {len(gaps)} identified capability gap(s).")
        if partials:
            actions.append(f"Add metrics and outcomes to strengthen {len(partials)} partial match(es).")
        if not gaps and not partials:
            actions.append("Prepare interview stories that quantify scope, actions, and business outcomes.")
    actions.extend(
        [
            "Verify every extracted requirement against the original job description.",
            "Tailor resume wording without inventing experience.",
        ]
    )

    return AnalysisResult(
        position=PositionOverview(
            company="Not explicitly identified",
            title=_infer_title(items, category),
            category=category,
            summary=f"The role is primarily classified as {category} based on the supplied description.",
        ),
        responsibilities=responsibilities,
        required_qualifications=required,
        preferred_qualifications=preferred,
        business_keywords=_unique_matches(jd_text, BUSINESS_KEYWORDS),
        technical_skills=_unique_matches(jd_text, TECHNICAL_KEYWORDS),
        matches=matches,
        interview_questions=_interview_questions(category, responsibilities),
        recommended_actions=actions,
        verification_note=(
            "Local demo mode uses transparent keyword and evidence-matching rules. "
            "Results are directional and should be checked against the source text."
        ),
    )


def result_to_markdown(result: AnalysisResult) -> str:
    lines = [
        "# AI Job Insight Report",
        "",
        f"**Role category:** {result.position.category}",
        f"**Position:** {result.position.title}",
        "",
        result.position.summary,
        "",
        "## Core Responsibilities",
        *[f"- {item}" for item in result.responsibilities],
        "",
        "## Required Qualifications",
        *[f"- {item}" for item in result.required_qualifications],
        "",
        "## Preferred Qualifications",
        *[f"- {item}" for item in result.preferred_qualifications],
        "",
        "## Resume Evidence Mapping",
    ]
    if result.matches:
        for match in result.matches:
            lines.extend(
                [
                    f"### {match.match_level.value}: {match.requirement}",
                    f"- **Evidence:** {match.resume_evidence}",
                    f"- **Gap:** {match.gap}",
                    f"- **Action:** {match.recommendation}",
                ]
            )
    else:
        lines.append("- Resume content was not provided.")

    lines.extend(["", "## Interview Preparation"])
    for question in result.interview_questions:
        lines.extend(
            [
                f"- **{question.question_type}:** {question.question}",
                f"  - Preparation: {question.preparation_hint}",
            ]
        )

    lines.extend(
        [
            "",
            "## Recommended Actions",
            *[f"- {item}" for item in result.recommended_actions],
            "",
            f"> Verification note: {result.verification_note}",
        ]
    )
    return "\n".join(lines)
