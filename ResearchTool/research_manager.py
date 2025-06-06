# ---------------------------------------------------------------------------
# Description
# ---------------------------------------------------------------------------
"""
Research Manager Module

This module provides the central orchestration class that ties together all agent
components to perform an end-to-end research workflow. It coordinates:

1. PlannerAgent → turns a user query into targeted web-searches
2. SearchAgent  → executes each search and returns concise summaries
3. WriterAgent  → synthesizes the summaries into a long-form markdown report
4. EmailAgent   → sends the finished report via email

The manager streams status updates and the final markdown report to the caller,
which can be piped directly into a UI (e.g., Gradio). All heavy work runs
asynchronously to maximize throughput.
"""

# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------
import asyncio
from agents import Runner, trace, gen_trace_id

from search_agent import get_search_agent
from planner_agent import planner_agent, WebSearchItem, WebSearchPlan
from writer_agent import writer_agent, ReportData
from email_agent import email_agent
from llm_helper import LLM_MODEL_NAME


# ---------------------------------------------------------------------------
# Research Manager Class
# ---------------------------------------------------------------------------
class ResearchManager:
    """Orchestrates the complete research workflow using multiple specialized agents.
    
    This class coordinates the interaction between different agents to perform
    comprehensive research on a given query. It handles the complete pipeline from
    planning searches to sending the final report via email.
    """

    async def run(self, query: str):
        """Execute the complete research process.

        Args:
            query (str): The research question or topic to investigate

        Yields:
            str: Status updates and the final markdown report as they become available
        """
        trace_id = gen_trace_id()  # Generate a unique trace ID for the research process
        with trace("Research trace", trace_id=trace_id):
            # Print the trace link and yield initial status
            print(f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}")
            yield f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}"
            
            # Execute the research pipeline
            print("Starting research...")
            search_plan = await self.plan_searches(query)
            yield "Searches planned, starting to search..."  
            self.search_agent = get_search_agent(LLM_MODEL_NAME.GEMINI)
            search_results = await self.perform_searches(search_plan)
            yield "Searches complete, writing report..."
            
            report = await self.write_report(query, search_results)
            yield "Report written, sending email..."
            
            await self.send_email(report)
            yield "Email sent, research complete"
            yield report.markdown_report

    async def plan_searches(self, query: str) -> WebSearchPlan:
        """Plan the set of searches to perform for the given query.

        Args:
            query (str): The research question to plan searches for

        Returns:
            WebSearchPlan: A structured plan containing multiple search queries
        """
        print("Planning searches...")
        result = await Runner.run(
            planner_agent,
            f"Query: {query}",
        )
        print(f"Will perform {len(result.final_output.searches)} searches")
        return result.final_output_as(WebSearchPlan)

    async def perform_searches(self, search_plan: WebSearchPlan) -> list[str]:
        """Execute all searches from the plan concurrently.

        Args:
            search_plan (WebSearchPlan): The plan containing search queries to execute

        Returns:
            list[str]: List of search result summaries
        """
        print("Searching...")
        num_completed = 0
        tasks = [asyncio.create_task(self.search(item)) for item in search_plan.searches]
        results = []
        
        for task in asyncio.as_completed(tasks):
            result = await task
            if result is not None:
                results.append(result)
            num_completed += 1
            print(f"Searching... {num_completed}/{len(tasks)} completed")
            
        print("Finished searching")
        return results

    async def search(self, item: WebSearchItem) -> str | None:
        """Execute a single search query.

        Args:
            item (WebSearchItem): The search query and its reasoning

        Returns:
            str | None: Search result summary if successful, None if failed
        """
        input = f"Search term: {item.query}\nReason for searching: {item.reason}"
        try:
            result = await Runner.run(
                self.search_agent,
                input,
            )
            return str(result.final_output)
        except Exception:
            return None
    
    async def write_report(self, query: str, search_results: list[str]) -> ReportData:
        """Generate a comprehensive report from search results.

        Args:
            query (str): The original research question
            search_results (list[str]): List of search result summaries

        Returns:
            ReportData: The complete report with summary and follow-up questions
        """
        print("Thinking about report...")
        input = f"Original query: {query}\nSummarized search results: {search_results}"
        result = await Runner.run(
            writer_agent,
            input,
        )
        print("Finished writing report")
        return result.final_output_as(ReportData)
    
    async def send_email(self, report: ReportData) -> None:
        """Send the final report via email.

        Args:
            report (ReportData): The report to be sent

        Returns:
            None
        """
        print("Writing email...")
        result = await Runner.run(
            email_agent,
            report.markdown_report,
        )
        print("Email sent")
        return report