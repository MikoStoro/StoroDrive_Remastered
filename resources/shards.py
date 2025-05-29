import os


def get_document(filename,catalogue="common"):
    element = '<div class="document">' 
    element += '<a href="download?catalogue=' + catalogue + '&filename=' + filename +'">'
    element += filename
    element += '</a>'
    element += '</div>'
    return element

def get_document_table_row(filename, catalogue="common"):
    pass

def get_document_download_link(filename, catalogue="common"):
    pass

def get_documents_table(catalogue="common"):
    pass

def get_documents(catalogue):
    path = os.path.join("volume", catalogue)
    elements = ''
    for filename in os.listdir(path):
        elements += get_document(filename,catalogue)
    return elements

