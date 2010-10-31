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

class PcsRequestMaker (object):
    def __init__(self, host="reservations.phillycarshare.org",
                 upcoming_path="/my_reservations.php?mv_action=main",
                 past_path="/my_reservations.php?mv_action=main",
                 price_path="/ajax_estimate.php?slider=true",
                 newres_path="/lightbox.php?mv_action=add",
                 detail_path="/my_reservations.php?mv_action=confirm",
                 confirm_path="/my_reservations.php?mv_action=confirm"):
        self.__host = host
        self.__upcoming_path = upcoming_path
        self.__past_path = past_path
        self.__price_path = price_path
        self.__newres_path = newres_path
        self.__detail_path = detail_path
        self.__confirm_path = confirm_path
    
    def get_driver_query(self, driverid):
        query = "main[multi_filter][driver_pk]=%s" % (driverid)
        return query
    
    def get_datefilter_query(self, year, month):
        query = "main[multi_filter][history][yearmonth]=%s%02d" % (year, month)
        return query
    
    def request_upcoming_reservations_from_pcs(self, conn, sessionid):
        host = self.__host
        path = self.__upcoming_path
        
        headers = {
            'Cookie': 'sid=%s' % sessionid}
        query = ''
        connector = ''
        
        url = "http://%s%s%s%s" % (host, path, connector, query)
        
        response = conn.request(url, "GET", {}, headers)
        return (response.read(), response.getheaders())
    
    def request_past_reservations_from_pcs(self, conn, sessionid, year, month):
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
    
    def request_create_reservation_from_pcs(self, conn, sessionid, vehicleid, transactionid, start_time, end_time, reservation_memo):
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
    
    def request_confirm_reservation_from_pcs(self, conn, sessionid, liveid):
        host = self.__host
        path = self.__confirm_path
        
        headers = {
            'Cookie': 'sid=%s' % sessionid}
        
        data = ''
        
        query = 'pk=%s' % liveid
        connector = '&' if '?' in path else '?'
        
        url = "http://%s%s%s%s" % (host, path, connector, query)
        
        response = conn.request(url, "GET", data, headers)
        return (response.read(), response.getheaders())
    
    def request_empty_create_reservation_box_from_pcs(self, conn, sessionid):
        host = self.__host
        path = self.__newres_path
        
        headers = {
            'Cookie': 'sid=%s' % sessionid}
        
        data = ''
        query = ''
        connector = ''
        
        url = "http://%s%s%s%s" % (host, path, connector, query)
        
        response = conn.request(url, "POST", data, headers)
        return(response.read(), response.getheaders())

class PcsDocumentDecoder(object):
    def get_text_from_element(self, td):
        td_text = td.text
        return td_text
    
    def build_vehicle_from_td_element(self, td):
        pod_a = td.find('a')
        
        pod_url = pod_a['href']
        pod_names = pod_a.text
        
        url_match = re.match(r'my_fleet\.php\?mv_action=show&_r=\d+&pk=(?P<pod_id>\d+)', pod_url)
        podid = url_match.group('pod_id')
        
        vehicle_model, pod_name = \
            self.decode_vehicle_name_info_from_element(pod_a)
        
        pod = Pod(podid)
        pod.url = pod_url
        pod.name = pod_name
        
        model = VehicleModel()
        model.name = vehicle_model
        
        vehicle = Vehicle(None)
        vehicle.model = model
        vehicle.pod = pod
        
        return vehicle
    
    def get_time_from_td_element(self, td):
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
    
    def build_price_from_td_element(self, td):
        price_a = td.find('a')
        
        price_pattern = r'\$(?P<dollars>[0-9.]+)'
        price_string = price_a.text
        
        price_match = re.match(price_pattern, price_string)
        price = PriceEstimate()
        price.total_amount = float(price_match.group('dollars'))
        
        return price
    
    def decode_reservation_liveid_from_td_element(self, td):
        edit_button = td.find('button', {'id':'edit'})
        early_button = td.find('button', {'id':'early'})
        
        if edit_button:
            confirm_script = edit_button['onclick']
        elif early_button:
            confirm_script = early_button['onclick']
        else:
            return None
        
        confirm_pattern = r"\&pk=(?P<liveid>[0-9]+)'"
        confirm_match = re.search(confirm_pattern, confirm_script)
        liveid = confirm_match.group('liveid')
        
        return liveid
    
    def build_reservation_from_table_row_element(self, reservation_tr):
        tds = reservation_tr.findAll('td')
        
        reservation = None
        
        td_count = 0
        for td in tds:
            if td_count == 0:
                logid = \
                    self.get_text_from_element(td)
                reservation = Reservation(logid)
                
            elif td_count == 1:
                reservation.vehicle = \
                    self.build_vehicle_from_td_element(td)
                    
            elif td_count == 2:
                reservation.start_time = \
                    self.get_time_from_td_element(td)
                    
            elif td_count == 3:
                reservation.end_time = \
                    self.get_time_from_td_element(td)
                    
            elif td_count == 4:
                reservation.price = \
                    self.build_price_from_td_element(td)
                    
