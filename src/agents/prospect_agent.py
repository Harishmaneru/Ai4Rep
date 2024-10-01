from langchain.agents import AgentType, initialize_agent
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import SystemMessage, HumanMessage
from ..config import OPENAI_API_KEY
from ..tools.api_tools import find_people_tool, enrich_people_tool
from ..utils import format_people_for_enrichment
import json

class ProspectAIAgent:
    def __init__(self):
        self.llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-16k", api_key=OPENAI_API_KEY)
        self.tools = [find_people_tool, enrich_people_tool]

        prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="You are an AI assistant that helps find and enrich people's data. When using tools, always provide the entire input as a single JSON-formatted string, including the action and action_input."),
            HumanMessage(content="{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])

        self.agent_executor = initialize_agent(
            self.tools,
            self.llm,
            agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
            agent_kwargs={
                "input_variables": ["input", "agent_scratchpad"],
                "prompt": prompt
            }
        )

    def find_people(self, criteria):
        input_text = json.dumps({
            "action": "Find People",
            "action_input": json.dumps(criteria)
        })
        return self.agent_executor.run(input_text)

    def enrich_people(self, found_people, people_to_enrich, enrich_type):
        # Parse the found_people JSON string
        found_people_data = json.loads(found_people)
        
        # Find the full data for the people we want to enrich
        people_data = []
        for person_to_enrich in people_to_enrich:
            for person in found_people_data.get('people', []):
                if person['id'] == person_to_enrich['id']:
                    people_data.append(person)
                    break
        
        input_data = {
            "people": people_data,
            "enrich_type": enrich_type
        }
        
        input_text = json.dumps({
            "action": "Enrich People",
            "action_input": json.dumps(input_data)
        })
        return self.agent_executor.run(input_text)

