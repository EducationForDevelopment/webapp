


import jinja2
import os
import webapp2

from google.appengine.api import users
# Import the NDB data modeling API
from google.appengine.ext import ndb

import httplib2
import logging

from apiclient import discovery
from oauth2client import appengine
from oauth2client import client
from google.appengine.api import memcache
from google.appengine.api import oauth



DEFAULT_GUESTBOOK_NAME = 'doubtbook_test0'

# We set a parent key on the 'Greetings' to ensure that they are all in the same
# entity group. Queries across the single entity group will be consistent.
# However, the write rate should be limited to ~1/second.

#def guestbook_key(guestbook_name='default_guestbook'):
def guestbook_key(guestbook_name=DEFAULT_GUESTBOOK_NAME):
    """Constructs a Datastore key for a Guestbook entity with guestbook_name.
        (for Datastore usage review, see https://developers.google.com/appengine/docs/python/gettingstartedpython27/usingdatastore)"""
    return ndb.Key('Guestbook', guestbook_name)

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


# # CLIENT_SECRETS, name of a file containing the OAuth 2.0 information for this
# # application, including client_id and client_secret, which are found
# # on the API Access tab on the Google APIs
# # Console <http://code.google.com/apis/console>
# CLIENT_SECRETS = os.path.join(os.path.dirname(__file__), 'client_secrets.json')
#
# # Helpful message to display in the browser if the CLIENT_SECRETS file
# # is missing.
# MISSING_CLIENT_SECRETS_MESSAGE = """
# <h1>Warning: Please configure OAuth 2.0</h1>
# <p>To make this sample run you will need to populate the client_secrets.json file
# found at:</p>
# <p> <code>%s</code>. </p>
# <p>with information found on the <a
# href="https://code.google.com/apis/console">APIs Console</a>. </p>
# """ % CLIENT_SECRETS
# http = httplib2.Http(memcache)
# service = discovery.build('plus', 'v1', http=http)
# decorator = appengine.oauth2decorator_from_clientsecrets(
#     CLIENT_SECRETS,
#     scope=[
#       'https://www.googleapis.com/auth/plus.login',
#       'https://www.googleapis.com/auth/plus.me',
#       'https://www.googleapis.com/auth/userinfo.email',
#       'https://www.googleapis.com/auth/userinfo.profile',
#     ],
#     message=MISSING_CLIENT_SECRETS_MESSAGE)
# people_resource = service.people()
# people_document = people_resource.get(userId='me').execute()



class Greeting(ndb.Model):
    """Models an individual Guestbook entry."""
    author = ndb.UserProperty()
    content = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)



class MainPage(webapp2.RequestHandler):

    def get(self):

        self.response.write('<html><body>')
        guestbook_name = self.request.get('guestbook_name', DEFAULT_GUESTBOOK_NAME)

        # Ancestor Queries, as shown here, are strongly consistent with the High Replication Datastore. Queries that span entity groups are eventually
        # consistent. If we omitted the ancestor from this query there would be a slight chance that Greeting that had just been written would not show up in a query.
        greetings_query = Greeting.query(ancestor=guestbook_key(guestbook_name)).order(-Greeting.date)
        greetings = greetings_query.fetch(10)

'''        for greeting in greetings:
            if greeting.author:
                self.response.write(
                        '<b>%s</b> wrote:' % greeting.author.nickname())
            else:
                self.response.write('An anonymous person wrote:')
            self.response.write('<blockquote>%s</blockquote>' %
                                cgi.escape(greeting.content))
'''


        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'LOGOUT' #'Logooooout'
            #url_linktext1 = str(users.get_current_user()) + ', welcome to E4D! '   #'welcome'
            url_linktext1 = ''
            user0 = users.get_current_user()
            user0id = user0.user_id()
            url_linktext2 = 'welcome, ' + str(user0.nickname()) + '! '


        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'LOGIN to begin!'  #'Logiiiiin'
            url_linktext1 = 'E4D.start.'
            url_linktext2 = ''
            user0 = ''
            user0id = ''

        #CHECK THIS IF PROBLEMS
        # Write the submission form and the footer of the page
        sign_query_params = urllib.urlencode({'guestbook_name': guestbook_name})
        self.response.write(MAIN_PAGE_FOOTER_TEMPLATE %
                            (sign_query_params, cgi.escape(guestbook_name),
                             url, url_linktext))


        template = jinja_environment.get_template('index.html')
        self.response.out.write(template.render(greetings=greetings,
                                                url=url,
                                                url_linktext=url_linktext,
                                                url_linktext1=url_linktext1,
                                                url_linktext2=url_linktext2,
                                                user0=user0))

class Guestbook(webapp2.RequestHandler):
    def post(self):
        # (as noted above) We set the same parent key on the 'Greeting' to ensure each Greeting is in the same entity group. Queries across the single entity group
        # will be consistent. However, the write rate to a single entity group should be limited to ~1/second.
        guestbook_name = self.request.get('guestbook_name', DEFAULT_GUESTBOOK_NAME)

        greeting = Greeting(parent=guestbook_key(guestbook_name))

        if users.get_current_user():
            greeting.author = users.get_current_user()

        greeting.content = self.request.get('content')
        greeting.put()
        #self.redirect('/')
        query_params = {'guestbook_name': guestbook_name}
        self.redirect('/?' + urllib.urlencode(query_params))



application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/index\.html', MainPage),
    ('/sign', Guestbook),
], debug=True)




#from: http://stackoverflow.com/questions/13555534/python-2-7-gae-app-yaml-getting-404-error
#It looks like your app variable in index does not have a handler for index.html. For instance:
#
#  app = webapp2.WSGIApplication([('/', MainPage)])
#
#If your application gets routed to index, it will look through the handlers defined and try to find
#a match to /index.html. In this example, if you go to /, it will work fine since that handler is defined;
#however if you go to index.html, GAE doesn't know which class to call, and it therefore returns a 404.
#As a simple test, try
#
#  app = webapp2.WSGIApplication([
#      ('/', MainPage),
#      ('/index\.html', MainPage)
#  ])
#
