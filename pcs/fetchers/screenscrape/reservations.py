import datetime
import httplib
import re
import urllib
import Cookie as cookielib
import HTMLParser as htmlparserlib
import time

try:
    import json
except ImportError:
    from django.utils import simplejson as json

from pcs.data.pod import Pod
from pcs.data.vehicle import PriceEstimate
from pcs.data.vehicle import Vehicle
from pcs.data.vehicle import VehicleModel
from pcs.data.reservation import Reservation
from pcs.fetchers import _ReservationsSourceInterface
from pcs.fetchers.screenscrape import ScreenscrapeParseError
from pcs.fetchers.screenscrape.pcsconnection import PcsConnection
from pcs.fetchers.screenscrape.availability import AvailabilityScreenscrapeSource
from util.abstract import override
from util.BeautifulSoup import BeautifulSoup
from util.TimeZone import Eastern
from util.TimeZone import to_timestamp
from util.TimeZone import to_pcs_date_time

class ReservationsScreenscrapeSource (_ReservationsSourceInterface):
    
    def __init__(self, host="reservations.phillycarshare.org",
                 upcoming_path="/my_reservations.php?mv_action=main",
                 past_path="/my_reservations.php?mv_action=main",
                 price_path="/ajax_estimate.php?slider=true",
                 newres_path="/lightbox.php?mv_action=add",
                 detail_path="/my_reservations.php?mv_action=confirm",
                 confirm_path="/my_reservations.php?mv_action=confirm",
                 vehicle_source = AvailabilityScreenscrapeSource()):
        super(ReservationsScreenscrapeSource, self).__init__()
        self.__host = host
        self.__upcoming_path = upcoming_path
        self.__past_path = past_path
        self.__price_path = price_path
        self.__newres_path = newres_path
        self.__detail_path = detail_path
        self.__confirm_path = confirm_path
        
        self.vehicle_source = vehicle_source
    
    def get_driver_query(self, driverid):
        query = "main[multi_filter][driver_pk]=%s" % (driverid)
        return query
    
    def get_datefilter_query(self, year, month):
        query = "main[multi_filter][history][yearmonth]=%s%02d" % (year, month)
        return query
    
    def upcoming_reservations_from_pcs(self, conn, sessionid):
        host = self.__host
        path = self.__upcoming_path
        
        headers = {
            'Cookie': 'sid=%s' % sessionid}
        query = ''
        connector = ''
        
        url = "http://%s%s%s%s" % (host, path, connector, query)
        
        response = conn.request(url, "GET", {}, headers)
        return (response.read(), response.getheaders())
    
    def past_reservations_from_pcs(self, conn, sessionid, year, month):
        host = self.__host
        path = self.__past_path
        
        headers = {
            'Cookie': 'sid=%s' % sessionid}
        query = ''
        query += self.get_datefilter_query(year, month)
        connector = '&' if '?' in path else '?'
        
        url = "http://%s%s%s%s" % (host, path, connector, query)
        
        response = conn.request(url, "GET", {}, headers)
        return (response.read(), response.getheaders())
    
    def get_html_data(self, response_body):
        html_data = BeautifulSoup(response_body)
        return html_data
    
    def get_text_from_td_data(self, td):
        td_text = td.text
        return td_text
    
    def get_vehicle_from_td_data(self, td):
        pod_a = td.find('a')
        
        pod_url = pod_a['href']
        pod_names = pod_a.text
        
        url_match = re.match(r'my_fleet\.php\?mv_action=show&_r=\d+&pk=(?P<pod_id>\d+)', pod_url)
        podid = url_match.group('pod_id')
        
        names_match = re.match(r'(?P<pod_name>.*) - (?P<vehicle_model>.*)', pod_names)
        pod_name = names_match.group('pod_name')
        vehicle_model = names_match.group('vehicle_model')
        
        pod = Pod(podid)
        pod.url = pod_url
        pod.name = pod_name
        
        model = VehicleModel()
        model.name = vehicle_model
        
        vehicle = Vehicle(None)
        vehicle.model = model
        vehicle.pod = pod
        
        return vehicle
    
    def get_time_from_td_data(self, td):
        time_pattern = r'(?P<hour>\d+):(?P<minute>\d+) (?P<midi>[ap])m [A-Za-z]+, (?P<month>[A-Za-z]+) (?P<day>\d+), (?P<year>\d+)'
        
        time_text = td.text
        time_match = re.match(time_pattern, time_text)
        
        months = { 'January':1, 'February':2, 'March':3, 'April':4, 
                       'May':5, 'June':6, 'July':7, 'August':8, 'September':9,
                       'October':10, 'November':11, 'December':12 }
        
        hour = int(time_match.group('hour'))
        if hour == 12:
            hour = 0
        minute = int(time_match.group('minute'))
        midi = time_match.group('midi')
        if midi == 'p':
            hour += 12
        month = months[time_match.group('month')]
        day = int(time_match.group('day'))
        year = int(time_match.group('year'))
        
        return datetime.datetime(year, month, day, hour, minute, tzinfo=Eastern)
    
    def get_price_from_td_data(self, td):
        price_a = td.find('a')
        
        price_pattern = r'\$(?P<dollars>[0-9.]+)'
        price_string = price_a.text
        
        price_match = re.match(price_pattern, price_string)
        price = PriceEstimate()
        price.total_amount = float(price_match.group('dollars'))
        
        return price
    
    def get_confirm_id_from_td_data(self, td):
        edit_button = td.find('button', {'id':'edit'})
        early_button = td.find('button', {'id':'early'})
        
        if edit_button:
            confirm_script = edit_button['onclick']
        elif early_button:
            confirm_script = early_button['onclick']
        else:
            return None
        
        confirm_pattern = r"\&pk=(?P<confirmid>[0-9]+)'"
        confirm_match = re.search(confirm_pattern, confirm_script)
        confirmid = confirm_match.group('confirmid')
        
        return confirmid
    
    def get_reservation_from_table_row_data(self, reservation_tr):
        tds = reservation_tr.findAll('td')
        
        reservation = None
        
        td_count = 0
        for td in tds:
            if td_count == 0:
                reservationid = \
                    self.get_text_from_td_data(td)
                reservation = Reservation(reservationid)
                
            elif td_count == 1:
                reservation.vehicle = \
                    self.get_vehicle_from_td_data(td)
                    
            elif td_count == 2:
                reservation.start_time = \
                    self.get_time_from_td_data(td)
                    
            elif td_count == 3:
                reservation.end_time = \
                    self.get_time_from_td_data(td)
                    
            elif td_count == 4:
                reservation.price = \
                    self.get_price_from_td_data(td)
                    
