from langchain.chains import LLMChain
from langchain.document_loaders import YoutubeLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

embeddings = OpenAIEmbeddings()


def create_vector_db_from_youtube_url(video_url: str) -> FAISS:
    loader = YoutubeLoader.from_youtube_url(
        video_url, language=["en", "id", "es", "fr", "ar"], translation="en"
    )
    transcription = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    docs = text_splitter.split_documents(transcription)

    db = FAISS.from_documents(docs, embeddings)

    return db


def get_response_from_query(
    db: FAISS,
    query: str,
    answer_language: str = "english",
    k: int = 4,
    model: str = "gpt-4-1106-preview",
    temperature: float = 0.7,
) -> tuple[str, list]:
    docs = db.similarity_search(query=query, k=k)
    docs_page_content = " ".join([doc.page_content for doc in docs])

    llm = ChatOpenAI(model=model, temperature=temperature)

    prompt_template = PromptTemplate(
        input_variables=["question", "docs", "answer_language"],
        template="""
            You are a helpful assistant that can answer questions about youtube videos 
            based on the video's transcript.

            Answer the following question: {question}
            By searching the following video transcript: {docs}

            Only use the factual information from the transcript to answer the question.

            If you feel like you don't have enough information to answer the question, say "I don't know".

            Your answers should be verbose and detailed.
            
            Give me directly the answer without any explanations or notes.
            
            Give me the answer in {answer_language}.
            
            Use markdown syntax .
            
            Don't respond to me with the phrase '...in the script...' but rather '...in the video'..."
            """,
    )

    chain = LLMChain(llm=llm, prompt=prompt_template, verbose=True)

    response = chain.run(
        question=query, answer_language=answer_language, docs=docs_page_content
    )

    return response, docs
