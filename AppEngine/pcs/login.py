import httplib
import Cookie as cookie

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from pcs.session import Session

class LoginHandler (webapp.RequestHandler):
    """
    Handles requests sent to the list of products
    """
    def __init__(self, host="reservations.phillycarshare.org",
                 path="/my_reservations.php"):
        super(LoginHandler, self).__init__()
        self.__host = host
        self.__path = path
    
    def get_credentials(self):
        username = self.request.get('username')
        password = self.request.get('password')
        
        return username, password
    
    def login(self, username, password):
        loginConn = httplib.HTTPSConnection(self.__host)
        loginCookie = cookie.SimpleCookie()
        
        loginParameters = '&'.join([
            'login[name]=%s',
            'login[password]=%s',
            'login[tid]=2']) % (username, password)
        loginConn.request("POST", self.__path,
            loginParameters)
        loginResponse = loginConn.getresponse()
        
        loginCookie.load(loginResponse.getheader('set-cookie'))
        loginSession = Session(loginCookie['sid'].value)
        
        for header, value in loginResponse.getheaders():
            self.response.headers.add_header(header, value)
        
        return loginSession
        
    def get(self):
        username, password = self.get_credentials()
        session = self.login(username, password)
        
        response_body = """
<!DOCTYPE html>

<html>
  <head>
    <title>Logged In</title>
  </head>
  
  <body>
    <p><a href="%s">Make a New Reservation</a></p>
    <p><a href="%s">Manage Existing Reservations</a></p>
    <p><a href="%s">View Messages</a></p>
    <p><a href="%s">Manage Account Info</a></p>
    <p><a href="%s">Give Feedback</a></p>
  </body>
</html>
          """ % (session.get_new_reservation_url(),
                 session.get_existing_reservations_url(),
                 session.get_messages_url(),
                 session.get_account_info_url(),
                 session.get_feedback_url())
        
        self.response.out.write(response_body);
        self.response.set_status(200);

class MessagesHandler (webapp.RequestHandler):
    pass

class NewReservationHandler (webapp.RequestHandler):
    def __init__(self, host="reservations.phillycarshare.org",
                 path="/my_reservations.php?_r=1"):
        super(NewReservationHandler, self).__init__()
        self.__host = host
        self.__path = path
    
    def get(self):
        session = Session.FromRequest(self.request)
        
        # fetch_new_reservation_page
        conn = httplib.HTTPSConnection(self.__host)
        conn.request('GET', self.__path, headers={'cookie':'sid='+session.id})
        response = conn.getresponse()
        
        self.response.out.write(response.read())
    

application = webapp.WSGIApplication(
        [('/login', LoginHandler),
         ('/messages', MessagesHandler),
         ('/newreservation', NewReservationHandler)],
        debug=True)

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
