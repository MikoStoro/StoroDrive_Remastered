import cherrypy
from cherrypy.lib import static, sessions
from tinydb import TinyDB, Query
from jinja2 import Template
import resources.shards as Shards
import os
from hashlib import sha256
import uuid

localDir = os.path.dirname(__file__)
absDir = os.path.join(os.getcwd(), localDir)

user_db = TinyDB(os.path.abspath("./databases/users.json"))

conf={
        
       '/style.css':
                    { 'tools.staticfile.on':True,
                      'tools.staticfile.filename': os.path.abspath("./resources/style.css"),
                    },
        '/panels.css':
                    { 'tools.staticfile.on':True,
                      'tools.staticfile.filename': os.path.abspath("./resources/panels.css"),
                    },
        '/dragDrop.js':
                    { 'tools.staticfile.on':True,
                      'tools.staticfile.filename': os.path.abspath("./resources/dragDrop.js"),
                    },
        '/panels.js':
                    { 'tools.staticfile.on':True,
                      'tools.staticfile.filename': os.path.abspath("./resources/panels.js"),
                    }
    }
conf = { '/' : { 'tools.sessions.on': True },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': os.path.abspath("./resources")
        }
        }

class StoroDrive(object):


    @cherrypy.expose
    def index(self):
        page_text = open('resources/index.html', encoding='utf-8').read()
        template = Template(page_text)
        data = {}
        if 'user' in cherrypy.session:
            data['uname'] = cherrypy.session['user']['username']
            data['catalogue'] = cherrypy.session['user']['catalogue']
        return template.render(data)

    @cherrypy.expose
    def storage(self, catalogue="common"):
        path = os.path.abspath("./volume/" + catalogue)
        if not os.path.exists(path):
            os.makedirs(path, mode=0o777, exist_ok=False)
        content = Shards.get_documents_table(catalogue)
        data = { "id" : catalogue, "content" : content}
        page_text = open('resources/storage.html', encoding='utf-8').read()
        template = Template(page_text)
        return template.render(data)

    @cherrypy.expose
    def login(self, username, password):
        #pswd_hash = sha256(password.encode)
        pswd_hash = password
        user_record = user_db.search(Query().username == username)[0]
        print(user_record)
        if user_record["pswd_hash"] == pswd_hash:
            cherrypy.session['user'] = user_record
        return self.index()

    @cherrypy.expose
    def register(self):
        return open('resources/register.html', encoding='utf-8')

    @cherrypy.expose
    def create_user(self, username, password, confirm):
        if(password == confirm):
            #pswd_hash = sha256(password.encode())
            pswd_hash = password
            user_db.insert({
                'username': username, 
                'pswd_hash': pswd_hash, 
                'catalogue': str(uuid.uuid1()), 
                'user_id': str(uuid.uuid1())
            })
        return self.index()
    

    @cherrypy.expose
    def download(self, filename, catalogue="common"):
        path = os.path.join(absDir,"volume",catalogue, filename)
        return static.serve_file(
            path,
            'application/x-download',
            'attachment',
            os.path.basename(path),
        )

    def _upload_file(self,file, catalogue):
        upload_path = os.path.join(absDir,"volume",catalogue, file.filename)
        with open(upload_path, 'wb') as out:
            while True:
                data = file.file.read(8192)
                if not data:
                    break
                out.write(data)

    @cherrypy.expose
    def upload(self, file, catalogue):
        if isinstance(file, list):
            for f in file:
                self._upload_file(f,catalogue)
        else:
            self._upload_file(file,catalogue)
        return self.storage(catalogue)

    @cherrypy.expose
    def delete(self, filename, catalogue):
        delete_path = os.path.join(absDir,"volume",catalogue, filename)
        os.remove(delete_path)
        return self.storage(catalogue)

if __name__ == '__main__':
    cherrypy.quickstart(StoroDrive(), "/" ,config=conf)