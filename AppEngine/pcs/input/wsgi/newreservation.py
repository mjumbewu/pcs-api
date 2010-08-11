import httplib
import urllib
import Cookie as cookielib

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from pcs.data.session import Session
from util.BeautifulSoup import BeautifulSoup

class PcsTimeBlock (object):
    def __init__(self, start, end):
        self.start = start
        self.end = end
    
    def __contains__(self, time):
        return start <= time <= end;
    
class PcsPod (object):
    def __init__(self):
        self.name = ''
        self.location = None

class PcsVehicle (object):
    def __init__(self):
        self.booked_times = []
        self.pod = None

class NewReservationHtmlView (object):
    @staticmethod
    def AvailabilityResponse(session, start_time, end_time):
        return """
<!DOCTYPE html>

<html>
  <head>
    <title>Check Vehicle Availability</title>
  </head>
  
  <body>
    <form action="/newreservation" method="POST">
      Start <label for="start_date">on</label> <input type="text" id="start_date" value="%s" />
            <label for="start_time">at</label> <input type="text" id="start_time" value="%s" /><br />
      End <label for="end_date">on</label> <input type="text" id="end_date" value="%s" />
          <label for="end_time">at</label> <input type="text" id="end_time" value="%s" /><br />
    </form>
  </body>
</html>
        """ % (
            start_time[0],
            start_time[1],
            end_time[0],
            end_time[1])
    
class NewReservationHandler (webapp.RequestHandler):
    def __init__(self, host="reservations.phillycarshare.org",
                 path="/my_reservations.php"):
        super(NewReservationHandler, self).__init__()
        self.__host = host
        self.__path = path
    
    def get_host_connection(self, scheme, host):
        """
        Create a connection to the host according to the given scheme/protocol.
        Supported schemes are http and https.
        """
        if scheme == 'https':
            self.response.out.write('https://')
            conn = httplib.HTTPSConnection(host)
        elif scheme == 'http':
            self.response.out.write('http://')
            conn = httplib.HTTPConnection(host)
        else:
            raise Exception()
        
        self.response.out.write(host)
        return conn
    
    def get_full_path(self, path, query):
        """
        Join the path and the query into a single URL path string.
        """
        if query:
            fullpath = '?'.join([path,query])
        else:
            fullpath = path
        self.response.out.write(fullpath)
        self.response.out.write('\n')
        
        return fullpath
        
    def parse_html(self, html_body):
        """
        Generate a document tree from html text.
        """
        soup = BeautifulSoup(html_body)
        return soup
    
    def get_elements_by_attr(self, parent, tag_name, attr_name, attr_value):
        """
        Get the child elements of parent that are of the given tag and have
        attributes with the given name set equal to the given value.
        """
        elements = parent.findAll(tag_name, {attr_name:attr_value})
#        elements = filter(
#            lambda elem: elem.getAttribute(attr_name) == attr_value)
        
        return elements
    
    def get_time_from_document(self, document, date_id, time_id):
        date_elements = self.get_elements_by_attr(
            document, 'input', 'id', date_id)
        assert len(date_elements) == 1, str(date_elements)
        date = date_elements[0]['value']
        
        START_TIME_ID = 'search_results_results_filter__range__start_time_'
        time_elements = self.get_elements_by_attr(
            document, 'select', 'id', time_id)
        assert len(time_elements) == 1, str(time_elements)
        time_options = self.get_elements_by_attr(
            time_elements[0], 'option', 'selected', 'selected')
        assert len(time_options) == 1, str(time_options)
        time = time_options[0]['value']
        
        return (date, time)
        
    def get_start_time(self, document):
        START_DATE_ID = 'search_results_results_filter__range__start_date__date_'
        START_TIME_ID = 'search_results_results_filter__range__start_time_'
        
        return self.get_time_from_document(document, START_DATE_ID, START_TIME_ID)
        
    def get_end_time(self, document):
        END_DATE_ID = 'search_results_results_filter__range__end_date__date_'
        END_TIME_ID = 'search_results_results_filter__range__end_time_'
        
        return self.get_time_from_document(document, END_DATE_ID, END_TIME_ID)
    
    def check_availability(self, session, scheme='http', host=None, path=None, forwards=0):
        if forwards >= 10:
            return '', []
        
        if host is None: host = self.__host
        if path is None: path = self.__path
        
        conn = self.get_host_connection(scheme, host)
        conn.request('GET', path, None, {'Cookie':'sid='+session.id})
        response = conn.getresponse()
        
        if response.status == 302 and forwards < 10:
            location = response.getheader('location')
            import urlparse
            
            scheme, host, path, query, _ = urlparse.urlsplit(location)
            fullpath = self.get_full_path(path, query)
            return self.check_availability(session, scheme, host, path, forwards+1)
        else:
            return response.read(), response.getheaders()
        
    def get(self):
        session = Session.FromRequest(self.request)
        pcs_availability_body, pcs_availability_headers = \
            self.check_availability(session)
        
        pcs_availability_doc = self.parse_html(pcs_availability_body)
        start_time = self.get_start_time(pcs_availability_doc)
        end_time = self.get_end_time(pcs_availability_doc)
        
        response_body = NewReservationHtmlView.AvailabilityResponse(session, start_time, end_time)
        
        self.response.out.write(response_body)
        self.response.out.write('<!-- %s -->' %
            pcs_availability_body.replace('-->', 'end_comment'))
    

application = webapp.WSGIApplication(
        [('/newreservation', NewReservationHandler)],
        debug=True)

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
