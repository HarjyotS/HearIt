from langchain_community.document_loaders import PyPDFLoader

# gives vector format
def read_pdf(file_path):
    loader = PyPDFLoader(file_path)
    pages = loader.load_and_split()
    return pages

# gives plain text
def read_pdf_plain(file_path):
    loader = PyPDFLoader(file_path)
    pages = loader.load()
    pages_plain = ""
    for page in pages:
        pages_plain += page.page_content
    return pages_plain