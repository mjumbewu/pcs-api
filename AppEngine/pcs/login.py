import httplib
import urllib
import Cookie as cookielib
import HTMLParser as htmlparserlib

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from pcs.data.session import Session
from pcs.view.login import LoginHtmlView

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
    
    def login_to_pcs(self, username, password):
        """
        Attempts to login with the given username and password.
        @return: The server response
        @raise: DownloadError if getting response from the server fails.
        """
        conn = httplib.HTTPSConnection(self.__host)
        
        parameters = urllib.urlencode({
            'login[name]': username,
            'login[password]': password})
        conn.request("POST", self.__path,
            parameters)
        conn._follow_redirects = True
        
        try:
            response = conn.getresponse()
        except:
            return "<html><head><title>Please Login</title></head><body></body></html>", []
        
        return response.read(), response.getheaders()
    
    def login_was_successful(self, response_body):
        """
        Check the server response to see whether the login was sucessful.
        @return: Whether the login was successful or not
        @raises: Exception if success of login cannot be discerned
        """
        class LoginParser (htmlparserlib.HTMLParser):

            def __init__(self):
                htmlparserlib.HTMLParser.__init__(self)
                self.in_title = False
                self.title = ''
            
            def handle_starttag(self, tag, attrs):
                if tag.lower() == 'title':
                    self.in_title = True
            
            def handle_data(self, data):
                TRIGGER_TEXT = 'Please Login'
                if self.in_title:
                    self.title += data
            
            def handle_endtag(self, tag):
                if tag.lower() == 'title':
                    self.in_title = False
        
        parser = LoginParser()
        parser.feed(response_body)
        parser.close()
        
        if parser.title == 'Please Login':
            return False
        elif parser.title == 'My Message Manager':
            return True
        else:
            raise Exception('Unknown Login Title: %r' % parser.title)
    
    def save_session(self, session):
        """
        Attempt to save the given login session to a cookie on the user's 
        machine.
        """
        self.response.headers.add_header('Set-Cookie',str('sid='+session.id+'; path=/'))
        self.response.headers.add_header('Set-Cookie',str('suser='+session.user+'; path=/'))
        self.response.headers.add_header('Set-Cookie',str('sname='+session.name+'; path=/'))
        
    def get(self):
        username, password = self.get_credentials()
        pcs_login_body, pcs_login_headers = self.login_to_pcs(username, password)
        
        if self.login_was_successful(pcs_login_body):
            session = Session.FromLoginResponse(username, pcs_login_body, pcs_login_headers)
            response_body = LoginHtmlView.SuccessResponse(session)
            self.save_session(session)
        else:
            response_body = LoginHtmlView.FailureResponse(username)
        
        self.response.out.write(response_body);
        pcs_login_body.replace('-->', 'end_comment')
        self.response.out.write('<!-- %s -->' % pcs_login_body)
        self.response.set_status(200);
    
    def post(self):
        self.get()

class CookiesHandler (webapp.RequestHandler):
    def get(self):
        session = Session.FromRequest(self.request)
        
        self.response.out.write('<html><textarea>')
        self.response.out.write('sid='+session.id)
        self.response.out.write('</textarea></html>')


application = webapp.WSGIApplication(
        [('/login', LoginHandler),
         ('/cookies', CookiesHandler)],
        debug=True)

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
