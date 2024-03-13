from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.prompts import (
  ChatPromptTemplate,
  HumanMessagePromptTemplate,
  MessagesPlaceholder
)
from langchain.memory import ConversationBufferMemory
from langchain.schema import SystemMessage
from langchain.agents import OpenAIFunctionsAgent, AgentExecutor

from tools.sql import run_query_tool, describe_tables_tools, list_tables
from tools.report import write_report_tool
from handlers.chat_model_start_handler import ChatModelStartHandler

load_dotenv()

handler = ChatModelStartHandler()
chat = ChatOpenAI(
  callbacks=[handler]
)

tables = list_tables()


"""
Here prompt is defined with human message with what ever message user sents
agent_scratchpad => is nothing but the intermediate memory that holds it till the agent executor ends
chat_history => is put just before the input, with all the memory of the previous requests
"""
prompt = ChatPromptTemplate(
  messages=[
    SystemMessage(content=(
      "You are an AI that has access to a SQLite Database.\n"
      f"The database have tables of: {tables}\n"
      "Do not make any assumptions about what tables exist "
      "or what column exist. Instead use the 'describe_tables' function"
    )),
    MessagesPlaceholder(variable_name="chat_history"),
    HumanMessagePromptTemplate.from_template("{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad")
  ]
)
"""
Between agent executor there intermediate memory that it has is deleted
So we need a conversation memory to save the humman message and agent message
for the next agent executor to perform actions on the same context.
"""
memory = ConversationBufferMemory(
  memory_key="chat_history",
  return_messages=True
)

# Define tools
tools = [run_query_tool, describe_tables_tools, write_report_tool]

"""
A agent is a method that tells the llm, prompt template and tools to use.
"""
agent = OpenAIFunctionsAgent(
  llm=chat,
  prompt=prompt,
  tools=tools
)

"""
A agent executor is nothing but a method that executes the agent method mutiple
times till a valid response is reached. Without a query response from the agent.
"""
agent_executor = AgentExecutor(
  agent=agent,
  #verbose=True,
  tools=tools,
  memory=memory
)

# agent_executor("How many users are there?")
# agent_executor("How many users have provided shipping address?")
# agent_executor("Summarize the top 5 products. Write the reports to a rports file.")
agent_executor("How many orders are there? Write the result to an html report.")
agent_executor("Repeat the exact same process for users.")

