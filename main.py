import cherrypy
from cherrypy.lib import static, sessions
import resources.shards as Shards
import os
from hashlib import sha256
import user_tools as UTools
import page_tools as PTools
import file_tools as FTools
import config

volume_path = config.path_to_volume


conf = { '/' : { 'tools.sessions.on': True },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': os.path.abspath("./resources")
        }
        }

class StoroDrive(object):
    def _upload_file(self,file, catalogue, relative_path = None):
        #file_path = FTools.get_catalogue_path(catalogue)
        FTools.insert_file(file, catalogue, relative_path)

    def _create_user_session(self, username, password):
        #pswd_hash = sha256(password.encode)
        error = None
        if not UTools.user_exists(username):
            error = "Użytkownik nie istnieje!"
        elif UTools.check_password(username, password):
                cherrypy.session['user'] = UTools.get_user(username)
        else: error = "Hasło niepoprawne!"
        return error

    @cherrypy.expose
    def index(self, error = None):
        data = {}
        if error is not None:
            data['error'] = error
        if 'user' in cherrypy.session:
            data['user'] = cherrypy.session['user']
            data['uname'] = cherrypy.session['user']['username']
            data['catalogue'] = cherrypy.session['user']['catalogue']
        return PTools.page_from_template('resources/index.html', data)

    @cherrypy.expose
    def storage(self, catalogue="common", relative_path=None, error = None):
        cat_name = FTools.get_catalogue_name(catalogue)
        files = FTools.get_all_files(catalogue, relative_path)
        directories = FTools.get_all_directories(catalogue, relative_path)
        data = { "catalogue_id" : catalogue, "catalogue_name" : cat_name}
        parent_path = None
        if relative_path == '':
            relative_path = None
        if relative_path is not None:
            parent_path = FTools.get_parent_path(relative_path)
        if error is not None:
            data['error'] = error
        if 'user' in cherrypy.session:
            data['user'] = cherrypy.session['user']
        if len(files) > 0:
            data['files'] = files
        if len(directories)>0:
            data['directories'] = directories
        if relative_path is not None:
            data['relative_path'] = relative_path
            data['relative_path_split'] = FTools.split_path(relative_path)
        if parent_path is not None:
            data['parent_path'] = parent_path
        return  PTools.page_from_template('resources/storage.html', data)

    @cherrypy.expose
    def login(self, username, password):
        error_msg = self._create_user_session(username,password)
        return self.index(error_msg)

    @cherrypy.expose
    def logout(self):
        cherrypy.session.regenerate()
        return self.index()

    @cherrypy.expose
    def register(self, error = None):
        data = {}
        if error is not None:
            data['error'] = error
        return PTools.page_from_template('resources/register.html', data)

    @cherrypy.expose
    def create_user(self, username, password, confirm):
        if UTools.user_exists(username):
            return self.register(error="Użytkownik " + username + " już istnieje!")
        error = None
        if(password == confirm):
            UTools.create_user(username,password)
            error = self._create_user_session(username, password)
        return self.index(error)
    

    @cherrypy.expose
    def download(self, filename, catalogue="common", relative_path=None):
        return static.serve_file(
            FTools.get_download_file_path(filename,catalogue,relative_path),
            'application/x-download',
            'attachment',
            filename,
        )
    
    def download_multiple(self, filenames, catalogue, relative_path=None):
        filename = FTools.get_multiple_files_zip(filenames,catalogue,relative_path)
        name = os.path.basename(filename)
        return static.serve_file(
            filename,
            'application/x-download',
            'attachment',
            name,
        )

    def get_url_suffix(self, catalogue, relative_path= None):
        if relative_path is not None:
            return '?catalogue='+catalogue+'&relative_path=' + relative_path
        else: return '?catalogue='+catalogue

    @cherrypy.expose
    def upload(self, file, catalogue, relative_path= None):
        if isinstance(file, list):
            for f in file:
                self._upload_file(f,catalogue, relative_path)
        else:
            self._upload_file(file,catalogue, relative_path)
        raise cherrypy.HTTPRedirect('/storage'+self.get_url_suffix(catalogue,relative_path))

    @cherrypy.expose
    def createDirectory(self, catalogue, name, relative_path= None):
        FTools.create_directory(name,catalogue,relative_path)
        return self.storage(catalogue, relative_path)

    @cherrypy.expose
    def delete(self, filename, catalogue="common", relative_path=None):
        error = FTools.remove_file(filename, catalogue,relative_path)
        return self.storage(catalogue, relative_path, error)
    
    @cherrypy.expose
    def delete_directory(self, directory_name, catalogue="common", relative_path=None):
        error = FTools.remove_directory(directory_name, catalogue,relative_path)
        return self.storage(catalogue, relative_path, error)

    @cherrypy.expose
    def batch_operation(self, catalogue, relative_path=None, delete=None, download=None, **kwargs):
        print(kwargs)
        if download is not None:
            names = [ key for key in kwargs ] 
            return self.download_multiple(names,catalogue,relative_path) 
        if delete is not None:
            for key in kwargs:
                self.delete(key,catalogue,relative_path) 
        raise cherrypy.HTTPRedirect('/storage'+self.get_url_suffix(catalogue,relative_path))
        

if __name__ == '__main__':
    cherrypy.quickstart(StoroDrive(), "/" ,config=conf)