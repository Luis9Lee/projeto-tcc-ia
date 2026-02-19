import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA

# 1. Configuração da API Key (Substitua pela sua ou use variável de ambiente)
os.environ["GOOGLE_API_KEY"] = "SUA_CHAVE_AQUI"

def iniciar_chat():
    # 2. Carregar os dados da pasta inputs
    print("--- Carregando documentos ---")
    loader = TextLoader("./inputs/dados.txt")
    documentos = loader.load()

    # 3. Fragmentação (Chunking)
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(documentos)

    # 4. Criar Embeddings e Base Vetorial
    print("--- Criando base de conhecimento vetorial ---")
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vectorstore = FAISS.from_documents(texts, embeddings)

    # 5. Configurar o Modelo de Chat
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
    
    # 6. Criar a Chain de Pergunta e Resposta (RAG)
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever()
    )

    print("\n✅ Sistema Pronto! Digite sua pergunta sobre o TCC (ou 'sair'):")
    
    while True:
        pergunta = input("\nSua pergunta: ")
        if pergunta.lower() == 'sair':
            break
        
        resposta = qa_chain.invoke(pergunta)
        print(f"\nAssistente IA: {resposta['result']}")

if __name__ == "__main__":
    iniciar_chat()
