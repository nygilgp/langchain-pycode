from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.prompts import (
  ChatPromptTemplate,
  HumanMessagePromptTemplate,
  MessagesPlaceholder
)
from langchain.agents import OpenAIFunctionsAgent, AgentExecutor

from tools.sql import run_query_tool

load_dotenv()

chat = ChatOpenAI()
"""
Here prompt is defined with human message with what ever message user sents
agent_scratchpad => is nothing but the memory that 
"""
prompt = ChatPromptTemplate(
  messages=[
    HumanMessagePromptTemplate.from_template("{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad")
  ]
)

# Define tools
tools = [run_query_tool]

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
  verbose=True,
  tools=tools
)

agent_executor("How many users have provided shipping address?")


"""OUTPUT:
  
> Entering new AgentExecutor chain...

Invoking: `run_sqlite_query` with `SELECT COUNT(DISTINCT user_id) FROM orders WHERE shipping_address IS NOT NULL`


The following error occured: no such column: shipping_address
Invoking: `run_sqlite_query` with `SELECT COUNT(DISTINCT user_id) FROM orders WHERE shipping_address_id IS NOT NULL`
responded: It seems that there was an error because the column "shipping_address" does not exist in the database. Let me correct the query and try again.

The following error occured: no such column: shipping_address_id
Invoking: `run_sqlite_query` with `SELECT COUNT(DISTINCT user_id) FROM orders WHERE shipping_address_id IS NOT NULL`
responded: It seems that the column name I used in the query is incorrect. Let me correct it and try again.

The following error occured: no such column: shipping_address_id
Invoking: `run_sqlite_query` with `SELECT COUNT(DISTINCT user_id) FROM orders WHERE shipping_address IS NOT NULL`
responded: I apologize for the error. It seems that the column name I used is still incorrect. Let me check the correct column name and try again.

The following error occured: no such column: shipping_address
Invoking: `run_sqlite_query` with `PRAGMA table_info(orders)`
responded: It seems that the column name "shipping_address" is not available in the database. Let me check the schema of the database to find the correct column name for shipping address and try again.

[(0, 'id', 'INTEGER', 0, None, 1), (1, 'user_id', 'INTEGER', 0, None, 0), (2, 'created', 'TEXT', 0, None, 0)]
Invoking: `run_sqlite_query` with `PRAGMA table_info(shipping_addresses)`
responded: Based on the schema of the "orders" table, I can see that the columns are "id", "user_id", and "created". It appears that there is no "shipping_address" column in the table. Let me try to find the correct column name for shipping address in the database.

[]
Invoking: `run_sqlite_query` with `PRAGMA table_info(users)`
responded: It seems that the "shipping_addresses" table does not exist in the database. Let me try to find the correct column name for shipping address in another way.

[(0, 'id', 'INTEGER', 0, None, 1), (1, 'name', 'TEXT', 0, None, 0), (2, 'email', 'TEXT', 0, None, 0), (3, 'password', 'TEXT', 0, None, 0)]
Invoking: `run_sqlite_query` with `PRAGMA table_info(user_addresses)`
responded: Based on the schema of the "users" table, I can see that the columns are "id", "name", "email", and "password". It appears that there is no "shipping_address" column in the "users" table either. Let me try to find the correct column name for shipping address in another way.

[]
Invoking: `run_sqlite_query` with `PRAGMA table_info(addresses)`
responded: It seems that the "user_addresses" table also does not exist in the database. Let me try to find the correct column name for shipping address in the database in a different way.

[(0, 'id', 'INTEGER', 0, None, 1), (1, 'user_id', 'INTEGER', 0, None, 0), (2, 'address', 'TEXT', 0, None, 0)]
Invoking: `run_sqlite_query` with `SELECT COUNT(DISTINCT user_id) FROM addresses`
responded: Based on the schema of the "addresses" table, I can see that the columns are "id", "user_id", and "address". The "address" column seems to contain the shipping address information. Let me correct the query and try again to find the number of users who have provided a shipping address.

[(2000,)]The query result shows that there are 2000 users who have provided a shipping address. If you need any further information or assistance, feel free to let me know!

> Finished chain.
"""