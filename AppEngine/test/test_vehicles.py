import unittest
import datetime
import new

from pcs.input.wsgi import WsgiParameterError
from pcs.input.wsgi.vehicles import VehiclesHandler
from pcs.source import _VehiclesSourceInterface
from pcs.source import _LocationsSourceInterface
from pcs.source import _SessionSourceInterface
from pcs.source.screenscrape import ScreenscrapeParseError
from pcs.view import _VehiclesViewInterface
from pcs.view import _ErrorViewInterface
from util.testing import patch
from util.testing import Stub
from util.TimeZone import Eastern

class VehiclesHandlerTest (unittest.TestCase):
    
    def setUp(self):
        # A fake request class
        class StubRequest (dict):
            pass
        
        # A fake response class
        import StringIO
        class StubResponse (object):
            out = StringIO.StringIO()
            def set_status(self, status):
                self.status = status
        
        # A source for session information
        @Stub(_SessionSourceInterface)
        class StubSessionSource (object):
            pass
        
        # A source for vehicle availability information
        @Stub(_VehiclesSourceInterface)
        class StubVehiclesSource (object):
            def get_available_vehicles_near(self, sessionid, location, start_time, end_time):
                pass
        
        @Stub(_LocationsSourceInterface)
        class StubLocationsSource (object):
            pass
        
        # A generator for a representation (view) of the availability information
        @Stub(_VehiclesViewInterface)
        class StubVehiclesView (object):
            def get_vehicle_availability(self, session, start_time, end_time, vehicles, location):
                return "Success"
        
        @Stub(_ErrorViewInterface)
        class StubErrorView (object):
            def get_error(self, error_code, error_msg):
                return "Failure"
        
        # The system under test
        self.session_source = StubSessionSource()
        self.vehicle_source = StubVehiclesSource()
        self.location_source = StubLocationsSource()
        self.vehicle_view = StubVehiclesView()
        self.error_view = StubErrorView()
        
        self.handler = VehiclesHandler(session_source=self.session_source, 
            vehicle_source=self.vehicle_source,
            location_source=self.location_source,
            vehicle_view=self.vehicle_view,
            error_view=self.error_view)
        self.handler.request = StubRequest()
        self.handler.response = StubResponse()
    
    def testShouldUseCurrentTimeAndThreeHourDurationWhenNoStartOrEndIsGiven(self):
        # Given...
        # ...(no explicit input state)
        
        # When...
        start_time, end_time = self.handler.get_time_range()
        
        # Then...
        import datetime
        now_time = datetime.datetime.now(Eastern)
        later_time = now_time + datetime.timedelta(hours=3)
        threshold = datetime.timedelta(seconds=10)
        # ...can't check equality, as now_time and start_time were calculated at
        #    different times.  However, they should have been calculated within
        #    a certain amount of seconds from each other.
        self.assert_(now_time - start_time < threshold, 
            "%r - %r >= %r" % (now_time, start_time, threshold))
        self.assert_(later_time - end_time < threshold,
            "%r - %r >= %r" % (later_time, end_time, threshold))
        
    def testShouldRespondWithFailureContentWhenSessionSourceCannotFindSessionWithGivenId(self):
        """With no valid session, the availability handler will give a failure document response."""
        
        # Given...
        # ...the times and session cookies are as follows:
        self.handler.request['start_time'] = 100
        self.handler.request['end_time'] = 10000
        self.handler.request['location_id'] = 12345
        self.handler.request.cookies = {
          'sid':'5',
          'suser':'4600'
        }
        
        # ...and the session source does not recognize the cookies:
        @patch(self.session_source)
        def get_existing_session(self, userid, sessionid):
            raise ScreenscrapeParseError()
        
        @patch(self.location_source)
        def get_location_profile(self, sessionid, locationid):
            class StubLocation (object):
                id = locationid
            return StubLocation()
        
        # When...
        self.handler.get()
        
        # Then...
        response = self.handler.response.out.getvalue()
        self.assertEqual(response, "Failure")
    
    def testShouldGetSessionAndUserIdsFromCookies(self):
        # Given...
        self.handler.request.cookies = {
            'sid':'123abc',
            'suser':'u12345'
        }
        
        # When...
        sessionid = self.handler.get_session_id()
        userid = self.handler.get_user_id()
        
        # Then...
        self.assertEqual(userid, 'u12345')
        self.assertEqual(sessionid, '123abc')
    
    def testMissingSessionIdRiasesError(self):
        # Given...
        self.handler.request.cookies = {
            'suser':'u12345'
        }
        
        # When...
        try:
            sessionid = self.handler.get_session_id()
        
        # Then...
        except WsgiParameterError:
            return
        
        self.fail('Lack of session id should have caused a WsgiParameterError')
    
    def testMissingUserIdRiasesError(self):
        # Given...
        self.handler.request.cookies = {
            'sid':'123abc'
        }
        
        # When...
        try:
            userid = self.handler.get_user_id()
        
        # Then...
        except WsgiParameterError:
            return
        
        self.fail('Lack of session id should have caused a WsgiParameterError')
    
    def testShouldRespondWithSuccessContentWhenSessionSourceRecognizesGivenSessionId(self):
        """With a valid session, the availability handler will give a success response."""
        
        # Given...
        # ...the time and session cookies are as follows:
        self.handler.request['start_time'] = 100
        self.handler.request['end_time'] = 10000
        self.handler.request['location_id'] = 12345
        self.handler.request.cookies = {
          'sid':'5',
          'suser':'4600'
        }
        
        # ...and the session source recognizes the cookies:
        @patch(self.session_source)
        def get_existing_session(self, userid, sessionid):
            class StubSession (object):
                id = 5
                user = '4600'
                name = "Jim Jacobsen"
            return StubSession()
        
        @patch(self.location_source)
        def get_location_profile(self, sessionid, locationid):
            class StubLocation (object):
                id = locationid
            return StubLocation()
        
        # When...
        self.handler.get()
        
        # Then...
        response = self.handler.response.out.getvalue()
        self.assertEqual(response, "Success")
    
    def testLocationIdOfZeroShouldBeValid(self):
        """Receiving a request with a location id of 0 should not raise an exception"""
        
        # Given...
        self.handler.request['start_time'] = 100
        self.handler.request['end_time'] = 10000
        self.handler.request['location_id'] = 0
        self.handler.request.cookies = {
          'sid':'5',
          'suser':'4600'
        }
        
        # ...and the session source recognizes the cookies:
        @patch(self.session_source)
        def get_existing_session(self, userid, sessionid):
            class StubSession (object):
                id = 5
                user = '4600'
                name = "Jim Jacobsen"
            return StubSession()
        
        @patch(self.location_source)
        def get_location_profile(self, sessionid, locationid):
            class StubLocation (object):
                id = locationid
            return StubLocation()
        
        # When...
        try:
            self.handler.get()
        
        # Then...
        except WsgiParameterError:
            self.fail('No parameter exception should have been raised.')
        
    def testShouldRespondWithVehicleDataFromTheVehiclesSource(self):
        pass
    
        

