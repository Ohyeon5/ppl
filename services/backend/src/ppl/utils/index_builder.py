import json
import os
from pathlib import Path

from llama_index.core import ServiceContext, VectorStoreIndex
from llama_index.core.schema import TextNode

from services.backend.src.ppl.utils.model_zoo import LLAMA_CPP  # , EMBED_MODEL

# TODO: Implement Azure OpenAI
# from ppl.utils.model_loader import OPENAI_LLM, OPENAI_EMBED

# def prepare_context_azure_openai() -> ServiceContext:
#     """Prepare the service context for the index builder
#     Use AzureOpenAI and AzureOpenAIEmbedding

#     Returns:
#         ServiceContext: ServiceContext object with llm and embed_model initialized
#     """
#     service_context = ServiceContext.from_defaults(
#         llm=OPENAI_LLM,
#         embed_model=OPENAI_EMBED,
#     )
#     return service_context


def prepare_context_llmcpp_huggingface() -> ServiceContext:
    """Prepare the service context for the index builder
    Use LLM CPP and HuggingFaceEmbedding

    Returns:
        ServiceContext: ServiceContext object with llm and embed_model initialized
    """

    service_context = ServiceContext.from_defaults(
        llm=LLAMA_CPP,
        # embed_model=EMBED_MODEL,
    )
    return service_context


def prepare_context() -> ServiceContext:
    """prepare the service context for the index builder

    Returns:
        ServiceContext: ServiceContext object with llm and embed_model initialized
    """
    if os.getenv("OPENAI_API_KEY") is not None:
        raise NotImplementedError("Azure OpenAI is not implemented yet")
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
