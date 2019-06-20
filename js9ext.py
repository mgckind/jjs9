from notebook.utils import url_path_join
from notebook.base.handlers import IPythonHandler,FileFindHandler
import tornado.web
import os
import subprocess
import logging




class MainHandler(IPythonHandler):
    @tornado.web.authenticated
    def get(self):
        self.finish(self.render_template("index_jjs9.html", jid=None, **self.application.settings))

class NewHandler(IPythonHandler):
    @tornado.web.authenticated
    def get(self, jid_id):
        self.finish(self.render_template("index_jjs9.html", jid=jid_id, **self.application.settings))

def load_jupyter_server_extension(nb_server_app):
    """
    Called when the extension is loaded.

    Args:
        nb_server_app (NotebookWebApplication): handle to the Notebook webserver instance.
    """
    logger = logging.getLogger('tornado.access')
    logger.info('Jjs9 - Launching js9Helper')
    localf = os.path.dirname(__file__)
    jhelper = os.path.join(localf, 'js9Helper.js')
    logger.info('Jjs9 - {}'.format(jhelper))
    subprocess.Popen(['node', '{}'.format(jhelper)])
    web_app = nb_server_app.web_app
    web_app.settings["jinja2_env"].loader.searchpath += [os.path.dirname(__file__)]
    host_pattern = '.*$'
    route_pattern_main = url_path_join(web_app.settings['base_url'], '/jjs9/')
    route_pattern_files = url_path_join(web_app.settings['base_url'], '/jjs9/(.*)')
    route_pattern_new = url_path_join(web_app.settings['base_url'], '/jjs9/([0-9a-zA-Z]+)')
    web_app.add_handlers(host_pattern, [(route_pattern_main, MainHandler)])
    web_app.add_handlers(host_pattern, [(route_pattern_new, NewHandler)])
    web_app.add_handlers(host_pattern, [(route_pattern_files, FileFindHandler, {"path": os.path.dirname(__file__)})])

