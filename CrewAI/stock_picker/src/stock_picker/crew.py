from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
from pydantic import BaseModel, Field
from typing import List
from crewai.agents.agent_builder.base_agent import BaseAgent
from .tools.push_tool import PushNotificationTool
from crewai.memory import LongTermMemory, ShortTermMemory, EntityMemory
from crewai.memory.storage.rag_storage import RAGStorage
from crewai.memory.storage.ltm_sqlite_storage import LTMSQLiteStorage

class TrendingCompany(BaseModel):
    name: str = Field(description="Company name")
    ticker: str = Field(description="Stock ticker symbol")
    reason: str = Field(description="Reason this company is treanding in the news")

class TrendingCompanyList(BaseModel):
    """List of trending companies in the news"""
    companies: List[TrendingCompany] = Field(description="List of trending companies in the news")

class TrendingCompaniesResearch(BaseModel):
    """Detailed research on a company"""
    name: str = Field(description="Company name")
    market_position: str = Field(description="Current market position an competitive analysis")
    future_outlook: str = Field(description="Future outlook and growth prospects")
    investment_potential: str = Field(description="Investment potential and suitability for investment")

class TrendingCompaniesResearchList(BaseModel):
    """List of detailed research on trending companies"""
    research: List[TrendingCompaniesResearch] = Field(description="Comprehensive research on all trending companies")


@CrewBase
class StockPicker():
    """StockPicker crew"""
  
    agents_config: List[BaseAgent]
    tasks_config: List[Task]

    @agent
    def trending_company_finder(self) -> Agent:
        return Agent(config=self.agents_config['trending_company_finder'], tools=[SerperDevTool()])
    
    @agent
    def financial_researcher(self) -> Agent:
        return Agent(config=self.agents_config['financial_researcher'], tools=[SerperDevTool()])
    
    @agent
    def stock_picker(self) -> Agent:
        return Agent(config=self.agents_config['stock_picker'], tools=[PushNotificationTool()])
    
    @task
    def find_trending_companies(self) -> Task:
        return Task(
            config=self.tasks_config['find_trending_companies'],
            output_pydantic=TrendingCompaniesResearchList,
        )
    
    @task
    def research_trending_companies(self) -> Task:
        return Task(
            config=self.tasks_config['research_trending_companies'],
            output_pydantic=TrendingCompaniesResearchList,
        )
    
    @task
    def pick_best_company(self) -> Task:
        return Task(
            config=self.tasks_config['pick_best_company']
        )
    
    @crew
    def crew(self) -> Crew:
        
        manager = Agent(
            config=self.agents_config['manager'],
            allow_delegation=True #similar to handoff in OpenAI SDK
        )

        
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.hierarchical,
            verbose=True,
            manager_agent=manager #this is the agent that will manage the crew. Can be an llm directly, but it is better to create a agent and describe the agent and the role

        )
    