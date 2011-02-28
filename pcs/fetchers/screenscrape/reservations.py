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
from pcs.fetchers.screenscrape import ScreenscrapeFetchError
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
                 transid_path="/lightbox.php",
                 newres_path="/lightbox.php?mv_action=add",
                 editres_path="/lightbox.php",
                 cancelres_path="/my_reservations.php",
                 detail_path="/my_reservations.php?mv_action=confirm",
                 confirm_path="/my_reservations.php?mv_action=confirm"):
        self.__host = host
        self.__upcoming_path = upcoming_path
        self.__past_path = past_path
        self.__price_path = price_path
        self.__transid_path = transid_path
        self.__newres_path = newres_path
        self.__editres_path = editres_path
        self.__cancelres_path = cancelres_path
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
    
    def get_restrans_time_query(self, transtype, start_time, end_time):
        sdate, stime = to_pcs_date_time(start_time)
        edate, etime = to_pcs_date_time(end_time)
        
        data = {
            transtype + '[start_stamp][start_date][date]' : sdate,
            transtype + '[start_stamp][start_time][time]' : stime,
            transtype + '[end_stamp][end_date][date]' : edate,
            transtype + '[end_stamp][end_time][time]' : etime}
        data = sorted(data.iteritems())
        query = urllib.urlencode(data)
        return query
    
    def get_restrans_vehicle_query(self, transtype, vehicleid):
        data = {
            transtype + '[stack_pk]' : (vehicleid)}
        query = urllib.urlencode(data)
        return query
    
    def get_restrans_memo_query(self, transtype, memo):
        data = {
            transtype + '[job_code]' : memo}
        query = urllib.urlencode(data)
        return query
    
    def get_transaction_query(self, transtype, transactionid):
        data = {
            'mv_action' : transtype,
            transtype + '[tid]' : transactionid}
        data = sorted(data.iteritems())
        query = urllib.urlencode(data)
        return query
    
    def get_restrans_reservation_query(self, transtype, liveid):
        data = {
            transtype + '[pk]' : liveid,
            'pk' : liveid}
        data = sorted(data.iteritems())
        query = urllib.urlencode(data)
        return query
    
    def request_create_reservation_from_pcs(self, conn, sessionid, vehicleid, transactionid, start_time, end_time, reservation_memo):
        host = self.__host
        path = self.__newres_path
        
        headers = {
            'Cookie': 'sid=%s' % sessionid}
        
        data = self.get_restrans_time_query('add', start_time, end_time)
        data += '&' + self.get_restrans_vehicle_query('add', vehicleid)
        data += '&' + self.get_restrans_memo_query('add', reservation_memo)
        data += '&' + self.get_transaction_query('add', transactionid)
        
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
    
    def request_empty_create_reservation_box_from_pcs(self, conn, sessionid, transtype, liveid=None):
        host = self.__host
        path = self.__transid_path
        
        headers = {
            'Cookie': 'sid=%s' % sessionid}
        
        data = 'mv_action=%s' % transtype
        if liveid is not None:
            data += '&pk=%s' % liveid
        query = ''
        connector = ''
        
        url = "http://%s%s%s%s" % (host, path, connector, query)
        
        response = conn.request(url, "POST", data, headers)
        return(response.read(), response.getheaders())
    
    def request_modify_reservation_from_pcs(self, conn, sessionid, mod_type, liveid, transactionid, vehicleid, start_time, end_time, memo):
        host = self.__host
        path = self.__editres_path
        
        headers = {
            'Cookie': 'sid=%s' % sessionid}
        
        data = self.get_restrans_time_query(mod_type, start_time, end_time)
        if vehicleid:
            data += '&' + self.get_restrans_vehicle_query(mod_type, vehicleid)
        if memo:
            data += '&' + self.get_restrans_memo_query(mod_type, memo)
        data += '&' + self.get_restrans_reservation_query(mod_type, liveid)
        data += '&' + self.get_transaction_query(mod_type, transactionid)
        
        query = ''
        connector = ''
        
        url = "http://%s%s%s%s" % (host, path, connector, query)
        
        response = conn.request(url, "POST", data, headers)
        return (response.read(), response.getheaders())
    
    def request_cancel_reservation_from_pcs(self, conn, sessionid, liveid, transactionid, vehicleid, start_time, end_time):
        host = self.__host
        path = self.__cancelres_path
        
        headers = {
            'Cookie': 'sid=%s' % sessionid}
        
        data = self.get_restrans_time_query('do_cancel', start_time, end_time)
        data += '&' + self.get_restrans_vehicle_query('do_cancel', vehicleid)
        data += '&' + self.get_restrans_reservation_query('do_cancel', liveid)
        data += '&' + self.get_transaction_query('do_cancel', transactionid)
        
        query = ''
        connector = ''
        
        url = "http://%s%s%s%s" % (host, path, connector, query)
        
        response = conn.request(url, "POST", data, headers)
        return (response.read(), response.getheaders())

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
        liveid_pattern = r"""(?P<window_script>window\.location = ')?my_reservations\.php\?mv_action=confirm&_r=([0-9]+)&pk=(?P<liveid>[0-9]+)(&payment_pk=[0-9]+)?(?(window_script)')""";
        liveid_match = re.match(liveid_pattern, script_code)
        
        if liveid_match is None:
            raise ScreenscrapeParseError('Resulting redirect script has no discernable confirm id: %r' % script_code)
        
        liveid = liveid_match.group('liveid')
        
        return liveid
    
    def verify_no_error_in_lightbox_doc(self, lgtbox_doc):
        error_p_elem = lgtbox_doc.find('p', {'class':'error'})
        
        if error_p_elem:
            error_txt = self.get_text_from_element(error_p_elem)
            error_code = None
            if error_txt == 'You can only make one reservation during a given time period.':
                error_code = 'time_period_conflict'
            elif error_txt == 'You must change your reservation in order to update it.':
                error_code = 'no_change_requested'
            
            raise ScreenscrapeFetchError(error_txt, error_code)
        
        return True
    
    def decode_reservation_liveid_from_redirect_script_element(self, script_doc):
        self.verify_no_error_in_lightbox_doc(script_doc)
        
        script_tag = script_doc.find('script')
        
        if script_tag is None:
            raise ScreenscrapeParseError('Resulting reservation confirmation document has no "script" tag: %s' 
                % (str(script_doc)))
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
    
    def decode_vehicle_id_info_from_element(self, elem):
        elem_href = elem['href']
        
        ids_match = re.search(r'my_fleet.php\?mv_action=stack_detail&_r=([0-9]+)&pk=(?P<podid>[0-9]+)&stack_pk=(?P<vehicleid>[0-9]+)', elem_href)
        if ids_match is None:
            raise Exception(elem_href)
        podid = ids_match.group('podid')
        vehicleid = ids_match.group('vehicleid')
        
        return vehicleid, podid
    
    def decode_reservation_info_from_confirmation_doc(self, html_doc):
        log_id_span = html_doc.find('span', {'id':'confirm_id_'})
        if log_id_span is None:
            raise ScreenscrapeParseError('Cannot find the confirmation log id: %s' 
                % (str(html_doc).replace('>','&gt;').replace('<','&lt;')))
        logid = self.get_text_from_element(log_id_span)
        
