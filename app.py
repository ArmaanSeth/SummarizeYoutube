from flask import Flask, request
from urllib.parse import urlparse
from youtube_transcript_api import YouTubeTranscriptApi
from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document

app = Flask(__name__)
def get_summary(url):
    if "www.youtube.com/watch" not in url:
        return "This is not a youtube page"
    vid=urlparse(url).query[2:]
    transcript=YouTubeTranscriptApi.get_transcript(vid, languages=["en","hi"])
    transcript=[t["text"] for t in transcript]
    transcript=' '.join(transcript)
    chunks=RecursiveCharacterTextSplitter(chunk_size=5000, chunk_overlap=0).split_text(transcript)
    docs=[Document(page_content=t) for t in chunks]
    llm=ChatGoogleGenerativeAI(model="gemini-pro",convert_system_message_to_human=True)
    chain=load_summarize_chain(chain_type="stuff", llm=llm, verbose=True)
    return chain.run(docs)

@app.route('/')
def index():
    url = request.args.get('url', 'No URL provided')
    res=get_summary(url)
    return {"text":res}

if __name__ == '__main__':
    app.run(debug=True)