import sqlite3
from pydantic.v1 import BaseModel
from typing import List
from langchain.tools import Tool


conn = sqlite3.connect("db.sqlite")

# list out all tables
def list_tables():
  c = conn.cursor()
  c.execute("SELECT name FROM sqlite_master WHERE type='table';");
  rows = c.fetchall()
  return "\n".join(row[0] for row in rows if row[0] is not None)

# method to excute query in sqlite
def run_sqlite_query(query):
  c = conn.cursor()
  try:
    c.execute(query)
    return c.fetchall()
  except sqlite3.OperationalError as err:
    return f"The following error occured: {str(err)}"


class RunQueryArgsSchema(BaseModel):
  query:str
  
# the tool exposed to langchain to execute query
run_query_tool = Tool.from_function(
  name="run_sqlite_query",
  description="Run a sqlite query",
  func=run_sqlite_query,
  args_schema=RunQueryArgsSchema
)

# describe table
def describe_tables(table_names):
  c = conn.cursor()
  tables = ', '.join("'" + table + "'" for table in table_names)
  rows = c.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name IN ({tables});")
  return "\n".join(row[0] for row in rows if row[0] is not None)

class DescribeTablesArgsSchema(BaseModel):
  table_names: List[str]

describe_tables_tools = Tool.from_function(
  name="describe_tables",
  description="Given a list of table names, returns the schema of the list of tables",
  func=describe_tables,
  args_schema=DescribeTablesArgsSchema
)