#        vehicle_info_span = html_doc.find('span', {'id':'stack_pk'})
        res_table = html_doc.find('table', {'class':'mi'})
        
        if not res_table:
            raise ScreenscrapeParseError("No table found with class 'mi': %s" % html_doc)
        
        # Pod/Vehicle names/ids are in the 3rd row, 2nd column.
        # Start/End times are in the 5th/6th rows, 2nd column.
        #
        # NOTE: Start/End times are in the 5th/6th rows because of an unclosed
        #       <tr> tag immediately before the start time row.  Beautiful soup
        #       interprets this as an empty row.  So, I'm counting it as the
        #       (empty) fourth row.
        res_rows = res_table.findAll('tr')
        
        if len(res_rows) < 6:
            raise ScreenscrapeParseError("Reservation info table must have at least 6 rows: %s" % res_table)
        
        # ... so we find the ids and names
        vehicle_info_row = res_rows[2]
        vehicle_info_tds = vehicle_info_row.findAll('td')
        
        if len(vehicle_info_tds) < 2:
            raise ScreenscrapeParseError("Vehicle info table row must have at least 2 columns: %s" % vehicle_info_row)
        
        vehicle_info_td = vehicle_info_tds[1]
        vehicle_info_a = vehicle_info_td.find('a')
        
        if not vehicle_info_a:
            raise ScreenscrapeParseError("No vehicle information anchor found: %s" % html_doc)
        
        modelname, podname = self.decode_vehicle_name_info_from_element(vehicle_info_a)
        vehicleid, podid = self.decode_vehicle_id_info_from_element(vehicle_info_a)
        
        # ... and we find the start time
        start_time_row = res_rows[4]
        start_time_tds = start_time_row.findAll('td')
        
        if len(start_time_tds) < 2:
            raise ScreenscrapeParseError("Start time table row must have at least 2 columns: %s" % start_time_row)
        
        start_time_td = start_time_tds[1]
        start_time_elem = start_time_td.find('font')
        
        if not start_time_elem:
            raise ScreenscrapeParseError("No start time found: %s" % html_doc)
        
        start_time = self.decode_res_time_from_element(start_time_elem)
        
        # .. and the end time
        end_time_row = res_rows[5]
        end_time_tds = end_time_row.findAll('td')
        
        if len(end_time_tds) < 2:
            raise ScreenscrapeParseError("End time table row must have at least 2 columns: %s" % end_time_row)
        
        end_time_td = end_time_tds[1]
        end_time_elem = end_time_td.find('font')
        
        if not end_time_elem:
            raise ScreenscrapeParseError("No end time found: %s" % html_doc)
        
        end_time = self.decode_res_time_from_element(end_time_elem)
        
        # .. and the memo
        memo_row = res_rows[7]
        memo_tds = memo_row.findAll('td')
        
        if len(memo_tds) < 2:
            raise ScreenscrapeParseError("Memo table row must have at least 2 columns: %s" % memo_row)
        
        memo_td = memo_tds[1]
        memo_elem = memo_td.find('font')
        
        if not memo_elem:
            raise ScreenscrapeParseError("No memo found: %s" % html_doc)
        
        memo = self.get_text_from_element(memo_elem)
        
        # .. and the total price
        price_elem = html_doc.find('span', {'id':'confirm_trip_estimate_pk_'})
        if price_elem:
            price_text = self.get_text_from_element(price_elem)
            price_pattern = r"\$(?P<total_amount>[0-9.]+) \(Total\)"
            
            price_match = re.search(price_pattern, price_text)
            if price_match is None:
                raise ScreenscrapeParseError("Total price not found: %r" % price_text)
            
            pricetotal = float(price_match.group('total_amount'))
        else:
            pricetotal = None
        
        return logid, start_time, end_time, vehicleid, modelname, podid, podname, memo, pricetotal
    
    def decode_res_time_from_element(self, elem):
        time_text = self.get_text_from_element(elem)
        
        pattern = '(?P<hour>[0-9]+):(?P<minute>[0-9]+) (?P<midi>[ap])m .*, (?P<month>[A-za-z]+) (?P<day>[0-9]+), (?P<year>[0-9]+)'
        time_match = re.match(pattern, time_text)
        
        if not time_match:
            raise ScreenscrapeParseError('Could not match %r to the pattern %r' % (time_text, pattern))
        
        months = {
            'January':1,
            'February':2,
            'March':3,
            'April':4,
            'May':5,
            'June':6,
            'July':7,
            'August':8,
            'September':9,
            'October':10,
            'November':11,
            'December':12
        }
        
        hour = int(time_match.group('hour'))
        if hour == 12:
            hour = 0
        midi = time_match.group('midi')
        if midi == 'p':
            hour += 12
        minute = int(time_match.group('minute'))
        try:
            month = months[time_match.group('month')]
        except KeyError:
            raise ScreenscrapeParseError("Unrecognized month: %r" % time_match.group('month'))
        day = int(time_match.group('day'))
        year = int(time_match.group('year'))
        
        return datetime.datetime(year, month, day, hour, minute, tzinfo=Eastern)
        
    def decode_transaction_id_from_lightbox_block(self, transtype, block):
        tid_input = block.find('input', {'id':transtype+'_tid_'})
        
        if tid_input is None:
            raise ScreenscrapeParseError('Failed to retrieve a transaction id.')
        
        transactionid = tid_input['value']
        
        return transactionid
        

