# from llama_index.embeddings.huggingface import HuggingFaceEmbedding
# from llama_index.llms.llama_cpp import LlamaCPP
# from llama_index.llms.llama_cpp.llama_utils import (
#     completion_to_prompt,
#     messages_to_prompt,
# )

## LLAMA_CPP is commented out because it requires downloading a 7B model
## TODO: mount model weights from Azure Blob Storage
# model_url = "https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7b-chat.Q3_K_S.gguf"
# LLAMA_CPP = LlamaCPP(
#     model_url=model_url,
#     model_path=None,
#     temperature=0.1,
#     max_new_tokens=1024,
#     context_window=3900,
#     generate_kwargs={},
#     model_kwargs={},
#     messages_to_prompt=messages_to_prompt,
#     completion_to_prompt=completion_to_prompt,
#     verbose=False,
# )
# TODO: Implement EMBED_MODEL
# EMBED_MODEL = HuggingFaceEmbedding(model_name="intfloat/e5-small")

# from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding
# from llama_index.llms.azure_openai import AzureOpenAI

# TODO: Implement Azure OpenAI
# OPENAI_LLM = AzureOpenAI(
#     engine="gpt-35-turbo",
#     model="gpt-35-turbo",
#     api_key=os.getenv("OPENAI_API_KEY"),
#     api_version=os.getenv("OPENAI_API_VERSION"),
#     azure_endpoint=os.getenv("OPENAI_BASE_URL"),
# )

# OPENAI_EMBED = AzureOpenAIEmbedding(
#     azure_deployment="text-embedding-ada-002",
#     model="text-embedding-ada-002",
#     api_key=os.getenv("OPENAI_API_KEY"),
#     api_version=os.getenv("OPENAI_API_VERSION"),
#     azure_endpoint=os.getenv("OPENAI_BASE_URL"),
#     embed_batch_size=1,
# )
