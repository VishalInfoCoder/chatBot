import openai
import pymongo
import os
from langchain.embeddings import OpenAIEmbeddings
from sentence_transformers import SentenceTransformer
# Set your OpenAI API key
os.environ["OPENAI_API_TYPE"] = "azure"
os.environ["OPENAI_API_VERSION"] = "2023-05-15"
os.environ["OPENAI_API_BASE"] = "https://ai-ramsol-traning.openai.azure.com/"
os.environ["OPENAI_API_KEY"] = "5b60d2473952443cafceeee0b2797cf4"
# Initialize the MongoDB client
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["mydatabase"]
collection = db["text_embeddings"]
model_name = "all-MiniLM-L6-v2"
embedding_model = SentenceTransformer(model_name)
# Create a function to generate embeddings
def generate_embeddings(text):
    embeddings = embedding_model.encode(text)
    return embeddings

# Create a function to write embeddings to MongoDB
def write_embeddings_to_mongodb(embeddings, collection):
    for embedding in embeddings:
        collection.insert_one({"embedding": embedding.tolist()})
sentence="HEY how are you?"
# Generate embeddings for the data you want to write to MongoDB
embeddings = generate_embeddings([sentence])

# Write the embeddings to MongoDB
write_embeddings_to_mongodb(embeddings, collection)

# Close the MongoDB connection
client.close()
