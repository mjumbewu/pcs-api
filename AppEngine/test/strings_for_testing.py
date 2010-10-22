PAST_RESERVATIONS_FIRST_OF_TWO_PAGES = r'''
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"><html xmlns="http://www.w3.org/1999/xhtml"><head> 
<meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1" /> 
<meta http-equiv="pragma" content="no-cache" /> 
<meta http-equiv="cache-control" content="no-cache" /> 
<title >Reservation Manager</title><link rel="stylesheet" type="text/css" href="/skin/pcs_ui.css_3_47_0_5" title="pcs_skin" media="screen, print" /><link rel="stylesheet" type="text/css" href="/skin/pcs_layout.css_3_47_0_5" title="pcs_skin" media="screen, print" /><link rel="stylesheet" type="text/css" href="/skin/pcs_buttons.css_3_47_0_5" title="pcs_skin" media="screen, print" /><link rel="stylesheet" type="text/css" href="/skin/pcs_skin.css_3_47_0_5" title="pcs_skin" media="screen, print" /></head> 
<body bgcolor="white"  ><script language="javascript" type="text/javascript" src="/js/helper.js_3_47_0_5"></script> 
<script language="javascript" type="text/javascript" src="/js/prototype.js_3_47_0_5"></script> 
<script language="javascript" type="text/javascript" src="/js/lowpro.js_3_47_0_5"></script> 
<script language="javascript" type="text/javascript" src="/js/slider.js_3_47_0_5"></script> 
<script language="javascript" type="text/javascript" src="/js/lightbox.js_3_47_0_5"></script> 
<script language="javascript" type="text/javascript" src="/js/mf_lightbox.js_3_47_0_5"></script> 
<script language="javascript" type="text/javascript" src="/js/mv_base.js_3_47_0_5"></script> 
<script language="javascript" type="text/javascript" src="/js/mv_reserve.js_3_47_0_5"></script> 
<div class="mv_header"> 
<img border="0" src="/images/client_images/pcs_web_logo.gif" alt="PhillyCarShare" title="PhillyCarShare" /> 
</div> 
<div id="wrapper"><div id="page_header"><div id="lame_image"><span class="switch"> 
<a class="text" href="/members/help.html?_r=9"  target="_blank"  >Help</a></span> 
<p >Mjumbe Poe, you are signed in. (Residential Account)</p><a href="my_reservations.php?_r=9&mv_action=logout"> 
                            <img class="logbutton" alt = "Log Out" src="/skin/base_images/btn_logout.gif" /> 
                   </a></div><img id="logo" src="/images/client_images/pcs_web_logo.gif" alt="PhillyCarShare" title="PhillyCarShare" /> 
        <div id="nav_bar"> 
        <div id="navcontainer"> 
        <ul id="navlist"><li ><a class="text link_new_reservation" href="my_reservations.php?_r=9"    >New Reservation</a></li><li ><a class="link_my_reservations" href="my_reservations.php?mv_action=main&_r=9"    >My Reservations</a></li><li ><a class="text link_my_messages" href="my_messages.php?_r=9"    >My Messages</a></li><li ><a class="text link_my_info" href="my_info.php?_r=9"    >My Account</a></li><li ><a class="text link_my_problems" href="my_problems.php?_r=9"    >Member Feedback</a></li></ul></div></div></div><div class="midbox"><h3 >My Reservations</h3><h5 >Past and Current Reservations</h5><div class="multi_filter"><form id="main_multi_filter_" name="multi_filter" action="my_reservations.php" method="get"  ><label for="main_multi_filter__history_" id="main_multi_filter__history__label"><b>Reservation&nbsp;Selection</b>:&nbsp;</label><select name="main[multi_filter][history][yearmonth]"    id="main_multi_filter__history__yearmonth_" tabindex="0"  > 
  <option value="-1">Current Reservations</option> 
  <option value="201010">October&nbsp;2010</option> 
  <option value="201009" selected>September&nbsp;2010</option> 
  <option value="201008">August&nbsp;2010</option> 
  <option value="201007">July&nbsp;2010</option> 
  <option value="201006">June&nbsp;2010</option> 
  <option value="201005">May&nbsp;2010</option> 
  <option value="201004">April&nbsp;2010</option> 
 </select><span class="instruction">&nbsp;</span><span ><td    align="center" valign="middle"  ><input type="hidden" name="mv_action" value="main"/> 
<input type="hidden" name="_r" value="9"/> 
<button  id="main" type="submit" class="button_update" ></button> 
</td> 
</span><input id="main_multi_filter__driver_pk_" type="hidden" name="main[multi_filter][driver_pk]" value="6285517" /></form></div><form name="main" method="post"><form id="main_dlist_" name="dlist" action="my_reservations.php" method="post"  ><tr ><td ><table class="dlist ma" id="main_dlist_"><thead ><tr ><td     align="center" valign="middle"  ><a class="text" href="my_reservations.php?main[multi_filter][history][yearmonth]=201009&mv_action=main&_r=9&main[multi_filter][driver_pk]=6285517&main[dlist][sort_col]=res_id&main[dlist][sort_dir]=asc"    >ID</a></td> 
<td     align="center" valign="middle"  ><a class="text" href="my_reservations.php?main[multi_filter][history][yearmonth]=201009&mv_action=main&_r=9&main[multi_filter][driver_pk]=6285517&main[dlist][sort_col]=ustack_descr&main[dlist][sort_dir]=asc"    >Stack</a></td> 
<td     align="center" valign="middle"  ><a class="text" href="my_reservations.php?main[multi_filter][history][yearmonth]=201009&mv_action=main&_r=9&main[multi_filter][driver_pk]=6285517&main[dlist][sort_col]=res_start&main[dlist][sort_dir]=asc"    >Start</a></td> 
<td     align="center" valign="middle"  ><a class="text" href="my_reservations.php?main[multi_filter][history][yearmonth]=201009&mv_action=main&_r=9&main[multi_filter][driver_pk]=6285517&main[dlist][sort_col]=res_end&main[dlist][sort_dir]=desc"    >End</a></td> 
<th  width="1%"  align="center" valign="middle"  ><font class="textbb">Est&nbsp;Cost</font></th> 
<td     align="center" valign="middle"  ><a class="text" href="my_reservations.php?main[multi_filter][history][yearmonth]=201009&mv_action=main&_r=9&main[multi_filter][driver_pk]=6285517&main[dlist][sort_col]=reservation_status&main[dlist][sort_dir]=asc"    >Status</a></td> 
<td     align="center" valign="middle"  ><a class="text" href="my_reservations.php?main[multi_filter][history][yearmonth]=201009&mv_action=main&_r=9&main[multi_filter][driver_pk]=6285517&main[dlist][sort_col]=res_extra&main[dlist][sort_dir]=asc"    >Memo</a></td> 
</tr></thead><tbody ><tr class="zebra"><td >2460589</td><td   width="25%"  align="center" valign="middle"  ><a class="text" href="my_fleet.php?mv_action=show&_r=9&pk=5736346"    >47th & Pine - Prius Liftback</a></td> 
<td >12:45 pm Wednesday, September 1, 2010</td><td >4:45 pm Wednesday, September 1, 2010</td><td ><a href="#" class="tooltip_target" style="cursor: help;">$29.28</a> 
                <span class="tooltip" style="position: absolute; z-index: 1000; display: none;">$17.80&nbsp;(Time)&nbsp;+<br/>$7.00&nbsp;(Distance&nbsp;@&nbsp;28&nbsp;mile(s))&nbsp;+<br/>$0.00&nbsp;(Fees)&nbsp;+<br/>$4.48&nbsp;(Tax)</span></td><td >Normal</td><td >rasheed</td></tr><tr ><td >2462897</td><td   width="25%"  align="center" valign="middle"  ><a class="text" href="my_fleet.php?mv_action=show&_r=9&pk=30005"    >47th & Baltimore - Prius Liftback</a></td> 
<td >6:00 pm Friday, September 3, 2010</td><td >7:30 pm Friday, September 3, 2010</td><td ><a href="#" class="tooltip_target" style="cursor: help;">$12.37</a> 
                <span class="tooltip" style="position: absolute; z-index: 1000; display: none;">$6.68&nbsp;(Time)&nbsp;+<br/>$2.75&nbsp;(Distance&nbsp;@&nbsp;11&nbsp;mile(s))&nbsp;+<br/>$0.00&nbsp;(Fees)&nbsp;+<br/>$2.94&nbsp;(Tax)</span></td><td >Normal</td><td >rasheed</td></tr><tr class="zebra"><td >2463133</td><td   width="25%"  align="center" valign="middle"  ><a class="text" href="my_fleet.php?mv_action=show&_r=9&pk=30005"    >47th & Baltimore - Prius Liftback</a></td> 
<td >8:00 am Saturday, September 4, 2010</td><td >10:30 am Saturday, September 4, 2010</td><td ><a href="#" class="tooltip_target" style="cursor: help;">$24.69</a> 
                <span class="tooltip" style="position: absolute; z-index: 1000; display: none;">$16.13&nbsp;(Time)&nbsp;+<br/>$4.50&nbsp;(Distance&nbsp;@&nbsp;18&nbsp;mile(s))&nbsp;+<br/>$0.00&nbsp;(Fees)&nbsp;+<br/>$4.06&nbsp;(Tax)</span></td><td >Normal</td><td >rasheed</td></tr><tr ><td >2463195</td><td   width="25%"  align="center" valign="middle"  ><a class="text" href="my_fleet.php?mv_action=show&_r=9&pk=30005"    >47th & Baltimore - Prius Liftback</a></td> 
<td >1:00 pm Saturday, September 4, 2010</td><td >3:00 pm Saturday, September 4, 2010</td><td ><a href="#" class="tooltip_target" style="cursor: help;">$20.04</a> 
                <span class="tooltip" style="position: absolute; z-index: 1000; display: none;">$12.90&nbsp;(Time)&nbsp;+<br/>$3.50&nbsp;(Distance&nbsp;@&nbsp;14&nbsp;mile(s))&nbsp;+<br/>$0.00&nbsp;(Fees)&nbsp;+<br/>$3.64&nbsp;(Tax)</span></td><td >Normal</td><td >yugi vet</td></tr><tr class="zebra"><td >2464805</td><td   width="25%"  align="center" valign="middle"  ><a class="text" href="my_fleet.php?mv_action=show&_r=9&pk=12174191"    >49th & Pine - Prius Liftback</a></td> 
<td >3:15 pm Monday, September 6, 2010</td><td >6:00 pm Monday, September 6, 2010</td><td ><a href="#" class="tooltip_target" style="cursor: help;">$26.74</a> 
                <span class="tooltip" style="position: absolute; z-index: 1000; display: none;">$17.74&nbsp;(Time)&nbsp;+<br/>$4.75&nbsp;(Distance&nbsp;@&nbsp;19&nbsp;mile(s))&nbsp;+<br/>$0.00&nbsp;(Fees)&nbsp;+<br/>$4.25&nbsp;(Tax)</span></td><td >Normal</td><td >shopping</td></tr><tr ><td >2468756</td><td   width="25%"  align="center" valign="middle"  ><a class="text" href="my_fleet.php?mv_action=show&_r=9&pk=12174191"    >49th & Pine - Prius Liftback</a></td> 
<td >3:45 pm Friday, September 10, 2010</td><td >5:00 pm Friday, September 10, 2010</td><td ><a href="#" class="tooltip_target" style="cursor: help;">$10.59</a> 
                <span class="tooltip" style="position: absolute; z-index: 1000; display: none;">$5.56&nbsp;(Time)&nbsp;+<br/>$2.25&nbsp;(Distance&nbsp;@&nbsp;9&nbsp;mile(s))&nbsp;+<br/>$0.00&nbsp;(Fees)&nbsp;+<br/>$2.78&nbsp;(Tax)</span></td><td >Normal</td><td >home depot & abyssinia</td></tr><tr class="zebra"><td >2470007</td><td   width="25%"  align="center" valign="middle"  ><a class="text" href="my_fleet.php?mv_action=show&_r=9&pk=30005"    >47th & Baltimore - Prius Liftback</a></td> 
<td >7:45 am Sunday, September 12, 2010</td><td >8:30 am Sunday, September 12, 2010</td><td ><a href="#" class="tooltip_target" style="cursor: help;">$8.71</a> 
                <span class="tooltip" style="position: absolute; z-index: 1000; display: none;">$4.84&nbsp;(Time)&nbsp;+<br/>$1.25&nbsp;(Distance&nbsp;@&nbsp;5&nbsp;mile(s))&nbsp;+<br/>$0.00&nbsp;(Fees)&nbsp;+<br/>$2.62&nbsp;(Tax)</span></td><td >Normal</td><td >&nbsp;</td></tr><tr ><td >2472500</td><td   width="25%"  align="center" valign="middle"  ><a class="text" href="my_fleet.php?mv_action=show&_r=9&pk=30005"    >47th & Baltimore - Prius Liftback</a></td> 
<td >12:45 am Wednesday, September 15, 2010</td><td >1:00 am Wednesday, September 15, 2010</td><td ><a href="#" class="tooltip_target" style="cursor: help;">$3.24</a> 
                <span class="tooltip" style="position: absolute; z-index: 1000; display: none;">$0.63&nbsp;(Time)&nbsp;+<br/>$0.50&nbsp;(Distance&nbsp;@&nbsp;2&nbsp;mile(s))&nbsp;+<br/>$0.00&nbsp;(Fees)&nbsp;+<br/>$2.11&nbsp;(Tax)</span></td><td >Normal</td><td >TESTING CURRENT</td></tr><tr class="zebra"><td >2473048</td><td   width="25%"  align="center" valign="middle"  ><a class="text" href="my_fleet.php?mv_action=show&_r=9&pk=12174191"    >49th & Pine - Prius Liftback</a></td> 
<td >4:00 pm Wednesday, September 15, 2010</td><td >5:15 pm Wednesday, September 15, 2010</td><td ><a href="#" class="tooltip_target" style="cursor: help;">$10.59</a> 
                <span class="tooltip" style="position: absolute; z-index: 1000; display: none;">$5.56&nbsp;(Time)&nbsp;+<br/>$2.25&nbsp;(Distance&nbsp;@&nbsp;9&nbsp;mile(s))&nbsp;+<br/>$0.00&nbsp;(Fees)&nbsp;+<br/>$2.78&nbsp;(Tax)</span></td><td >Normal</td><td >&nbsp;</td></tr><tr ><td >2474252</td><td   width="25%"  align="center" valign="middle"  ><a class="text" href="my_fleet.php?mv_action=show&_r=9&pk=30005"    >47th & Baltimore - Prius Liftback</a></td> 
<td >7:45 am Friday, September 17, 2010</td><td >9:45 am Friday, September 17, 2010</td><td ><a href="#" class="tooltip_target" style="cursor: help;">$15.64</a> 
                <span class="tooltip" style="position: absolute; z-index: 1000; display: none;">$8.90&nbsp;(Time)&nbsp;+<br/>$3.50&nbsp;(Distance&nbsp;@&nbsp;14&nbsp;mile(s))&nbsp;+<br/>$0.00&nbsp;(Fees)&nbsp;+<br/>$3.24&nbsp;(Tax)</span></td><td >Normal</td><td >awc</td></tr></tbody></table></td></tr><table width="100%" id="dlist_pagination"><tr ><td width="20%">&nbsp;</td><td align="center"><span style="padding: 5px"><font class="text">1</font></span><span style="padding: 5px"><a class="text" href="my_reservations.php?main[multi_filter][history][yearmonth]=201009&mv_action=main&_r=9&main[multi_filter][driver_pk]=6285517&main[dlist][sort_col]=res_end&main[dlist][sort_dir]=asc&main[dlist][page_num]=2"    >2</a></span></td><td  width="20%"  align="right" valign="middle"  ><input type="hidden" name="main[multi_filter][history][yearmonth]" value="201009"/> 
<input type="hidden" name="mv_action" value="main"/> 
<input type="hidden" name="_r" value="9"/> 
<input type="hidden" name="main[multi_filter][driver_pk]" value="6285517"/> 
<input type="hidden" name="main[dlist][sort_col]" value="res_end"/> 
<input type="hidden" name="main[dlist][sort_dir]" value="asc"/> 
<input type="hidden" name="main[dlist][page_num]" value="2"/> 
<button  id="next" type="submit" class="button_next" >Next</button> 
</td> 
</tr></table></form></form><form action="my_reservations.php" method="post"><table class="full_width"><tr ><td ><td    align="right" valign="middle"  ><input type="hidden" name="main[multi_filter][history][yearmonth]" value="201009"/> 
<input type="hidden" name="mv_action" value="export_reservations"/> 
<input type="hidden" name="_r" value="9"/> 
<input type="hidden" name="main[multi_filter][driver_pk]" value="6285517"/> 
<button  id="export_reservations" type="submit" class="button button_export" ></button> 
</td> 
</td></tr></table></form></div><br style="clear: both" /><div id="mv_powered"><div id="mv_powered_left"><a href="http://www.metavera.com"><img src="/skin/base_images/mv_logo_small.gif" alt="Powered by Metavera"/></a></div><div id="mv_powered_right"><a href="http://www.metavera.com"><span>Powered by Metavera</span><br/>CarSharing Technology Leader</a></div></div></div><script language="javascript" type="text/javascript" src="/js/browser.js_3_47_0_5"></script> 
</body></html>'''

