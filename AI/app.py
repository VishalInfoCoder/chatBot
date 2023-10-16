import os

os.environ["OPENAI_API_TYPE"] = "azure"
os.environ["OPENAI_API_VERSION"] = "2023-05-15"
os.environ["OPENAI_API_BASE"] = "https://ai-ramsol-traning.openai.azure.com/"
os.environ["OPENAI_API_KEY"] = "5b60d2473952443cafceeee0b2797cf4"
#os.environ["HUGGINGFACEHUB_API_TOKEN"] = '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'
from ragas.testset import TestsetGenerator
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.llms import AzureOpenAI
from langchain.document_loaders import PyPDFLoader
from langchain.prompts.prompt import PromptTemplate
from langchain.chains import LLMChain
# documents = load your documents
# loader = PyPDFLoader("employee-handbookV3.pdf")
# pages = loader.load()
from llama_index import download_loader
# PDFReader = download_loader("PDFReader")
# loader = PDFReader()
# documents = loader.load_data(file="employee-handbookV3.pdf")
# Add custom llms and embeddings
# generator_llm = ChatOpenAI(model="gpt-3.5-turbo")
# critic_llm = ChatOpenAI(model="gpt-4")
embeddings_model = OpenAIEmbeddings(
                        api_key="5b60d2473952443cafceeee0b2797cf4",
                        openai_api_base="https://ai-ramsol-traning.openai.azure.com/",
                        openai_api_type="azure",
                        api_version="2023-05-15",
                        deployment="embedding-dev",
                        model="text-embedding-ada-002")
text = "This is a test query."
query_result = embeddings_model.embed_query(text)
generator_llm = AzureOpenAI(
                    deployment_id="Ai-training-example",   
                    model_name="gpt-35-turbo", 
                    temperature=0.5,
                    api_key="5b60d2473952443cafceeee0b2797cf4",
                    openai_api_base="https://ai-ramsol-traning.openai.azure.com/",
                    openai_api_type="azure",
                    api_version="2023-05-15",
                )

prompt = PromptTemplate(
    input_variables=["product"],
    template="What is a good name for a company that makes {product}?",
)
chain = LLMChain(llm=generator_llm, prompt=prompt)
print(chain.run("colorful socks"))

critic_llm = ChatOpenAI(
                    deployment_id="Ai-training-example",   
                    model_name="gpt-35-turbo", 
                    temperature=0.5,
                )

# Change resulting question type distribution
testset_distribution = {
    "simple": 0.25,
    "reasoning": 0.5,
    "multi_context": 0.0,
    "conditional": 0.25,
}

# percentage of conversational question
chat_qa = 0.2


# test_generator = TestsetGenerator(
#     generator_llm=generator_llm,
#     critic_llm=critic_llm,
#     embeddings_model=embeddings_model,
#     testset_distribution=testset_distribution,
#     chat_qa=chat_qa,
# )
testsetgenerator = TestsetGenerator.from_default()
test_size = 10


