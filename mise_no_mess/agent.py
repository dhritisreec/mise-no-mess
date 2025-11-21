# mise_no_mess/agent.py
from google.adk.agents.llm_agent import Agent

# For now, a very simple root agent.

root_agent = Agent(
    model="gemini-2.5-flash",
    name="mise_no_mess",
    description="Analyzes Indian restaurant menus to optimize kitchen operations and reduce waste.",
    instruction=(
        "You are Mise No Mess, a kitchen-ops consultant. "
        "You specialize in Indian restaurant menus (tandoor, curry, tawa, biryani, etc.) "
        "and help identify overloaded stations, ingredient bottlenecks, and menu inefficiencies. "
        "When tools are available, use them for parsing menus and running analyses."
    ),
    tools=[],  # we'll add Cloud Run tools later
)
