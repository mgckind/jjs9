import tornado.ioloop
import tornado.web
import os
import subprocess

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html", jid=None)

class NewHandler(tornado.web.RequestHandler):
    def get(self, jid_id):
        self.render("index.html", jid=jid_id)

settings = {
    #"static_path": os.path.join(os.path.dirname(__file__), "static"),
    "static_path": '.',
}

def make_app():
    return tornado.web.Application([
        (r"/jjs9/", MainHandler),
        (r"/jjs9/([0-9a-zA-Z]+)", NewHandler),
        (r"/jjs9/(.*)", tornado.web.StaticFileHandler, {"path": os.path.dirname(__file__), "default_filename": "js9Prefs.json"}),
        (r"/jjs9/(.*)", tornado.web.StaticFileHandler, {"path": os.path.dirname(__file__), "default_filename": "favicon.ico"})
    ], **settings)

if __name__ == '__main__':
    subprocess.Popen(['node', 'js9Helper.js'])
    port = 8000
    app = make_app()
    app.listen(port)
    print('Listening at port {}'.format(port))
    tornado.ioloop.IOLoop.current().start()
