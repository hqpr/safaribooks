import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options
import riak
import datetime
 
# mongodb example
# https://www.safaribooksonline.com/library/view/introduction-to-tornado/9781449312787/ch04.html
# riak api
# http://docs.basho.com/riak/latest/dev/taste-of-riak/querying-python/ - samples of data
# http://books.google.com.ua/books?id=B-krWzb6KMQC&pg=PA9&lpg=PA9&dq=save_to_db+tornado&source=bl&ots=3FYi72dccm&sig=trRQQpd7o0cD0mNXZtv-8h8q4H4&hl=ru&sa=X&ei=qRx-VNXbL8bnywPBp4LYCQ&ved=0CCEQ6AEwAA#v=onepage&q=save_to_db%20tornado&f=false
 
port = 8087

client = riak.RiakClient(pb_port=port, protocol='pbc')
post = {
    'type': 'post',
    'post_id': 1,
    'name': "Black Hole",
    'title': "Black Hole Article",
    'author': "Wikipedia",
    'created_date': "2014-12-02 14:30:26",
    'body': "A black hole is a region of spacetime from which gravity prevents anything, including light, "
            "from escaping. The theory of general relativity predicts that a sufficiently compact mass will "
            "deform spacetime to form a black hole."
}
 
post_bucket = client.bucket('Posts')
cr = post_bucket.new(str(post['post_id']), data=post)
cr.store()

define("port", default=8000, help="run on the given port", type=int)

# for keys in post_bucket.stream_keys():
#     for key in keys:
#         print('Deleting %s' % key)
#         post_bucket.delete(key)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', IndexHandler),
            (r'/add', AddPostHandler),
            (r'/post/(\d+)', PostHandler)
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            debug=True,
        )
        tornado.web.Application.__init__(self, handlers, **settings)


# https://riak-python-client.readthedocs.org/en/1.5-stable/tutorial.html
class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        lst = []
        x = post_bucket.get_keys()
        for i in range(1, len(x)+1):
            entries = post_bucket.get(str(i)).data
            lst.append(entries)

        self.render(
            "index.html",
            title="Home Page",
            data=lst
        )

 
class PostHandler(tornado.web.RequestHandler):
    def get(self, post_id):
        widget = post_bucket.get(post_id).data
        self.render("single.html", data=widget)


class AddPostHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('add_post.html')

    def post(self):
        name = self.get_argument('name')
        body = self.get_argument('body')
        author = self.get_argument('author')
        d = {'name': name,
             'body': body,
             'author': author,
             'created_date': str(datetime.date.today()),
             'type': 'post'}
        new_key = sorted(post_bucket.get_keys())
        k = int(new_key[-1]) + 1
        entry = post_bucket.new(str(k), data=d)
        entry.store()
        self.redirect('/post/%s' % entry.key)


if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()