#            elif td_count == 5:
#                reservation.status = \
#                    self.get_text_from_element(td)
                    
            elif td_count == 6:
                reservation.memo = \
                    self.get_text_from_element(td)
            
            elif td_count == 7:
                liveid = self.decode_reservation_liveid_from_td_element(td)
                if liveid is not None:
                    reservation.liveid = liveid
            
            td_count += 1
        
        return reservation
    
    def build_reservation_log_from_log_doc(self, html_document):
        reservations = []

        res_table = html_document.find('table', {'id': 'main_dlist_'})
        
        if res_table is not None:
            res_tbody = res_table.find('tbody')
            res_trs = res_tbody.findAll('tr')
            
            for res_tr in res_trs:
                reservation = self.build_reservation_from_table_row_element(res_tr)
                reservations.append(reservation)
        
        return reservations
    
    def decode_page_info_from_log_doc(self, html_document):
        pages_table = html_document.find('table', {'id': 'dlist_pagination'})
        
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
    
    def decode_reservation_logid_from_confirmation_doc(self, html_doc):
        log_id_span = html_doc.find('span', {'id':'confirm_id_'})
        logid = log_id_span.text
        
        return logid
        
    def decode_reservation_liveid_from_redirect_script_code(self, script_code):
        liveid_pattern = r"""window\.location = 'my_reservations\.php\?mv_action=confirm&_r=([0-9]+)&pk=(?P<liveid>[0-9]+)'""";
        liveid_match = re.match(liveid_pattern, script_code)
        
        if liveid_match is None:
            raise ScreenscrapeParseError('Resulting redirect script has no discernable confirm id: %r' % script_code)
        
        liveid = liveid_match.group('liveid')
        
        return liveid
    
    def decode_reservation_liveid_from_redirect_script_element(self, script_doc):
        script_tag = script_doc.find('script')
        
        if script_tag is None:
            raise ScreenscrapeParseError('Resulting reservation confirmation document has no "script" tag: %s' 
                % (str(script_doc).replace('>','&gt;').replace('<','&lt;')))
        script_code = script_tag.text
        
        liveid = \
            self.decode_reservation_liveid_from_redirect_script_code(
                script_code)
        return liveid
    
    def decode_vehicle_name_info_from_element(self, elem):
        elem_text = self.get_text_from_element(elem)
        
        names_match = re.match(r'(?P<pod_name>.*) - (?P<vehicle_model>.*)', elem_text)
        podname = names_match.group('pod_name')
        modelname = names_match.group('vehicle_model')
        
        return modelname, podname
        
    def decode_reservation_info_from_confirmation_doc(self, html_doc):
        log_id_span = html_doc.find('span', {'id':'confirm_id_'})
        logid = self.get_text_from_element(log_id_span)
        
        vehicle_info_span = html_doc.find('span', {'id':'stack_pk'})
        modelname, podname = self.decode_vehicle_name_info_from_element(vehicle_info_span)
        
        return logid, modelname, podname
    
    def decode_transaction_id_from_lightbox_block(self, block):
        tid_input = block.find('input', {'id':'add_tid_'})
        
        if tid_input is None:
            raise ScreenscrapeParseError('Failed to retrieve a transaction id.')
        
        transactionid = tid_input['value']
        
        return transactionid
        

