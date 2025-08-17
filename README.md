# GraphQuery AI

A natural language interface to a Neo4j graph database powered by LangChain and Groq's blazing-fast inference of Google’s Gemma 2B model.

## 🚀 Overview

This project allows users to ask natural language questions, which are converted into Cypher queries using Google Gemma 2B via Groq. The queries are executed against a Neo4j graph database, and the results are returned in plain English.

### Example:

> "Who was the director of the movie *Casino*?"

→ Automatically translated to Cypher and answered using real graph data.

## 🧠 Features

- 🔗 Integration with Neo4j graph database
- 🧾 Automatic conversion of natural language to Cypher
- ⚡ Inference via Groq’s ultra-low latency LPU backend
- 🧠 Uses Google’s Gemma 2B model via LangChain's LLM interface
- 🗂️ Secure query execution (requires `allow_dangerous_requests=True`)

## 🔧 Tech Stack

- **Python**
- **LangChain**
- **Groq API** (Gemma 2B)
- **Neo4j**
- .py / CLI-based interface 

## ⚙️ Setup Instructions

### reate a .env file or export manually:
```
export NEO4J_URI="bolt://localhost:7687"
export NEO4J_USERNAME="neo4j"
export NEO4J_PASSWORD="your-password"
export GROQ_API_KEY="your-groq-api-key"
```