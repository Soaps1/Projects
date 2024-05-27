import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template
from bs4 import BeautifulSoup
from langchain.community.document_loaders import WebBaseLoader
from langchain.core.output_parsers import StrOutputParser
from langchain.core.runnables import RunnablePassthrough
from langchain.openai import OpenAIEmbeddings, ChatOpenAI
from langchain.text_splitters import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma

# Load environment variables from .env file
load_dotenv()

llm = ChatOpenAI(model="gpt-3.5-turbo-0125")

# Load, chunk, and index the contents of the blog.
loader = WebBaseLoader(
    web_paths=("https://lilianweng.github.io/posts/2023-06-23-agent/",),
    bs_kwargs=dict(
        parse_only=BeautifulSoup.SoupStrainer(
            class_=("post-content", "post-title", "post-header")
        )
    ),
)
docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(docs)
vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())

# Retrieve and generate using the relevant snippets of the blog.
retriever = vectorstore.as_retriever()
prompt_template = """
Use the following context to answer the question.

Context:
{context}

Question:
{question}

Answer:"""

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def create_prompt(context, question):
    return prompt_template.format(context=context, question=question)

def rag_chain(question):
    context_docs = retriever.retrieve(question)
    formatted_context = format_docs(context_docs)
    prompt = create_prompt(formatted_context, question)
    response = llm(prompt)
    return response

result = rag_chain("Who is Lillian Weng?")

# Print the result
print(result)

vectorstore.delete_collection()
