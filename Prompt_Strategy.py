import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.graphs import Neo4jGraph
from langchain.chains import GraphCypherQAChain
from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate

# --------------------
# Load environment variables
# --------------------
load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
groq_api_key = os.getenv("GROQ_API_KEY")

# --------------------
# Connect to Neo4j
# --------------------
graph = Neo4jGraph(
    url=NEO4J_URI,
    username=NEO4J_USERNAME,
    password=NEO4J_PASSWORD,
)

# --------------------
# Few-shot examples
# --------------------
examples = [
    {
        "question": "How many artists are there?",
        "query": "MATCH (a:Person)-[:ACTED_IN]->(:Movie) RETURN count(DISTINCT a)",
    },
    {
        "question": "Which actors played in the movie Casino?",
        # 🔥 FIX: escaped curly braces
        "query": "MATCH (m:Movie {{title: 'Casino'}})<-[:ACTED_IN]-(a:Person) RETURN a.name",
    },
    {
        "question": "How many movies has Tom Hanks acted in?",
        # 🔥 FIX: escaped curly braces
        "query": "MATCH (a:Person {{name: 'Tom Hanks'}})-[:ACTED_IN]->(m:Movie) RETURN count(m)",
    },
]

# Template for one example
example_prompt = PromptTemplate(
    input_variables=["question", "query"],
    template="User input: {question}\nCypher query: {query}"
)

# Few-shot wrapper
cypher_prompt = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    prefix="You are a Neo4j expert. Given an input question, create a syntactically correct Cypher query.",
    suffix="User input: {question}\nCypher query:",
    input_variables=["question"],   # only 'question' required
)

# --------------------
# Test prompt output
# --------------------
print("\n===== FINAL PROMPT OUTPUT =====\n")
print(cypher_prompt.format(question="How many artists are there?"))

# --------------------
# LLM + GraphCypherQAChain
# --------------------
llm = ChatGroq(groq_api_key=groq_api_key, model_name="Gemma2-9b-It")

chain = GraphCypherQAChain.from_llm(
    graph=graph,
    llm=llm,
    cypher_prompt=cypher_prompt,
    verbose=True,
    allow_dangerous_requests=True
)

# --------------------
# Run a query
# --------------------
response = chain.invoke("Which actors played in the movie Casino?")
print("\nQuery Response:\n", response)
