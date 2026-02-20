#Nodos del pipeline en LangGraph

import json
from uuid import UUID, uuid4

from langchain_openai import ChatOpenAI 

from app.config import settings
from app.domain.models import ChartAnalysis, ChartInsightItem, ExecutiveReport, ResearchContext

from app.infraestructure.graphs.prompts import *

from app.infraestructure.graphs.state import PipelineState

llm = ChatOpenAI(
    model=getattr(settings, "LLM_MODEL", "openai/gpt-4o-mini"),
    api_key=settings.OPENAI_API_KEY,
    base_url=getattr(settings, "LLM_BASE_URL", "https://openrouter.ai/api/v1"),
    temperature=0.3,
)

def validate_context_node(state: PipelineState) -> PipelineState:
    #Valida que el contexto del estudio sea suficiente
    study = state["study"]
    ctx = study.context
    
    prompt = VALIDATE_CONTEXT.format(
        profile = ctx.profile,
        background = ctx.background,
        business_question = ctx.business_question,
        study_type = ctx.study_type,
        sample = ctx.sample or "No especificado",
        significance_threshold = ctx.significance_threshold or "No especificado",
    )

    response = llm.invoke(prompt)

    text = response.content.strip().upper()

    if "INVALID" in text:
        return {
            **state,
            "status":"failed",
            "error": "contexto insuficiente para el análisis"
        }
    return {
        **state, "status":"validating"
    }

def classify_charts_node(state: PipelineState) -> PipelineState:
    #Clasifica cada gráfica 
    charts = state["charts"]
    context_summary = f"{state['context'].profile} - {state['context'].business_question}"

    for chart in charts: 
        prompt = CLASSIFY_CHART.format(
            context_summary = context_summary,
            filename = chart.original_filename,
        )
        response = llm.invoke(prompt)
        chart.chart_type = response.content.strip().lower()[:50]
    
    return {**state, "charts": charts, "status":"classifying"}

def analyze_charts_node(state: PipelineState) -> PipelineState:
    #Analiza cada gráfica y genera el ChartAnalysis
    charts = state["charts"]
    ctx = state["context"]
    analyses : list[ChartAnalysis] = []

    for chart in charts:
        chart_info = f"Archivo: {chart.original_filename}, tipo: {chart.chart_type or 'unknown'}"

        prompt = ANALYZE_CHART.format(
            profile = ctx.profile,
            business_question = ctx.business_question,
            study_type = ctx.study_type,
            chart_info = chart_info,
        )

        response = llm.invoke(prompt)
        text = response.content.strip()
        if "´´´" in text:
            text = text.split("")[1]
            if text.strip().lower().startswith("json"):
                text = text.strip()[4:]        
        try:
            data = json.loads(text)
        except json.JSONDecodeError:
            data = {
                "explanation": text[:500],
                "hypotheses": [],
                "business_impact": "",
            }
        
        analysis = ChartAnalysis(
            id = uuid4(),
            chart_id = chart.id,
            study_id = UUID(state["study_id"]),
            explanation = data.get("explanation", ""),
            hypotheses = data.get("hypotheses", []),
            business_impact = data.get("business_impact"),
            created_at= __import__("datetime").datetime.utcnow(),
        )
        analyses.append(analysis)
    
    return {**state, "chart_analyses": analyses, "status":"analyzing"}

def generate_hypotheses_node(state: PipelineState) -> PipelineState:
    #Consolida hipótesis de todas las gráficas
    analyses = state["chart_analyses"]
    ctx = state["context"]

    hypotheses_text = "\n".join(
        f"Gráfica {i+1}: " + ", ".join(a.hypotheses) for i, a in enumerate(analyses)
    )

    prompt = GENERATE_HYPOTHESES.format(
        hypotheses_per_chart = hypotheses_text,
        business_question = ctx.business_question
    )

    response = llm.invoke(prompt)
    text = response.content.strip()
    if "" in text:
        text = text.split("")[1]
        if text.strip().lower().startswith("json"):
            text = text.strip()[4:]
    try:
        data = json.loads(text)
        hypotheses = data.get("hypotheses", [])
    except json.JSONDecodeError:
        hypotheses = [h for a in analyses for h in a.hypotheses][:10]
    
    return {**state, "hypotheses": hypotheses, "status":"synthesizing"}

def synthesize_findings_node(state: PipelineState) -> PipelineState:
    #Convierte las hipótesis en hallazgos clave
    hypotheses = state["hypotheses"]
    prompt = SYNTHESIZE_FINDINGS.format(hypotheses = "\n".join(hypotheses))
    response = llm.invoke(prompt)
    text = response.content.strip()

    if "" in text:
        text = text.split("")[1]
        if text.strip().lower().startswith("json"):
            text = text.strip()[4:]
    try:
        data = json.loads(text)
        key_findings = data.get("key_findings", [])
    except json.JSONDecodeError:
        key_findings = hypotheses[:5]
    
    return {**state, "key_findings": key_findings}

def executive_summary_node(state: PipelineState) -> PipelineState:
    #Genera el resumen ejecutivo
    key_findings = state["key_findings"]
    ctx = state["context"]

    prompt = EXECUTIVE_SUMMARY.format(
        key_findings = "\n".join(key_findings),
        profile = ctx.profile,
        business_question = ctx.business_question,
    )

    response = llm.invoke(prompt)
    executive_summary = response.content.strip()

    return {**state, "executive_summary": executive_summary}

def recommendations_node(state: PipelineState) -> PipelineState:
    #Genera recomendaciones y estrategias
    key_findings = state["key_findings"]
    executive_summary = state["executive_summary"][:500]

    prompt = RECOMMENDATIONS.format(
        key_findings = "\n".join(key_findings),
        executive_summary = executive_summary,
    )
    response = llm.invoke(prompt)
    text = response.content.strip()
    if text.startswith("json"):
        if "json" in text.lower():
            text = text.split("\n", 1)[-1]
    try:
        data = json.loads(text)
        recommendations = data.get("recommendations", [])
        strategies = data.get("strategies", [])
    except json.JSONDecodeError:
        recommendations = key_findings[:3]
        strategies = []

    return {
        **state,
        "recommendations": recommendations,
        "strategies": strategies,
        "status":"completed",
    }

