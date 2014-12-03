<<<<<<< HEAD
__author__ = 'o.dubnyak'
=======
import riak

client = riak.RiakClient(pb_port=8087, protocol='pbc')
post_bucket = client.bucket('Posts')
post = {
    'post_id': 1,
    'name': "Black Hole",
    'title': "Black Hole Article",
    'author': "Wikipedia",
    'created_date': "2014-12-02 14:30:26",
    'body': "A black hole is a region of spacetime from which gravity prevents anything, including light, from escaping.[1] The theory of general relativity predicts that a sufficiently compact mass will deform spacetime to form a black hole.[2] The boundary of the region from which no escape is possible is called the event horizon. Although crossing the event horizon has enormous effect on the fate of the object crossing it, it appears to have no locally detectable features. In many ways a black hole acts like an ideal black body, as it reflects no light.[3][4] Moreover, quantum field theory in curved spacetime predicts that event horizons emit Hawking radiation, with the same spectrum as a black body of a temperature inversely proportional to its mass. This temperature is on the order of billionths of a kelvin for black holes of stellar mass, making it all but impossible to observe."
}
cr = post_bucket.new(str(post['post_id']), data=post)
cr.store()
>>>>>>> 7f2666abc38984236afce6d4652212ea2eab3d89
