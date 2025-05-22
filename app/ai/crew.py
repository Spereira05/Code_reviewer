from app.ai.agents import * 
from app.ai.tasks import quality_task, performance_task, security_task
from crewai import Crew

crew = Crew(
    name = "Code review crew",
    description = "A crew capable of reviewing code and check its quality, its performance and its security", 
    agents = [code_quality_agent, security_agent, performance_agent],
    tasks = [quality_task, performance_task, security_task],
)