class ReservationsScreenscrapeSource (_ReservationsSourceInterface):
    
    def __init__(self,
                 vehicle_source = AvailabilityScreenscrapeSource(),
                 requester = None,
                 decoder = None):
        super(ReservationsScreenscrapeSource, self).__init__()
        
        self.requester = requester or PcsRequestMaker()
        self.decoder = decoder or PcsDocumentDecoder()
        self.vehicle_source = vehicle_source
    
    def get_pcs_connection(self):
        return PcsConnection()
    
    def get_html_document(self, response_body):
        html_document = BeautifulSoup(response_body)
        return html_document
    
    @override
    def fetch_reservations(self, sessionid, year_month=None):
        conn = self.get_pcs_connection()
        
        if year_month is None:
            pcs_body, pcs_head = \
                self.requester.request_upcoming_reservations_from_pcs(conn, sessionid)
        else:
            pcs_body, pcs_head = \
                self.requester.request_past_reservations_from_pcs(conn, sessionid, year_month.year, year_month.month)
        
        reservations_html_doc = self.get_html_document(pcs_body)
        reservations = \
            self.decoder.build_reservation_log_from_log_doc(
                reservations_html_doc)
        current_page, page_count = \
            self.decoder.decode_page_info_from_log_doc(
                reservations_html_doc)
        
        return reservations, current_page, page_count
    
#    def get_vehicle_id_from_confirmation_doc(self, confirm_doc):
#        table = confirm_doc.find('table', {'class':'mi'})
#        tbody = table.find('tbody')
#        trs = tbody.findAll('tr')
#        
#        row = 0
#        for tr in trs:
#            row += 1
#            if row == 3:
#                td = tr.find('td', {'align':'left'})
#                anchor = td.find('a')
#                href = anchor['href']
#                
#                vid_pattern = r'stack_pk=(?P<vid>[0-9]+)'
#                vid_match = re.match(vid_pattern, href)
#                return vid_match.groups('vid')
    
    def build_vehicle(self, vehicleid, modelname, podid, podname):
        vehicle = Vehicle(vehicleid)
        vehicle.model = VehicleModel()
        vehicle.model.name = modelname
        vehicle.pod = Pod(podid)
        vehicle.pod.name = podname
        
        return vehicle
    
    def build_reservation(self, logid, liveid, start_time, end_time, vehicleid, modelname, podid, podname):
        reservation = Reservation(logid,liveid)
        reservation.start_time = start_time
        reservation.end_time = end_time
        
        reservation.vehicle = self.build_vehicle(vehicleid, modelname, podid, podname)
        
        return reservation
    
    @override 
    def create_reservation(self, sessionid, vehicleid, start_time, end_time, reservation_memo):
        conn = self.get_pcs_connection()
        
        # Get a transaction id
        pcs_body, pcs_head = \
            self.requester.request_empty_create_reservation_box_from_pcs(
                conn, sessionid)
        
        lgtbox_block = self.get_html_document(pcs_body)
        transactionid = \
            self.decoder.decode_transaction_id_from_lightbox_block(
                lgtbox_block)
        
        # Get the Live ID
        pcs_body, pcs_head = \
            self.requester.request_create_reservation_from_pcs(
                conn, sessionid, vehicleid, transactionid, start_time, end_time, reservation_memo)
        
        redir_script = self.get_html_document(pcs_body)
        liveid = \
            self.decoder.decode_reservation_liveid_from_redirect_script_element(
                redir_script)
        
        # Get the other reservation info (Log ID, Model Name, Pod Name)
        pcs_body, pcs_head = \
            self.requester.request_confirm_reservation_from_pcs(
                conn, sessionid, liveid)
        
        conf_html_doc = self.get_html_document(pcs_body)
        logid, modelname, podname = \
            self.decoder.decode_reservation_info_from_confirmation_doc(
                conf_html_doc)
        # We don't know the pod id from the confirmation, and I'm not sure it's
        # worth it to make an additional request to get it.
        podid = None
        
        reservation = self.build_reservation(logid, liveid, 
            start_time, end_time, vehicleid, modelname, podid, podname)
        
        return reservation
    
    @override
    def get_existing_reservation(self, sessionid, logid):
        pass