#            elif td_count == 5:
#                reservation.status = \
#                    self.get_text_from_td_data(td)
                    
            elif td_count == 6:
                reservation.memo = \
                    self.get_text_from_td_data(td)
            
            elif td_count == 7:
                confirmid = self.get_confirm_id_from_td_data(td)
                if confirmid is not None:
                    reservation.confirmid = confirmid
            
            td_count += 1
        
        return reservation
    
    def get_pcs_connection(self):
        return PcsConnection()
    
    def get_reservation_data_from_html_data(self, html_data):
        reservations = []

        res_table = html_data.find('table', {'id': 'main_dlist_'})
        
        if res_table is not None:
            res_tbody = res_table.find('tbody')
            res_trs = res_tbody.findAll('tr')
            
            for res_tr in res_trs:
                reservation = self.get_reservation_from_table_row_data(res_tr)
                reservations.append(reservation)
        
        return reservations
    
    def get_page_data_from_html_data(self, html_data):
        pages_table = html_data.find('table', {'id': 'dlist_pagination'})
        
        if not pages_table:
            current_page = 1
            last_page = 1
        else:
            current_page_font = pages_table.find('font', {'class': 'text'})
            
            all_page_anchors = pages_table.findAll('a', {'class': 'text'})
            last_page_anchor = all_page_anchors[-1]
            
            current_page = int(current_page_font.text)
            last_page = max(current_page, int(last_page_anchor.text))
        
        return current_page, last_page
    
    @override
    def fetch_reservations(self, sessionid, year_month=None):
        conn = self.get_pcs_connection()
        
        if year_month is None:
            pcs_body, pcs_head = \
                self.upcoming_reservations_from_pcs(conn, sessionid)
        else:
            pcs_body, pcs_head = \
                self.past_reservations_from_pcs(conn, sessionid, year_month.year, year_month.month)
        
        reservations_html_doc = self.get_html_data(pcs_body)
        reservations = self.get_reservation_data_from_html_data(reservations_html_doc)
        current_page, page_count = self.get_page_data_from_html_data(reservations_html_doc)
        
        return reservations, current_page, page_count
    
    def get_time_query(self, start_time, end_time):
        sdate, stime = to_pcs_date_time(start_time)
        edate, etime = to_pcs_date_time(end_time)
        
        data = {
            'add[start_stamp][start_date][date]' : sdate,
            'add[start_stamp][start_time][time]' : stime,
            'add[end_stamp][end_date][date]' : edate,
            'add[end_stamp][end_time][time]' : etime}
        query = urllib.urlencode(data)
        return query
    
    def get_vehicle_query(self, vehicleid):
        data = {
            'add[stack_pk]' : (vehicleid)}
        query = urllib.urlencode(data)
        return query
    
    def get_memo_query(self, memo):
        data = {
            'add[job_code]' : memo}
        query = urllib.urlencode(data)
        return query
    
    def get_transaction_query(self, transactionid):
        data = {
            'add[tid]' : transactionid}
        query = urllib.urlencode(data)
        return query
    
    def send_reservation_request_to_pcs(self, conn, sessionid, vehicleid, transactionid, start_time, end_time, reservation_memo):
        host = self.__host
        path = self.__newres_path
        
        headers = {
            'Cookie': 'sid=%s' % sessionid}
        
        data = self.get_time_query(start_time, end_time)
        data += '&' + self.get_vehicle_query(vehicleid)
        data += '&' + self.get_memo_query(reservation_memo)
        data += '&' + self.get_transaction_query(transactionid)
        
        query = ''
        connector = ''
        
        url = "http://%s%s%s%s" % (host, path, connector, query)
        
        response = conn.request(url, "POST", data, headers)
        return (response.read(), response.getheaders())
    
    def get_reservation_from_pcs_with_confirmation_id(self, conn, sessionid, confirmid):
        host = self.__host
        path = self.__confirm_path
        
        headers = {
            'Cookie': 'sid=%s' % sessionid}
        
        data = ''
        
        query = 'pk=%s' % confirmid
        connector = '&' if '?' in path else '?'
        
        url = "http://%s%s%s%s" % (host, path, connector, query)
        
        response = conn.request(url, "GET", data, headers)
        return (response.read(), response.getheaders())
    
    def get_vehicle_id_from_confirmation_doc(self, confirm_doc):
        table = confirm_doc.find('table', {'class':'mi'})
        tbody = table.find('tbody')
        trs = tbody.findAll('tr')
        
        row = 0
        for tr in trs:
            row += 1
            if row == 3:
                td = tr.find('td', {'align':'left'})
                anchor = td.find('a')
                href = anchor['href']
                
                vid_pattern = r'stack_pk=(?P<vid>[0-9]+)'
                vid_match = re.match(vid_pattern, href)
                return vid_match.groups('vid')
    
    def get_reservation_from_confirmation_id(self, conn, sessionid, confirmid):
        confirm_body, confirm_head = self.get_reservation_from_pcs_with_confirmation_id(conn, sessionid, confirmid)
        confirm_doc = self.get_html_data(confirm_body)
        
        # NOTE: I am switching up the reservation id and the confirmation id.  
        #       PhillyCarShare uses "reservation id" when referring to the human
        #       reservations in the Existing Reservations list, as well as on
        #       the gas reimbursement request form.  Moreover, what I'm calling
        #       the confirmation id is only available (to my knowledge) for 
        #       current and upcoming reservations.  The other reservations have
        #       confirmation ids, they're just not available publicly.  So, to
        #       save a little bit of headache, PCS's confirmation id is my 
        #       reservation id.  I keep both around because the confirmation id
        #       is useful when changing or cancelling a reservation.  I can 
        #       obtain it in other ways than storing it directly, but not in 
        #       any way that will be fast yet.
        res_id_span = confirm_doc.find('span', {'id':'confirm_id_'})
        reservationid = res_id_span.text
        
        return reservationid
        
    def get_reservation_from_confirmation_script_code(self, conn, sessionid, script_code):
        resid_pattern = r"""window\.location = 'my_reservations\.php\?mv_action=confirm&_r=([0-9]+)&pk=(?P<resid>[0-9]+)'""";
        resid_match = re.match(resid_pattern, script_code)
        confirmid = resid_match.group('resid')
        
        reservationid = self.get_reservation_from_confirmation_id(conn, sessionid, confirmid)
        return reservationid, confirmid
    
    def get_reservation_from_html_pcs_confirmation_redirect_script(self, conn, sessionid, script_doc):
        script_tag = script_doc.find('script')
        if script_tag is None:
            raise ScreenscrapeParseError('Resulting reservation confirmation document has no "script" tag: %s' 
                % (str(script_doc).replace('>','&gt;').replace('<','&lt;')))
        script_code = script_tag.text
        reservationid, confirmid = \
            self.get_reservation_from_confirmation_script_code(conn, sessionid, script_code)
        return reservationid, confirmid
    
    @override 
    def create_reservation(self, sessionid, vehicleid, transactionid, start_time, end_time, reservation_memo):
        conn = self.get_pcs_connection()
        
        pcs_body, pcs_head = \
            self.send_reservation_request_to_pcs(conn, sessionid, vehicleid, transactionid, start_time, end_time, reservation_memo)
        
        reservation_html_doc = self.get_html_data(pcs_body)
        reservationid, confirmid = self.get_reservation_from_html_pcs_confirmation_redirect_script(
            conn, sessionid, reservation_html_doc)
        
        reservation = Reservation(reservationid, confirmid)
        reservation.vehicle = self.vehicle_source.fetch_vehicle(sessionid, vehicleid, start_time, end_time)
        reservation.start_time = start_time
        reservation.end_time = end_time
        
        return reservation
    
    @override
    def get_existing_reservation(self, sessionid, reservationid):
        pass