class ReservationsScreenscrapeSource (_ReservationsSourceInterface):
    
    def __init__(self,
                 requester = None,
                 decoder = None):
        super(ReservationsScreenscrapeSource, self).__init__()
        
        self.requester = requester or PcsRequestMaker()
        self.decoder = decoder or PcsDocumentDecoder()
    
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
    
    def get_a_transaction_id(self, conn, sessionid, transtype, liveid=None):
        # Get a transaction id -- I'm not quite certain what these are for, but
        # I know we need one each time we make/change a reservation.
        pcs_body, pcs_head = \
            self.requester.request_empty_create_reservation_box_from_pcs(
                conn, sessionid, transtype, liveid)
        
        lgtbox_block = self.get_html_document(pcs_body)
        transactionid = \
            self.decoder.decode_transaction_id_from_lightbox_block(
                transtype, lgtbox_block)
        
        return transactionid
    
    def send_creation_info(self, conn, sessionid, vehicleid, transactionid, start_time, end_time, memo):
        # Request for the reservation to be created and get the Live ID
        pcs_body, pcs_head = \
            self.requester.request_create_reservation_from_pcs(
                conn, sessionid, vehicleid, transactionid, start_time, end_time, memo)
        
        redir_script = self.get_html_document(pcs_body)
        liveid = \
            self.decoder.decode_reservation_liveid_from_redirect_script_element(
                redir_script)
        
        return liveid
    
    def send_modification_info(self, conn, sessionid, mod_type, liveid, transactionid, vehicleid, start_time, end_time, memo):
        # Request for the reservation to be modified and get the Live ID
        pcs_body, pcs_head = \
            self.requester.request_modify_reservation_from_pcs(
                conn, sessionid, mod_type, liveid, transactionid, vehicleid, start_time, end_time, memo)
        
        redir_script = self.get_html_document(pcs_body)
        liveid = \
            self.decoder.decode_reservation_liveid_from_redirect_script_element(
                redir_script)
        
        return liveid
    
    def send_cancellation_info(self, conn, sessionid, liveid, transactionid, vehicleid, start_time, end_time):
        pcs_body, pcs_head = \
            self.requester.request_cancel_reservation_from_pcs(
                conn, sessionid, liveid, transactionid, vehicleid, start_time, end_time)
        
        conf_html_doc = self.get_html_document(pcs_body)
        logid, start_time, end_time, vehicleid, modelname, podid, podname, memo, pricetotal = \
            self.decoder.decode_reservation_info_from_confirmation_doc(
                conf_html_doc)
        
        return logid, modelname, podname, memo, pricetotal
    
    def send_reservation_request(self, conn, sessionid, liveid):
        pcs_body, pcs_head = \
            self.requester.request_confirm_reservation_from_pcs(
                conn, sessionid, liveid)
        
        conf_html_doc = self.get_html_document(pcs_body)
        logid, start_time, end_time, vehicleid, modelname, podid, podname, memo, pricetotal = \
            self.decoder.decode_reservation_info_from_confirmation_doc(
                conf_html_doc)
        
        return logid, start_time, end_time, vehicleid, modelname, podid, podname, memo, pricetotal
    
    def build_vehicle(self, vehicleid, modelname, podid, podname):
        vehicle = Vehicle(vehicleid)
        
        if modelname:
            vehicle.model = VehicleModel()
            vehicle.model.name = modelname
        
        if podid or podname:
            vehicle.pod = Pod(podid)
            vehicle.pod.name = podname
        
        return vehicle
    
    def build_reservation(self, logid, liveid, start_time, end_time, vehicleid, modelname, podid, podname, memo, pricetotal):
        reservation = Reservation(logid,liveid)
        reservation.start_time = start_time
        reservation.end_time = end_time
        
        if memo:
            reservation.memo = memo
        
        if pricetotal is not None:
            reservation.price = PriceEstimate()
            reservation.price.total_amount = pricetotal
        
        reservation.vehicle = self.build_vehicle(vehicleid, modelname, podid, podname)
        
        return reservation
    
    @override
    def fetch_reservation_information(self, sessionid, liveid):
        conn = self.get_pcs_connection()
        
        logid, start_time, end_time, vehicleid, modelname, podid, podname, memo, pricetotal = \
            self.send_reservation_request(conn, sessionid, liveid)
        
        reservation = self.build_reservation(logid, liveid, start_time, 
            end_time, vehicleid, modelname, podid, podname, memo, pricetotal)
        
        return reservation
    
    @override 
    def fetch_reservation_creation(self, sessionid, vehicleid, start_time, end_time, reservation_memo):
        conn = self.get_pcs_connection()
        
        transactionid = \
            self.get_a_transaction_id(conn, sessionid, 'add')
        
        liveid = \
            self.send_creation_info(conn, sessionid, vehicleid, transactionid, 
                start_time, end_time, reservation_memo)
        
        # We don't know the pod id from the confirmation, and I'm not sure it's
        # worth it to make an additional request to get it.  If we need it in 
        # the future, we'll work it out.
        logid = modelname = podid = podname = memo = pricetotal = None
        
        reservation = self.build_reservation(logid, liveid, 
            start_time, end_time, vehicleid, modelname, podid, podname, memo, pricetotal)
        
        return reservation
    
    @override
    def fetch_reservation_modification(self, sessionid, mod_type, liveid, vehicleid, start_time, end_time, reservation_memo):
        conn = self.get_pcs_connection()
        
        transactionid = \
            self.get_a_transaction_id(conn, sessionid, mod_type, liveid)
        
        liveid = \
            self.send_modification_info(conn, sessionid, mod_type, liveid, 
                transactionid, vehicleid, start_time, end_time, 
                reservation_memo)
        
        # We don't know the pod id or vehicle if from the confirmation.
        logid = modelname = podname = podid = memo = price_total = None
        
        reservation = self.build_reservation(logid, liveid, start_time, 
            end_time, vehicleid, modelname, podid, podname, memo, price_total)
        
        return reservation
    
    @override
    def fetch_reservation_cancellation(self, sessionid, liveid, vehicleid, start_time, end_time):
        conn = self.get_pcs_connection()
        
        transactionid = \
            self.get_a_transaction_id(conn, sessionid, 'do_cancel', liveid)
        
        res_info = \
            self.send_cancellation_info(conn, sessionid, liveid, transactionid,
                vehicleid, start_time, end_time)
        logid, modelname, podname, memo, pricetotal = res_info
        podid = None
        
        reservation = self.build_reservation(logid, liveid, 
            start_time, end_time, vehicleid, modelname, podid, podname, memo, pricetotal)
        
        return reservation

