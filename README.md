# agentic-rag-crag-srag-arag
agentic-rag-crag-srag-arag is a Python-based framework implementing advanced Retrieval-Augmented Generation (RAG) workflows using LangGraph to orchestrate agentic pipelines and improve the quality of responses from large language models by intelligently retrieving, evaluating, and generating information.

This repository includes implementations of multiple RAG variants, such as:

Agentic RAG — an enhanced RAG pipeline where autonomous agents control the retrieval and generation process, dynamically deciding how and when to fetch context and generate responses to complex inputs. 
Salesforce

CRAG (Corrective RAG) — a variant that self-grades retrieved content and can fall back to alternate knowledge sources (e.g., web search) when retrieved contexts aren’t relevant or accurate. 


SRAG (Self-RAG) — a self-reflective approach that incorporates quality checks on both retrieval and generation steps to reduce hallucinations and improve response reliability. 


ARAG (Agentic RAG / Adaptive RAG) — advanced agentic retrieval with adaptive strategies for routing queries, optimizing retrieval, and enabling more nuanced multi-agent collaboration workflows. 

The workflow orchestration is handled using LangGraph, which organizes the logic for how these RAG variants interact with each other and with external knowledge sources such as vector databases or search APIs. Together, these components enable a flexible, intelligent RAG system that goes beyond traditional static retrieval pipelines — offering dynamic retrieval decision-making, self-correction, and adaptive response generation.
