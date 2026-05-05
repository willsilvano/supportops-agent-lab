from __future__ import annotations

from typing import Any

from langgraph.graph import END, START, StateGraph

from supportops_agent.agent.nodes import analyze_node, check_access_node, fetch_ticket_node
from supportops_agent.agent.state import AgentState, create_initial_state


def _fetch_ticket(state: AgentState) -> dict[str, Any]:
    return fetch_ticket_node(state)


def _check_access(state: AgentState) -> dict[str, Any]:
    return check_access_node(state)


def _analyze(state: AgentState) -> dict[str, Any]:
    return analyze_node(state)


def compile_supportops_graph() -> Any:
    """Compila o grafo LangGraph para o fluxo SupportOps."""
    graph = StateGraph(AgentState)

    # Adicionar nós
    graph.add_node("fetch_ticket", _fetch_ticket)
    graph.add_node("check_access", _check_access)
    graph.add_node("analyze", _analyze)

    # Definir fluxo: START -> fetch_ticket -> check_access -> analyze -> END
    graph.add_edge(START, "fetch_ticket")
    graph.add_edge("fetch_ticket", "check_access")
    graph.add_edge("check_access", "analyze")
    graph.add_edge("analyze", END)

    return graph.compile()


def run_supportops_flow(user_input: str) -> dict[str, Any]:
    """Executa o fluxo completo do agente via LangGraph."""
    initial_state = create_initial_state(user_input)
    app = compile_supportops_graph()
    result = app.invoke(initial_state)
    return result


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Uso: python -m supportops_agent.agent.graph <ticket_id>")
        print("Exemplo: python -m supportops_agent.agent.graph TCK-4821")
        sys.exit(1)

    ticket_id = sys.argv[1]
    result = run_supportops_flow(f"Analise o ticket {ticket_id}")
    print(result["final_answer"])
