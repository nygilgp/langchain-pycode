# My GenAI playground projects

## Pycode

A prompt project that generates code and the test case for the code on user input. We connect to OpenAI using Langchain and use prompt templates to generate the code. Followed by it we use sequential to pass the first result to the second prompt and generate the test code. This shows how chaining is done.

## tchat

A prompt chat project, which keeps history like OpenAI chat. Used langchin memory to keep tack of previous response.

## facts

A prompt project that reads through the facts document and returns the most optimum
Used chroma as vector DB. Most relevant data is then sent to OpenAI on user query against the facts using chain Retrieval.

## Steps to run the each project

> Create .env with key
> pipenv install
> pipenv shell
> python main.py

Thanks to [Stephen Grider](https://www.udemy.com/user/sgslo/) => [ChatGPT and LangChain](https://www.udemy.com/course/chatgpt-and-langchain-the-complete-developers-masterclass/)
