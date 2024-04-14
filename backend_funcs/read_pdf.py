from langchain_community.document_loaders import PyPDFLoader

def read_pdf(file_path):
    loader = PyPDFLoader(file_path)
    pages = loader.load_and_split()
    return pages