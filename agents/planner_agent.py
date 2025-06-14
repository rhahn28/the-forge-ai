# agents/planner_agent.py
import json
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from state import ForgeState
from core.models import Plan, PlanStep
from typing import List

# --- NEW IMPORTS for our local RAG pipeline ---
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

class PlannerAgent:
    """
    This agent now functions as an "Architect." It uses a RAG pipeline
    to retrieve expert knowledge from a local vector store before generating a plan.
    """
    def __init__(self):
        load_dotenv()
        # The Pydantic parser ensures the AI's final output is structured correctly.
        self.pydantic_parser = PydanticOutputParser(pydantic_object=Plan)
        
        # --- NEW RAG-FOCUSED PROMPT ---
        # This prompt is designed to accept external, expert context.
        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
You are a hyper-efficient, expert software architect. Your sole purpose is to convert a user request into a high-quality, professional JSON plan that strictly adheres to the provided schema.
You will be given expert context retrieved from a knowledge base. You MUST use this context to inform the plan you create, especially regarding project structure (like using a 'src' directory).
You MUST create a test file for every script file.
DO NOT output any text other than the JSON plan.
"""
                ),
                (
                    "human",
                    """
--- EXPERT CONTEXT ---
{context}
--------------------

User Request: "{task}"
Error Feedback (if any): "{error}"

Based on the expert context and the user request, generate the JSON plan.

SCHEMA:
{format_instructions}
"""
                ),
            ]
        )

        self.llm_chain = self.prompt | ChatOpenAI(model="gpt-4o") | self.pydantic_parser

    def _get_retriever(self):
        """
        This private method initializes our local knowledge base.
        """
        # Initialize the same open-source embedding model we used for ingestion.
        embedding_model = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")
        
        # Load the persisted vector store from the 'chroma_db' directory.
        vectorstore = Chroma(
            persist_directory="chroma_db", 
            embedding_function=embedding_model
        )
        
        # Create a retriever that can search the vector store.
        return vectorstore.as_retriever(search_kwargs={"k": 3}) # Retrieve top 3 relevant chunks

    async def run(self, state: ForgeState) -> dict:
        """
        The main logic for the Architect. It retrieves context, then generates a plan.
        """
        print("---ARCHITECT AGENT (RAG): Starting...---")
        try:
            task = state['task']
            error = state.get("error", "None")

            # --- RAG PIPELINE IN ACTION ---
            # 1. Get the retriever for our knowledge base.
            print("---ARCHITECT AGENT: Loading knowledge base...---")
            retriever = self._get_retriever()
            
            # 2. Search the knowledge base for documents relevant to the task.
            print(f"---ARCHITECT AGENT: Searching for expert context related to: '{task}'...---")
            retrieved_docs = retriever.get_relevant_documents(task)
            
            # Format the retrieved documents into a single string to be "stuffed" into the prompt.
            context_str = "\n\n---\n\n".join([doc.page_content for doc in retrieved_docs])
            print("---ARCHITECT AGENT: Found relevant context. Injecting into prompt.---")
            # --- END OF RAG PIPELINE ---

            # Now, invoke the LLM with the task AND the retrieved expert context.
            plan_obj = await self.llm_chain.ainvoke({
                "task": task,
                "error": error,
                "context": context_str, # <<< The new, expert context
                "format_instructions": self.pydantic_parser.get_format_instructions(),
            })
            
            plan_list = [step.model_dump() for step in plan_obj.steps]
            
            if not plan_list:
                raise ValueError("Architect returned an empty plan.")

            print("---ARCHITECT AGENT: Plan Generated and Validated.---")
            print(plan_list)
            
            return {"plan": plan_list, "current_step": 0, "error": None}
        except Exception as e:
            print(f"---ARCHITECT AGENT: ERROR - {e}---")
            return {"error": f"Architect failed to generate a valid plan: {e}"}