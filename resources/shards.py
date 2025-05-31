import os
import tinydb

def get_document(filename:str,catalogue="common"):
    element = '<div class="document">' 
    element += '<a href="download?catalogue=' + catalogue + '&filename=' + filename +'">'
    element += filename
    element += '</a>'
    element += '</div>'
    return element

def get_document_table_row(filename:str, catalogue="common"):
    ## nazwa, pobierz, usuń
    row = """<tr> 
                <td>{0}</td> 
                <td>{1}</td>
                <td>{2}</td>
            </tr>""".format(filename, 
                            get_download_btn(filename, catalogue),
                            get_delete_button(filename, catalogue))
    return row

def get_delete_button(filename:str, catalogue="common"):
    return '<button> <a href="delete?catalogue={0}&filename={1}" class="no_decor"> 🪓 </a> </button>'.format(catalogue,filename) 


def get_download_btn(filename:str, catalogue="common"):
    return '<button> <a href="download?catalogue={0}&filename={1}" class="no_decor"> 📥 </a> </button>'.format(catalogue,filename)

def get_documents_table(catalogue:str="common"):
    table = "<table class='centered_table'> <tr>"
    table += "<th> Nazwa </th>"
    table += "<th> Pobierz </th>"
    table += "<th> Usuń </th>"
    table += "</tr>"
 

    for d in get_documents(catalogue):
        table += get_document_table_row(d, catalogue)
    table += "</table>"
    return table

def get_documents(catalogue:str):
    path = os.path.join("volume", catalogue)
    elements = []
    for filename in os.listdir(path):
        elements.append(filename)
    return elements

