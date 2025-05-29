import cherrypy
from cherrypy.lib import static
import tinydb
from jinja2 import Template
import resources.shards as Shards
import os

localDir = os.path.dirname(__file__)
absDir = os.path.join(os.getcwd(), localDir)

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

class StoroDrive(object):

    @cherrypy.expose
    def index(self):
        return open('resources/index.html', encoding='utf-8')

    @cherrypy.expose
    def storage(self, catalogue="common"):
        content = Shards.get_documents(catalogue)
        data = { "id" : catalogue, "content" : content}
        page_text = open('resources/storage.html', encoding='utf-8').read()
        template = Template(page_text)
        return template.render(data)

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

if __name__ == '__main__':
    cherrypy.quickstart(StoroDrive(), config=conf)