from pcs.source.screenscrape.vehicles import VehiclesScreenscrapeSource
class VehiclesScreenscrapeSourceTest (unittest.TestCase):
    def testShouldLoadAppropriateJsonObjectFromString(self):
        # Given...
        source = VehiclesScreenscrapeSource()
        
        # When...
        json_data = source.get_json_data(
            '{"pods":["<div class=\\"pod_top\\"><\\/div>","<div class=\\"pod_bottom\\"><\/div>"]}')
        
        # Then...
        self.assertEqual(json_data,
            {'pods':['<div class="pod_top"></div>','<div class="pod_bottom"></div>']})
    
    def testShouldLoadAppropriateHtmlDocumentObjectFromPodsFieldOfJsonObject(self):
        """Should load appropriate HTML document object from the 'pods' field of the JSON object"""
        # Given...
        source = VehiclesScreenscrapeSource()
        
        # When...
        html_data = source.get_html_data(
            {'pods':['<div class="pod_top"></div><div class="pod_bottom"></div>','<div class="pod_top"></div><div class="pod_bottom"></div><div class="pod_bottom"></div>']})
        
        # Then...
        all_divs = html_data.findAll('div')
        btm_divs = html_data.findAll('div', {'class':'pod_bottom'})
        
        self.assertEqual(len(all_divs), 5)
        self.assertEqual(len(btm_divs), 3)
    
    def testShouldCreateCorrectPodFromHtmlData(self):
        # Given...
        doc_string = '''<html><body><div class="pod_top"><div class="pod_head"><h4><a class="text" href="my_fleet.php?mv_action=show&amp;_r=8&amp;pk=30005" onclick="MV.controls.results.show_pod_details(30005); return false;">47th &amp; Baltimore - 0.08 mile(s)</a></h4></div></div><div class="pod_top"><div class="pod_head"><h4><a class="text" href="my_fleet.php?mv_action=show&amp;_r=8&amp;pk=12174212" onclick="MV.controls.results.show_pod_details(12174212); return false;">46th &amp; Baltimore - 0.2 mile(s)</a></h4></div></div></body></html>'''
        from util.BeautifulSoup import BeautifulSoup
        doc = BeautifulSoup(doc_string)
        pod_info_divs = doc.findAll('div', {'class': 'pod_top'})
        pod_info_div = pod_info_divs[0]
        source = VehiclesScreenscrapeSource()
        
        # When...
        pod, dist = source.get_pod_and_distance_from_html_data(pod_info_div)
        
        # Then...
        self.assertEqual(pod.name, '47th &amp; Baltimore')
        self.assertEqual(dist, 0.08)
    
    def testShouldCreateCorrectVehicleFromHtmlData(self):
        # Given...
        doc_string = '''<html><body><div class="pod_bot pod_bot_maybe" id="page_result_1"><div id="time_line"><img width="439" height="25" src="skin/base_images/day_guage.gif"><span class="pod_estimates_images"><img src="/skin/base_images/hourly_cost.gif"></span></div><div class="list_left"><div class="v_img"><a href="http://www.phillycarshare.org/cars/prius" target="_blank"><img style="border: 0;" src="/images/client_images/prius_lift_thumb.gif"></a></div><div class="v_name"><h4>Prius Liftback</h4></div><div class="v_amenities"><ul><li><img src="/skin/base_images/hybrid.gif" label="Hybrid" title="Hybrid"></li><li><img src="/skin/base_images/folding_seat.gif" label="Folding Rear Seats" title="Folding Rear Seats"></li></ul></div></div><div class="list_mid"><div class="time"><ul class="segments"><li><ul><li class="bad pad_end"></li><li class="bad"></li><li class="bad"></li><li class="bad pad_end"></li></ul></li><li><ul><li class="bad pad_end"></li><li class="bad"></li><li class="bad"></li><li class="bad pad_end"></li></ul></li><li><ul><li class="bad pad_end"></li><li class="bad"></li><li class="bad"></li><li class="bad pad_end"></li></ul></li><li><ul><li class="bad pad_end"></li><li class="bad"></li><li class="bad"></li><li class="bad pad_end"></li></ul></li><li><ul><li class="bad pad_end"></li><li class="bad"></li><li class="bad"></li><li class="bad pad_end"></li></ul></li><li><ul><li class="bad pad_end"></li><li class="bad"></li><li class="bad"></li><li class="bad pad_end"></li></ul></li><li><ul><li class="bad pad_end"></li><li class="bad"></li><li class="bad"></li><li class="bad pad_end"></li></ul></li><li><ul><li class="bad pad_end"></li><li class="bad"></li><li class="bad"></li><li class="bad pad_end"></li></ul></li><li><ul><li class="slct_bkd pad_end"></li><li class="slct_bkd"></li><li class="slct_bkd"></li><li class="slct_bkd pad_end"></li></ul></li><li><ul><li class="slct_bkd pad_end"></li><li class="good"></li><li class="good"></li><li class="good pad_end"></li></ul></li><li><ul><li class="good pad_end"></li><li class="good"></li><li class="good"></li><li class="good pad_end"></li></ul></li><li><ul><li class="free pad_end"></li><li class="free"></li><li class="free"></li><li class="free pad_end"></li></ul></li><li><ul><li class="free pad_end"></li><li class="free"></li><li class="free"></li><li class="free pad_end"></li></ul></li><li><ul><li class="free pad_end"></li><li class="free"></li><li class="free"></li><li class="free pad_end"></li></ul></li><li><ul><li class="free pad_end"></li><li class="free"></li><li class="free"></li><li class="free pad_end"></li></ul></li><li><ul><li class="free pad_end"></li><li class="free"></li><li class="free"></li><li class="free pad_end"></li></ul></li><li><ul><li class="free pad_end"></li><li class="free"></li><li class="free"></li><li class="free pad_end"></li></ul></li><li><ul><li class="free pad_end"></li><li class="free"></li><li class="free"></li><li class="free pad_end"></li></ul></li><li><ul><li class="free pad_end"></li><li class="free"></li><li class="free"></li><li class="free pad_end"></li></ul></li><li><ul><li class="free pad_end"></li><li class="free"></li><li class="free"></li><li class="free pad_end"></li></ul></li><li><ul><li class="free pad_end"></li><li class="free"></li><li class="free"></li><li class="free pad_end"></li></ul></li><li><ul><li class="free pad_end"></li><li class="free"></li><li class="free"></li><li class="free pad_end"></li></ul></li><li><ul><li class="free pad_end"></li><li class="free"></li><li class="free"></li><li class="free pad_end"></li></ul></li><li><ul><li class="free pad_end"></li><li class="free"></li><li class="free"></li><li class="free pad_end"></li></ul></li></ul></div><div class="brick" style="width:50px; margin-left: 141px; -margin-left: 68px;"></div><div class="timestamp"><p class="maybe">Available from 3:15 pm on 08/24</p></div></div><div class="list_right"><div class="reserve"><a href="javascript:MV.controls.reserve.lightbox.create('1282672800', '1282683600', '96692246', '');">Select<span id="estimate_stack_956" class="est">$22.47</span></a></div><div id="rates_stack_956" class="price"><div><nobr><strong>$4.45</strong></nobr><br><nobr></nobr></div></div></div></div></body></html>'''
        from util.BeautifulSoup import BeautifulSoup
        doc = BeautifulSoup(doc_string)
        bodies = doc.findAll('body')
        body = bodies[0]
        vehicle_info_divs = body.findAll('div', recursive=False)
        vehicle_info_div = vehicle_info_divs[0]
        
        source = VehiclesScreenscrapeSource()
        fake_pod = object()
        
        # When...
        vehicle = source.get_vehicle_from_html_data(fake_pod, vehicle_info_div)
        
        # Then...
        self.assertEqual(vehicle.model, 'Prius Liftback')
        self.assertEqual(vehicle.pod, fake_pod)
    
    def testShouldGetTheCorrectNumberOfVehiclesSpecifiedOnPcsSite(self):
        # Given...
        class StubConnection (object):
            def request(self, method, path, data, headers):
                pass
            def getresponse(self):
                import StringIO
                class StubResponse (StringIO.StringIO):
                    def getheaders(self):
                        return {}
                return StubResponse('{"pods":[' +
                    ','.join(['''"<div class=\\"pod_top\\"><div class=\\"pod_head\\"><h4 ><a class=\\"text\\" href=\\"my_fleet.php?mv_action=show&_r=16&pk=30005\\"   onclick=\\"MV.controls.results.show_pod_details(30005); return false;\\" >47th & Baltimore - 0.08 mile(s)<\\/a><\\/h4><\\/div><\\/div><div class=\\"pod_bot \\" id=\\"page_result_1\\"><div id=\\"time_line\\"><img width=\\"439\\" height=\\"25\\" src=\\"skin\\/base_images\\/day_guage.gif\\" \\/><span class=\\"pod_estimates_images\\"><img src=\\"\\/skin\\/base_images\\/hourly_cost.gif\\" \\/><\\/span><\\/div><div class=\\"list_left\\"><div class=\\"v_img\\"><a href=\\"http:\\/\\/www.phillycarshare.org\\/cars\\/tacoma\\" target=\\"_blank\\"><img style=\\"border: 0;\\" src=\\"\\/images\\/client_images\\/toyota_tacoma_thumb.gif\\"\\/><\\/a><\\/div><div class=\\"v_name\\"><h4>Tacoma Pickup<\\/h4><\\/div><div class=\\"v_amenities\\"><ul><\\/ul><\\/div><\\/div><div class=\\"list_mid\\"><div class=\\"time\\"><ul class=\\"segments\\"><li ><ul ><li class=\\"bad pad_end\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad pad_end\\" \\/><\\/ul><\\/li><li ><ul ><li class=\\"bad pad_end\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad pad_end\\" \\/><\\/ul><\\/li><li ><ul ><li class=\\"bad pad_end\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad pad_end\\" \\/><\\/ul><\\/li><li ><ul ><li class=\\"bad pad_end\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad pad_end\\" \\/><\\/ul><\\/li><li ><ul ><li class=\\"bad pad_end\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad pad_end\\" \\/><\\/ul><\\/li><li ><ul ><li class=\\"bad pad_end\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad pad_end\\" \\/><\\/ul><\\/li><li ><ul ><li class=\\"bad pad_end\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad pad_end\\" \\/><\\/ul><\\/li><li ><ul ><li class=\\"bad pad_end\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad pad_end\\" \\/><\\/ul><\\/li><li ><ul ><li class=\\"bad pad_end\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad pad_end\\" \\/><\\/ul><\\/li><li ><ul ><li class=\\"bad pad_end\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad pad_end\\" \\/><\\/ul><\\/li><li ><ul ><li class=\\"bad pad_end\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad pad_end\\" \\/><\\/ul><\\/li><li ><ul ><li class=\\"bad pad_end\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad pad_end\\" \\/><\\/ul><\\/li><li ><ul ><li class=\\"bad pad_end\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad pad_end\\" \\/><\\/ul><\\/li><li ><ul ><li class=\\"bad pad_end\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad pad_end\\" \\/><\\/ul><\\/li><li ><ul ><li class=\\"bad pad_end\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad pad_end\\" \\/><\\/ul><\\/li><li ><ul ><li class=\\"bad pad_end\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad pad_end\\" \\/><\\/ul><\\/li><li ><ul ><li class=\\"bad pad_end\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad pad_end\\" \\/><\\/ul><\\/li><li ><ul ><li class=\\"bad pad_end\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad pad_end\\" \\/><\\/ul><\\/li><li ><ul ><li class=\\"bad pad_end\\" \\/><li class=\\"bad\\" \\/><li class=\\"free\\" \\/><li class=\\"free pad_end\\" \\/><\\/ul><\\/li><li ><ul ><li class=\\"free pad_end\\" \\/><li class=\\"good\\" \\/><li class=\\"good\\" \\/><li class=\\"good pad_end\\" \\/><\\/ul><\\/li><li ><ul ><li class=\\"good pad_end\\" \\/><li class=\\"good\\" \\/><li class=\\"good\\" \\/><li class=\\"good pad_end\\" \\/><\\/ul><\\/li><li ><ul ><li class=\\"good pad_end\\" \\/><li class=\\"free\\" \\/><li class=\\"free\\" \\/><li class=\\"free pad_end\\" \\/><\\/ul><\\/li><li ><ul ><li class=\\"free pad_end\\" \\/><li class=\\"free\\" \\/><li class=\\"free\\" \\/><li class=\\"free pad_end\\" \\/><\\/ul><\\/li><li ><ul ><li class=\\"free pad_end\\" \\/><li class=\\"free\\" \\/><li class=\\"free\\" \\/><li class=\\"free pad_end\\" \\/><\\/ul><\\/li><\\/ul><\\/div><div class=\\"brick\\" style=\\"width:32px; margin-left: 333px; -margin-left: 164px;\\"><\\/div><div class=\\"timestamp\\"><p class=\\"good\\">Available<\\/p><\\/div><\\/div><div class=\\"list_right\\"><div class=\\"reserve\\"><a href=\\"javascript:MV.controls.reserve.lightbox.create('1282540500', '1282547700', '91800598', '');\\">Select<span id=\\"estimate_stack_894\\" class=\\"est\\"><\\/span><\\/a><\\/div><div id=\\"rates_stack_894\\" class=\\"price\\"><\\/div><\\/div><\\/div><div class=\\"pod_bot \\" id=\\"page_result_2\\"><div class=\\"list_left\\"><div class=\\"v_img\\"><img style=\\"border: 0;\\" src=\\"\\/images\\/client_images\\/prius_lift_thumb.gif\\"\\/><\\/div><div class=\\"v_name\\"><h4>Prius Liftback<\\/h4><\\/div><div class=\\"v_amenities\\"><ul><li><img src=\\"\\/skin\\/base_images\\/hybrid.gif\\" label=\\"Hybrid\\" title=\\"Hybrid\\"\\/><\\/li>\\n<li><img src=\\"\\/skin\\/base_images\\/folding_seat.gif\\" label=\\"Folding Rear Seats\\" title=\\"Folding Rear Seats\\"\\/><\\/li><\\/ul><\\/div><\\/div><div class=\\"list_mid\\"><div class=\\"time\\"><ul class=\\"segments\\"><li ><ul ><li class=\\"bad pad_end\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad pad_end\\" \\/><\\/ul><\\/li><li ><ul ><li class=\\"bad pad_end\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad pad_end\\" \\/><\\/ul><\\/li><li ><ul ><li class=\\"bad pad_end\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad pad_end\\" \\/><\\/ul><\\/li><li ><ul ><li class=\\"bad pad_end\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad pad_end\\" \\/><\\/ul><\\/li><li ><ul ><li class=\\"bad pad_end\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad pad_end\\" \\/><\\/ul><\\/li><li ><ul ><li class=\\"bad pad_end\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad pad_end\\" \\/><\\/ul><\\/li><li ><ul ><li class=\\"bad pad_end\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad pad_end\\" \\/><\\/ul><\\/li><li ><ul ><li class=\\"bad pad_end\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad pad_end\\" \\/><\\/ul><\\/li><li ><ul ><li class=\\"bad pad_end\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad pad_end\\" \\/><\\/ul><\\/li><li ><ul ><li class=\\"bad pad_end\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad pad_end\\" \\/><\\/ul><\\/li><li ><ul ><li class=\\"bad pad_end\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad pad_end\\" \\/><\\/ul><\\/li><li ><ul ><li class=\\"bad pad_end\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad pad_end\\" \\/><\\/ul><\\/li><li ><ul ><li class=\\"bad pad_end\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad pad_end\\" \\/><\\/ul><\\/li><li ><ul ><li class=\\"bad pad_end\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad pad_end\\" \\/><\\/ul><\\/li><li ><ul ><li class=\\"bad pad_end\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad pad_end\\" \\/><\\/ul><\\/li><li ><ul ><li class=\\"bad pad_end\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad pad_end\\" \\/><\\/ul><\\/li><li ><ul ><li class=\\"bad pad_end\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad pad_end\\" \\/><\\/ul><\\/li><li ><ul ><li class=\\"bad pad_end\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad pad_end\\" \\/><\\/ul><\\/li><li ><ul ><li class=\\"bad pad_end\\" \\/><li class=\\"bad\\" \\/><li class=\\"free\\" \\/><li class=\\"free pad_end\\" \\/><\\/ul><\\/li><li ><ul ><li class=\\"free pad_end\\" \\/><li class=\\"good\\" \\/><li class=\\"good\\" \\/><li class=\\"good pad_end\\" \\/><\\/ul><\\/li><li ><ul ><li class=\\"good pad_end\\" \\/><li class=\\"good\\" \\/><li class=\\"good\\" \\/><li class=\\"good pad_end\\" \\/><\\/ul><\\/li><li ><ul ><li class=\\"good pad_end\\" \\/><li class=\\"free\\" \\/><li class=\\"free\\" \\/><li class=\\"free pad_end\\" \\/><\\/ul><\\/li><li ><ul ><li class=\\"free pad_end\\" \\/><li class=\\"free\\" \\/><li class=\\"free\\" \\/><li class=\\"free pad_end\\" \\/><\\/ul><\\/li><li ><ul ><li class=\\"free pad_end\\" \\/><li class=\\"free\\" \\/><li class=\\"free\\" \\/><li class=\\"free pad_end\\" \\/><\\/ul><\\/li><\\/ul><\\/div><div class=\\"brick\\" style=\\"width:32px; margin-left: 333px; -margin-left: 164px;\\"><\\/div><div class=\\"timestamp\\"><p class=\\"good\\">Available<\\/p><\\/div><\\/div><div class=\\"list_right\\"><div class=\\"reserve\\"><a href=\\"javascript:MV.controls.reserve.lightbox.create('1282540500', '1282547700', '96692246', '');\\">Select<span id=\\"estimate_stack_956\\" class=\\"est\\"><\\/span><\\/a><\\/div><div id=\\"rates_stack_956\\" class=\\"price\\"><\\/div><\\/div><\\/div>"''',
                              '''"<div class=\\"pod_top\\"><div class=\\"pod_head\\"><h4 ><a class=\\"text\\" href=\\"my_fleet.php?mv_action=show&_r=16&pk=12174212\\"   onclick=\\"MV.controls.results.show_pod_details(12174212); return false;\\" >46th & Baltimore - 0.2 mile(s)<\\/a><\\/h4><\\/div><\\/div><div class=\\"pod_bot \\" id=\\"page_result_3\\"><div class=\\"list_left\\"><div class=\\"v_img\\"><a href=\\"http:\\/\\/www.phillycarshare.org\\/cars\\/element\\" target=\\"_blank\\"><img style=\\"border: 0;\\" src=\\"\\/images\\/client_images\\/honda_element_thumb.gif\\"\\/><\\/a><\\/div><div class=\\"v_name\\"><h4>Honda Element<\\/h4><\\/div><div class=\\"v_amenities\\"><ul><li><img src=\\"\\/skin\\/base_images\\/awd.gif\\" label=\\"All Wheel Drive\\" title=\\"All Wheel Drive\\"\\/><\\/li>\\n<li><img src=\\"\\/skin\\/base_images\\/folding_seat.gif\\" label=\\"Folding Rear Seats\\" title=\\"Folding Rear Seats\\"\\/><\\/li><\\/ul><\\/div><\\/div><div class=\\"list_mid\\"><div class=\\"time\\"><ul class=\\"segments\\"><li ><ul ><li class=\\"bad pad_end\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad pad_end\\" \\/><\\/ul><\\/li><li ><ul ><li class=\\"bad pad_end\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad pad_end\\" \\/><\\/ul><\\/li><li ><ul ><li class=\\"bad pad_end\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad pad_end\\" \\/><\\/ul><\\/li><li ><ul ><li class=\\"bad pad_end\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad pad_end\\" \\/><\\/ul><\\/li><li ><ul ><li class=\\"bad pad_end\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad pad_end\\" \\/><\\/ul><\\/li><li ><ul ><li class=\\"bad pad_end\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad pad_end\\" \\/><\\/ul><\\/li><li ><ul ><li class=\\"bad pad_end\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad pad_end\\" \\/><\\/ul><\\/li><li ><ul ><li class=\\"bad pad_end\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad pad_end\\" \\/><\\/ul><\\/li><li ><ul ><li class=\\"bad pad_end\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad pad_end\\" \\/><\\/ul><\\/li><li ><ul ><li class=\\"bad pad_end\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad pad_end\\" \\/><\\/ul><\\/li><li ><ul ><li class=\\"bad pad_end\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad pad_end\\" \\/><\\/ul><\\/li><li ><ul ><li class=\\"bad pad_end\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad pad_end\\" \\/><\\/ul><\\/li><li ><ul ><li class=\\"bad pad_end\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad pad_end\\" \\/><\\/ul><\\/li><li ><ul ><li class=\\"bad pad_end\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad pad_end\\" \\/><\\/ul><\\/li><li ><ul ><li class=\\"bad pad_end\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad pad_end\\" \\/><\\/ul><\\/li><li ><ul ><li class=\\"bad pad_end\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad pad_end\\" \\/><\\/ul><\\/li><li ><ul ><li class=\\"bad pad_end\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad pad_end\\" \\/><\\/ul><\\/li><li ><ul ><li class=\\"bad pad_end\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad pad_end\\" \\/><\\/ul><\\/li><li ><ul ><li class=\\"bad pad_end\\" \\/><li class=\\"bad\\" \\/><li class=\\"free\\" \\/><li class=\\"free pad_end\\" \\/><\\/ul><\\/li><li ><ul ><li class=\\"free pad_end\\" \\/><li class=\\"good\\" \\/><li class=\\"good\\" \\/><li class=\\"good pad_end\\" \\/><\\/ul><\\/li><li ><ul ><li class=\\"good pad_end\\" \\/><li class=\\"good\\" \\/><li class=\\"good\\" \\/><li class=\\"good pad_end\\" \\/><\\/ul><\\/li><li ><ul ><li class=\\"good pad_end\\" \\/><li class=\\"free\\" \\/><li class=\\"free\\" \\/><li class=\\"free pad_end\\" \\/><\\/ul><\\/li><li ><ul ><li class=\\"free pad_end\\" \\/><li class=\\"free\\" \\/><li class=\\"free\\" \\/><li class=\\"free pad_end\\" \\/><\\/ul><\\/li><li ><ul ><li class=\\"free pad_end\\" \\/><li class=\\"free\\" \\/><li class=\\"free\\" \\/><li class=\\"free pad_end\\" \\/><\\/ul><\\/li><\\/ul><\\/div><div class=\\"brick\\" style=\\"width:32px; margin-left: 333px; -margin-left: 164px;\\"><\\/div><div class=\\"timestamp\\"><p class=\\"good\\">Available<\\/p><\\/div><\\/div><div class=\\"list_right\\"><div class=\\"reserve\\"><a href=\\"javascript:MV.controls.reserve.lightbox.create('1282540500', '1282547700', '130868710', '');\\">Select<span id=\\"estimate_stack_1195\\" class=\\"est\\"><\\/span><\\/a><\\/div><div id=\\"rates_stack_1195\\" class=\\"price\\"><\\/div><\\/div><\\/div><div class=\\"pod_bot \\" id=\\"page_result_4\\"><div class=\\"list_left\\"><div class=\\"v_img\\"><img style=\\"border: 0;\\" src=\\"\\/images\\/client_images\\/prius_lift_thumb.gif\\"\\/><\\/div><div class=\\"v_name\\"><h4>Prius Liftback<\\/h4><\\/div><div class=\\"v_amenities\\"><ul><li><img src=\\"\\/skin\\/base_images\\/hybrid.gif\\" label=\\"Hybrid\\" title=\\"Hybrid\\"\\/><\\/li>\\n<li><img src=\\"\\/skin\\/base_images\\/folding_seat.gif\\" label=\\"Folding Rear Seats\\" title=\\"Folding Rear Seats\\"\\/><\\/li><\\/ul><\\/div><\\/div><div class=\\"list_mid\\"><div class=\\"time\\"><ul class=\\"segments\\"><li ><ul ><li class=\\"bad pad_end\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad pad_end\\" \\/><\\/ul><\\/li><li ><ul ><li class=\\"bad pad_end\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad pad_end\\" \\/><\\/ul><\\/li><li ><ul ><li class=\\"bad pad_end\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad pad_end\\" \\/><\\/ul><\\/li><li ><ul ><li class=\\"bad pad_end\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad pad_end\\" \\/><\\/ul><\\/li><li ><ul ><li class=\\"bad pad_end\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad pad_end\\" \\/><\\/ul><\\/li><li ><ul ><li class=\\"bad pad_end\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad pad_end\\" \\/><\\/ul><\\/li><li ><ul ><li class=\\"bad pad_end\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad pad_end\\" \\/><\\/ul><\\/li><li ><ul ><li class=\\"bad pad_end\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad pad_end\\" \\/><\\/ul><\\/li><li ><ul ><li class=\\"bad pad_end\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad pad_end\\" \\/><\\/ul><\\/li><li ><ul ><li class=\\"bad pad_end\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad pad_end\\" \\/><\\/ul><\\/li><li ><ul ><li class=\\"bad pad_end\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad pad_end\\" \\/><\\/ul><\\/li><li ><ul ><li class=\\"bad pad_end\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad pad_end\\" \\/><\\/ul><\\/li><li ><ul ><li class=\\"bad pad_end\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad pad_end\\" \\/><\\/ul><\\/li><li ><ul ><li class=\\"bad pad_end\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad pad_end\\" \\/><\\/ul><\\/li><li ><ul ><li class=\\"bad pad_end\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad pad_end\\" \\/><\\/ul><\\/li><li ><ul ><li class=\\"bad pad_end\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad pad_end\\" \\/><\\/ul><\\/li><li ><ul ><li class=\\"bad pad_end\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad pad_end\\" \\/><\\/ul><\\/li><li ><ul ><li class=\\"bad pad_end\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad pad_end\\" \\/><\\/ul><\\/li><li ><ul ><li class=\\"bad pad_end\\" \\/><li class=\\"bad\\" \\/><li class=\\"bad\\" \\/><li class=\\"free pad_end\\" \\/><\\/ul><\\/li><li ><ul ><li class=\\"free pad_end\\" \\/><li class=\\"good\\" \\/><li class=\\"good\\" \\/><li class=\\"good pad_end\\" \\/><\\/ul><\\/li><li ><ul ><li class=\\"good pad_end\\" \\/><li class=\\"good\\" \\/><li class=\\"good\\" \\/><li class=\\"good pad_end\\" \\/><\\/ul><\\/li><li ><ul ><li class=\\"good pad_end\\" \\/><li class=\\"free\\" \\/><li class=\\"free\\" \\/><li class=\\"free pad_end\\" \\/><\\/ul><\\/li><li ><ul ><li class=\\"free pad_end\\" \\/><li class=\\"free\\" \\/><li class=\\"free\\" \\/><li class=\\"free pad_end\\" \\/><\\/ul><\\/li><li ><ul ><li class=\\"free pad_end\\" \\/><li class=\\"free\\" \\/><li class=\\"free\\" \\/><li class=\\"free pad_end\\" \\/><\\/ul><\\/li><\\/ul><\\/div><div class=\\"brick\\" style=\\"width:32px; margin-left: 333px; -margin-left: 164px;\\"><\\/div><div class=\\"timestamp\\"><p class=\\"good\\">Available<\\/p><\\/div><\\/div><div class=\\"list_right\\"><div class=\\"reserve\\"><a href=\\"javascript:MV.controls.reserve.lightbox.create('1282540500', '1282547700', '73484842', '');\\">Select<span id=\\"estimate_stack_734\\" class=\\"est\\"><\\/span><\\/a><\\/div><div id=\\"rates_stack_734\\" class=\\"price\\"><\\/div><\\/div><\\/div>"''']) + 
                    ']}')
        
        source = VehiclesScreenscrapeSource()
        @patch(source)
        def create_host_connection(self):
            return StubConnection()
        
        # When...
        stime = etime = datetime.datetime.now(Eastern)
        vehicles = source.get_available_vehicles_near('','',stime,etime)
        
        # Then...
        self.assertEqual([v.model for v in vehicles], ['Tacoma Pickup','Prius Liftback','Honda Element','Prius Liftback'])
    
    def testTimeQueryShouldReflectGivenDatetimes(self):
        source = VehiclesScreenscrapeSource()
        starttime = datetime.datetime(2003,1,2,1,15,tzinfo=Eastern)
        endtime = datetime.datetime(2003,1,2,1,30,tzinfo=Eastern)
        
        query = source.get_time_query(starttime, endtime)
        
        self.assertEqual(query, "start_date=1/2/2003&start_time=4500&end_date=1/2/2003&end_time=5400")
    
    def testShouldCorrectlyParseVehiclesFromStipulationAboutEarliestVehicles(self):
        source = VehiclesScreenscrapeSource()
        class StubVehicle (object):
            pass
        vehicle = StubVehicle()
        stipulation = 'Available from 3:30 pm on 09/01'
        
        source.assign_vehicle_availability_stipulation(vehicle, stipulation)
        
        now = datetime.datetime.now(Eastern)
        year = now.year if now.month < 9 else now.year+1
        month = 9
        day = 1
        hour = 15
        minute = 30
        self.assertEqual(vehicle.available_from, datetime.datetime(year, month, day, hour, minute, tzinfo=Eastern))
    
    def testShouldCorrectlyParseVehiclesFromStipulationAboutLatestVehicles(self):
        source = VehiclesScreenscrapeSource()
        class StubVehicle (object):
            pass
        vehicle = StubVehicle()
        stipulation = 'Available until 3:30 pm on 09/01'
        
        source.assign_vehicle_availability_stipulation(vehicle, stipulation)
        
        now = datetime.datetime.now(Eastern)
        year = now.year if now.month < 9 else now.year+1
        month = 9
        day = 1
        hour = 15
        minute = 30
        self.assertEqual(vehicle.available_until, datetime.datetime(year, month, day, hour, minute, tzinfo=Eastern))
    
    def testShouldCorrectlyParseVehiclesFromStipulationAboutSandwichedVehicles(self):
        source = VehiclesScreenscrapeSource()
        class StubVehicle (object):
            pass
        vehicle = StubVehicle()
        stipulation = 'Available from 3:30 pm on 09/01 to 4:45 am on 09/02'
        
        source.assign_vehicle_availability_stipulation(vehicle, stipulation)
        
        now = datetime.datetime.now(Eastern)
        year = now.year if now.month < 9 else now.year+1
        month = 9
        day = 1
        hour = 15
        minute = 30
        self.assertEqual(vehicle.available_from, datetime.datetime(year, month, day, hour, minute, tzinfo=Eastern))
        
        now = datetime.datetime.now(Eastern)
        day = 2
        hour = 4
        minute = 45
        self.assertEqual(vehicle.available_until, datetime.datetime(year, month, day, hour, minute, tzinfo=Eastern))
    
from pcs.input.wsgi.vehicles import VehiclesHtmlHandler
class VehiclesHtmlHandlerTest (unittest.TestCase):
    def testShouldBeInitializedWithHtmlViewsAndScreenscrapeSources(self):
        handler = VehiclesHtmlHandler()
        
        from pcs.source.screenscrape.session import SessionScreenscrapeSource
        from pcs.source.screenscrape.locations import LocationsScreenscrapeSource
        from pcs.source.screenscrape.vehicles import VehiclesScreenscrapeSource
        from pcs.view.html.vehicles import VehiclesHtmlView
        
        self.assertEqual(handler.vehicle_view.__class__.__name__,
                         VehiclesHtmlView.__name__)
        self.assertEqual(handler.vehicle_source.__class__.__name__,
                         VehiclesScreenscrapeSource.__name__)
        self.assertEqual(handler.location_source.__class__.__name__,
                         LocationsScreenscrapeSource.__name__)
        self.assertEqual(handler.session_source.__class__.__name__,
                         SessionScreenscrapeSource.__name__)

