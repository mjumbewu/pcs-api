import unittest
import datetime
import new

from pcs.input.wsgi.availability import AvailabilityHandler
from pcs.source import _AvailabilitySourceInterface
from pcs.source import _SessionSourceInterface
from pcs.view import _AvailabilityViewInterface
from util.testing import patch
from util.testing import Stub

class AvailabilityHandlerTest (unittest.TestCase):
    
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
        @Stub(_AvailabilitySourceInterface)
        class StubAvailabilitySource (object):
            def get_available_vehicles_near(self, sessionid, location, start_time, end_time):
                pass
        
        # A generator for a representation (view) of the availability information
        @Stub(_AvailabilityViewInterface)
        class StubAvailabilityView (object):
            def get_vehicle_availability(self, session, start_time, end_time, vehicles, location):
                if session:
                    return "Success"
                else:
                    return "Failure"
        
        # The system under test
        self.session_source = StubSessionSource()
        self.availability_source = StubAvailabilitySource()
        self.availability_view = StubAvailabilityView()
        
        self.handler = AvailabilityHandler(session_source=self.session_source, 
            availability_source=self.availability_source,
            availability_view=self.availability_view)
        self.handler.request = StubRequest()
        self.handler.response = StubResponse()
    
    def testShouldUseCurrentTimeAndThreeHourDurationWhenNoStartOrEndIsGiven(self):
        # Given...
        # ...(no explicit input state)
        
        # When...
        start_time, end_time = self.handler.get_time_range()
        
        # Then...
        import datetime
        now_time = datetime.datetime.now()
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
        self.handler.request.cookies = {
          'sid':'5',
          'suser':'4600'
        }
        
        # ...and the session source does not recognize the cookies:
        @patch(self.session_source)
        def get_existing_session(self, userid, sessionid):
            return None
        
        # When...
        self.handler.get()
        
        # Then...
        response = self.handler.response.out.getvalue()
        self.assertEqual(response, "Failure")

    def testShouldRespondWithSuccessContentWhenSessionSourceRecognizesGivenSessionId(self):
        """With a valid session, the availability handler will give a success response."""
        
        # Given...
        # ...the time and session cookies are as follows:
        self.handler.request['start_time'] = 100
        self.handler.request['end_time'] = 10000
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
        
        # When...
        self.handler.get()
        
        # Then...
        response = self.handler.response.out.getvalue()
        self.assertEqual(response, "Success")
    
    def testShouldRespondWithVehicleDataFromTheAvailabilitySource(self):
        pass

from pcs.source.screenscrape.availability import AvailabilityScreenscrapeSource
class AvailabilityScreenscrapeSourceTest (unittest.TestCase):
    def testShouldLoadAppropriateJsonObjectFromString(self):
        # Given...
        source = AvailabilityScreenscrapeSource()
        
        # When...
        json_data = source.get_json_data(
            '{"pods":["<div class=\\"pod_top\\"><\\/div>","<div class=\\"pod_bottom\\"><\/div>"]}')
        
        # Then...
        self.assertEqual(json_data,
            {'pods':['<div class="pod_top"></div>','<div class="pod_bottom"></div>']})
    
    def testShouldLoadAppropriateHtmlDocumentObjectFromPodsFieldOfJsonObject(self):
        """Should load appropriate HTML document object from the 'pods' field of the JSON object"""
        # Given...
        source = AvailabilityScreenscrapeSource()
        
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
        source = AvailabilityScreenscrapeSource()
        
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
        
        source = AvailabilityScreenscrapeSource()
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
        
        source = AvailabilityScreenscrapeSource()
        @patch(source)
        def create_host_connection(self):
            return StubConnection()
        
        # When...
        vehicles = source.get_available_vehicles_near('','','','')
        
        # Then...
        self.assertEqual([v.model for v in vehicles], ['Tacoma Pickup','Prius Liftback','Honda Element','Prius Liftback'])

