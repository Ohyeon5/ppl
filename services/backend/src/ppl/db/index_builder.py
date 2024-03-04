import json
import os
from pathlib import Path

from llama_index import ServiceContext, VectorStoreIndex
from llama_index.core.schema import TextNode
from llama_index.embeddings import AzureOpenAIEmbedding
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms import AzureOpenAI
from llama_index.llms.llama_cpp import LlamaCPP
from llama_index.llms.llama_cpp.llama_utils import (
    completion_to_prompt,
    messages_to_prompt,
)


def prepare_context_azure_openai() -> ServiceContext:
    """Prepare the service context for the index builder
    Use AzureOpenAI and AzureOpenAIEmbedding

    Returns:
        ServiceContext: ServiceContext object with llm and embed_model initialized
    """
    llm = AzureOpenAI(
        engine="gpt-35-turbo",
        model="gpt-35-turbo",
        api_key=os.getenv("OPENAI_API_KEY"),
        api_version=os.getenv("OPENAI_API_VERSION"),
        azure_endpoint=os.getenv("OPENAI_BASE_URL"),
    )

    embed_model = AzureOpenAIEmbedding(
        azure_deployment="text-embedding-ada-002",
        model="text-embedding-ada-002",
        api_key=os.getenv("OPENAI_API_KEY"),
        api_version=os.getenv("OPENAI_API_VERSION"),
        azure_endpoint=os.getenv("OPENAI_BASE_URL"),
        embed_batch_size=1,
    )

    service_context = ServiceContext.from_defaults(
        llm=llm,
        embed_model=embed_model,
    )
    return service_context


def prepare_context_llmcpp_huggingface() -> ServiceContext:
    """Prepare the service context for the index builder
    Use LLM CPP and HuggingFaceEmbedding

    Returns:
        ServiceContext: ServiceContext object with llm and embed_model initialized
    """
    llmcpp_path = os.getenv("LLM_CPP_PATH")
    llm = LlamaCPP(
        model_url=llmcpp_path if "http" in llmcpp_path else None,
        model_path=llmcpp_path if "http" not in llmcpp_path else None,
        temperature=0.1,
        max_new_tokens=256,
        context_window=3900,
        generate_kwargs={},
        model_kwargs={},
        messages_to_prompt=messages_to_prompt,
        completion_to_prompt=completion_to_prompt,
        verbose=False,
    )
    embed_model = HuggingFaceEmbedding(model_name="intfloat/e5-small")

    service_context = ServiceContext.from_defaults(
        llm=llm,
        embed_model=embed_model,
    )
    return service_context


def prepare_context() -> ServiceContext:
    """prepare the service context for the index builder

    Returns:
        ServiceContext: ServiceContext object with llm and embed_model initialized
    """
    if os.getenv("OPENAI_API_KEY") is not None:
        return prepare_context_azure_openai()
    else:
        return prepare_context_llmcpp_huggingface()


def build_index(patents_path: Path, save_path: Path):
    """build index and save it to save_path

    Args:
        patents_path (Path): parent directory of json files
        save_path (Path): save directory
    """
    # Create LlamaIndex nodes, each node is a separate vector
    nodes = []
    for filepath in patents_path.glob(f"*.json"):
        print(f"Processing file: {filepath}")
        with open(filepath, "r") as f:
            json_content = json.load(f)
        nodes = []
        for article in json_content:
            node = TextNode(text=str(article))
            nodes.append(node)

    service_context = prepare_context()
    # Get embeddings and index them
    index = VectorStoreIndex(nodes, service_context=service_context, show_progress=True)
    # By default saves to save_path
    index.storage_context.persist(persist_dir=save_path)
