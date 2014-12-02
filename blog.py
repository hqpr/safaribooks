import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options
import riak
 
# mongodb example
# https://www.safaribooksonline.com/library/view/introduction-to-tornado/9781449312787/ch04.html
# riak api
# http://docs.basho.com/riak/latest/dev/taste-of-riak/querying-python/
# http://books.google.com.ua/books?id=B-krWzb6KMQC&pg=PA9&lpg=PA9&dq=save_to_db+tornado&source=bl&ots=3FYi72dccm&sig=trRQQpd7o0cD0mNXZtv-8h8q4H4&hl=ru&sa=X&ei=qRx-VNXbL8bnywPBp4LYCQ&ved=0CCEQ6AEwAA#v=onepage&q=save_to_db%20tornado&f=false
 
 
client = riak.RiakClient(pb_port=8087, protocol='pbc')
post = {
    'post_id': 1,
    'name': "Black Hole",
    'title': "Black Hole Article",
    'author': "Wikipedia",
    'created_date': "2014-12-02 14:30:26",
    'body': "A black hole is a region of spacetime from which gravity prevents anything, including light, from escaping.[1] The theory of general relativity predicts that a sufficiently compact mass will deform spacetime to form a black hole.[2] The boundary of the region from which no escape is possible is called the event horizon. Although crossing the event horizon has enormous effect on the fate of the object crossing it, it appears to have no locally detectable features. In many ways a black hole acts like an ideal black body, as it reflects no light.[3][4] Moreover, quantum field theory in curved spacetime predicts that event horizons emit Hawking radiation, with the same spectrum as a black body of a temperature inversely proportional to its mass. This temperature is on the order of billionths of a kelvin for black holes of stellar mass, making it all but impossible to observe."
}
 
post_bucket = client.bucket('Posts')
 
cr = post_bucket.new(str(post['post_id']), data=post)
cr.store()
 
# key1 = myBucket.new('one', data=val1)
 
 
define("port", default=8000, help="run on the given port", type=int)


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

 
class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render(
            "index.html",
            title="Home Page",
            header="All entries",
            # data=post_bucket.get('1')
            data=post_bucket.get_index(self, '1')
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
             'author': author}
        entry = post_bucket.new('2', data=d)
        entry.store()
        self.render('add_post.html', data=d)



if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()