ONE_CURRENT_ONE_UPCOMING_RESERVATIONS = r'''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"><html xmlns="http://www.w3.org/1999/xhtml"><head>
<meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1" />
<meta http-equiv="pragma" content="no-cache" />
<meta http-equiv="cache-control" content="no-cache" />
<title >Reservation Manager</title><link rel="stylesheet" type="text/css" href="/skin/pcs_ui.css_3_44_0_3" title="pcs_skin" media="screen, print" /><link rel="stylesheet" type="text/css" href="/skin/pcs_layout.css_3_44_0_3" title="pcs_skin" media="screen, print" /><link rel="stylesheet" type="text/css" href="/skin/pcs_buttons.css_3_44_0_3" title="pcs_skin" media="screen, print" /><link rel="stylesheet" type="text/css" href="/skin/pcs_skin.css_3_44_0_3" title="pcs_skin" media="screen, print" /></head>
<body bgcolor="white"  ><script language="javascript" type="text/javascript" src="/js/helper.js_3_44_0_3"></script>
<script language="javascript" type="text/javascript" src="/js/prototype.js_3_44_0_3"></script>
<script language="javascript" type="text/javascript" src="/js/lowpro.js_3_44_0_3"></script>
<script language="javascript" type="text/javascript" src="/js/slider.js_3_44_0_3"></script>
<script language="javascript" type="text/javascript" src="/js/lightbox.js_3_44_0_3"></script>
<script language="javascript" type="text/javascript" src="/js/mf_lightbox.js_3_44_0_3"></script>
<script language="javascript" type="text/javascript" src="/js/mv_base.js_3_44_0_3"></script>
<script language="javascript" type="text/javascript" src="/js/mv_reserve.js_3_44_0_3"></script>
<div class="mv_header">
<img border="0" src="/images/client_images/pcs_web_logo.gif" alt="PhillyCarShare" title="PhillyCarShare" />
</div>
<div id="wrapper"><div id="page_header"><div id="lame_image"><span class="switch">
<a class="text" href="/members/help.html?_r=35"  target="_blank"  >Help</a></span>
<p >Mjumbe Poe, you are signed in. (Residential Account)</p><a href="my_reservations.php?_r=35&mv_action=logout">
                            <img class="logbutton" alt = "Log Out" src="/skin/base_images/btn_logout.gif" />
                   </a></div><img id="logo" src="/images/client_images/pcs_web_logo.gif" alt="PhillyCarShare" title="PhillyCarShare" />
        <div id="nav_bar">
        <div id="navcontainer">
        <ul id="navlist"><li ><a class="text link_new_reservation" href="my_reservations.php?_r=35"    >New Reservation</a></li><li ><a class="link_my_reservations" href="my_reservations.php?mv_action=main&_r=35"    >My Reservations</a></li><li ><a class="text link_my_messages" href="my_messages.php?_r=35"    >My Messages</a></li><li ><a class="text link_my_info" href="my_info.php?_r=35"    >My Account</a></li><li ><a class="text link_my_problems" href="my_problems.php?_r=35"    >Member Feedback</a></li></ul></div></div></div><div class="midbox"><h3 >My Reservations</h3><h5 >Past and Current Reservations</h5><div class="multi_filter"><form id="main_multi_filter_" name="multi_filter" action="my_reservations.php" method="get"  ><label for="main_multi_filter__history_" id="main_multi_filter__history__label"><b>Reservation&nbsp;Selection</b>:&nbsp;</label><select name="main[multi_filter][history][yearmonth]"    id="main_multi_filter__history__yearmonth_" tabindex="0"  >
  <option value="-1" selected>Current Reservations</option>
  <option value="201009">September&nbsp;2010</option>
  <option value="201008">August&nbsp;2010</option>
  <option value="201007">July&nbsp;2010</option>
  <option value="201006">June&nbsp;2010</option>
  <option value="201005">May&nbsp;2010</option>
  <option value="201004">April&nbsp;2010</option>
  <option value="201003">March&nbsp;2010</option>
 </select><span class="instruction">&nbsp;</span><span ><td    align="center" valign="middle"  ><input type="hidden" name="mv_action" value="main"/>
<input type="hidden" name="_r" value="35"/>
<button  id="main" type="submit" class="button_update" ></button>
</td>
</span><input id="main_multi_filter__driver_pk_" type="hidden" name="main[multi_filter][driver_pk]" value="6285517" /></form></div><form name="main" method="post"><form id="main_dlist_" name="dlist" action="my_reservations.php" method="post"  ><tr ><td ><table class="dlist ma" id="main_dlist_"><thead ><tr ><td     align="center" valign="middle"  ><a class="text" href="my_reservations.php?mv_action=main&_r=35&main[dlist][sort_col]=res_id&main[dlist][sort_dir]=asc"    >ID</a></td>
<td     align="center" valign="middle"  ><a class="text" href="my_reservations.php?mv_action=main&_r=35&main[dlist][sort_col]=ustack_descr&main[dlist][sort_dir]=asc"    >Stack</a></td>
<td     align="center" valign="middle"  ><a class="text" href="my_reservations.php?mv_action=main&_r=35&main[dlist][sort_col]=res_start&main[dlist][sort_dir]=asc"    >Start</a></td>
<td     align="center" valign="middle"  ><a class="text" href="my_reservations.php?mv_action=main&_r=35&main[dlist][sort_col]=res_end&main[dlist][sort_dir]=desc"    >End</a></td>
<th  width="1%"  align="center" valign="middle"  ><font class="textbb">Est&nbsp;Cost</font></th>
<td     align="center" valign="middle"  ><a class="text" href="my_reservations.php?mv_action=main&_r=35&main[dlist][sort_col]=reservation_status&main[dlist][sort_dir]=asc"    >Status</a></td>
<td     align="center" valign="middle"  ><a class="text" href="my_reservations.php?mv_action=main&_r=35&main[dlist][sort_col]=res_extra&main[dlist][sort_dir]=asc"    >Memo</a></td>
<td align="center"><font class="textbb">&nbsp;</font></td>
</tr></thead><tbody ><tr class="zebra"><td >2472500</td><td   width="25%"  align="center" valign="middle"  ><a class="text" href="my_fleet.php?mv_action=show&_r=35&pk=30005"    >47th & Baltimore - Prius Liftback</a></td>
<td >12:45 am Wednesday, September 15, 2010</td><td >1:00 am Wednesday, September 15, 2010</td><td ><a href="#" class="tooltip_target" style="cursor: help;">$3.24</a>
                <span class="tooltip" style="position: absolute; z-index: 1000; display: none;">$0.63&nbsp;(Time)&nbsp;+<br/>$0.50&nbsp;(Distance&nbsp;@&nbsp;2&nbsp;mile(s))&nbsp;+<br/>$0.00&nbsp;(Fees)&nbsp;+<br/>$2.11&nbsp;(Tax)</span></td><td >Normal</td><td >TESTING CURRENT</td><td width="176"><button  id="early" type="button" class="button button_early" onclick="; window.location='my_reservations.php?mv_action=early&_r=35&pk=146299030'">Return Early</button>
<button  id="extend" type="button" class="button button_extend" onclick="; window.location='my_reservations.php?mv_action=extend&_r=35&pk=146299030'">Extend</button>
</td></tr><tr ><td >2472498</td><td   width="25%"  align="center" valign="middle"  ><a class="text" href="my_fleet.php?mv_action=show&_r=35&pk=30005"    >47th & Baltimore - Prius Liftback</a></td>
<td >6:00 am Wednesday, September 15, 2010</td><td >6:15 am Wednesday, September 15, 2010</td><td ><a href="#" class="tooltip_target" style="cursor: help;">$3.24</a>
                <span class="tooltip" style="position: absolute; z-index: 1000; display: none;">$0.63&nbsp;(Time)&nbsp;+<br/>$0.50&nbsp;(Distance&nbsp;@&nbsp;2&nbsp;mile(s))&nbsp;+<br/>$0.00&nbsp;(Fees)&nbsp;+<br/>$2.11&nbsp;(Tax)</span></td><td >Normal</td><td >&nbsp;</td><td width="176"><button  id="edit" type="button" class="button button_edit" onclick="; window.location='my_reservations.php?mv_action=edit&_r=35&pk=146299013'">Change</button>
<button  id="do_cancel" type="button" class="button button_do_cancel" onclick="; window.location='my_reservations.php?mv_action=do_cancel&_r=35&pk=146299013'">Cancel</button>
</td></tr></tbody></table></td></tr></form></form><form action="my_reservations.php" method="post"><table class="full_width"><tr ><td ><td    align="right" valign="middle"  ><input type="hidden" name="mv_action" value="export_reservations"/>
<input type="hidden" name="_r" value="35"/>
<button  id="export_reservations" type="submit" class="button button_export" ></button>
</td>
</td></tr></table></form></div><br style="clear: both" /><div id="mv_powered"><div id="mv_powered_left"><a href="http://www.metavera.com"><img src="/skin/base_images/mv_logo_small.gif" alt="Powered by Metavera"/></a></div><div id="mv_powered_right"><a href="http://www.metavera.com"><span>Powered by Metavera</span><br/>CarSharing Technology Leader</a></div></div></div><script language="javascript" type="text/javascript" src="/js/browser.js_3_44_0_3"></script>
</body></html>'''