from pcs.view.html.availability import AvailabilityHtmlView
class AvailabilityHtmlViewTest (unittest.TestCase):
    def testShouldReturnHtmlContentReflectingVehicleAvailability(self):
        """The HTML view returned by get_vehicle_availability should reflect the data given."""
        
        # Given...
        class StubSession (object):
            pass
        
        class StubPod (object):
            pass
        
        class StubVehicle (object):
            pass
        
        session = StubSession()
        
        p1 = StubPod(); p1.id = 1; p1.name = "Pod 1"
        p2 = StubPod(); p2.id = 2; p2.name = "Pod 2"
        
        v1 = StubVehicle()
        v1.id = 3
        v1.pod = p1
        v1.availability = 1
        v1.make = 'Toyota'
        v1.model = 'Prius'
        
        v2 = StubVehicle()
        v2.id = 4
        v2.pod = p1
        v2.availability = 0.5
        v2.make = 'Toyota'
        v2.model = 'Prius'
        v2.available_at = datetime.datetime.fromtimestamp(4000)
        
        v3 = StubVehicle()
        v3.id = 5
        v3.pod = p1
        v3.availability = 1
        v3.make = 'Toyota'
        v3.model = 'Prius'
        
        v4 = StubVehicle()
        v4.id = 6
        v4.pod = p2
        v4.availability = 0
        v4.make = 'Toyota'
        v4.model = 'Prius'
        
        start_time = datetime.datetime.fromtimestamp(0)
        end_time = datetime.datetime.fromtimestamp(10000)
        
        view = AvailabilityHtmlView()
        
        # When...
        response_body = view.get_vehicle_availability(session, start_time, end_time, 
            [v1,v2,v3,v4], 'My Current Location')
        
        # Then...
        expected_body = \
"""<!DOCTYPE html>

<html>
  <head>
    <title>PhillyCarShare - Available Cars </title>
  </head>
  
  <body>
    
      
      
  
  <style>
    .available-vehicle {
      border: 1px solid green;
    }
    .unavailable-vehicle {
      border: 1px solid red;
    }
    .partially-available-vehicle {
      border: 1px solid yellow;
    }
  </style>
  
  <h1>Available Cars</h1>
  
  <div class="availability-options">
    <span>Showing cars near My Current Location</span>
    <span>from midnight Thu Jan 01 1970</span>
    <span>until 2:46 a.m. Thu Jan 01 1970</span>
  </div>
  
  
  
    <div class="available-pod">
      <div class="pod-name">Pod 1</div>
      
        
          <div class="available-vehicle">
        
          
          <span>Toyota Prius</span>
          <div class="vehicle-stipulations">
            
            
          </div>
        </div>
      
        
          <div class="partially-available-vehicle">
        
          
          <span>Toyota Prius</span>
          <div class="vehicle-stipulations">
            
              <span>Available at 1:06 a.m.</span>
            
            
          </div>
        </div>
      
        
          <div class="available-vehicle">
        
          
          <span>Toyota Prius</span>
          <div class="vehicle-stipulations">
            
            
          </div>
        </div>
      
    </div>
  
    <div class="available-pod">
      <div class="pod-name">Pod 2</div>
      
        
          <div class="unavailabe-vehicle">
        
          
          <span>Toyota Prius</span>
          <div class="vehicle-stipulations">
            
            
          </div>
        </div>
      
    </div>
  
  

      
    
  </body>
</html>

"""
        response_body = response_body.replace('<','&lt;')
        response_body = response_body.replace('>','&gt;')
        expected_body = expected_body.replace('<','&lt;')
        expected_body = expected_body.replace('>','&gt;')
        
        self.assertEqual(response_body, expected_body)

from pcs.input.wsgi.availability import AvailabilityHtmlHandler
class AvailabilityHtmlHandlerTest (unittest.TestCase):
    def testShouldBeInitializedWithHtmlViewsAndScreenscrapeSources(self):
        handler = AvailabilityHtmlHandler()
        
        self.assertEqual(handler.availability_view.__class__.__name__,
                         AvailabilityHtmlView.__name__)


