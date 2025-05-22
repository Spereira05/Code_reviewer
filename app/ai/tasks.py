from crewai import Task 
from app.ai.agents import *

def quality_task():
   return Task(
    description=f"Analyze the following {language} code for quality issues. Focus on code structure, readability, maintainability, and adherence to best practices.",
    expected_output="Detailed analysis with specific code quality issues found and recommendations for improvement.",
    agent=code_quality_agent
    )

def performance_task():
    return Task(
    description=f"Analyze the following {language} code for performance optimization opportunities. Look for inefficient algorithms, resource leaks, and optimization potential.",
    expected_output="Detailed performance analysis with bottlenecks identified and optimization recommendations.",
    agent=performance_agent
    )
    
def security_task():
    return Task(
    description=f"Analyze the following {language} code for security vulnerabilities. Look for common security issues like injection flaws, authentication issues, sensitive data exposure, etc.",
    expected_output="Detailed security analysis with vulnerabilities found and recommendations to fix them.",
    agent=security_agent
    )
