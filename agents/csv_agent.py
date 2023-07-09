from langchain.agents import create_csv_agent
from langchain.chat_models import ChatOpenAI
from langchain.agents.agent_types import AgentType
from dotenv import load_dotenv

load_dotenv()
agent = create_csv_agent(
    ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613"),
    'heartdis.csv',
    verbose=True, 
    agent_type=AgentType.OPENAI_FUNCTIONS,
)

# takes user prompt until the user chooses to exit 
while True:
    user_input = input("question: ")
    if user_input == "exit":
        break
    agent.run(user_input)

