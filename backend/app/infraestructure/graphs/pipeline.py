#Grafo LangGraph para el pipeline cognitivo

from langgraph.graph import END, StateGraph 

from app.infraestructure.graphs.nodes import *

from app.infraestructure.graphs.state import PipelineState

def build_pipeline_graph():
    #Construye el grafo del pipeline
    graph = StateGraph(PipelineState)

    graph.add_node("validate_context", validate_context_node)
    graph.add_node("classify_charts", classify_charts_node)
    graph.add_node("analyze_charts", analyze_charts_node)
    graph.add_node("generate_hypotheses", generate_hypotheses_node)
    graph.add_node("synthesize_findings", synthesize_findings_node)
    graph.add_node("executive_summary", executive_summary_node)
    graph.add_node("recommendations", recommendations_node)

    graph.set_entry_point("validate_context")

    graph.add_coditional_edges(
        "validate_context",
        lambda s: "failed" if s.get("status") == "failed" else "continue",
        {
            "failed": END,
            "continue": "classify_charts",
        },
    )

    graph.add_edge("classify_charts", "analyze_charts")
    graph.add_edge("analyze_charts", "generate_hypotheses")
    graph.add_edge("generate_hypotheses", "synthesize_findings")
    graph.add_edge("synthesize_findings", "executive_summary")
    graph.add_edge("executive_summary", "recommendations")
    graph.add_edge("recommendations", END)

    return graph.compile()
    