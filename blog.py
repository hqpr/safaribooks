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
 
 
client = riak.RiakClient(pb_port=8087, protocol='pbc')
post = {
    'post_id': 1,
    'name': "Black Hole",
    'title': "Black Hole Article",
    'author': "Wikipedia",
    'created_date': "2013-10-01 14:30:26",
    'body': "A black hole is a region of spacetime from which gravity prevents anything, including light, from escaping.[1] The theory of general relativity predicts that a sufficiently compact mass will deform spacetime to form a black hole.[2] The boundary of the region from which no escape is possible is called the event horizon. Although crossing the event horizon has enormous effect on the fate of the object crossing it, it appears to have no locally detectable features. In many ways a black hole acts like an ideal black body, as it reflects no light.[3][4] Moreover, quantum field theory in curved spacetime predicts that event horizons emit Hawking radiation, with the same spectrum as a black body of a temperature inversely proportional to its mass. This temperature is on the order of billionths of a kelvin for black holes of stellar mass, making it all but impossible to observe."
}
 
# Creating Buckets
post_bucket = client.bucket('Customers')
 
# Storing Data
cr = post_bucket.new(str(post['post_id']), data=post)
cr.store()
 
# key1 = myBucket.new('one', data=val1)
 
 
define("port", default=8000, help="run on the given port", type=int)
 
 
class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render(
            "index.html",
            title="Home Page",
            header="Books that are great",
            books=[
                post_bucket.get('1').data
            ]
        )
 
 
class PostHandler(tornado.web.RequestHandler):
    def get(self, post_id):
        widget = post_bucket.get(post_id).data
        self.render("single.html", data=widget)
 
 
class AddPostHandler(tornado.web.RequestHandler):
    def post(self, widget_id):
        widget = post_bucket(widget_id)
        widget['foo'] = self.get_argument('foo')
        # save_to_db(widget)
 
 
if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[(r'/', IndexHandler), (r'/add', AddPostHandler), (r'/post/(\d+)', PostHandler)],
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        debug=True
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()