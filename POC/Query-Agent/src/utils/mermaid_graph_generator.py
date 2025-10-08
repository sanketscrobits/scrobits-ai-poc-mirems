from src.agents.multi_agent_guardrails import workflow

mermaid_text = workflow.get_graph().draw_mermaid()
print(mermaid_text)  # Copy-paste into https://mermaid.live/ for interactive PNG/SVG