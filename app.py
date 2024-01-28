from dotenv import load_dotenv
from flask import Flask, request
from langchain_community.document_loaders import YoutubeLoader
from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
# from waitress import serve

app = Flask(__name__)
def get_summary(url):
    print("URL="+url)
    if "www.youtube.com/watch" not in url:
        return "This is not a youtube page"
    transcript=YoutubeLoader.from_youtube_url(url, language=["en"], translation="en").load()
    chunks=RecursiveCharacterTextSplitter(chunk_size=5000, chunk_overlap=0).split_documents(transcript)
    llm=ChatGoogleGenerativeAI(model="gemini-pro",convert_system_message_to_human=True)
    chain=load_summarize_chain(chain_type="stuff", llm=llm, verbose=True)
    return chain.run(chunks)

@app.route('/')
def index():
    url = request.args.get('url', 'No URL provided')
    res=get_summary(url)
    return {"text":res}

if __name__ == '__main__':
    load_dotenv()
    app.run(host="0.0.0.0", port=5000, debug=False)