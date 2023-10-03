import chromadb
from chromadb.config import Settings

hostname = "https://tg60a835a6.execute-api.us-east-1.amazonaws.com/dev"
apikey = "tKx9nlDBoGaOmyIZUb1du9s0ZwrNSHln5lIU5meA"


# Example setup of the client to connect to your chroma server
#client = chromadb.HttpClient(host='3.90.187.44', port=8000)

client = chromadb.HttpClient(
    host=hostname,
    ssl=True,
    port="8000",
    headers={
        "X-Api-Key": apikey
    }
)
 

 
   