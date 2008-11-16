import os
import cgi
import datetime
import uuid
import wsgiref.handlers

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp import template

class KmlData(db.Model):
	kml = db.TextProperty()
	uuid = db.StringProperty(multiline=False)
	
	def reset_uuid(self):
		self.uuid = str(uuid.uuid1())

class MainPage(webapp.RequestHandler):
  def get(self):
    cookie_str = self.request.headers.get('Cookie')
    kml_data = self.find_kml_data()
    template_values = {
      'key': kml_data.key(),
      'kml_data': kml_data,
      'lat': 41.875696,
      'long': -87.624207,
      'zoom_level': 1,
      'google_map_key': 'ABQIAAAAku8DcWMwO9f8YVy4Qbom3RSmOB7sRPneGnHdBjmMnq4YTUhpZxQLtjgcKvFYOImH-uVUqU8bi4sEOQ'
    }
    path = os.path.join(os.path.dirname(__file__), 'index.html')
    self.response.out.write(template.render(path, template_values))
  
  def post(self):
		key_id = self.request.get('key')
		kml_data = db.get(db.Key(key_id))
		kml_data.kml = self.request.get('kml')
		kml_data.put()
		self.redirect('/')
  
  def find_kml_data(self):
    if self.request.cookies.has_key('key_id'): 
	    key_id = self.request.cookies['key_id']
	    kml_data = db.get(db.Key(key_id))
    else:
			kml_data = KmlData()
			kml_data.reset_uuid()
			kml_data.kml = ''
			kml_data.put()
			self.create_cookie('key_id', kml_data.key())
    return kml_data
  
  def create_cookie(self, key, value):
		expires = datetime.datetime.now() + datetime.timedelta(minutes=5)
		expires_rfc822 = expires.strftime('%a, %d %b %Y %H:%M:%S -0800')
		self.response.headers.add_header('Set-Cookie', '%s=%s; expires=%s' % (key, value, expires_rfc822))

class KmlFile(webapp.RequestHandler):
	def get(self, uuid):
		try:
				kml_datas = KmlData.gql("WHERE uuid = :1", uuid) #db.get(uuid=uuid)
				kml_data = kml_datas.get()
				self.response.headers['Content-Type'] = 'data/xml'
				self.response.out.write(kml_data.kml)
		except Exception:
				self.error(500)

def main():
  application = webapp.WSGIApplication(
                                       [('/', MainPage), (r'/get_kml/\d+/(?P<uuid_to_find>.+)\.kml', KmlFile)], debug=True)
  wsgiref.handlers.CGIHandler().run(application)

if __name__ == "__main__":
  main()