ONE_UPCOMING_RESERVATION = r'''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"><html xmlns="http://www.w3.org/1999/xhtml"><head>
<meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1" />
<meta http-equiv="pragma" content="no-cache" />
<meta http-equiv="cache-control" content="no-cache" />
<title >Reservation Manager</title><link rel="stylesheet" type="text/css" href="/skin/pcs_ui.css_3_44_0_3" title="pcs_skin" media="screen, print" /><link rel="stylesheet" type="text/css" href="/skin/pcs_layout.css_3_44_0_3" title="pcs_skin" media="screen, print" /><link rel="stylesheet" type="text/css" href="/skin/pcs_buttons.css_3_44_0_3" title="pcs_skin" media="screen, print" /><link rel="stylesheet" type="text/css" href="/skin/pcs_skin.css_3_44_0_3" title="pcs_skin" media="screen, print" /></head>
<body bgcolor="white"  ><script language="javascript" type="text/javascript" src="/js/helper.js_3_44_0_3"></script>
<script language="javascript" type="text/javascript" src="/js/prototype.js_3_44_0_3"></script>
<script language="javascript" type="text/javascript" src="/js/lowpro.js_3_44_0_3"></script>
<script language="javascript" type="text/javascript" src="/js/slider.js_3_44_0_3"></script>
<script language="javascript" type="text/javascript" src="/js/lightbox.js_3_44_0_3"></script>
<script language="javascript" type="text/javascript" src="/js/mf_lightbox.js_3_44_0_3"></script>
<script language="javascript" type="text/javascript" src="/js/mv_base.js_3_44_0_3"></script>
<script language="javascript" type="text/javascript" src="/js/mv_reserve.js_3_44_0_3"></script>
<div class="mv_header">
<img border="0" src="/images/client_images/pcs_web_logo.gif" alt="PhillyCarShare" title="PhillyCarShare" />
</div>
<div id="wrapper"><div id="page_header"><div id="lame_image"><span class="switch">
<a class="text" href="/members/help.html?_r=26"  target="_blank"  >Help</a></span>
<p >Mjumbe Poe, you are signed in. (Residential Account)</p><a href="my_reservations.php?_r=26&mv_action=logout">
                            <img class="logbutton" alt = "Log Out" src="/skin/base_images/btn_logout.gif" />
                   </a></div><img id="logo" src="/images/client_images/pcs_web_logo.gif" alt="PhillyCarShare" title="PhillyCarShare" />
        <div id="nav_bar">
        <div id="navcontainer">
        <ul id="navlist"><li ><a class="text link_new_reservation" href="my_reservations.php?_r=26"    >New Reservation</a></li><li ><a class="link_my_reservations" href="my_reservations.php?mv_action=main&_r=26"    >My Reservations</a></li><li ><a class="text link_my_messages" href="my_messages.php?_r=26"    >My Messages</a></li><li ><a class="text link_my_info" href="my_info.php?_r=26"    >My Account</a></li><li ><a class="text link_my_problems" href="my_problems.php?_r=26"    >Member Feedback</a></li></ul></div></div></div><div class="midbox"><h3 >My Reservations</h3><h5 >Past and Current Reservations</h5><div class="multi_filter"><form id="main_multi_filter_" name="multi_filter" action="my_reservations.php" method="get"  ><label for="main_multi_filter__history_" id="main_multi_filter__history__label"><b>Reservation&nbsp;Selection</b>:&nbsp;</label><select name="main[multi_filter][history][yearmonth]"    id="main_multi_filter__history__yearmonth_" tabindex="0"  >
  <option value="-1" selected>Current Reservations</option>
  <option value="201009">September&nbsp;2010</option>
  <option value="201008">August&nbsp;2010</option>
  <option value="201007">July&nbsp;2010</option>
  <option value="201006">June&nbsp;2010</option>
  <option value="201005">May&nbsp;2010</option>
  <option value="201004">April&nbsp;2010</option>
  <option value="201003">March&nbsp;2010</option>
 </select><span class="instruction">&nbsp;</span><span ><td    align="center" valign="middle"  ><input type="hidden" name="mv_action" value="main"/>
<input type="hidden" name="_r" value="26"/>
<button  id="main" type="submit" class="button_update" ></button>
</td>
</span><input id="main_multi_filter__driver_pk_" type="hidden" name="main[multi_filter][driver_pk]" value="6285517" /></form></div><form name="main" method="post"><form id="main_dlist_" name="dlist" action="my_reservations.php" method="post"  ><tr ><td ><table class="dlist ma" id="main_dlist_"><thead ><tr ><td     align="center" valign="middle"  ><a class="text" href="my_reservations.php?mv_action=main&_r=26&main[dlist][sort_col]=res_id&main[dlist][sort_dir]=asc"    >ID</a></td>
<td     align="center" valign="middle"  ><a class="text" href="my_reservations.php?mv_action=main&_r=26&main[dlist][sort_col]=ustack_descr&main[dlist][sort_dir]=asc"    >Stack</a></td>
<td     align="center" valign="middle"  ><a class="text" href="my_reservations.php?mv_action=main&_r=26&main[dlist][sort_col]=res_start&main[dlist][sort_dir]=asc"    >Start</a></td>
<td     align="center" valign="middle"  ><a class="text" href="my_reservations.php?mv_action=main&_r=26&main[dlist][sort_col]=res_end&main[dlist][sort_dir]=desc"    >End</a></td>
<th  width="1%"  align="center" valign="middle"  ><font class="textbb">Est&nbsp;Cost</font></th>
<td     align="center" valign="middle"  ><a class="text" href="my_reservations.php?mv_action=main&_r=26&main[dlist][sort_col]=reservation_status&main[dlist][sort_dir]=asc"    >Status</a></td>
<td align="center"><font class="textbb">&nbsp;</font></td>
</tr></thead><tbody ><tr class="zebra"><td >2472498</td><td   width="25%"  align="center" valign="middle"  ><a class="text" href="my_fleet.php?mv_action=show&_r=26&pk=30005"    >47th & Baltimore - Prius Liftback</a></td>
<td >6:00 am Wednesday, September 15, 2010</td><td >6:15 am Wednesday, September 15, 2010</td><td ><a href="#" class="tooltip_target" style="cursor: help;">$3.24</a>
                <span class="tooltip" style="position: absolute; z-index: 1000; display: none;">$0.63&nbsp;(Time)&nbsp;+<br/>$0.50&nbsp;(Distance&nbsp;@&nbsp;2&nbsp;mile(s))&nbsp;+<br/>$0.00&nbsp;(Fees)&nbsp;+<br/>$2.11&nbsp;(Tax)</span></td><td >Normal</td><td width="176"><button  id="edit" type="button" class="button button_edit" onclick="; window.location='my_reservations.php?mv_action=edit&_r=26&pk=146299013'">Change</button>
<button  id="do_cancel" type="button" class="button button_do_cancel" onclick="; window.location='my_reservations.php?mv_action=do_cancel&_r=26&pk=146299013'">Cancel</button>
</td></tr></tbody></table></td></tr></form></form><form action="my_reservations.php" method="post"><table class="full_width"><tr ><td ><td    align="right" valign="middle"  ><input type="hidden" name="mv_action" value="export_reservations"/>
<input type="hidden" name="_r" value="26"/>
<button  id="export_reservations" type="submit" class="button button_export" ></button>
</td>
</td></tr></table></form></div><br style="clear: both" /><div id="mv_powered"><div id="mv_powered_left"><a href="http://www.metavera.com"><img src="/skin/base_images/mv_logo_small.gif" alt="Powered by Metavera"/></a></div><div id="mv_powered_right"><a href="http://www.metavera.com"><span>Powered by Metavera</span><br/>CarSharing Technology Leader</a></div></div></div><script language="javascript" type="text/javascript" src="/js/browser.js_3_44_0_3"></script>
</body></html>'''

