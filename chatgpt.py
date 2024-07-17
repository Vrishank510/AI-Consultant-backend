import os
import sys
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from dotenv import load_dotenv
import openai
from langchain.chains import ConversationalRetrievalChain, RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import DirectoryLoader, TextLoader

from langchain.indexes import VectorstoreIndexCreator

from langchain.llms import OpenAI



app = Flask(__name__)
cors = CORS(app)

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv('api_key')
loader = DirectoryLoader('.', glob='*.txt')
index = VectorstoreIndexCreator().from_loaders([loader])

@app.route("/", methods=["POST"])
def get_prompt():
    data = request.get_json()

    print(data)
    d = (index.query(data, llm=ChatOpenAI()))
    print("returned data is", file=sys.stdout)
    return jsonify(d)


if __name__ == "__main__":
    app.run(debug=True)

