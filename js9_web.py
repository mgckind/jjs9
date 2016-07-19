import tornado.ioloop
import tornado.web
import os

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html",jid=None)

class NewHandler(tornado.web.RequestHandler):
    def get(self, jid_id):
        self.render("index.html", jid=jid_id)

settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
}
def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/new/([0-9a-zA-Z]+)", NewHandler),
    ], **settings)

if __name__ == "__main__":
    app = make_app()
    app.listen(8000)
    tornado.ioloop.IOLoop.current().start()