NO_UPCOMING_RESERVATIONS_BODY = r'''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"><html xmlns="http://www.w3.org/1999/xhtml"><head>
<meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1" />
<meta http-equiv="pragma" content="no-cache" />
<meta http-equiv="cache-control" content="no-cache" />
<title >Reservation Manager</title><link rel="stylesheet" type="text/css" href="/skin/pcs_ui.css_3_44_0_3" title="pcs_skin" media="screen, print" /><link rel="stylesheet" type="text/css" href="/skin/pcs_layout.css_3_44_0_3" title="pcs_skin" media="screen, print" /><link rel="stylesheet" type="text/css" href="/skin/pcs_buttons.css_3_44_0_3" title="pcs_skin" media="screen, print" /><link rel="stylesheet" type="text/css" href="/skin/pcs_skin.css_3_44_0_3" title="pcs_skin" media="screen, print" /></head>
<body bgcolor="white"  ><script language="javascript" type="text/javascript" src="/js/helper.js_3_44_0_3"></script>
<script language="javascript" type="text/javascript" src="/js/prototype.js_3_44_0_3"></script>
<script language="javascript" type="text/javascript" src="/js/lowpro.js_3_44_0_3"></script>
<script language="javascript" type="text/javascript" src="/js/slider.js_3_44_0_3"></script>
<script language="javascript" type="text/javascript" src="/js/lightbox.js_3_44_0_3"></script>
<script language="javascript" type="text/javascript" src="/js/mf_lightbox.js_3_44_0_3"></script>
<script language="javascript" type="text/javascript" src="/js/mv_base.js_3_44_0_3"></script>
<script language="javascript" type="text/javascript" src="/js/mv_reserve.js_3_44_0_3"></script>
<div class="mv_header">
<img border="0" src="/images/client_images/pcs_web_logo.gif" alt="PhillyCarShare" title="PhillyCarShare" />
</div>
<div id="wrapper"><div id="page_header"><div id="lame_image"><span class="switch">
<a class="text" href="/members/help.html?_r=12"  target="_blank"  >Help</a></span>
<p >Mjumbe Poe, you are signed in. (Residential Account)</p><a href="my_reservations.php?_r=12&mv_action=logout">
                            <img class="logbutton" alt = "Log Out" src="/skin/base_images/btn_logout.gif" />
                   </a></div><img id="logo" src="/images/client_images/pcs_web_logo.gif" alt="PhillyCarShare" title="PhillyCarShare" />
        <div id="nav_bar">
        <div id="navcontainer">
        <ul id="navlist"><li ><a class="text link_new_reservation" href="my_reservations.php?_r=12"    >New Reservation</a></li><li ><a class="link_my_reservations" href="my_reservations.php?mv_action=main&_r=12"    >My Reservations</a></li><li ><a class="text link_my_messages" href="my_messages.php?_r=12"    >My Messages</a></li><li ><a class="text link_my_info" href="my_info.php?_r=12"    >My Account</a></li><li ><a class="text link_my_problems" href="my_problems.php?_r=12"    >Member Feedback</a></li></ul></div></div></div><div class="midbox"><h3 >My Reservations</h3><h5 >Past and Current Reservations</h5><div class="multi_filter"><form id="main_multi_filter_" name="multi_filter" action="my_reservations.php" method="get"  ><label for="main_multi_filter__history_" id="main_multi_filter__history__label"><b>Reservation&nbsp;Selection</b>:&nbsp;</label><select name="main[multi_filter][history][yearmonth]"    id="main_multi_filter__history__yearmonth_" tabindex="0"  >
  <option value="-1" selected>Current Reservations</option>
  <option value="201009">September&nbsp;2010</option>
  <option value="201008">August&nbsp;2010</option>
  <option value="201007">July&nbsp;2010</option>
  <option value="201006">June&nbsp;2010</option>
  <option value="201005">May&nbsp;2010</option>
  <option value="201004">April&nbsp;2010</option>
  <option value="201003">March&nbsp;2010</option>
 </select><span class="instruction">&nbsp;</span><span ><td    align="center" valign="middle"  ><input type="hidden" name="mv_action" value="main"/>
<input type="hidden" name="_r" value="12"/>
<button  id="main" type="submit" class="button_update" ></button>
</td>
</span><input id="main_multi_filter__driver_pk_" type="hidden" name="main[multi_filter][driver_pk]" value="6285517" /></form></div><form name="main" method="post"><form id="main_dlist_" name="dlist" action="my_reservations.php" method="post"  ><div class="dlist_empty"><span class="dlist_empty">The query did not return any results.</span></div></form></form></div><br style="clear: both" /><div id="mv_powered"><div id="mv_powered_left"><a href="http://www.metavera.com"><img src="/skin/base_images/mv_logo_small.gif" alt="Powered by Metavera"/></a></div><div id="mv_powered_right"><a href="http://www.metavera.com"><span>Powered by Metavera</span><br/>CarSharing Technology Leader</a></div></div></div><script language="javascript" type="text/javascript" src="/js/browser.js_3_44_0_3"></script>
</body></html>'''

