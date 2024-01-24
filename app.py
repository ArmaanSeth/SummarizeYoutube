import os
from selenium import webdriver
from urllib.parse import urlparse
from youtube_transcript_api import YouTubeTranscriptApi
from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document
from langchain_core.prompts import PromptTemplate
# driver=webdriver.Chrome()
# url=driver.current_url

url="https://www.youtube.com/watch?v=mrKuDK9dGlg&t=2641s"
url="https://www.youtube.com/watch?v=LNq_2s_H01Y"
# url="https://www.youtube.com/watch?v=__sETDiAYqM"
url="https://www.youtube.com/watch?v=sZZDw0i6WSA"
vid=urlparse(url).query[2:]

transcript=YouTubeTranscriptApi.get_transcript(vid, languages=["en","hi"])
transcript=[t["text"] for t in transcript]
transcript=' '.join(transcript)
chunks=RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200).split_text(transcript)
docs=[Document(page_content=t) for t in chunks]

os.environ["GOOGLE_API_KEY"]="AIzaSyB3xjgb0DF84EvKsvKafVFdih9jpaj4jGQ"
llm=ChatGoogleGenerativeAI(model="gemini-pro",convert_system_message_to_human=True)

prompt=""""""

chain=load_summarize_chain(chain_type="map_reduce", llm=llm, verbose=False, return_intermediate_steps=False)
output_summary=chain.run(docs)
print(output_summary)