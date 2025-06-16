"""
This module implements a Crew-based AI system for stock analysis and trading decisions.
A Crew is a group of specialized AI agents that work together to accomplish complex tasks.
Each agent has a specific role and expertise in the stock market analysis process.
"""

from crewai import Agent, Task, Crew, Process
from textwrap import dedent
from langchain.tools import tool
from datetime import datetime, timedelta
import pandas as pd
from typing import List, Dict, Any
import os
from dotenv import load_dotenv

# Load environment variables from .env file
# This is where we store sensitive information like API keys
load_dotenv()

class StockAnalysisCrew:
    """
    A class that orchestrates a team of AI agents to analyze stocks and make trading decisions.
    Each agent has a specific role in the analysis process, from data gathering to final decision making.
    """

    def __init__(self):
        """
        Initialize the StockAnalysisCrew with necessary API keys and configuration.
        The API keys are loaded from environment variables for security.
        """
        # Load API keys from environment variables
        self.alpha_vantage_api_key = os.getenv('ALPHA_VANTAGE_API_KEY')
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        
        # Verify that required API keys are present
        if not self.alpha_vantage_api_key or not self.openai_api_key:
            raise ValueError("Missing required API keys. Please check your .env file.")

    def create_agents(self) -> List[Agent]:
        """
        Creates and returns a list of specialized AI agents, each with a specific role in the analysis process.
        
        Returns:
            List[Agent]: A list of configured AI agents with specific roles and tools.
        """
        # Create a Data Analyst agent that specializes in gathering and analyzing stock data
        data_analyst = Agent(
            role='Data Analyst',
            goal='Gather and analyze comprehensive stock data to identify market trends and patterns',
            backstory=dedent("""
                You are an expert data analyst with years of experience in financial markets.
                Your expertise lies in gathering, processing, and interpreting complex financial data.
                You have a keen eye for patterns and trends that others might miss.
            """),
            verbose=True,
            allow_delegation=False,
            tools=[self.get_stock_data]  # This agent can fetch stock data
        )

        # Create a Market Researcher agent that focuses on market conditions and news
        market_researcher = Agent(
            role='Market Researcher',
            goal='Analyze market conditions and news to understand the broader market context',
            backstory=dedent("""
                You are a seasoned market researcher with deep knowledge of financial markets.
                You excel at understanding market dynamics and how news affects stock prices.
                Your insights help make informed trading decisions.
            """),
            verbose=True,
            allow_delegation=False,
            tools=[self.get_market_news]  # This agent can fetch market news
        )

        # Create a Trading Strategist agent that makes final trading decisions
        trading_strategist = Agent(
            role='Trading Strategist',
            goal='Make informed trading decisions based on data analysis and market research',
            backstory=dedent("""
                You are a successful trading strategist with a proven track record.
                You combine technical analysis with market insights to make profitable trading decisions.
                Your decisions are always backed by solid data and research.
            """),
            verbose=True,
            allow_delegation=False,
            tools=[self.get_technical_indicators]  # This agent can calculate technical indicators
        )

        return [data_analyst, market_researcher, trading_strategist]

    def create_tasks(self, agents: List[Agent], symbol: str) -> List[Task]:
        """
        Creates a sequence of tasks for the agents to perform in order to analyze a stock.
        
        Args:
            agents (List[Agent]): The list of agents that will perform the tasks
            symbol (str): The stock symbol to analyze
            
        Returns:
            List[Task]: A list of tasks to be performed by the agents
        """
        # Task 1: Gather and analyze stock data
        data_analysis_task = Task(
            description=dedent(f"""
                Analyze the stock data for {symbol}:
                1. Gather historical price data
                2. Calculate key metrics
                3. Identify trends and patterns
                4. Prepare a comprehensive data analysis report
            """),
            agent=agents[0]  # Data Analyst agent
        )

        # Task 2: Research market conditions and news
        market_research_task = Task(
            description=dedent(f"""
                Research market conditions for {symbol}:
                1. Gather recent market news
                2. Analyze market sentiment
                3. Identify relevant market trends
                4. Prepare a market research report
            """),
            agent=agents[1]  # Market Researcher agent
        )

        # Task 3: Make trading decision
        trading_decision_task = Task(
            description=dedent(f"""
                Make a trading decision for {symbol}:
                1. Review data analysis and market research
                2. Consider technical indicators
                3. Evaluate risk factors
                4. Make a final trading recommendation
            """),
            agent=agents[2]  # Trading Strategist agent
        )

        return [data_analysis_task, market_research_task, trading_decision_task]

    def run_analysis(self, symbol: str) -> Dict[str, Any]:
        """
        Runs the complete stock analysis process using the crew of agents.
        
        Args:
            symbol (str): The stock symbol to analyze
            
        Returns:
            Dict[str, Any]: A dictionary containing the analysis results and trading decision
        """
        # Create the team of agents
        agents = self.create_agents()
        
        # Create the sequence of tasks
        tasks = self.create_tasks(agents, symbol)
        
        # Create and run the crew
        crew = Crew(
            agents=agents,
            tasks=tasks,
            verbose=2,  # Show detailed progress
            process=Process.sequential  # Tasks are performed in sequence
        )
        
        # Execute the analysis and get results
        result = crew.kickoff()
        
        return {
            'symbol': symbol,
            'analysis_date': datetime.now().isoformat(),
            'result': result
        }

    # Tool methods that agents can use to perform their tasks
    @tool
    def get_stock_data(self, symbol: str) -> Dict[str, Any]:
        """
        Fetches historical stock data for analysis.
        This is a tool that the Data Analyst agent can use.
        """
        # Implementation would go here
        pass

    @tool
    def get_market_news(self, symbol: str) -> List[Dict[str, Any]]:
        """
        Fetches relevant market news and updates.
        This is a tool that the Market Researcher agent can use.
        """
        # Implementation would go here
        pass

    @tool
    def get_technical_indicators(self, symbol: str) -> Dict[str, Any]:
        """
        Calculates technical indicators for the stock.
        This is a tool that the Trading Strategist agent can use.
        """
        # Implementation would go here
        pass 