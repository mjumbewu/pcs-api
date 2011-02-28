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

PAST_RESERVATIONS_SECOND_OF_TWO_PAGES = r'''
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
<a class="text" href="/members/help.html?_r=17"  target="_blank"  >Help</a></span> 
<p >Mjumbe Poe, you are signed in. (Residential Account)</p><a href="my_reservations.php?_r=17&mv_action=logout"> 
                            <img class="logbutton" alt = "Log Out" src="/skin/base_images/btn_logout.gif" /> 
                   </a></div><img id="logo" src="/images/client_images/pcs_web_logo.gif" alt="PhillyCarShare" title="PhillyCarShare" /> 
        <div id="nav_bar"> 
        <div id="navcontainer"> 
        <ul id="navlist"><li ><a class="text link_new_reservation" href="my_reservations.php?_r=17"    >New Reservation</a></li><li ><a class="link_my_reservations" href="my_reservations.php?mv_action=main&_r=17"    >My Reservations</a></li><li ><a class="text link_my_messages" href="my_messages.php?_r=17"    >My Messages</a></li><li ><a class="text link_my_info" href="my_info.php?_r=17"    >My Account</a></li><li ><a class="text link_my_problems" href="my_problems.php?_r=17"    >Member Feedback</a></li></ul></div></div></div><div class="midbox"><h3 >My Reservations</h3><h5 >Past and Current Reservations</h5><div class="multi_filter"><form id="main_multi_filter_" name="multi_filter" action="my_reservations.php" method="get"  ><label for="main_multi_filter__history_" id="main_multi_filter__history__label"><b>Reservation&nbsp;Selection</b>:&nbsp;</label><select name="main[multi_filter][history][yearmonth]"    id="main_multi_filter__history__yearmonth_" tabindex="0"  > 
  <option value="-1">Current Reservations</option> 
  <option value="201010">October&nbsp;2010</option> 
  <option value="201009" selected>September&nbsp;2010</option> 
  <option value="201008">August&nbsp;2010</option> 
  <option value="201007">July&nbsp;2010</option> 
  <option value="201006">June&nbsp;2010</option> 
  <option value="201005">May&nbsp;2010</option> 
  <option value="201004">April&nbsp;2010</option> 
 </select><span class="instruction">&nbsp;</span><span ><td    align="center" valign="middle"  ><input type="hidden" name="mv_action" value="main"/> 
<input type="hidden" name="_r" value="17"/> 
<button  id="main" type="submit" class="button_update" ></button> 
</td> 
</span><input id="main_multi_filter__driver_pk_" type="hidden" name="main[multi_filter][driver_pk]" value="6285517" /></form></div><form name="main" method="post"><input id="main_dlist_" type="hidden" name="main[dlist]" value="" /><form id="main_dlist_" name="dlist" action="my_reservations.php" method="post"  ><tr ><td ><table class="dlist ma" id="main_dlist_"><thead ><tr ><td     align="center" valign="middle"  ><a class="text" href="my_reservations.php?main[multi_filter][history][yearmonth]=201009&mv_action=main&_r=17&main[multi_filter][driver_pk]=6285517&main[dlist][sort_col]=res_id&main[dlist][sort_dir]=asc"    >ID</a></td> 
<td     align="center" valign="middle"  ><a class="text" href="my_reservations.php?main[multi_filter][history][yearmonth]=201009&mv_action=main&_r=17&main[multi_filter][driver_pk]=6285517&main[dlist][sort_col]=ustack_descr&main[dlist][sort_dir]=asc"    >Stack</a></td> 
<td     align="center" valign="middle"  ><a class="text" href="my_reservations.php?main[multi_filter][history][yearmonth]=201009&mv_action=main&_r=17&main[multi_filter][driver_pk]=6285517&main[dlist][sort_col]=res_start&main[dlist][sort_dir]=asc"    >Start</a></td> 
<td     align="center" valign="middle"  ><a class="text" href="my_reservations.php?main[multi_filter][history][yearmonth]=201009&mv_action=main&_r=17&main[multi_filter][driver_pk]=6285517&main[dlist][sort_col]=res_end&main[dlist][sort_dir]=desc"    >End</a></td> 
<th  width="1%"  align="center" valign="middle"  ><font class="textbb">Est&nbsp;Cost</font></th> 
<td     align="center" valign="middle"  ><a class="text" href="my_reservations.php?main[multi_filter][history][yearmonth]=201009&mv_action=main&_r=17&main[multi_filter][driver_pk]=6285517&main[dlist][sort_col]=reservation_status&main[dlist][sort_dir]=asc"    >Status</a></td> 
<td     align="center" valign="middle"  ><a class="text" href="my_reservations.php?main[multi_filter][history][yearmonth]=201009&mv_action=main&_r=17&main[multi_filter][driver_pk]=6285517&main[dlist][sort_col]=res_extra&main[dlist][sort_dir]=asc"    >Memo</a></td> 
</tr></thead><tbody ><tr class="zebra"><td >2476904</td><td   width="25%"  align="center" valign="middle"  ><a class="text" href="my_fleet.php?mv_action=show&_r=17&pk=30005"    >47th & Baltimore - Prius Liftback</a></td> 
<td >9:30 pm Sunday, September 19, 2010</td><td >10:30 pm Sunday, September 19, 2010</td><td ><a href="#" class="tooltip_target" style="cursor: help;">$11.03</a> 
                <span class="tooltip" style="position: absolute; z-index: 1000; display: none;">$6.45&nbsp;(Time)&nbsp;+<br/>$1.75&nbsp;(Distance&nbsp;@&nbsp;7&nbsp;mile(s))&nbsp;+<br/>$0.00&nbsp;(Fees)&nbsp;+<br/>$2.83&nbsp;(Tax)</span></td><td >Normal</td><td >five guys</td></tr><tr ><td >2482804</td><td   width="25%"  align="center" valign="middle"  ><a class="text" href="my_fleet.php?mv_action=show&_r=17&pk=30005"    >47th & Baltimore - Prius Liftback</a></td> 
<td >10:55 pm Saturday, September 25, 2010</td><td >11:00 pm Saturday, September 25, 2010</td><td ><a href="#" class="tooltip_target" style="cursor: help;">$4.32</a> 
                <span class="tooltip" style="position: absolute; z-index: 1000; display: none;">$1.61&nbsp;(Time)&nbsp;+<br/>$0.50&nbsp;(Distance&nbsp;@&nbsp;2&nbsp;mile(s))&nbsp;+<br/>$0.00&nbsp;(Fees)&nbsp;+<br/>$2.21&nbsp;(Tax)</span></td><td >Normal</td><td >new reservation</td></tr><tr class="zebra"><td >2482842</td><td   width="25%"  align="center" valign="middle"  ><a class="text" href="my_fleet.php?mv_action=show&_r=17&pk=12174212"    >46th & Baltimore - Honda Element</a></td> 
<td >6:00 am Sunday, September 26, 2010</td><td >6:15 am Sunday, September 26, 2010</td><td ><a href="#" class="tooltip_target" style="cursor: help;">$3.24</a> 
                <span class="tooltip" style="position: absolute; z-index: 1000; display: none;">$0.63&nbsp;(Time)&nbsp;+<br/>$0.50&nbsp;(Distance&nbsp;@&nbsp;2&nbsp;mile(s))&nbsp;+<br/>$0.00&nbsp;(Fees)&nbsp;+<br/>$2.11&nbsp;(Tax)</span></td><td >Normal</td><td >new reservation</td></tr><tr ><td >2484939</td><td   width="25%"  align="center" valign="middle"  ><a class="text" href="my_fleet.php?mv_action=show&_r=17&pk=30005"    >47th & Baltimore - Prius Liftback</a></td> 
<td >1:15 am Tuesday, September 28, 2010</td><td >2:30 am Tuesday, September 28, 2010</td><td ><a href="#" class="tooltip_target" style="cursor: help;">$7.92</a> 
                <span class="tooltip" style="position: absolute; z-index: 1000; display: none;">$3.13&nbsp;(Time)&nbsp;+<br/>$2.25&nbsp;(Distance&nbsp;@&nbsp;9&nbsp;mile(s))&nbsp;+<br/>$0.00&nbsp;(Fees)&nbsp;+<br/>$2.54&nbsp;(Tax)</span></td><td >Normal</td><td >giant</td></tr><tr class="zebra"><td >2487978</td><td   width="25%"  align="center" valign="middle"  ><a class="text" href="my_fleet.php?mv_action=show&_r=17&pk=30005"    >47th & Baltimore - Prius Liftback</a></td> 
<td >9:15 pm Thursday, September 30, 2010</td><td >9:45 pm Thursday, September 30, 2010</td><td ><a href="#" class="tooltip_target" style="cursor: help;">$5.55</a> 
                <span class="tooltip" style="position: absolute; z-index: 1000; display: none;">$2.23&nbsp;(Time)&nbsp;+<br/>$1.00&nbsp;(Distance&nbsp;@&nbsp;4&nbsp;mile(s))&nbsp;+<br/>$0.00&nbsp;(Fees)&nbsp;+<br/>$2.32&nbsp;(Tax)</span></td><td >Normal</td><td >&nbsp;</td></tr></tbody></table></td></tr><table width="100%" id="dlist_pagination"><tr ><td  width="20%"  align="left" valign="middle"  ><input type="hidden" name="main[multi_filter][history][yearmonth]" value="201009"/> 
<input type="hidden" name="mv_action" value="main"/> 
<input type="hidden" name="_r" value="17"/> 
<input type="hidden" name="main[multi_filter][driver_pk]" value="6285517"/> 
<input type="hidden" name="main[dlist][sort_col]" value="res_end"/> 
<input type="hidden" name="main[dlist][sort_dir]" value="asc"/> 
<input type="hidden" name="main[dlist][page_num]" value="1"/> 
<button  id="previous" type="submit" class="button_previous" >Previous</button> 
</td> 
<td align="center"><span style="padding: 5px"><a class="text" href="my_reservations.php?main[multi_filter][history][yearmonth]=201009&mv_action=main&_r=17&main[multi_filter][driver_pk]=6285517&main[dlist][sort_col]=res_end&main[dlist][sort_dir]=asc&main[dlist][page_num]=1"    >1</a></span><span style="padding: 5px"><font class="text">2</font></span></td><td width="20%">&nbsp;</td></tr></table></form></form><form action="my_reservations.php" method="post"><table class="full_width"><tr ><td ><td    align="right" valign="middle"  ><input type="hidden" name="main[multi_filter][history][yearmonth]" value="201009"/> 
<input type="hidden" name="mv_action" value="export_reservations"/> 
<input type="hidden" name="_r" value="17"/> 
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

PAST_RESERVATIONS_SINGLE_PAGE = r'''
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
<a class="text" href="/members/help.html?_r=19"  target="_blank"  >Help</a></span> 
<p >Mjumbe Poe, you are signed in. (Residential Account)</p><a href="my_reservations.php?_r=19&mv_action=logout"> 
                            <img class="logbutton" alt = "Log Out" src="/skin/base_images/btn_logout.gif" /> 
                   </a></div><img id="logo" src="/images/client_images/pcs_web_logo.gif" alt="PhillyCarShare" title="PhillyCarShare" /> 
        <div id="nav_bar"> 
        <div id="navcontainer"> 
        <ul id="navlist"><li ><a class="text link_new_reservation" href="my_reservations.php?_r=19"    >New Reservation</a></li><li ><a class="link_my_reservations" href="my_reservations.php?mv_action=main&_r=19"    >My Reservations</a></li><li ><a class="text link_my_messages" href="my_messages.php?_r=19"    >My Messages</a></li><li ><a class="text link_my_info" href="my_info.php?_r=19"    >My Account</a></li><li ><a class="text link_my_problems" href="my_problems.php?_r=19"    >Member Feedback</a></li></ul></div></div></div><div class="midbox"><h3 >My Reservations</h3><h5 >Past and Current Reservations</h5><div class="multi_filter"><form id="main_multi_filter_" name="multi_filter" action="my_reservations.php" method="get"  ><label for="main_multi_filter__history_" id="main_multi_filter__history__label"><b>Reservation&nbsp;Selection</b>:&nbsp;</label><select name="main[multi_filter][history][yearmonth]"    id="main_multi_filter__history__yearmonth_" tabindex="0"  > 
  <option value="-1">Current Reservations</option> 
  <option value="201010" selected>October&nbsp;2010</option> 
  <option value="201009">September&nbsp;2010</option> 
  <option value="201008">August&nbsp;2010</option> 
  <option value="201007">July&nbsp;2010</option> 
  <option value="201006">June&nbsp;2010</option> 
  <option value="201005">May&nbsp;2010</option> 
  <option value="201004">April&nbsp;2010</option> 
 </select><span class="instruction">&nbsp;</span><span ><td    align="center" valign="middle"  ><input type="hidden" name="mv_action" value="main"/> 
<input type="hidden" name="_r" value="19"/> 
<button  id="main" type="submit" class="button_update" ></button> 
</td> 
</span><input id="main_multi_filter__driver_pk_" type="hidden" name="main[multi_filter][driver_pk]" value="6285517" /></form></div><form name="main" method="post"><form id="main_dlist_" name="dlist" action="my_reservations.php" method="post"  ><tr ><td ><table class="dlist ma" id="main_dlist_"><thead ><tr ><td     align="center" valign="middle"  ><a class="text" href="my_reservations.php?main[multi_filter][history][yearmonth]=201010&mv_action=main&_r=19&main[multi_filter][driver_pk]=6285517&main[dlist][sort_col]=res_id&main[dlist][sort_dir]=asc"    >ID</a></td> 
<td     align="center" valign="middle"  ><a class="text" href="my_reservations.php?main[multi_filter][history][yearmonth]=201010&mv_action=main&_r=19&main[multi_filter][driver_pk]=6285517&main[dlist][sort_col]=ustack_descr&main[dlist][sort_dir]=asc"    >Stack</a></td> 
<td     align="center" valign="middle"  ><a class="text" href="my_reservations.php?main[multi_filter][history][yearmonth]=201010&mv_action=main&_r=19&main[multi_filter][driver_pk]=6285517&main[dlist][sort_col]=res_start&main[dlist][sort_dir]=asc"    >Start</a></td> 
<td     align="center" valign="middle"  ><a class="text" href="my_reservations.php?main[multi_filter][history][yearmonth]=201010&mv_action=main&_r=19&main[multi_filter][driver_pk]=6285517&main[dlist][sort_col]=res_end&main[dlist][sort_dir]=desc"    >End</a></td> 
<th  width="1%"  align="center" valign="middle"  ><font class="textbb">Est&nbsp;Cost</font></th> 
<td     align="center" valign="middle"  ><a class="text" href="my_reservations.php?main[multi_filter][history][yearmonth]=201010&mv_action=main&_r=19&main[multi_filter][driver_pk]=6285517&main[dlist][sort_col]=reservation_status&main[dlist][sort_dir]=asc"    >Status</a></td> 
<td     align="center" valign="middle"  ><a class="text" href="my_reservations.php?main[multi_filter][history][yearmonth]=201010&mv_action=main&_r=19&main[multi_filter][driver_pk]=6285517&main[dlist][sort_col]=res_extra&main[dlist][sort_dir]=asc"    >Memo</a></td> 
</tr></thead><tbody ><tr class="zebra"><td >2491921</td><td   width="25%"  align="center" valign="middle"  ><a class="text" href="my_fleet.php?mv_action=show&_r=19&pk=30005"    >47th & Baltimore - Prius Liftback</a></td> 
<td >12:00 am Tuesday, October 5, 2010</td><td >1:00 am Tuesday, October 5, 2010</td><td ><a href="#" class="tooltip_target" style="cursor: help;">$6.68</a> 
                <span class="tooltip" style="position: absolute; z-index: 1000; display: none;">$2.50&nbsp;(Time)&nbsp;+<br/>$1.75&nbsp;(Distance&nbsp;@&nbsp;7&nbsp;mile(s))&nbsp;+<br/>$0.00&nbsp;(Fees)&nbsp;+<br/>$2.43&nbsp;(Tax)</span></td><td >Normal</td><td >jennifer</td></tr><tr ><td >2494232</td><td   width="25%"  align="center" valign="middle"  ><a class="text" href="my_fleet.php?mv_action=show&_r=19&pk=30005"    >47th & Baltimore - Prius Liftback</a></td> 
<td >11:45 am Thursday, October 7, 2010</td><td >1:45 pm Thursday, October 7, 2010</td><td ><a href="#" class="tooltip_target" style="cursor: help;">$15.64</a> 
                <span class="tooltip" style="position: absolute; z-index: 1000; display: none;">$8.90&nbsp;(Time)&nbsp;+<br/>$3.50&nbsp;(Distance&nbsp;@&nbsp;14&nbsp;mile(s))&nbsp;+<br/>$0.00&nbsp;(Fees)&nbsp;+<br/>$3.24&nbsp;(Tax)</span></td><td >Normal</td><td >rasheed</td></tr><tr class="zebra"><td >2497938</td><td   width="25%"  align="center" valign="middle"  ><a class="text" href="my_fleet.php?mv_action=show&_r=19&pk=30005"    >47th & Baltimore - Prius Liftback</a></td> 
<td >6:15 am Monday, October 11, 2010</td><td >7:00 am Monday, October 11, 2010</td><td ><a href="#" class="tooltip_target" style="cursor: help;">$5.45</a> 
                <span class="tooltip" style="position: absolute; z-index: 1000; display: none;">$1.88&nbsp;(Time)&nbsp;+<br/>$1.25&nbsp;(Distance&nbsp;@&nbsp;5&nbsp;mile(s))&nbsp;+<br/>$0.00&nbsp;(Fees)&nbsp;+<br/>$2.32&nbsp;(Tax)</span></td><td >Normal</td><td >home depot</td></tr><tr ><td >2505758</td><td   width="25%"  align="center" valign="middle"  ><a class="text" href="my_fleet.php?mv_action=show&_r=19&pk=1390100"    >50th & Baltimore - Prius Liftback</a></td> 
<td >12:00 am Tuesday, October 19, 2010</td><td >1:15 am Tuesday, October 19, 2010</td><td ><a href="#" class="tooltip_target" style="cursor: help;">$7.92</a> 
                <span class="tooltip" style="position: absolute; z-index: 1000; display: none;">$3.13&nbsp;(Time)&nbsp;+<br/>$2.25&nbsp;(Distance&nbsp;@&nbsp;9&nbsp;mile(s))&nbsp;+<br/>$0.00&nbsp;(Fees)&nbsp;+<br/>$2.54&nbsp;(Tax)</span></td><td >Normal</td><td >jennifer</td></tr><tr class="zebra"><td >2505884</td><td   width="25%"  align="center" valign="middle"  ><a class="text" href="my_fleet.php?mv_action=show&_r=19&pk=1390100"    >50th & Baltimore - Prius Liftback</a></td> 
<td >9:30 am Tuesday, October 19, 2010</td><td >9:45 am Tuesday, October 19, 2010</td><td ><a href="#" class="tooltip_target" style="cursor: help;">$3.77</a> 
                <span class="tooltip" style="position: absolute; z-index: 1000; display: none;">$1.11&nbsp;(Time)&nbsp;+<br/>$0.50&nbsp;(Distance&nbsp;@&nbsp;2&nbsp;mile(s))&nbsp;+<br/>$0.00&nbsp;(Fees)&nbsp;+<br/>$2.16&nbsp;(Tax)</span></td><td >Normal</td><td >my phone is in the car</td></tr></tbody></table></td></tr></form></form><form action="my_reservations.php" method="post"><table class="full_width"><tr ><td ><td    align="right" valign="middle"  ><input type="hidden" name="main[multi_filter][history][yearmonth]" value="201010"/> 
<input type="hidden" name="mv_action" value="export_reservations"/> 
<input type="hidden" name="_r" value="19"/> 
<input type="hidden" name="main[multi_filter][driver_pk]" value="6285517"/> 
<button  id="export_reservations" type="submit" class="button button_export" ></button> 
</td> 
</td></tr></table></form></div><br style="clear: both" /><div id="mv_powered"><div id="mv_powered_left"><a href="http://www.metavera.com"><img src="/skin/base_images/mv_logo_small.gif" alt="Powered by Metavera"/></a></div><div id="mv_powered_right"><a href="http://www.metavera.com"><span>Powered by Metavera</span><br/>CarSharing Technology Leader</a></div></div></div><script language="javascript" type="text/javascript" src="/js/browser.js_3_47_0_5"></script> 
</body></html>'''

PAST_RESERVATIONS_SECOND_OF_FIVE_PAGES = r'''
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
<a class="text" href="/members/help.html?_r=17"  target="_blank"  >Help</a></span> 
<p >Mjumbe Poe, you are signed in. (Residential Account)</p><a href="my_reservations.php?_r=17&mv_action=logout"> 
                            <img class="logbutton" alt = "Log Out" src="/skin/base_images/btn_logout.gif" /> 
                   </a></div><img id="logo" src="/images/client_images/pcs_web_logo.gif" alt="PhillyCarShare" title="PhillyCarShare" /> 
        <div id="nav_bar"> 
        <div id="navcontainer"> 
        <ul id="navlist"><li ><a class="text link_new_reservation" href="my_reservations.php?_r=17"    >New Reservation</a></li><li ><a class="link_my_reservations" href="my_reservations.php?mv_action=main&_r=17"    >My Reservations</a></li><li ><a class="text link_my_messages" href="my_messages.php?_r=17"    >My Messages</a></li><li ><a class="text link_my_info" href="my_info.php?_r=17"    >My Account</a></li><li ><a class="text link_my_problems" href="my_problems.php?_r=17"    >Member Feedback</a></li></ul></div></div></div><div class="midbox"><h3 >My Reservations</h3><h5 >Past and Current Reservations</h5><div class="multi_filter"><form id="main_multi_filter_" name="multi_filter" action="my_reservations.php" method="get"  ><label for="main_multi_filter__history_" id="main_multi_filter__history__label"><b>Reservation&nbsp;Selection</b>:&nbsp;</label><select name="main[multi_filter][history][yearmonth]"    id="main_multi_filter__history__yearmonth_" tabindex="0"  > 
  <option value="-1">Current Reservations</option> 
  <option value="201010">October&nbsp;2010</option> 
  <option value="201009" selected>September&nbsp;2010</option> 
  <option value="201008">August&nbsp;2010</option> 
  <option value="201007">July&nbsp;2010</option> 
  <option value="201006">June&nbsp;2010</option> 
  <option value="201005">May&nbsp;2010</option> 
  <option value="201004">April&nbsp;2010</option> 
 </select><span class="instruction">&nbsp;</span><span ><td    align="center" valign="middle"  ><input type="hidden" name="mv_action" value="main"/> 
<input type="hidden" name="_r" value="17"/> 
<button  id="main" type="submit" class="button_update" ></button> 
</td> 
</span><input id="main_multi_filter__driver_pk_" type="hidden" name="main[multi_filter][driver_pk]" value="6285517" /></form></div><form name="main" method="post"><input id="main_dlist_" type="hidden" name="main[dlist]" value="" /><form id="main_dlist_" name="dlist" action="my_reservations.php" method="post"  ><tr ><td ><table class="dlist ma" id="main_dlist_"><thead ><tr ><td     align="center" valign="middle"  ><a class="text" href="my_reservations.php?main[multi_filter][history][yearmonth]=201009&mv_action=main&_r=17&main[multi_filter][driver_pk]=6285517&main[dlist][sort_col]=res_id&main[dlist][sort_dir]=asc"    >ID</a></td> 
<td     align="center" valign="middle"  ><a class="text" href="my_reservations.php?main[multi_filter][history][yearmonth]=201009&mv_action=main&_r=17&main[multi_filter][driver_pk]=6285517&main[dlist][sort_col]=ustack_descr&main[dlist][sort_dir]=asc"    >Stack</a></td> 
<td     align="center" valign="middle"  ><a class="text" href="my_reservations.php?main[multi_filter][history][yearmonth]=201009&mv_action=main&_r=17&main[multi_filter][driver_pk]=6285517&main[dlist][sort_col]=res_start&main[dlist][sort_dir]=asc"    >Start</a></td> 
<td     align="center" valign="middle"  ><a class="text" href="my_reservations.php?main[multi_filter][history][yearmonth]=201009&mv_action=main&_r=17&main[multi_filter][driver_pk]=6285517&main[dlist][sort_col]=res_end&main[dlist][sort_dir]=desc"    >End</a></td> 
<th  width="1%"  align="center" valign="middle"  ><font class="textbb">Est&nbsp;Cost</font></th> 
<td     align="center" valign="middle"  ><a class="text" href="my_reservations.php?main[multi_filter][history][yearmonth]=201009&mv_action=main&_r=17&main[multi_filter][driver_pk]=6285517&main[dlist][sort_col]=reservation_status&main[dlist][sort_dir]=asc"    >Status</a></td> 
<td     align="center" valign="middle"  ><a class="text" href="my_reservations.php?main[multi_filter][history][yearmonth]=201009&mv_action=main&_r=17&main[multi_filter][driver_pk]=6285517&main[dlist][sort_col]=res_extra&main[dlist][sort_dir]=asc"    >Memo</a></td> 
</tr></thead><tbody ><tr class="zebra"><td >2476904</td><td   width="25%"  align="center" valign="middle"  ><a class="text" href="my_fleet.php?mv_action=show&_r=17&pk=30005"    >47th & Baltimore - Prius Liftback</a></td> 
<td >9:30 pm Sunday, September 19, 2010</td><td >10:30 pm Sunday, September 19, 2010</td><td ><a href="#" class="tooltip_target" style="cursor: help;">$11.03</a> 
                <span class="tooltip" style="position: absolute; z-index: 1000; display: none;">$6.45&nbsp;(Time)&nbsp;+<br/>$1.75&nbsp;(Distance&nbsp;@&nbsp;7&nbsp;mile(s))&nbsp;+<br/>$0.00&nbsp;(Fees)&nbsp;+<br/>$2.83&nbsp;(Tax)</span></td><td >Normal</td><td >five guys</td></tr><tr ><td >2482804</td><td   width="25%"  align="center" valign="middle"  ><a class="text" href="my_fleet.php?mv_action=show&_r=17&pk=30005"    >47th & Baltimore - Prius Liftback</a></td> 
<td >10:55 pm Saturday, September 25, 2010</td><td >11:00 pm Saturday, September 25, 2010</td><td ><a href="#" class="tooltip_target" style="cursor: help;">$4.32</a> 
                <span class="tooltip" style="position: absolute; z-index: 1000; display: none;">$1.61&nbsp;(Time)&nbsp;+<br/>$0.50&nbsp;(Distance&nbsp;@&nbsp;2&nbsp;mile(s))&nbsp;+<br/>$0.00&nbsp;(Fees)&nbsp;+<br/>$2.21&nbsp;(Tax)</span></td><td >Normal</td><td >new reservation</td></tr><tr class="zebra"><td >2482842</td><td   width="25%"  align="center" valign="middle"  ><a class="text" href="my_fleet.php?mv_action=show&_r=17&pk=12174212"    >46th & Baltimore - Honda Element</a></td> 
<td >6:00 am Sunday, September 26, 2010</td><td >6:15 am Sunday, September 26, 2010</td><td ><a href="#" class="tooltip_target" style="cursor: help;">$3.24</a> 
                <span class="tooltip" style="position: absolute; z-index: 1000; display: none;">$0.63&nbsp;(Time)&nbsp;+<br/>$0.50&nbsp;(Distance&nbsp;@&nbsp;2&nbsp;mile(s))&nbsp;+<br/>$0.00&nbsp;(Fees)&nbsp;+<br/>$2.11&nbsp;(Tax)</span></td><td >Normal</td><td >new reservation</td></tr><tr ><td >2484939</td><td   width="25%"  align="center" valign="middle"  ><a class="text" href="my_fleet.php?mv_action=show&_r=17&pk=30005"    >47th & Baltimore - Prius Liftback</a></td> 
<td >1:15 am Tuesday, September 28, 2010</td><td >2:30 am Tuesday, September 28, 2010</td><td ><a href="#" class="tooltip_target" style="cursor: help;">$7.92</a> 
                <span class="tooltip" style="position: absolute; z-index: 1000; display: none;">$3.13&nbsp;(Time)&nbsp;+<br/>$2.25&nbsp;(Distance&nbsp;@&nbsp;9&nbsp;mile(s))&nbsp;+<br/>$0.00&nbsp;(Fees)&nbsp;+<br/>$2.54&nbsp;(Tax)</span></td><td >Normal</td><td >giant</td></tr><tr class="zebra"><td >2487978</td><td   width="25%"  align="center" valign="middle"  ><a class="text" href="my_fleet.php?mv_action=show&_r=17&pk=30005"    >47th & Baltimore - Prius Liftback</a></td> 
<td >9:15 pm Thursday, September 30, 2010</td><td >9:45 pm Thursday, September 30, 2010</td><td ><a href="#" class="tooltip_target" style="cursor: help;">$5.55</a> 
                <span class="tooltip" style="position: absolute; z-index: 1000; display: none;">$2.23&nbsp;(Time)&nbsp;+<br/>$1.00&nbsp;(Distance&nbsp;@&nbsp;4&nbsp;mile(s))&nbsp;+<br/>$0.00&nbsp;(Fees)&nbsp;+<br/>$2.32&nbsp;(Tax)</span></td><td >Normal</td><td >&nbsp;</td></tr></tbody></table></td></tr><table width="100%" id="dlist_pagination"><tr ><td  width="20%"  align="left" valign="middle"  ><input type="hidden" name="main[multi_filter][history][yearmonth]" value="201009"/> 
<input type="hidden" name="mv_action" value="main"/> 
<input type="hidden" name="_r" value="17"/> 
<input type="hidden" name="main[multi_filter][driver_pk]" value="6285517"/> 
<input type="hidden" name="main[dlist][sort_col]" value="res_end"/> 
<input type="hidden" name="main[dlist][sort_dir]" value="asc"/> 
<input type="hidden" name="main[dlist][page_num]" value="1"/> 
<button  id="previous" type="submit" class="button_previous" >Previous</button> 
</td> 
<td align="center"><span style="padding: 5px"><a class="text" href="my_reservations.php?main[multi_filter][history][yearmonth]=201009&mv_action=main&_r=17&main[multi_filter][driver_pk]=6285517&main[dlist][sort_col]=res_end&main[dlist][sort_dir]=asc&main[dlist][page_num]=1"    >1</a></span><span style="padding: 5px"><font class="text">2</font></span><span style="padding: 5px"><a class="text">3</a></span><span style="padding: 5px"><a class="text">4</a></span><span style="padding: 5px"><a class="text">5</a></span></td><td width="20%">&nbsp;</td></tr></table></form></form><form action="my_reservations.php" method="post"><table class="full_width"><tr ><td ><td    align="right" valign="middle"  ><input type="hidden" name="main[multi_filter][history][yearmonth]" value="201009"/> 
<input type="hidden" name="mv_action" value="export_reservations"/> 
<input type="hidden" name="_r" value="17"/> 
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

ONE_UPCOMING_RESERVATION_IN_OCTOBER = r'''
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"><html xmlns="http://www.w3.org/1999/xhtml"><head> 
<meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1" /> 
<meta http-equiv="pragma" content="no-cache" /> 
<meta http-equiv="cache-control" content="no-cache" /> 
<title >Reservation Manager</title><link rel="stylesheet" type="text/css" href="/skin/pcs_ui.css_3_47_0_8" title="pcs_skin" media="screen, print" /><link rel="stylesheet" type="text/css" href="/skin/pcs_layout.css_3_47_0_8" title="pcs_skin" media="screen, print" /><link rel="stylesheet" type="text/css" href="/skin/pcs_buttons.css_3_47_0_8" title="pcs_skin" media="screen, print" /><link rel="stylesheet" type="text/css" href="/skin/pcs_skin.css_3_47_0_8" title="pcs_skin" media="screen, print" /></head> 
<body bgcolor="white"  ><script language="javascript" type="text/javascript" src="/js/helper.js_3_47_0_8"></script> 
<script language="javascript" type="text/javascript" src="/js/prototype.js_3_47_0_8"></script> 
<script language="javascript" type="text/javascript" src="/js/lowpro.js_3_47_0_8"></script> 
<script language="javascript" type="text/javascript" src="/js/slider.js_3_47_0_8"></script> 
<script language="javascript" type="text/javascript" src="/js/lightbox.js_3_47_0_8"></script> 
<script language="javascript" type="text/javascript" src="/js/mf_lightbox.js_3_47_0_8"></script> 
<script language="javascript" type="text/javascript" src="/js/mv_base.js_3_47_0_8"></script> 
<script language="javascript" type="text/javascript" src="/js/mv_reserve.js_3_47_0_8"></script> 
<div class="mv_header"> 
<img border="0" src="/images/client_images/pcs_web_logo.gif" alt="PhillyCarShare" title="PhillyCarShare" /> 
</div> 
<div id="wrapper"><div id="page_header"><div id="lame_image"><span class="switch"> 
<a class="text" href="/members/help.html?_r=18"  target="_blank"  >Help</a></span> 
<p >Mjumbe Poe, you are signed in. (Residential Account)</p><a href="my_reservations.php?_r=18&mv_action=logout"> 
                            <img class="logbutton" alt = "Log Out" src="/skin/base_images/btn_logout.gif" /> 
                   </a></div><img id="logo" src="/images/client_images/pcs_web_logo.gif" alt="PhillyCarShare" title="PhillyCarShare" /> 
        <div id="nav_bar"> 
        <div id="navcontainer"> 
        <ul id="navlist"><li ><a class="text link_new_reservation" href="my_reservations.php?_r=18"    >New Reservation</a></li><li ><a class="link_my_reservations" href="my_reservations.php?mv_action=main&_r=18"    >My Reservations</a></li><li ><a class="text link_my_messages" href="my_messages.php?_r=18"    >My Messages</a></li><li ><a class="text link_my_info" href="my_info.php?_r=18"    >My Account</a></li><li ><a class="text link_my_problems" href="my_problems.php?_r=18"    >Member Feedback</a></li></ul></div></div></div><div class="midbox"><h3 >My Reservations</h3><h5 >Past and Current Reservations</h5><div class="multi_filter"><form id="main_multi_filter_" name="multi_filter" action="my_reservations.php" method="get"  ><label for="main_multi_filter__history_" id="main_multi_filter__history__label"><b>Reservation&nbsp;Selection</b>:&nbsp;</label><select name="main[multi_filter][history][yearmonth]"    id="main_multi_filter__history__yearmonth_" tabindex="0"  > 
  <option value="-1">Current Reservations</option> 
  <option value="201010" selected>October&nbsp;2010</option> 
  <option value="201009">September&nbsp;2010</option> 
  <option value="201008">August&nbsp;2010</option> 
  <option value="201007">July&nbsp;2010</option> 
  <option value="201006">June&nbsp;2010</option> 
  <option value="201005">May&nbsp;2010</option> 
  <option value="201004">April&nbsp;2010</option> 
 </select><span class="instruction">&nbsp;</span><span ><td    align="center" valign="middle"  ><input type="hidden" name="mv_action" value="main"/> 
<input type="hidden" name="_r" value="18"/> 
<button  id="main" type="submit" class="button_update" ></button> 
</td> 
</span><input id="main_multi_filter__driver_pk_" type="hidden" name="main[multi_filter][driver_pk]" value="6285517" /></form></div><form name="main" method="post"><form id="main_dlist_" name="dlist" action="my_reservations.php" method="post"  ><tr ><td ><table class="dlist ma" id="main_dlist_"><thead ><tr ><td     align="center" valign="middle"  ><a class="text" href="my_reservations.php?main[multi_filter][history][yearmonth]=201010&mv_action=main&_r=18&main[multi_filter][driver_pk]=6285517&main[dlist][sort_col]=res_id&main[dlist][sort_dir]=asc"    >ID</a></td> 
<td     align="center" valign="middle"  ><a class="text" href="my_reservations.php?main[multi_filter][history][yearmonth]=201010&mv_action=main&_r=18&main[multi_filter][driver_pk]=6285517&main[dlist][sort_col]=ustack_descr&main[dlist][sort_dir]=asc"    >Stack</a></td> 
<td     align="center" valign="middle"  ><a class="text" href="my_reservations.php?main[multi_filter][history][yearmonth]=201010&mv_action=main&_r=18&main[multi_filter][driver_pk]=6285517&main[dlist][sort_col]=res_start&main[dlist][sort_dir]=asc"    >Start</a></td> 
<td     align="center" valign="middle"  ><a class="text" href="my_reservations.php?main[multi_filter][history][yearmonth]=201010&mv_action=main&_r=18&main[multi_filter][driver_pk]=6285517&main[dlist][sort_col]=res_end&main[dlist][sort_dir]=desc"    >End</a></td> 
<th  width="1%"  align="center" valign="middle"  ><font class="textbb">Est&nbsp;Cost</font></th> 
<td     align="center" valign="middle"  ><a class="text" href="my_reservations.php?main[multi_filter][history][yearmonth]=201010&mv_action=main&_r=18&main[multi_filter][driver_pk]=6285517&main[dlist][sort_col]=reservation_status&main[dlist][sort_dir]=asc"    >Status</a></td> 
<td     align="center" valign="middle"  ><a class="text" href="my_reservations.php?main[multi_filter][history][yearmonth]=201010&mv_action=main&_r=18&main[multi_filter][driver_pk]=6285517&main[dlist][sort_col]=res_extra&main[dlist][sort_dir]=asc"    >Memo</a></td> 
<td align="center"><font class="textbb">&nbsp;</font></td> 
</tr></thead><tbody ><tr class="zebra"><td >2491921</td><td   width="25%"  align="center" valign="middle"  ><a class="text" href="my_fleet.php?mv_action=show&_r=18&pk=30005"    >47th & Baltimore - Prius Liftback</a></td> 
<td >12:00 am Tuesday, October 5, 2010</td><td >1:00 am Tuesday, October 5, 2010</td><td ><a href="#" class="tooltip_target" style="cursor: help;">$6.68</a> 
                <span class="tooltip" style="position: absolute; z-index: 1000; display: none;">$2.50&nbsp;(Time)&nbsp;+<br/>$1.75&nbsp;(Distance&nbsp;@&nbsp;7&nbsp;mile(s))&nbsp;+<br/>$0.00&nbsp;(Fees)&nbsp;+<br/>$2.43&nbsp;(Tax)</span></td><td >Normal</td><td >jennifer</td><td width="176"></td></tr><tr ><td >2494232</td><td   width="25%"  align="center" valign="middle"  ><a class="text" href="my_fleet.php?mv_action=show&_r=18&pk=30005"    >47th & Baltimore - Prius Liftback</a></td> 
<td >11:45 am Thursday, October 7, 2010</td><td >1:45 pm Thursday, October 7, 2010</td><td ><a href="#" class="tooltip_target" style="cursor: help;">$15.64</a> 
                <span class="tooltip" style="position: absolute; z-index: 1000; display: none;">$8.90&nbsp;(Time)&nbsp;+<br/>$3.50&nbsp;(Distance&nbsp;@&nbsp;14&nbsp;mile(s))&nbsp;+<br/>$0.00&nbsp;(Fees)&nbsp;+<br/>$3.24&nbsp;(Tax)</span></td><td >Normal</td><td >rasheed</td><td width="176"></td></tr><tr class="zebra"><td >2497938</td><td   width="25%"  align="center" valign="middle"  ><a class="text" href="my_fleet.php?mv_action=show&_r=18&pk=30005"    >47th & Baltimore - Prius Liftback</a></td> 
<td >6:15 am Monday, October 11, 2010</td><td >7:00 am Monday, October 11, 2010</td><td ><a href="#" class="tooltip_target" style="cursor: help;">$5.45</a> 
                <span class="tooltip" style="position: absolute; z-index: 1000; display: none;">$1.88&nbsp;(Time)&nbsp;+<br/>$1.25&nbsp;(Distance&nbsp;@&nbsp;5&nbsp;mile(s))&nbsp;+<br/>$0.00&nbsp;(Fees)&nbsp;+<br/>$2.32&nbsp;(Tax)</span></td><td >Normal</td><td >home depot</td><td width="176"></td></tr><tr ><td >2505758</td><td   width="25%"  align="center" valign="middle"  ><a class="text" href="my_fleet.php?mv_action=show&_r=18&pk=1390100"    >50th & Baltimore - Prius Liftback</a></td> 
<td >12:00 am Tuesday, October 19, 2010</td><td >1:15 am Tuesday, October 19, 2010</td><td ><a href="#" class="tooltip_target" style="cursor: help;">$7.92</a> 
                <span class="tooltip" style="position: absolute; z-index: 1000; display: none;">$3.13&nbsp;(Time)&nbsp;+<br/>$2.25&nbsp;(Distance&nbsp;@&nbsp;9&nbsp;mile(s))&nbsp;+<br/>$0.00&nbsp;(Fees)&nbsp;+<br/>$2.54&nbsp;(Tax)</span></td><td >Normal</td><td >jennifer</td><td width="176"></td></tr><tr class="zebra"><td >2505884</td><td   width="25%"  align="center" valign="middle"  ><a class="text" href="my_fleet.php?mv_action=show&_r=18&pk=1390100"    >50th & Baltimore - Prius Liftback</a></td> 
<td >9:30 am Tuesday, October 19, 2010</td><td >9:45 am Tuesday, October 19, 2010</td><td ><a href="#" class="tooltip_target" style="cursor: help;">$3.77</a> 
                <span class="tooltip" style="position: absolute; z-index: 1000; display: none;">$1.11&nbsp;(Time)&nbsp;+<br/>$0.50&nbsp;(Distance&nbsp;@&nbsp;2&nbsp;mile(s))&nbsp;+<br/>$0.00&nbsp;(Fees)&nbsp;+<br/>$2.16&nbsp;(Tax)</span></td><td >Normal</td><td >my phone is in the car</td><td width="176"></td></tr><tr ><td >2514083</td><td   width="25%"  align="center" valign="middle"  ><a class="text" href="my_fleet.php?mv_action=show&_r=18&pk=30005"    >47th & Baltimore - Prius Liftback</a></td> 
<td >6:45 am Thursday, October 28, 2010</td><td >7:00 am Thursday, October 28, 2010</td><td ><a href="#" class="tooltip_target" style="cursor: help;">$3.24</a> 
                <span class="tooltip" style="position: absolute; z-index: 1000; display: none;">$0.63&nbsp;(Time)&nbsp;+<br/>$0.50&nbsp;(Distance&nbsp;@&nbsp;2&nbsp;mile(s))&nbsp;+<br/>$0.00&nbsp;(Fees)&nbsp;+<br/>$2.11&nbsp;(Tax)</span></td><td >Normal</td><td >testing</td><td width="176"><button  id="edit" type="button" class="button button_edit" onclick="; window.location='my_reservations.php?mv_action=edit&_r=18&pk=149337407'">Change</button> 
<button  id="do_cancel" type="button" class="button button_do_cancel" onclick="; window.location='my_reservations.php?mv_action=do_cancel&_r=18&pk=149337407'">Cancel</button> 
</td></tr></tbody></table></td></tr></form></form><form action="my_reservations.php" method="post"><table class="full_width"><tr ><td ><td    align="right" valign="middle"  ><input type="hidden" name="main[multi_filter][history][yearmonth]" value="201010"/> 
<input type="hidden" name="mv_action" value="export_reservations"/> 
<input type="hidden" name="_r" value="18"/> 
<input type="hidden" name="main[multi_filter][driver_pk]" value="6285517"/> 
<button  id="export_reservations" type="submit" class="button button_export" ></button> 
</td> 
</td></tr></table></form></div><br style="clear: both" /><div id="mv_powered"><div id="mv_powered_left"><a href="http://www.metavera.com"><img src="/skin/base_images/mv_logo_small.gif" alt="Powered by Metavera"/></a></div><div id="mv_powered_right"><a href="http://www.metavera.com"><span>Powered by Metavera</span><br/>CarSharing Technology Leader</a></div></div></div><script language="javascript" type="text/javascript" src="/js/browser.js_3_47_0_8"></script> 
</body></html>'''

NEW_RESERVATION_REDIRECT_SCRIPT=r'''<script type="text/javascript">window.location = 'my_reservations.php?mv_action=confirm&_r=11&pk=149385106';</script>'''

NEW_RESERVATION_CONFIRMATION=r'''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"><html xmlns="http://www.w3.org/1999/xhtml"><head>
<meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1" />
<meta http-equiv="pragma" content="no-cache" />
<meta http-equiv="cache-control" content="no-cache" />
<title >Reservation Manager</title><link rel="stylesheet" type="text/css" href="/skin/pcs_ui.css_3_47_0_10" title="pcs_skin" media="screen, print" /><link rel="stylesheet" type="text/css" href="/skin/pcs_layout.css_3_47_0_10" title="pcs_skin" media="screen, print" /><link rel="stylesheet" type="text/css" href="/skin/pcs_buttons.css_3_47_0_10" title="pcs_skin" media="screen, print" /><link rel="stylesheet" type="text/css" href="/skin/pcs_skin.css_3_47_0_10" title="pcs_skin" media="screen, print" /><link rel="stylesheet" type="text/css" href="/js/calendar.css_3_47_0_10" media="screen, print" /><script language="javascript" type="text/javascript">
        function start_gmap(){
            this.js_gmap = new MVgmap('google_map');
            js_gmap.fav_lots = [];
            js_gmap.marker_event = 'click';

            js_gmap.icon_def = new GIcon(G_DEFAULT_ICON, '/images/client_images/gmarker_def.png');
            js_gmap.icon_def.iconSize = new GSize(15, 26);
            js_gmap.icon_def.iconAnchor = new GPoint(8, 26);
            js_gmap.icon_def.shadowSize = new GSize(15, 26);

            js_gmap.icon_fav = new GIcon(G_DEFAULT_ICON, '/images/client_images/gmarker_fav.png');
            js_gmap.icon_fav.iconSize = new GSize(15, 26);
            js_gmap.icon_fav.iconAnchor = new GPoint(8, 26);
            js_gmap.icon_fav.shadowSize = new GSize(15, 26);

            js_gmap.load(39.948429, -75.218014, 16);
            js_gmap.addMarkers([[39.948429,-75.218014,'47th & Baltimore',[],0]]);
        
            js_gmap.map.disableDragging();
            js_gmap.map.disableDoubleClickZoom();
        }
</script>
<script language="javascript" type="text/javascript">function unload_gmap() {
                            js_gmap.unload();
                          }
</script>
</head>
<body bgcolor="white" onload="start_gmap(); " onunload="unload_gmap(); "><script language="javascript" type="text/javascript" src="/js/helper.js_3_47_0_10"></script>
<script language="javascript" type="text/javascript" src="/js/popup.js_3_47_0_10"></script>
<script language="javascript" type="text/javascript" src="/js/browser.js_3_47_0_10"></script>
<script language="javascript" type="text/javascript" src="/js/calendar.js_3_47_0_10"></script>
<script language="javascript" type="text/javascript" src="/js/calendarDateInput.js_3_47_0_10"></script>
<script language="javascript" type="text/javascript" src="/js/prototype.js_3_47_0_10"></script>
<script language="javascript" type="text/javascript" src="/js/lowpro.js_3_47_0_10"></script>
<script language="javascript" type="text/javascript" src="/js/mf_lightbox.js_3_47_0_10"></script>
<script language="javascript" type="text/javascript" src="/js/mv_base.js_3_47_0_10"></script>
<script language="javascript" type="text/javascript" src="/js/mv_location.js_3_47_0_10"></script>
<script language="javascript" type="text/javascript" src="http://maps.google.com/maps?file=api&amp;v=2&amp;key=ABQIAAAANNQNgPHY7hmfMuDnzGRL8xRCiyh3L1O9lXHVi81tmDjTTZCYKBSsT-tdn3x62eoISpd9Z2wIbqPixQ"></script>
<script language="javascript" type="text/javascript" src="/js/xmlhttp.js_3_47_0_10"></script>
<script language="javascript" type="text/javascript" src="/js/gmap.js_3_47_0_10"></script>
<script language="javascript" type="text/javascript" src="/js/slider.js_3_47_0_10"></script>
<script language="javascript" type="text/javascript" src="/js/lightbox.js_3_47_0_10"></script>
<script language="javascript" type="text/javascript" src="/js/mv_reserve.js_3_47_0_10"></script>
<div class="mv_header">
<img border="0" src="/images/client_images/pcs_web_logo.gif" alt="PhillyCarShare" title="PhillyCarShare" />
</div>
<div id="wrapper"><div id="page_header"><div id="lame_image"><span class="switch">
<a class="text" href="/members/help.html?_r=14"  target="_blank"  >Help</a></span>
<p >Mjumbe Poe, you are signed in. (Residential Account)</p><a href="my_reservations.php?_r=14&mv_action=logout">
                            <img class="logbutton" alt = "Log Out" src="/skin/base_images/btn_logout.gif" />
                   </a></div><img id="logo" src="/images/client_images/pcs_web_logo.gif" alt="PhillyCarShare" title="PhillyCarShare" />
        <div id="nav_bar">
        <div id="navcontainer">
        <ul id="navlist"><li ><a class="text link_new_reservation" href="my_reservations.php?_r=14"    >New Reservation</a></li><li ><a class="link_my_reservations" href="my_reservations.php?mv_action=main&_r=14"    >My Reservations</a></li><li ><a class="text link_my_messages" href="my_messages.php?_r=14"    >My Messages</a></li><li ><a class="text link_my_info" href="my_info.php?_r=14"    >My Account</a></li><li ><a class="text link_my_problems" href="my_problems.php?_r=14"    >Member Feedback</a></li></ul></div></div></div><div class="midbox"><h3 >NEW Reservation Confirmation</h3><h5 class="confirm_title"><img src="/skin/img/information.gif"/>Please <a class="largeo" href="javascript://" onclick="window.print(); return(false);">Print</a> or copy the following confirmation details. Please always have these details with you for reference.</h5><div id="left"><h4 >Your new reservation details are:  </h4><table class="mi"><tr ><td align="right">Member&nbsp;Name</td><td align="left">Mjumbe Poe</td></tr><tr ><td align="right">Member&nbsp;ID:</td><td align="left">6489</td></tr><tr ><td width="23%"    align="right" valign="middle"  >
<font class="text">Stack:</font>
</td>
<td  colspan="2" width="80%"  align="left" valign="middle"  ><a class="text" href="my_fleet.php?mv_action=stack_detail&_r=14&pk=30005&stack_pk=96692246"    >47th & Baltimore - Prius Liftback</a></td>
</tr><tr ><tr ><td width=25% colspan=1   align="right" valign="middle"  >
<font class="text">Start:</font>
</td>
<td colspan="2" width="80%" colspan=1   align="left" valign="middle"  >
<font class="text">2:45 am Sunday, October 31, 2010</font>
</td>

<script language="javascript" type="text/javascript">
 new_date_control('confirm[start_stamp][date]', 'Show_Date', 20101030, 20110131, 20101030, 'm/d/y');</script>
</tr><tr ><td width=25% colspan=1   align="right" valign="middle"  >
<font class="text">End:</font>
</td>
<td colspan="2" width="80%" colspan=1   align="left" valign="middle"  >
<font class="text">3:00 am Sunday, October 31, 2010</font>
</td>

<script language="javascript" type="text/javascript">
 new_date_control('confirm[end_stamp][date]', 'Show_Date', 20101030, 20110131, 20101030, 'm/d/y');</script>
</tr><tr ><td width="25%"    align="right" valign="middle"  >
<font class="text">Duration:</font>
</td>
<td colspan="2" width="75%"    align="left" valign="middle"  >
<font class="text">0.25&nbsp;hour(s)</font>
</td>
</tr></tr><tr ><td width=20%    align="right" valign="middle"  >
<font class="text">Memo:</font>
</td>
<td colspan="2" width="75%"    align="left" valign="middle"  >
<font class="text">testing</font>
</td>
</tr><tr ><td ><label for="confirm_id_" id="confirm_id__label">Reservation&nbsp;ID:</label></td><td ><span id="confirm_id_">2516709</span></td><td ><span class="instruction">&nbsp;</span></td></tr><tr ><td ><label for="confirm_trip_estimate_pk_" id="confirm_trip_estimate_pk__label">Estimated&nbsp;Cost:</label></td><td ><span id="confirm_trip_estimate_pk_">$0.63 (Time) +<br/>$0.50 (Distance @ 2 mile(s)) +<br/>$0.00 (Fees) +<br/>$2.11 (Tax) =<br/>$3.24 (Total)</span></td><td ><span class="instruction">&nbsp;</span></td></tr></table><br  /><h4 >POD Information:</h4><div id="lot_descr"><p ><span id="stack_pk">47th & Baltimore - Prius Liftback</span><span class="instruction">&nbsp;</span></p><p ><span id="location_descr"><b>4720 Baltimore Avenue</b><br>Philadelphia Parking Authority lot<br><br>Vehicles are parked in this open PPA lot on the south side of Baltimore Avenue, mid-block between 47th & 48th Streets, and are parked in reserved spaces on the north side of the lot, adjacent to Baltimore Avenue.<br><br />
<br />
If you are picking up a vehicle and cannot locate it in one of the reserved spaces, please check around the rest of the lot before calling the emergency line.<br><br />
<br><br />
<b>SEPTA access:</b> via the Route 34 trolley or the Route 64 bus.<br />
<br><br />
<br />
</span><span class="instruction">&nbsp;</span></p></div></div><div id="right"><div id="small_map"><td align="center" colspan="2"><script src='http://maps.google.com/maps?file=api&amp;v=2&amp;key=ABQIAAAANNQNgPHY7hmfMuDnzGRL8xRCiyh3L1O9lXHVi81tmDjTTZCYKBSsT-tdn3x62eoISpd9Z2wIbqPixQ' type='text/javascript'></script><div id="google_map" style="width: 300px; height: 300px; border: solid 1px; border-color:#00ad87;"></div></td></div><div class="buttons_box"><div style="color: #f50c0c; font-weight: bold;">Consider padding your time. <br>Returning after your reservation End Time will cost you $40 per half hour.</div><tr ><td ><table class="dlist ma" id="change_actions"><thead ><tr ><td align="center"><font class="textbb">&nbsp;</font></td>
</tr></thead><tbody ><tr class="zebra"><td width="100%"><button  id="edit" type="button" class="button button_edit" onclick="; window.location='my_reservations.php?mv_action=edit&_r=14&pk=149381945'">Change</button>
<button  id="do_cancel" type="button" class="button button_do_cancel" onclick="; window.location='my_reservations.php?mv_action=do_cancel&_r=14&pk=149381945'">Cancel</button>
</td></tr></tbody></table></td></tr><table ><tr ><td    align="left" valign="middle"  ><form id="print" name="print" action="my_reservations.php" method="post"  >
<table  width="100%"   border="0" cellspacing="0" cellpadding="0">
<tr ><td>&nbsp;</td>
<td    align="left" valign="middle"  ><input type="hidden" name="mv_action" value="print"/>
<input type="hidden" name="_r" value="14"/>
<button  id="print" type="submit" class="button button_print" onclick="window.print(); return(false);">Print this Confirmation</button>
</td>
<td></td></tr>
</table></form></td>
</tr></table><table ><tr ><td    align="left" valign="middle"  ><form id="outlook" name="outlook" action="outlook.php" method="GET"  >
<table  width="100%"   border="0" cellspacing="0" cellpadding="0">
<tr ><td>&nbsp;</td>
<td    align="left" valign="middle"  ><input type="hidden" name="mv_action" value="outlook"/>
<input type="hidden" name="_r" value="14"/>
<input type="hidden" name="pk" value="149381945"/>
<button  id="outlook" type="submit" class="button button_outlook" >Save to Outlook</button>
</td>
<td></td></tr>
</table></form></td>
</tr></table><table ><tr ><td    align="left" valign="middle"  ><form id="email" name="email" action="confirmation.php" method="post"  >
<table  width="100%"   border="0" cellspacing="0" cellpadding="0">
<tr ><td>&nbsp;</td>
<td    align="left" valign="middle"  ><table><tr><td><input type="hidden" name="mv_action" value="email"/>
<input type="hidden" name="_r" value="14"/>
<input type="hidden" name="pk" value="149381945"/>
<button  id="email" type="submit" class="button_disabled" onclick="return(false);">Confirmation Email Sent</button>
</td></tr><tr><td     align="center" valign="middle"  ><a class="text" href="my_info.php?mv_action=dpref&_r=14&pk=6285517"    >Edit&nbsp;Email&nbsp;Preferences</a></td>
</tr></table></td>
<td></td></tr>
</table></form></td>
</tr></table></div><div class="costs"><h4 >Prius Liftback</h4><img src="/images/client_images/toyota_prius_lift.jpg" /><br  /><div class="price"><p >$2.50 Hourly / $69.00 Daily</p></div><ul ><li ><img src="/skin/base_images/hybrid.gif" label="Hybrid" title="Hybrid" /><span style="padding-left: 0.5em;">Hybrid</span></li><li ><img src="/skin/base_images/folding_seat.gif" label="Folding Rear Seats" title="Folding Rear Seats" /><span style="padding-left: 0.5em;">Folding Rear Seats</span></li></ul></div></div><br style="clear: both;"><h5 class="confirm_title"><img src="/skin/img/information.gif"/>For easy reference to our online handbook, click <a href="http://www.phillycarshare.org/sites/default/files/member-handbook.pdf" target="_blank">here</a>.</h5><p class="note"><img src="/skin/img/exclamation.gif" />For time-sensitive matters during your reservation, please call the 24-hour emergency line at 215.730.0988 x1.</p></div><br style="clear: both" /><div id="mv_powered"><div id="mv_powered_left"><a href="http://www.metavera.com"><img src="/skin/base_images/mv_logo_small.gif" alt="Powered by Metavera"/></a></div><div id="mv_powered_right"><a href="http://www.metavera.com"><span>Powered by Metavera</span><br/>CarSharing Technology Leader</a></div></div></div></body></html>'''

RESERVATION_LIGHTBOX_WITH_NO_VEHICLE_INFO=r'''<div class="lightbox" id="fakeLightbox"><h3 >Your Reservation</h3><div class="lightbox_contents"><p id="lightbox_instruction" class="error"></p><form class="reservation" id="add" name="add" method="post" action="lightbox.php"><div class="left_panel"><fieldset class="stack_fieldset"><input type="hidden" name="add[stack_pk]" value="" /><table ><tr ><td ><label for="add_stack_pk__location">Location:</label></td><td ><span id="add_stack_pk__location" /></td></tr><tr ><td ><label for="add_stack_pk_vt">Vehicle Type:</label></td><td ><span id="add_stack_pk_vt" /></td></tr></table></fieldset><fieldset class="range_fieldset"><table ><tr ><td ><label for="add_start_stamp__start_date_">Start:</label></td><td class="stamp_control"><input id="add_start_stamp__start_date_" name="add[start_stamp][start_date][date]" class="date_control" onchange="" value="---" />    <script language="javascript" type="text/javascript">
        DateInput('add_start_stamp__start_date__calendar', 'add_start_stamp__start_date_', true, '1288506713', 'm/d/y', null, null);
    </script><select id="add_start_stamp__start_time_" name="add[start_stamp][start_time][time]" class="time_control"><option value="0">Midnight</option><option value="900">12:15 AM</option><option value="1800">12:30 AM</option><option value="2700">12:45 AM</option><option value="3600">01:00 AM</option><option value="4500">01:15 AM</option><option value="5400">01:30 AM</option><option value="6300">01:45 AM</option><option value="7200">02:00 AM</option><option value="8100">02:15 AM</option><option value="9000">02:30 AM</option><option value="9900">02:45 AM</option><option value="10800">03:00 AM</option><option value="11700">03:15 AM</option><option value="12600">03:30 AM</option><option value="13500">03:45 AM</option><option value="14400">04:00 AM</option><option value="15300">04:15 AM</option><option value="16200">04:30 AM</option><option value="17100">04:45 AM</option><option value="18000">05:00 AM</option><option value="18900">05:15 AM</option><option value="19800">05:30 AM</option><option value="20700">05:45 AM</option><option value="21600">06:00 AM</option><option value="22500">06:15 AM</option><option value="23400">06:30 AM</option><option value="24300">06:45 AM</option><option value="25200">07:00 AM</option><option value="26100">07:15 AM</option><option value="27000">07:30 AM</option><option value="27900">07:45 AM</option><option value="28800">08:00 AM</option><option value="29700">08:15 AM</option><option value="30600">08:30 AM</option><option value="31500">08:45 AM</option><option value="32400">09:00 AM</option><option value="33300">09:15 AM</option><option value="34200">09:30 AM</option><option value="35100">09:45 AM</option><option value="36000">10:00 AM</option><option value="36900">10:15 AM</option><option value="37800">10:30 AM</option><option value="38700">10:45 AM</option><option value="39600">11:00 AM</option><option value="40500">11:15 AM</option><option value="41400">11:30 AM</option><option value="42300">11:45 AM</option><option value="-1" selected="selected"></option><option value="43200">Noon</option><option value="44100">12:15 PM</option><option value="45000">12:30 PM</option><option value="45900">12:45 PM</option><option value="46800">01:00 PM</option><option value="47700">01:15 PM</option><option value="48600">01:30 PM</option><option value="49500">01:45 PM</option><option value="50400">02:00 PM</option><option value="51300">02:15 PM</option><option value="52200">02:30 PM</option><option value="53100">02:45 PM</option><option value="54000">03:00 PM</option><option value="54900">03:15 PM</option><option value="55800">03:30 PM</option><option value="56700">03:45 PM</option><option value="57600">04:00 PM</option><option value="58500">04:15 PM</option><option value="59400">04:30 PM</option><option value="60300">04:45 PM</option><option value="61200">05:00 PM</option><option value="62100">05:15 PM</option><option value="63000">05:30 PM</option><option value="63900">05:45 PM</option><option value="64800">06:00 PM</option><option value="65700">06:15 PM</option><option value="66600">06:30 PM</option><option value="67500">06:45 PM</option><option value="68400">07:00 PM</option><option value="69300">07:15 PM</option><option value="70200">07:30 PM</option><option value="71100">07:45 PM</option><option value="72000">08:00 PM</option><option value="72900">08:15 PM</option><option value="73800">08:30 PM</option><option value="74700">08:45 PM</option><option value="75600">09:00 PM</option><option value="76500">09:15 PM</option><option value="77400">09:30 PM</option><option value="78300">09:45 PM</option><option value="79200">10:00 PM</option><option value="80100">10:15 PM</option><option value="81000">10:30 PM</option><option value="81900">10:45 PM</option><option value="82800">11:00 PM</option><option value="83700">11:15 PM</option><option value="84600">11:30 PM</option><option value="85500">11:45 PM</option></select></td></tr><tr ><td ><label for="add_end_stamp__end_date_">End:</label></td><td class="stamp_control"><input id="add_end_stamp__end_date_" name="add[end_stamp][end_date][date]" class="date_control" onchange="" value="---" />    <script language="javascript" type="text/javascript">
        DateInput('add_end_stamp__end_date__calendar', 'add_end_stamp__end_date_', true, '1288506713', 'm/d/y', null, null);
    </script><select id="add_end_stamp__end_time_" name="add[end_stamp][end_time][time]" class="time_control"><option value="0">Midnight</option><option value="900">12:15 AM</option><option value="1800">12:30 AM</option><option value="2700">12:45 AM</option><option value="3600">01:00 AM</option><option value="4500">01:15 AM</option><option value="5400">01:30 AM</option><option value="6300">01:45 AM</option><option value="7200">02:00 AM</option><option value="8100">02:15 AM</option><option value="9000">02:30 AM</option><option value="9900">02:45 AM</option><option value="10800">03:00 AM</option><option value="11700">03:15 AM</option><option value="12600">03:30 AM</option><option value="13500">03:45 AM</option><option value="14400">04:00 AM</option><option value="15300">04:15 AM</option><option value="16200">04:30 AM</option><option value="17100">04:45 AM</option><option value="18000">05:00 AM</option><option value="18900">05:15 AM</option><option value="19800">05:30 AM</option><option value="20700">05:45 AM</option><option value="21600">06:00 AM</option><option value="22500">06:15 AM</option><option value="23400">06:30 AM</option><option value="24300">06:45 AM</option><option value="25200">07:00 AM</option><option value="26100">07:15 AM</option><option value="27000">07:30 AM</option><option value="27900">07:45 AM</option><option value="28800">08:00 AM</option><option value="29700">08:15 AM</option><option value="30600">08:30 AM</option><option value="31500">08:45 AM</option><option value="32400">09:00 AM</option><option value="33300">09:15 AM</option><option value="34200">09:30 AM</option><option value="35100">09:45 AM</option><option value="36000">10:00 AM</option><option value="36900">10:15 AM</option><option value="37800">10:30 AM</option><option value="38700">10:45 AM</option><option value="39600">11:00 AM</option><option value="40500">11:15 AM</option><option value="41400">11:30 AM</option><option value="42300">11:45 AM</option><option value="-1" selected="selected"></option><option value="43200">Noon</option><option value="44100">12:15 PM</option><option value="45000">12:30 PM</option><option value="45900">12:45 PM</option><option value="46800">01:00 PM</option><option value="47700">01:15 PM</option><option value="48600">01:30 PM</option><option value="49500">01:45 PM</option><option value="50400">02:00 PM</option><option value="51300">02:15 PM</option><option value="52200">02:30 PM</option><option value="53100">02:45 PM</option><option value="54000">03:00 PM</option><option value="54900">03:15 PM</option><option value="55800">03:30 PM</option><option value="56700">03:45 PM</option><option value="57600">04:00 PM</option><option value="58500">04:15 PM</option><option value="59400">04:30 PM</option><option value="60300">04:45 PM</option><option value="61200">05:00 PM</option><option value="62100">05:15 PM</option><option value="63000">05:30 PM</option><option value="63900">05:45 PM</option><option value="64800">06:00 PM</option><option value="65700">06:15 PM</option><option value="66600">06:30 PM</option><option value="67500">06:45 PM</option><option value="68400">07:00 PM</option><option value="69300">07:15 PM</option><option value="70200">07:30 PM</option><option value="71100">07:45 PM</option><option value="72000">08:00 PM</option><option value="72900">08:15 PM</option><option value="73800">08:30 PM</option><option value="74700">08:45 PM</option><option value="75600">09:00 PM</option><option value="76500">09:15 PM</option><option value="77400">09:30 PM</option><option value="78300">09:45 PM</option><option value="79200">10:00 PM</option><option value="80100">10:15 PM</option><option value="81000">10:30 PM</option><option value="81900">10:45 PM</option><option value="82800">11:00 PM</option><option value="83700">11:15 PM</option><option value="84600">11:30 PM</option><option value="85500">11:45 PM</option></select></td></tr><tr ><td ><label for="add_job_code_">Memo:</label></td><td ><input id="add_job_code_" name="add[job_code]" type="text" size="25" maxlength="25" value="" onkeypress="
            var keyCode = event.keyCode ? event.keyCode : event.which ? event.which : event.charCode;
                if (keyCode == 13) {
                    return false;
                }
                return true;
        " class="memo_control" /></td></tr><tr ><td colspan="2" style="color: #f50c0c; font-size: 11px; font-weight: bold;">Consider padding your time. Returning after your reservation End Time will cost you $40 per half hour.</td></tr></table><input id="add_tid_" type="hidden" name="add[tid]" value="5"/>
<input type="hidden" name="mv_action" value="add" /><input type="hidden" name="_r" value="10" /></fieldset></div><div class="right_panel"><div class="price"><div id="add_price__price_" class="container">$??.00 hourly / $??.00 daily</div></div><ul class="amenity"><li ></li></ul></div><div class="bottom_panel"><div class="cost"><div id="add_balance__balance__div"><label for="add_balance__balance_">AVAILABLE BALANCE:</label><span id="add_balance__balance_" class=""></span></div></div><div class="cost"><label for="add_estimate__estimate_">ESTIMATED COST:</label><span id="add_estimate__estimate_" class="">?</span><div class="price_box"> <label for="add_estimate__estimate__time_amount" class="top">Time:</label>
<span id="add_estimate__estimate__time_amount">?</span>
<label for="add_estimate__estimate__distance_amount" >Distance:</label>
<span id="add_estimate__estimate__distance_amount" >?</span>
<label for="add_estimate__estimate__fee_amount">Fees:</label>
<span id="add_estimate__estimate__fee_amount">?</span>
<label for="add_estimate__estimate__tax_amount" id="add_estimate__estimate__tax_summary_label"  class="bottom">Total&nbsp;Tax</label>
<span id="add_estimate__estimate__tax_amount">?</span></div></div><div class="cost"><div id="add_available_credit__available_credit__div"><label for="add_available_credit__available_credit_">AVAILABLE CREDIT:</label><span id="add_available_credit__available_credit_" class=""></span></div><div id="add_credit__balance__div"><label for="add_credit__balance_">APPLIED CREDIT:</label><span id="add_credit__balance_" class=""></span></div><div id="add_amount_due__amount_due__div"><label for="add_amount_due__amount_due_">AMOUNT DUE:</label><span id="add_amount_due__amount_due_" class="amount_due"></span><div class="instruction">NOTE: By clicking the "reserve it" button, your card will be billed the "amount due" shown above.</div></div></div><div id="add_timeline__error" class="slider error_display"></div><div id='optional_rate_plan_adjustment' style='text-align:left;'><font class='text'></font></div><button id="lb_cancel_button" class="cancel"></button><button id="lb_reserve_button" class="reserve"></button></div></form><br style="clear: both;" /></div></div><script language="javascript" type="text/javascript">MV.globals.reserve.lightbox = new MV.controls.reserve.lightbox({"range_params":{"start_control":{"date_id":"add_start_stamp__start_date_","time_id":"add_start_stamp__start_time_"},"end_control":{"date_id":"add_end_stamp__end_date_","time_id":"add_end_stamp__end_time_"}},"estimate_params":{"price_id":"add_price__price_","available_balance_id":"add_balance__balance_","amount_due_id":"add_amount_due__amount_due_","credit_id":"add_credit__balance_","credit_box_id":"add_credit__balance__div","available_credit_box_id":"add_available_credit__available_credit__div","available_credit_id":"add_available_credit__available_credit_","cost_params":{"id":"add_estimate__estimate_","time_id":"add_estimate__estimate__time_amount","distance_id":"add_estimate__estimate__distance_amount","fees_id":"add_estimate__estimate__fee_amount","tax_id":"add_estimate__estimate__tax_amount","tax_pks":[],"labels":{"please_wait":"Please wait...","hourly":"Hourly","daily":"Daily"}},"hide_ab_shortfall":false},"accept_button_id":"lb_reserve_button","cancel_button_id":"lb_cancel_button","instruction_id":"lightbox_instruction","form_id":"add","attach_close_event":true,"attach_confirm_event":true,"use_dynamic_timeline":true,"initial_update":true,"preserve_instruction":true,"is_lightbox":true,"disabled_class":"reserve_disabled","slider_params":{"action":"add","stack_pk":null,"reservation_pk":0,"start_stamp":null,"start_stamp_min":1288506600,"start_stamp_max":1296450000,"end_stamp":null,"end_stamp_min":1288506600,"end_stamp_max":1296450000,"start_date_control":"add_start_stamp__start_date_","start_time_control":"add_start_stamp__start_time_","end_date_control":"add_end_stamp__end_date_","end_time_control":"add_end_stamp__end_time_","lower":null,"upper":null,"increment":900,"date_calibration":"10\/31\/10","control_ids":{"track_id":"reservation_bar_track","start_handle_id":"reservation_bar_start_handle","end_handle_id":"reservation_bar_end_handle","res_marker_id":"reservation_bar","error_id":"add_timeline__error"},"no_slider":true,"error_label":"Please adjust your times to an available period. Use the form above or click-and-drag your times."}});</script>'''

EXTEND_RESERVATION_INVALID_REQUEST_BLOCK=r'''Resulting reservation confirmation document has no "script" tag: <div class="midbox"><h3>Notice</h3><p class="note"><img src="/skin/img/exclamation.gif" /><label for="notice_notice_0_" id="notice_notice_0__label">Error:</label><span id="notice_notice_0_">The requested page is no longer available.</span><span class="instruction">&nbsp;</span></p></div>'''

CANCELLED_RESERVATION_CONFIRMATION=r'''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"><html xmlns="http://www.w3.org/1999/xhtml"><head>
<meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1" />
<meta http-equiv="pragma" content="no-cache" />
<meta http-equiv="cache-control" content="no-cache" />
<title >Reservation Manager</title><link rel="stylesheet" type="text/css" href="/skin/pcs_ui.css_3_47_0_10" title="pcs_skin" media="screen, print" /><link rel="stylesheet" type="text/css" href="/skin/pcs_layout.css_3_47_0_10" title="pcs_skin" media="screen, print" /><link rel="stylesheet" type="text/css" href="/skin/pcs_buttons.css_3_47_0_10" title="pcs_skin" media="screen, print" /><link rel="stylesheet" type="text/css" href="/skin/pcs_skin.css_3_47_0_10" title="pcs_skin" media="screen, print" /><link rel="stylesheet" type="text/css" href="/js/calendar.css_3_47_0_10" media="screen, print" /><script language="javascript" type="text/javascript">
        function start_gmap(){
            this.js_gmap = new MVgmap('google_map');
            js_gmap.fav_lots = [];
            js_gmap.marker_event = 'click';

            js_gmap.icon_def = new GIcon(G_DEFAULT_ICON, '/images/client_images/gmarker_def.png');
            js_gmap.icon_def.iconSize = new GSize(15, 26);
            js_gmap.icon_def.iconAnchor = new GPoint(8, 26);
            js_gmap.icon_def.shadowSize = new GSize(15, 26);

            js_gmap.icon_fav = new GIcon(G_DEFAULT_ICON, '/images/client_images/gmarker_fav.png');
            js_gmap.icon_fav.iconSize = new GSize(15, 26);
            js_gmap.icon_fav.iconAnchor = new GPoint(8, 26);
            js_gmap.icon_fav.shadowSize = new GSize(15, 26);

            js_gmap.load(39.948429, -75.218014, 16);
            js_gmap.addMarkers([[39.948429,-75.218014,'47th & Baltimore',[],0]]);
        
            js_gmap.map.disableDragging();
            js_gmap.map.disableDoubleClickZoom();
        }
</script>
<script language="javascript" type="text/javascript">function unload_gmap() {
                            js_gmap.unload();
                          }
</script>
</head>
<body bgcolor="white" onload="start_gmap(); " onunload="unload_gmap(); "><script language="javascript" type="text/javascript" src="/js/helper.js_3_47_0_10"></script>
<script language="javascript" type="text/javascript" src="/js/popup.js_3_47_0_10"></script>
<script language="javascript" type="text/javascript" src="/js/browser.js_3_47_0_10"></script>
<script language="javascript" type="text/javascript" src="/js/calendar.js_3_47_0_10"></script>
<script language="javascript" type="text/javascript" src="/js/calendarDateInput.js_3_47_0_10"></script>
<script language="javascript" type="text/javascript" src="/js/prototype.js_3_47_0_10"></script>
<script language="javascript" type="text/javascript" src="/js/lowpro.js_3_47_0_10"></script>
<script language="javascript" type="text/javascript" src="/js/mf_lightbox.js_3_47_0_10"></script>
<script language="javascript" type="text/javascript" src="/js/mv_base.js_3_47_0_10"></script>
<script language="javascript" type="text/javascript" src="/js/mv_location.js_3_47_0_10"></script>
<script language="javascript" type="text/javascript" src="http://maps.google.com/maps?file=api&amp;v=2&amp;key=ABQIAAAANNQNgPHY7hmfMuDnzGRL8xRCiyh3L1O9lXHVi81tmDjTTZCYKBSsT-tdn3x62eoISpd9Z2wIbqPixQ"></script>
<script language="javascript" type="text/javascript" src="/js/xmlhttp.js_3_47_0_10"></script>
<script language="javascript" type="text/javascript" src="/js/gmap.js_3_47_0_10"></script>
<script language="javascript" type="text/javascript" src="/js/slider.js_3_47_0_10"></script>
<script language="javascript" type="text/javascript" src="/js/lightbox.js_3_47_0_10"></script>
<script language="javascript" type="text/javascript" src="/js/mv_reserve.js_3_47_0_10"></script>
<div class="mv_header">
<img border="0" src="/images/client_images/pcs_web_logo.gif" alt="PhillyCarShare" title="PhillyCarShare" />
</div>
<div id="wrapper"><div id="page_header"><div id="lame_image"><span class="switch">
<a class="text" href="/members/help.html?_r=31"  target="_blank"  >Help</a></span>
<p >Mjumbe Poe, you are signed in. (Residential Account)</p><a href="my_reservations.php?_r=31&mv_action=logout">
                            <img class="logbutton" alt = "Log Out" src="/skin/base_images/btn_logout.gif" />
                   </a></div><img id="logo" src="/images/client_images/pcs_web_logo.gif" alt="PhillyCarShare" title="PhillyCarShare" />
        <div id="nav_bar">
        <div id="navcontainer">
        <ul id="navlist"><li ><a class="text link_new_reservation" href="my_reservations.php?_r=31"    >New Reservation</a></li><li ><a class="link_my_reservations" href="my_reservations.php?mv_action=main&_r=31"    >My Reservations</a></li><li ><a class="text link_my_messages" href="my_messages.php?_r=31"    >My Messages</a></li><li ><a class="text link_my_info" href="my_info.php?_r=31"    >My Account</a></li><li ><a class="text link_my_problems" href="my_problems.php?_r=31"    >Member Feedback</a></li></ul></div></div></div><div class="midbox"><h3 >CANCELLED Reservation Confirmation</h3><h5 class="confirm_title"><img src="/skin/img/information.gif"/>Please <a class="largeo" href="javascript://" onclick="window.print(); return(false);">Print</a> or copy the following confirmation details. Please always have these details with you for reference.</h5><div id="left"><h4 >Your cancelled reservation details are:  </h4><table class="mi"><tr ><td align="right">Member&nbsp;Name</td><td align="left">Mjumbe Poe</td></tr><tr ><td align="right">Member&nbsp;ID:</td><td align="left">6489</td></tr><tr ><td width="23%"    align="right" valign="middle"  >
<font class="text">Stack:</font>
</td>
<td  colspan="2" width="80%"  align="left" valign="middle"  ><a class="text" href="my_fleet.php?mv_action=stack_detail&_r=31&pk=30005&stack_pk=96692246"    >47th & Baltimore - Prius Liftback</a></td>
</tr><tr ><tr ><td width=25% colspan=1   align="right" valign="middle"  >
<font class="text">Start:</font>
</td>
<td colspan="2" width="80%" colspan=1   align="left" valign="middle"  >
<font class="text">3:45 am Wednesday, November 3, 2010</font>
</td>

<script language="javascript" type="text/javascript">
 new_date_control('confirm[start_stamp][date]', 'Show_Date', 20101031, 20110131, 20101031, 'm/d/y');</script>
</tr><tr ><td width=25% colspan=1   align="right" valign="middle"  >
<font class="text">End:</font>
</td>
<td colspan="2" width="80%" colspan=1   align="left" valign="middle"  >
<font class="text">4:00 am Wednesday, November 3, 2010</font>
</td>

<script language="javascript" type="text/javascript">
 new_date_control('confirm[end_stamp][date]', 'Show_Date', 20101031, 20110131, 20101031, 'm/d/y');</script>
</tr><tr ><td width="25%"    align="right" valign="middle"  >
<font class="text">Duration:</font>
</td>
<td colspan="2" width="75%"    align="left" valign="middle"  >
<font class="text">0.25&nbsp;hour(s)</font>
</td>
</tr></tr><tr ><td width=20%    align="right" valign="middle"  >
<font class="text">Memo:</font>
</td>
<td colspan="2" width="75%"    align="left" valign="middle"  >
<font class="text">reservation modify test</font>
</td>
</tr><tr ><td ><label for="confirm_id_" id="confirm_id__label">Reservation&nbsp;ID:</label></td><td ><span id="confirm_id_">2517617</span></td><td ><span class="instruction">&nbsp;</span></td></tr></table><br  /><h4 >POD Information:</h4><div id="lot_descr"><p ><span id="stack_pk">47th & Baltimore - Prius Liftback</span><span class="instruction">&nbsp;</span></p><p ><span id="location_descr"><b>4720 Baltimore Avenue</b><br>Philadelphia Parking Authority lot<br><br>Vehicles are parked in this open PPA lot on the south side of Baltimore Avenue, mid-block between 47th & 48th Streets, and are parked in reserved spaces on the north side of the lot, adjacent to Baltimore Avenue.<br><br />
<br />
If you are picking up a vehicle and cannot locate it in one of the reserved spaces, please check around the rest of the lot before calling the emergency line.<br><br />
<br><br />
<b>SEPTA access:</b> via the Route 34 trolley or the Route 64 bus.<br />
<br><br />
<br />
</span><span class="instruction">&nbsp;</span></p></div></div><div id="right"><div id="small_map"><td align="center" colspan="2"><script src='http://maps.google.com/maps?file=api&amp;v=2&amp;key=ABQIAAAANNQNgPHY7hmfMuDnzGRL8xRCiyh3L1O9lXHVi81tmDjTTZCYKBSsT-tdn3x62eoISpd9Z2wIbqPixQ' type='text/javascript'></script><div id="google_map" style="width: 300px; height: 300px; border: solid 1px; border-color:#00ad87;"></div></td></div><div class="buttons_box"><div style="color: #f50c0c; font-weight: bold;">Consider padding your time. <br>Returning after your reservation End Time will cost you $40 per half hour.</div><tr ><td ><table class="dlist ma" id="change_actions"><thead ><tr ></tr></thead><tbody ><tr class="zebra"></tr></tbody></table></td></tr><table ><tr ><td    align="left" valign="middle"  ><form id="print" name="print" action="my_reservations.php" method="post"  >
<table  width="100%"   border="0" cellspacing="0" cellpadding="0">
<tr ><td>&nbsp;</td>
<td    align="left" valign="middle"  ><input type="hidden" name="mv_action" value="print"/>
<input type="hidden" name="_r" value="31"/>
<button  id="print" type="submit" class="button button_print" onclick="window.print(); return(false);">Print this Confirmation</button>
</td>
<td></td></tr>
</table></form></td>
</tr></table><table ><tr ><td    align="left" valign="middle"  ><form id="outlook" name="outlook" action="outlook.php" method="GET"  >
<table  width="100%"   border="0" cellspacing="0" cellpadding="0">
<tr ><td>&nbsp;</td>
<td    align="left" valign="middle"  ><input type="hidden" name="mv_action" value="outlook"/>
<input type="hidden" name="_r" value="31"/>
<input type="hidden" name="pk" value="149396505"/>
<button  id="outlook" type="submit" class="button button_outlook" >Save to Outlook</button>
</td>
<td></td></tr>
</table></form></td>
</tr></table><table ><tr ><td    align="left" valign="middle"  ><form id="email" name="email" action="confirmation.php" method="post"  >
<table  width="100%"   border="0" cellspacing="0" cellpadding="0">
<tr ><td>&nbsp;</td>
<td    align="left" valign="middle"  ><table><tr><td><input type="hidden" name="mv_action" value="email"/>
<input type="hidden" name="_r" value="31"/>
<input type="hidden" name="pk" value="149396505"/>
<button  id="email" type="submit" class="button_disabled" onclick="return(false);">Confirmation Email Sent</button>
</td></tr><tr><td     align="center" valign="middle"  ><a class="text" href="my_info.php?mv_action=dpref&_r=31&pk=6285517"    >Edit&nbsp;Email&nbsp;Preferences</a></td>
</tr></table></td>
<td></td></tr>
</table></form></td>
</tr></table></div><div class="costs"><h4 >Prius Liftback</h4><img src="/images/client_images/toyota_prius_lift.jpg" /><br  /><div class="price"><p >$2.50 Hourly / $49.00 Daily</p></div><ul ><li ><img src="/skin/base_images/hybrid.gif" label="Hybrid" title="Hybrid" /><span style="padding-left: 0.5em;">Hybrid</span></li><li ><img src="/skin/base_images/folding_seat.gif" label="Folding Rear Seats" title="Folding Rear Seats" /><span style="padding-left: 0.5em;">Folding Rear Seats</span></li></ul></div></div><br style="clear: both;"><h5 class="confirm_title"><img src="/skin/img/information.gif"/>For easy reference to our online handbook, click <a href="http://www.phillycarshare.org/sites/default/files/member-handbook.pdf" target="_blank">here</a>.</h5><p class="note"><img src="/skin/img/exclamation.gif" />For time-sensitive matters during your reservation, please call the 24-hour emergency line at 215.730.0988 x1.</p></div><br style="clear: both" /><div id="mv_powered"><div id="mv_powered_left"><a href="http://www.metavera.com"><img src="/skin/base_images/mv_logo_small.gif" alt="Powered by Metavera"/></a></div><div id="mv_powered_right"><a href="http://www.metavera.com"><span>Powered by Metavera</span><br/>CarSharing Technology Leader</a></div></div></div></body></html>'''

EXPIRED_PASSWORD_LOGIN_FORM=r'''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"><html xmlns="http://www.w3.org/1999/xhtml"><head>\n<meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1" />\n<meta http-equiv="pragma" content="no-cache" />\n<meta http-equiv="cache-control" content="no-cache" />\n<title >Please Login</title><link rel="stylesheet" type="text/css" href="/skin/pcs_ui.css_3_48_0_0" title="pcs_skin" media="screen, print" /><link rel="stylesheet" type="text/css" href="/skin/pcs_layout.css_3_48_0_0" title="pcs_skin" media="screen, print" /><link rel="stylesheet" type="text/css" href="/skin/pcs_buttons.css_3_48_0_0" title="pcs_skin" media="screen, print" /><link rel="stylesheet" type="text/css" href="/skin/pcs_skin.css_3_48_0_0" title="pcs_skin" media="screen, print" /><script language="javascript" type="text/javascript">\n        function init_focus() {\n            set_focus(document.login, \'login[name]\');\n        }\n</script>\n</head>\n<body bgcolor="white" onload="init_focus(); " ><script language="javascript" type="text/javascript" src="/js/focus.js_3_48_0_0"></script>\n<script language="javascript" type="text/javascript" src="/js/prototype.js_3_48_0_0"></script>\n<script language="javascript" type="text/javascript" src="/js/lowpro.js_3_48_0_0"></script>\n<script language="javascript" type="text/javascript" src="/js/slider.js_3_48_0_0"></script>\n<script language="javascript" type="text/javascript" src="/js/lightbox.js_3_48_0_0"></script>\n<script language="javascript" type="text/javascript" src="/js/mf_lightbox.js_3_48_0_0"></script>\n<script language="javascript" type="text/javascript" src="/js/mv_base.js_3_48_0_0"></script>\n<script language="javascript" type="text/javascript" src="/js/mv_reserve.js_3_48_0_0"></script>\n<div class="mv_header">\n<img border="0" src="/images/client_images/pcs_web_logo.gif" alt="PhillyCarShare" title="PhillyCarShare" />\n</div>\n<div id="wrapper"><div id="page_header"><div id="lame_image"></div><img id="logo" src="/images/client_images/pcs_web_logo.gif" alt="PhillyCarShare" title="PhillyCarShare" />\n        <div id="nav_bar">\n        <div id="navcontainer">\n        </div></div></div><div class="midbox"><h3 >Login</h3><h5 >Welcome to PhillyCarShare Online!</h5><h4 >Please&nbsp;sign&nbsp;in&nbsp;below:</h4><div id="login_box"><table ><tr ><td ><form id="login" name="login" action="index.php" method="post"  autocomplete="off"><table width="100%"><tr ><td ><label for="login_name_" id="login_name__label">Member ID:</label></td><td ><input  id="login_name_" tabindex="0" class = "entry" maxlength="15"  size="15" name="login[name]" value=""  /><span class="mandatory">&nbsp;*</span></td><td ><span class="instruction">&nbsp;</span></td></tr><tr ><td ><label for="login_password_" id="login_password__label">Password:</label></td><td ><input  id="login_password_" tabindex="0" class = "entry" maxlength="50" type="Password" size="15" name="login[password]" value=""  /><span class="mandatory">&nbsp;*</span></td><td ><span class="instruction">&nbsp;</span></td></tr><tr ><td >&nbsp;</td><td ><table ><tr ><td    align="left" valign="middle"  ><input type="hidden" name="mv_action" value="login"/>\n<input type="hidden" name="_r" value="2"/>\n<button  id="login" type="submit" class="button imageButton_save" ></button>\n</td>\n<td ><input id="login_tid_" type="hidden" name="login[tid]" value="2" /></td></tr></table></td></tr></table></form></td></tr></table></div><br  /><p class="note"><img src="/skin/img/exclamation.gif" style="" /><span style=""><font class="text">I forgot my password. Please <a href="index.php?mv_action=password&_r=2">email my password</a> to me</font></span></p></div><br style="clear: both" /><div id="mv_powered"><div id="mv_powered_left"><a href="http://www.metavera.com"><img src="/skin/base_images/mv_logo_small.gif" alt="Powered by Metavera"/></a></div><div id="mv_powered_right"><a href="http://www.metavera.com"><span>Powered by Metavera</span><br/>CarSharing Technology Leader</a></div></div></div></body></html>'''

VEHICLE_AVAIL_FOR_NEW_RESERVATION=r'''<div class="lightbox" id="fakeLightbox"><h3 >Your Reservation</h3><div class="lightbox_contents"><p id="lightbox_instruction" class="error"></p><form class="reservation" id="add" name="add" method="post" action="lightbox.php"><div class="left_panel"><fieldset class="stack_fieldset"><input type="hidden" name="add[stack_pk]" value="96692246" /><table ><tr ><td ><label for="add_stack_pk__location">Location:</label></td><td ><span id="add_stack_pk__location">47th & Baltimore</span></td></tr><tr ><td ><label for="add_stack_pk_vt">Vehicle Type:</label></td><td ><span id="add_stack_pk_vt">Prius Liftback</span></td></tr></table></fieldset><fieldset class="range_fieldset"><table ><tr ><td ><label for="add_start_stamp__start_date_">Start:</label></td><td class="stamp_control"><input id="add_start_stamp__start_date_" name="add[start_stamp][start_date][date]" class="date_control" onchange="" value="11/03/10" />    <script language="javascript" type="text/javascript">
        DateInput('add_start_stamp__start_date__calendar', 'add_start_stamp__start_date_', true, '1288757701', 'm/d/y', null, null);
    </script><select id="add_start_stamp__start_time_" name="add[start_stamp][start_time][time]" class="time_control"><option value="0">Midnight</option><option value="900" selected="selected">12:15 AM</option><option value="1800">12:30 AM</option><option value="2700">12:45 AM</option><option value="3600">01:00 AM</option><option value="4500">01:15 AM</option><option value="5400">01:30 AM</option><option value="6300">01:45 AM</option><option value="7200">02:00 AM</option><option value="8100">02:15 AM</option><option value="9000">02:30 AM</option><option value="9900">02:45 AM</option><option value="10800">03:00 AM</option><option value="11700">03:15 AM</option><option value="12600">03:30 AM</option><option value="13500">03:45 AM</option><option value="14400">04:00 AM</option><option value="15300">04:15 AM</option><option value="16200">04:30 AM</option><option value="17100">04:45 AM</option><option value="18000">05:00 AM</option><option value="18900">05:15 AM</option><option value="19800">05:30 AM</option><option value="20700">05:45 AM</option><option value="21600">06:00 AM</option><option value="22500">06:15 AM</option><option value="23400">06:30 AM</option><option value="24300">06:45 AM</option><option value="25200">07:00 AM</option><option value="26100">07:15 AM</option><option value="27000">07:30 AM</option><option value="27900">07:45 AM</option><option value="28800">08:00 AM</option><option value="29700">08:15 AM</option><option value="30600">08:30 AM</option><option value="31500">08:45 AM</option><option value="32400">09:00 AM</option><option value="33300">09:15 AM</option><option value="34200">09:30 AM</option><option value="35100">09:45 AM</option><option value="36000">10:00 AM</option><option value="36900">10:15 AM</option><option value="37800">10:30 AM</option><option value="38700">10:45 AM</option><option value="39600">11:00 AM</option><option value="40500">11:15 AM</option><option value="41400">11:30 AM</option><option value="42300">11:45 AM</option><option value="-1"></option><option value="43200">Noon</option><option value="44100">12:15 PM</option><option value="45000">12:30 PM</option><option value="45900">12:45 PM</option><option value="46800">01:00 PM</option><option value="47700">01:15 PM</option><option value="48600">01:30 PM</option><option value="49500">01:45 PM</option><option value="50400">02:00 PM</option><option value="51300">02:15 PM</option><option value="52200">02:30 PM</option><option value="53100">02:45 PM</option><option value="54000">03:00 PM</option><option value="54900">03:15 PM</option><option value="55800">03:30 PM</option><option value="56700">03:45 PM</option><option value="57600">04:00 PM</option><option value="58500">04:15 PM</option><option value="59400">04:30 PM</option><option value="60300">04:45 PM</option><option value="61200">05:00 PM</option><option value="62100">05:15 PM</option><option value="63000">05:30 PM</option><option value="63900">05:45 PM</option><option value="64800">06:00 PM</option><option value="65700">06:15 PM</option><option value="66600">06:30 PM</option><option value="67500">06:45 PM</option><option value="68400">07:00 PM</option><option value="69300">07:15 PM</option><option value="70200">07:30 PM</option><option value="71100">07:45 PM</option><option value="72000">08:00 PM</option><option value="72900">08:15 PM</option><option value="73800">08:30 PM</option><option value="74700">08:45 PM</option><option value="75600">09:00 PM</option><option value="76500">09:15 PM</option><option value="77400">09:30 PM</option><option value="78300">09:45 PM</option><option value="79200">10:00 PM</option><option value="80100">10:15 PM</option><option value="81000">10:30 PM</option><option value="81900">10:45 PM</option><option value="82800">11:00 PM</option><option value="83700">11:15 PM</option><option value="84600">11:30 PM</option><option value="85500">11:45 PM</option></select></td></tr><tr ><td ><label for="add_end_stamp__end_date_">End:</label></td><td class="stamp_control"><input id="add_end_stamp__end_date_" name="add[end_stamp][end_date][date]" class="date_control" onchange="" value="11/03/10" />    <script language="javascript" type="text/javascript">
        DateInput('add_end_stamp__end_date__calendar', 'add_end_stamp__end_date_', true, '1288757701', 'm/d/y', null, null);
    </script><select id="add_end_stamp__end_time_" name="add[end_stamp][end_time][time]" class="time_control"><option value="0">Midnight</option><option value="900">12:15 AM</option><option value="1800">12:30 AM</option><option value="2700">12:45 AM</option><option value="3600">01:00 AM</option><option value="4500">01:15 AM</option><option value="5400">01:30 AM</option><option value="6300">01:45 AM</option><option value="7200">02:00 AM</option><option value="8100">02:15 AM</option><option value="9000">02:30 AM</option><option value="9900">02:45 AM</option><option value="10800">03:00 AM</option><option value="11700" selected="selected">03:15 AM</option><option value="12600">03:30 AM</option><option value="13500">03:45 AM</option><option value="14400">04:00 AM</option><option value="15300">04:15 AM</option><option value="16200">04:30 AM</option><option value="17100">04:45 AM</option><option value="18000">05:00 AM</option><option value="18900">05:15 AM</option><option value="19800">05:30 AM</option><option value="20700">05:45 AM</option><option value="21600">06:00 AM</option><option value="22500">06:15 AM</option><option value="23400">06:30 AM</option><option value="24300">06:45 AM</option><option value="25200">07:00 AM</option><option value="26100">07:15 AM</option><option value="27000">07:30 AM</option><option value="27900">07:45 AM</option><option value="28800">08:00 AM</option><option value="29700">08:15 AM</option><option value="30600">08:30 AM</option><option value="31500">08:45 AM</option><option value="32400">09:00 AM</option><option value="33300">09:15 AM</option><option value="34200">09:30 AM</option><option value="35100">09:45 AM</option><option value="36000">10:00 AM</option><option value="36900">10:15 AM</option><option value="37800">10:30 AM</option><option value="38700">10:45 AM</option><option value="39600">11:00 AM</option><option value="40500">11:15 AM</option><option value="41400">11:30 AM</option><option value="42300">11:45 AM</option><option value="-1"></option><option value="43200">Noon</option><option value="44100">12:15 PM</option><option value="45000">12:30 PM</option><option value="45900">12:45 PM</option><option value="46800">01:00 PM</option><option value="47700">01:15 PM</option><option value="48600">01:30 PM</option><option value="49500">01:45 PM</option><option value="50400">02:00 PM</option><option value="51300">02:15 PM</option><option value="52200">02:30 PM</option><option value="53100">02:45 PM</option><option value="54000">03:00 PM</option><option value="54900">03:15 PM</option><option value="55800">03:30 PM</option><option value="56700">03:45 PM</option><option value="57600">04:00 PM</option><option value="58500">04:15 PM</option><option value="59400">04:30 PM</option><option value="60300">04:45 PM</option><option value="61200">05:00 PM</option><option value="62100">05:15 PM</option><option value="63000">05:30 PM</option><option value="63900">05:45 PM</option><option value="64800">06:00 PM</option><option value="65700">06:15 PM</option><option value="66600">06:30 PM</option><option value="67500">06:45 PM</option><option value="68400">07:00 PM</option><option value="69300">07:15 PM</option><option value="70200">07:30 PM</option><option value="71100">07:45 PM</option><option value="72000">08:00 PM</option><option value="72900">08:15 PM</option><option value="73800">08:30 PM</option><option value="74700">08:45 PM</option><option value="75600">09:00 PM</option><option value="76500">09:15 PM</option><option value="77400">09:30 PM</option><option value="78300">09:45 PM</option><option value="79200">10:00 PM</option><option value="80100">10:15 PM</option><option value="81000">10:30 PM</option><option value="81900">10:45 PM</option><option value="82800">11:00 PM</option><option value="83700">11:15 PM</option><option value="84600">11:30 PM</option><option value="85500">11:45 PM</option></select></td></tr><tr ><td ><label for="add_job_code_">Memo:</label></td><td ><input id="add_job_code_" name="add[job_code]" type="text" size="25" maxlength="25" value="" onkeypress="
            var keyCode = event.keyCode ? event.keyCode : event.which ? event.which : event.charCode;
                if (keyCode == 13) {
                    return false;
                }
                return true;
        " class="memo_control" /></td></tr><tr ><td colspan="2" style="color: #f50c0c; font-size: 11px; font-weight: bold;">Consider padding your time. Returning after your reservation End Time will cost you $40 per half hour.</td></tr></table><input id="add_tid_" type="hidden" name="add[tid]" value="8"/>
<input type="hidden" name="mv_action" value="add" /><input type="hidden" name="_r" value="25" /></fieldset></div><div class="right_panel"><img class="vehicle" src="/images/client_images/toyota_prius_lift.jpg" alt="Prius Liftback" /><div class="price"><div id="add_price__price_" class="container">$??.00 hourly / $??.00 daily</div></div><ul class="amenity"><li ></li></ul></div><div class="bottom_panel"><div class="cost"><div id="add_balance__balance__div"><label for="add_balance__balance_">AVAILABLE BALANCE:</label><span id="add_balance__balance_" class=""></span></div></div><div class="cost"><label for="add_estimate__estimate_">ESTIMATED COST:</label><span id="add_estimate__estimate_" class="">?</span><div class="price_box"> <label for="add_estimate__estimate__time_amount" class="top">Time:</label>
<span id="add_estimate__estimate__time_amount">?</span>
<label for="add_estimate__estimate__distance_amount" >Distance:</label>
<span id="add_estimate__estimate__distance_amount" >?</span>
<label for="add_estimate__estimate__fee_amount">Fees:</label>
<span id="add_estimate__estimate__fee_amount">?</span>
<label for="add_estimate__estimate__tax_amount" id="add_estimate__estimate__tax_summary_label"  class="bottom">Total&nbsp;Tax</label>
<span id="add_estimate__estimate__tax_amount">?</span></div></div><div class="cost"><div id="add_available_credit__available_credit__div"><label for="add_available_credit__available_credit_">AVAILABLE CREDIT:</label><span id="add_available_credit__available_credit_" class=""></span></div><div id="add_credit__balance__div"><label for="add_credit__balance_">APPLIED CREDIT:</label><span id="add_credit__balance_" class=""></span></div><div id="add_amount_due__amount_due__div"><label for="add_amount_due__amount_due_">AMOUNT DUE:</label><span id="add_amount_due__amount_due_" class="amount_due"></span><div class="instruction">NOTE: By clicking the "reserve it" button, your card will be billed the "amount due" shown above.</div></div></div><div id="add_timeline___track" class="timeline slider"><div class="slider reservation good_reservation" id="reservation_bar"></div><div class="slider handle start" id="reservation_bar_start_handle"></div><div class="slider handle end" id="reservation_bar_end_handle"></div><ul class="segments" id="reservation_bar_track"><li ><ul ><li class="bad pad_end"></li><li class="bad"></li><li class="bad"></li><li class="bad pad_end"></li></ul></li><li ><ul ><li class="bad pad_end"></li><li class="bad"></li><li class="bad"></li><li class="bad pad_end"></li></ul></li><li ><ul ><li class="bad pad_end"></li><li class="bad"></li><li class="bad"></li><li class="bad pad_end"></li></ul></li><li ><ul ><li class="bad pad_end"></li><li class="bad"></li><li class="bad"></li><li class="bad pad_end"></li></ul></li><li ><ul ><li class="bad pad_end"></li><li class="bad"></li><li class="bad"></li><li class="bad pad_end"></li></ul></li><li ><ul ><li class="bad pad_end"></li><li class="bad"></li><li class="bad"></li><li class="bad pad_end"></li></ul></li><li ><ul ><li class="bad pad_end"></li><li class="bad"></li><li class="bad"></li><li class="bad pad_end"></li></ul></li><li ><ul ><li class="bad pad_end"></li><li class="bad"></li><li class="bad"></li><li class="bad pad_end"></li></ul></li><li ><ul ><li class="bad pad_end"></li><li class="bad"></li><li class="bad"></li><li class="bad pad_end"></li></ul></li><li ><ul ><li class="bad pad_end"></li><li class="bad"></li><li class="bad"></li><li class="bad pad_end"></li></ul></li><li ><ul ><li class="bad pad_end"></li><li class="bad"></li><li class="bad"></li><li class="bad pad_end"></li></ul></li><li ><ul ><li class="bad pad_end"></li><li class="bad"></li><li class="bad"></li><li class="bad pad_end"></li></ul></li><li ><ul ><li class="bad pad_end"></li><li class="bad"></li><li class="bad"></li><li class="bad pad_end"></li></ul></li><li ><ul ><li class="bad pad_end"></li><li class="bad"></li><li class="bad"></li><li class="bad pad_end"></li></ul></li><li ><ul ><li class="bad pad_end"></li><li class="bad"></li><li class="bad"></li><li class="bad pad_end"></li></ul></li><li ><ul ><li class="bad pad_end"></li><li class="bad"></li><li class="bad"></li><li class="bad pad_end"></li></ul></li><li ><ul ><li class="bad pad_end"></li><li class="bad"></li><li class="bad"></li><li class="bad pad_end"></li></ul></li><li ><ul ><li class="bad pad_end"></li><li class="bad"></li><li class="bad"></li><li class="bad pad_end"></li></ul></li><li ><ul ><li class="bad pad_end"></li><li class="good"></li><li class="good"></li><li class="good pad_end"></li></ul></li><li ><ul ><li class="good pad_end"></li><li class="good"></li><li class="good"></li><li class="good pad_end"></li></ul></li><li ><ul ><li class="good pad_end"></li><li class="good"></li><li class="good"></li><li class="good pad_end"></li></ul></li><li ><ul ><li class="good pad_end"></li><li class="free"></li><li class="free"></li><li class="free pad_end"></li></ul></li><li class="free_16px"></li><li class="free_16px"></li></ul><img src="/skin/base_images//day_gauge.gif" /></div><div id="add_timeline__error" class="slider error_display"></div><div id='optional_rate_plan_adjustment' style='text-align:left;'><font class='text'></font></div><button id="lb_cancel_button" class="cancel"></button><button id="lb_reserve_button" class="reserve"></button></div></form><br style="clear: both;" /></div></div><script language="javascript" type="text/javascript">MV.globals.reserve.lightbox = new MV.controls.reserve.lightbox({"range_params":{"start_control":{"date_id":"add_start_stamp__start_date_","time_id":"add_start_stamp__start_time_"},"end_control":{"date_id":"add_end_stamp__end_date_","time_id":"add_end_stamp__end_time_"}},"estimate_params":{"price_id":"add_price__price_","available_balance_id":"add_balance__balance_","amount_due_id":"add_amount_due__amount_due_","credit_id":"add_credit__balance_","credit_box_id":"add_credit__balance__div","available_credit_box_id":"add_available_credit__available_credit__div","available_credit_id":"add_available_credit__available_credit_","cost_params":{"id":"add_estimate__estimate_","time_id":"add_estimate__estimate__time_amount","distance_id":"add_estimate__estimate__distance_amount","fees_id":"add_estimate__estimate__fee_amount","tax_id":"add_estimate__estimate__tax_amount","tax_pks":[],"labels":{"please_wait":"Please wait...","hourly":"Hourly","daily":"Daily"}},"hide_ab_shortfall":false},"accept_button_id":"lb_reserve_button","cancel_button_id":"lb_cancel_button","instruction_id":"lightbox_instruction","form_id":"add","attach_close_event":true,"attach_confirm_event":true,"use_dynamic_timeline":true,"initial_update":true,"preserve_instruction":true,"is_lightbox":true,"disabled_class":"reserve_disabled","slider_params":{"action":"add","stack_pk":"96692246","reservation_pk":0,"start_stamp":"1288757700","start_stamp_min":1288756800,"start_stamp_max":1298869200,"end_stamp":"1288768500","end_stamp_min":1288756800,"end_stamp_max":1298869200,"start_date_control":"add_start_stamp__start_date_","start_time_control":"add_start_stamp__start_time_","end_date_control":"add_end_stamp__end_date_","end_time_control":"add_end_stamp__end_time_","lower":1288692000,"upper":1288778400,"increment":900,"date_calibration":"11\/02\/10","control_ids":{"track_id":"reservation_bar_track","start_handle_id":"reservation_bar_start_handle","end_handle_id":"reservation_bar_end_handle","res_marker_id":"reservation_bar","error_id":"add_timeline__error"},"no_slider":false,"error_label":"Please adjust your times to an available period. Use the form above or click-and-drag your times."}});</script>'''

RESERVATION_LIGHTBOX_WITH_CONFLICTING_TIME=r'''<div class="lightbox" id="fakeLightbox"><h3 >Your Reservation</h3><div class="lightbox_contents"><p id="lightbox_instruction" class="error">You can only make one reservation during a given time period.</p><form class="reservation" id="add" name="add" method="post" action="lightbox.php"><div class="left_panel"><fieldset class="stack_fieldset"><input type="hidden" name="add[stack_pk]" value="96692246" /><table ><tr ><td ><label for="add_stack_pk__location">Location:</label></td><td ><span id="add_stack_pk__location">47th & Baltimore</span></td></tr><tr ><td ><label for="add_stack_pk_vt">Vehicle Type:</label></td><td ><span id="add_stack_pk_vt">Prius Liftback</span></td></tr></table></fieldset><fieldset class="range_fieldset"><table ><tr ><td ><label for="add_start_stamp__start_date_">Start:</label></td><td class="stamp_control"><input id="add_start_stamp__start_date_" name="add[start_stamp][start_date][date]" class="date_control" onchange="" value="11/11/10" />    <script language="javascript" type="text/javascript">
        DateInput('add_start_stamp__start_date__calendar', 'add_start_stamp__start_date_', true, '1289258097', 'm/d/y', null, null);
    </script><select id="add_start_stamp__start_time_" name="add[start_stamp][start_time][time]" class="time_control"><option value="0">Midnight</option><option value="900">12:15 AM</option><option value="1800">12:30 AM</option><option value="2700">12:45 AM</option><option value="3600">01:00 AM</option><option value="4500">01:15 AM</option><option value="5400">01:30 AM</option><option value="6300">01:45 AM</option><option value="7200">02:00 AM</option><option value="8100">02:15 AM</option><option value="9000">02:30 AM</option><option value="9900">02:45 AM</option><option value="10800" selected="selected">03:00 AM</option><option value="11700">03:15 AM</option><option value="12600">03:30 AM</option><option value="13500">03:45 AM</option><option value="14400">04:00 AM</option><option value="15300">04:15 AM</option><option value="16200">04:30 AM</option><option value="17100">04:45 AM</option><option value="18000">05:00 AM</option><option value="18900">05:15 AM</option><option value="19800">05:30 AM</option><option value="20700">05:45 AM</option><option value="21600">06:00 AM</option><option value="22500">06:15 AM</option><option value="23400">06:30 AM</option><option value="24300">06:45 AM</option><option value="25200">07:00 AM</option><option value="26100">07:15 AM</option><option value="27000">07:30 AM</option><option value="27900">07:45 AM</option><option value="28800">08:00 AM</option><option value="29700">08:15 AM</option><option value="30600">08:30 AM</option><option value="31500">08:45 AM</option><option value="32400">09:00 AM</option><option value="33300">09:15 AM</option><option value="34200">09:30 AM</option><option value="35100">09:45 AM</option><option value="36000">10:00 AM</option><option value="36900">10:15 AM</option><option value="37800">10:30 AM</option><option value="38700">10:45 AM</option><option value="39600">11:00 AM</option><option value="40500">11:15 AM</option><option value="41400">11:30 AM</option><option value="42300">11:45 AM</option><option value="-1"></option><option value="43200">Noon</option><option value="44100">12:15 PM</option><option value="45000">12:30 PM</option><option value="45900">12:45 PM</option><option value="46800">01:00 PM</option><option value="47700">01:15 PM</option><option value="48600">01:30 PM</option><option value="49500">01:45 PM</option><option value="50400">02:00 PM</option><option value="51300">02:15 PM</option><option value="52200">02:30 PM</option><option value="53100">02:45 PM</option><option value="54000">03:00 PM</option><option value="54900">03:15 PM</option><option value="55800">03:30 PM</option><option value="56700">03:45 PM</option><option value="57600">04:00 PM</option><option value="58500">04:15 PM</option><option value="59400">04:30 PM</option><option value="60300">04:45 PM</option><option value="61200">05:00 PM</option><option value="62100">05:15 PM</option><option value="63000">05:30 PM</option><option value="63900">05:45 PM</option><option value="64800">06:00 PM</option><option value="65700">06:15 PM</option><option value="66600">06:30 PM</option><option value="67500">06:45 PM</option><option value="68400">07:00 PM</option><option value="69300">07:15 PM</option><option value="70200">07:30 PM</option><option value="71100">07:45 PM</option><option value="72000">08:00 PM</option><option value="72900">08:15 PM</option><option value="73800">08:30 PM</option><option value="74700">08:45 PM</option><option value="75600">09:00 PM</option><option value="76500">09:15 PM</option><option value="77400">09:30 PM</option><option value="78300">09:45 PM</option><option value="79200">10:00 PM</option><option value="80100">10:15 PM</option><option value="81000">10:30 PM</option><option value="81900">10:45 PM</option><option value="82800">11:00 PM</option><option value="83700">11:15 PM</option><option value="84600">11:30 PM</option><option value="85500">11:45 PM</option></select></td></tr><tr ><td ><label for="add_end_stamp__end_date_">End:</label></td><td class="stamp_control"><input id="add_end_stamp__end_date_" name="add[end_stamp][end_date][date]" class="date_control" onchange="" value="11/11/10" />    <script language="javascript" type="text/javascript">
        DateInput('add_end_stamp__end_date__calendar', 'add_end_stamp__end_date_', true, '1289258097', 'm/d/y', null, null);
    </script><select id="add_end_stamp__end_time_" name="add[end_stamp][end_time][time]" class="time_control"><option value="0">Midnight</option><option value="900">12:15 AM</option><option value="1800">12:30 AM</option><option value="2700">12:45 AM</option><option value="3600">01:00 AM</option><option value="4500">01:15 AM</option><option value="5400">01:30 AM</option><option value="6300">01:45 AM</option><option value="7200">02:00 AM</option><option value="8100">02:15 AM</option><option value="9000">02:30 AM</option><option value="9900">02:45 AM</option><option value="10800">03:00 AM</option><option value="11700" selected="selected">03:15 AM</option><option value="12600">03:30 AM</option><option value="13500">03:45 AM</option><option value="14400">04:00 AM</option><option value="15300">04:15 AM</option><option value="16200">04:30 AM</option><option value="17100">04:45 AM</option><option value="18000">05:00 AM</option><option value="18900">05:15 AM</option><option value="19800">05:30 AM</option><option value="20700">05:45 AM</option><option value="21600">06:00 AM</option><option value="22500">06:15 AM</option><option value="23400">06:30 AM</option><option value="24300">06:45 AM</option><option value="25200">07:00 AM</option><option value="26100">07:15 AM</option><option value="27000">07:30 AM</option><option value="27900">07:45 AM</option><option value="28800">08:00 AM</option><option value="29700">08:15 AM</option><option value="30600">08:30 AM</option><option value="31500">08:45 AM</option><option value="32400">09:00 AM</option><option value="33300">09:15 AM</option><option value="34200">09:30 AM</option><option value="35100">09:45 AM</option><option value="36000">10:00 AM</option><option value="36900">10:15 AM</option><option value="37800">10:30 AM</option><option value="38700">10:45 AM</option><option value="39600">11:00 AM</option><option value="40500">11:15 AM</option><option value="41400">11:30 AM</option><option value="42300">11:45 AM</option><option value="-1"></option><option value="43200">Noon</option><option value="44100">12:15 PM</option><option value="45000">12:30 PM</option><option value="45900">12:45 PM</option><option value="46800">01:00 PM</option><option value="47700">01:15 PM</option><option value="48600">01:30 PM</option><option value="49500">01:45 PM</option><option value="50400">02:00 PM</option><option value="51300">02:15 PM</option><option value="52200">02:30 PM</option><option value="53100">02:45 PM</option><option value="54000">03:00 PM</option><option value="54900">03:15 PM</option><option value="55800">03:30 PM</option><option value="56700">03:45 PM</option><option value="57600">04:00 PM</option><option value="58500">04:15 PM</option><option value="59400">04:30 PM</option><option value="60300">04:45 PM</option><option value="61200">05:00 PM</option><option value="62100">05:15 PM</option><option value="63000">05:30 PM</option><option value="63900">05:45 PM</option><option value="64800">06:00 PM</option><option value="65700">06:15 PM</option><option value="66600">06:30 PM</option><option value="67500">06:45 PM</option><option value="68400">07:00 PM</option><option value="69300">07:15 PM</option><option value="70200">07:30 PM</option><option value="71100">07:45 PM</option><option value="72000">08:00 PM</option><option value="72900">08:15 PM</option><option value="73800">08:30 PM</option><option value="74700">08:45 PM</option><option value="75600">09:00 PM</option><option value="76500">09:15 PM</option><option value="77400">09:30 PM</option><option value="78300">09:45 PM</option><option value="79200">10:00 PM</option><option value="80100">10:15 PM</option><option value="81000">10:30 PM</option><option value="81900">10:45 PM</option><option value="82800">11:00 PM</option><option value="83700">11:15 PM</option><option value="84600">11:30 PM</option><option value="85500">11:45 PM</option></select></td></tr><tr ><td ><label for="add_job_code_">Memo:</label></td><td ><input id="add_job_code_" name="add[job_code]" type="text" size="25" maxlength="25" value="new reservation" onkeypress="
            var keyCode = event.keyCode ? event.keyCode : event.which ? event.which : event.charCode;
                if (keyCode == 13) {
                    return false;
                }
                return true;
        " class="memo_control" /></td></tr><tr ><td colspan="2" style="color: #f50c0c; font-size: 11px; font-weight: bold;">Consider padding your time. Returning after your reservation End Time will cost you $40 per half hour.</td></tr></table><input id="add_tid_" type="hidden" name="add[tid]" value="4"/>
<input type="hidden" name="mv_action" value="add" /><input type="hidden" name="_r" value="6" /></fieldset></div><div class="right_panel"><img class="vehicle" src="/images/client_images/toyota_prius_lift.jpg" alt="Prius Liftback" /><div class="price"><div id="add_price__price_" class="container">$??.00 hourly / $??.00 daily</div></div><ul class="amenity"><li ></li></ul></div><div class="bottom_panel"><div class="cost"><div id="add_balance__balance__div"><label for="add_balance__balance_">AVAILABLE BALANCE:</label><span id="add_balance__balance_" class=""></span></div></div><div class="cost"><label for="add_estimate__estimate_">ESTIMATED COST:</label><span id="add_estimate__estimate_" class="">?</span><div class="price_box"> <label for="add_estimate__estimate__time_amount" class="top">Time:</label>
<span id="add_estimate__estimate__time_amount">?</span>
<label for="add_estimate__estimate__distance_amount" >Distance:</label>
<span id="add_estimate__estimate__distance_amount" >?</span>
<label for="add_estimate__estimate__fee_amount">Fees:</label>
<span id="add_estimate__estimate__fee_amount">?</span>
<label for="add_estimate__estimate__tax_amount" id="add_estimate__estimate__tax_summary_label"  class="bottom">Total&nbsp;Tax</label>
<span id="add_estimate__estimate__tax_amount">?</span></div></div><div class="cost"><div id="add_available_credit__available_credit__div"><label for="add_available_credit__available_credit_">AVAILABLE CREDIT:</label><span id="add_available_credit__available_credit_" class=""></span></div><div id="add_credit__balance__div"><label for="add_credit__balance_">APPLIED CREDIT:</label><span id="add_credit__balance_" class=""></span></div><div id="add_amount_due__amount_due__div"><label for="add_amount_due__amount_due_">AMOUNT DUE:</label><span id="add_amount_due__amount_due_" class="amount_due"></span><div class="instruction">NOTE: By clicking the "reserve it" button, your card will be billed the "amount due" shown above.</div></div></div><div id="add_timeline___track" class="timeline slider"><div class="slider reservation good_reservation" id="reservation_bar"></div><div class="slider handle start" id="reservation_bar_start_handle"></div><div class="slider handle end" id="reservation_bar_end_handle"></div><ul class="segments" id="reservation_bar_track"><li class="free_16px"></li><li class="free_16px"></li><li class="free_16px"></li><li class="free_16px"></li><li class="free_16px"></li><li class="free_16px"></li><li class="free_16px"></li><li class="free_16px"></li><li class="free_16px"></li><li class="free_16px"></li><li class="free_16px"></li><li class="free_16px"></li><li class="free_16px"></li><li class="free_16px"></li><li class="free_16px"></li><li class="free_16px"></li><li class="free_16px"></li><li class="free_16px"></li><li class="free_16px"></li><li class="free_16px"></li><li class="free_16px"></li><li ><ul ><li class="bad pad_end"></li><li class="free"></li><li class="free"></li><li class="bad pad_end"></li></ul></li><li class="free_16px"></li><li class="free_16px"></li></ul><img src="/skin/base_images//day_gauge.gif" /></div><div id="add_timeline__error" class="slider error_display"></div><div id='optional_rate_plan_adjustment' style='text-align:left;'><font class='text'></font></div><button id="lb_cancel_button" class="cancel"></button><button id="lb_reserve_button" class="reserve"></button></div></form><br style="clear: both;" /></div></div><script language="javascript" type="text/javascript">MV.globals.reserve.lightbox = new MV.controls.reserve.lightbox({"range_params":{"start_control":{"date_id":"add_start_stamp__start_date_","time_id":"add_start_stamp__start_time_"},"end_control":{"date_id":"add_end_stamp__end_date_","time_id":"add_end_stamp__end_time_"}},"estimate_params":{"price_id":"add_price__price_","available_balance_id":"add_balance__balance_","amount_due_id":"add_amount_due__amount_due_","credit_id":"add_credit__balance_","credit_box_id":"add_credit__balance__div","available_credit_box_id":"add_available_credit__available_credit__div","available_credit_id":"add_available_credit__available_credit_","cost_params":{"id":"add_estimate__estimate_","time_id":"add_estimate__estimate__time_amount","distance_id":"add_estimate__estimate__distance_amount","fees_id":"add_estimate__estimate__fee_amount","tax_id":"add_estimate__estimate__tax_amount","tax_pks":[],"labels":{"please_wait":"Please wait...","hourly":"Hourly","daily":"Daily"}},"hide_ab_shortfall":false},"accept_button_id":"lb_reserve_button","cancel_button_id":"lb_cancel_button","instruction_id":"lightbox_instruction","form_id":"add","attach_close_event":true,"attach_confirm_event":true,"use_dynamic_timeline":true,"initial_update":true,"preserve_instruction":true,"is_lightbox":true,"disabled_class":"reserve_disabled","slider_params":{"action":"add","stack_pk":"96692246","reservation_pk":0,"start_stamp":1289462400,"start_stamp_min":1289257200,"start_stamp_max":1298869200,"end_stamp":1289463300,"end_stamp_min":1289257200,"end_stamp_max":1298869200,"start_date_control":"add_start_stamp__start_date_","start_time_control":"add_start_stamp__start_time_","end_date_control":"add_end_stamp__end_date_","end_time_control":"add_end_stamp__end_time_","lower":1289386800,"upper":1289473200,"increment":900,"date_calibration":"11\/10\/10","control_ids":{"track_id":"reservation_bar_track","start_handle_id":"reservation_bar_start_handle","end_handle_id":"reservation_bar_end_handle","res_marker_id":"reservation_bar","error_id":"add_timeline__error"},"no_slider":false,"error_label":"Please adjust your times to an available period. Use the form above or click-and-drag your times."}});</script>'''

KEY_TO_THE_CITY_DOCUMENT=r'''
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"> 
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en" dir="ltr"> 
 
<head> 
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" /> 
  <title>Promos/Key to the City | PhillyCarShare</title> 
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8" /> 
<meta name="keywords" content="car share, car sharing, carshare, carsharing, philly, philadelphia" /> 
<link rel="shortcut icon" href="/sites/default/files/zen_favicon.ico" type="image/x-icon" /> 
  <link type="text/css" rel="stylesheet" media="all" href="/sites/default/files/css/css_659df6e2113866f52c8cc39434d846aa.css" /> 
<link type="text/css" rel="stylesheet" media="print" href="/sites/default/files/css/css_1b07ca9eb88b84c8bd0fbecd8e370209.css" /> 
<!--[if IE]>
<link type="text/css" rel="stylesheet" media="all" href="/sites/all/themes/zen/zen/ie.css?T" />
<![endif]--> 
  <script type="text/javascript" src="/sites/default/files/js/js_b7d75e059c86d1836dce7a384c31ae73.js"></script> 
<script type="text/javascript"> 
<!--//--><![CDATA[//><!--
jQuery.extend(Drupal.settings, { "basePath": "/", "googleanalytics": { "trackOutgoing": 1, "trackMailto": 1, "trackDownload": 1, "trackDownloadExtensions": "7z|aac|avi|csv|doc|exe|flv|gif|gz|jpe?g|js|mp(3|4|e?g)|mov|pdf|phps|png|ppt|rar|sit|tar|torrent|txt|wma|wmv|xls|xml|zip" } });
//--><!]]>
</script> 
     <link rel="stylesheet" type="text/css" href="/sites/all/themes/css/reset.css" /> 
     <link rel="stylesheet" type="text/css" href="/sites/all/themes/css/pcs.css" /> 
     <script src="/sites/all/themes/js/jquery.js" type="text/javascript"></script> 
     <script src="/sites/all/themes/js/expander.js" type="text/javascript"></script> 
 
 
     <script src="/sites/all/themes/js/nav.js" type="text/javascript"></script> 
     <script src="/sites/all/themes/js/login.js_2_2_1_1" type="text/javascript"></script> 
 
 
 
</head> 
<body class="not-front not-logged-in node-type-page no-sidebars page-promos-key-to-the-city section-promos"> 
 
  <div id="page"><div id="page-inner"> 
 
    <a name="top" id="navigation-top"></a> 
    
    <div id="header"><div id="header-inner" class="clear-block"> 
 
      
      
    </div></div> <!-- /#header-inner, /#header --> 
 
    <div id="main"><div id="main-inner" class="clear-block"> 
 
      <div id="content"><div id="content-inner"> 
	<div id="main_body"> 
<div class="top_cont"> 
<div class="logo_cont"><a href="/"><img src="/sites/all/themes/images/logo.gif" alt="PhillyCarShare" /></a></div> 
<div class="main_nav_cont"> 
<ul id="nav"> 
<li id="btn_residents"><a href="/residents"><span class="btn_text">residents</span></a> 
 
<ul> 
<li><a href="/sites/default/files/member-handbook.pdf" target="_blank">member handbook</a></li> 
<li><a href="/residents">how it works</a></li> 
<li><a href="/residents/is-car-sharing-right-for-me" style="display: block;">is car sharing right for me?</a></li> 
<li><a href="/residents/rates" style="display: block;">rates</a></li> 
<li><a href="/residents/students" style="display: block;">students</a></li> 
<li><a href="/residents/benefits" style="display: block;">benefits</a></li> 
<li><a href="/faq/residents">FAQ</a></li> 
<li><a href="/faq/survey">survey FAQ</a></li> 
<li><a href="/join">join now</a></li> 
<li><a href="/sites/default/files/gas-reimburse.pdf" target="_blank">gas reimbursement</a></li> 
 
</ul> 
</li> 
 
<li id="btn_businesses"><a href="/businesses"><span class="btn_text">businesses</span></a> 
<ul> 
<li><a href="/sites/default/files/member-handbook.pdf" target="_blank">member handbook</a></li> 
<li><a href="/businesses">how it works</a></li> 
<li><a href="/businesses/rates" style="display: block;">rates</a></li> 
<li><a href="/businesses/fleet" style="display: block;">fleet</a></li> 
<li><a href="/businesses/benefits" style="display: block;">benefits</a></li> 
<li><a href="/businesses/penn" style="display: block;">Penn</a></li> 
<li><a href="/faq/businesses">FAQ</a></li> 
<li><a href="/join">join now</a></li> 
<li><a href="/sites/default/files/gas-reimburse.pdf" target="_blank">gas reimbursement</a></li> 
 
 
</ul> 
</li> 
<li id="btn_cars"><a href="/cars"><span class="btn_text">Cars</span></a></li> 
<li id="btn_locations"><a href="/locations/pod-search"><span class="btn_text">Locations</span></a> 
<ul> 
<li><a href="/locations/pod-search" style="display: block;">pod search</a></li> 
<li><a href="/locations/offer-a-parking-spot" style="display: block;">offer a parking spot</a></li> 
</ul> 
</li> 
 
<li id="btn_promos"><a href="/promos/press-room"><span class="btn_text">Promos</span></a> 
<ul> 
<li><a href="/promos/press-room" style="display: block;">roaming memberships</a></li> 
<li><a href="/promos/phillyaptco" style="display: block;">the philly apartment co</a></li> 
<li><a href="/promos/referrals" style="display: block;">refer a friend</a></li> 
<li><a href="/promos/gift-certificates" style="display: block;">gift certificates</a></li> 
<li><a href="/promos/share-haul-save" style="display: block;">share it, haul it, save it!</a></li> 
<li><a href="/promos/free-rail-to-phillycarshare" style="display: block;">free rail to PhillyCarShare</a></li> 
<li><a href="/promos/key-to-the-city" style="display: block;">key to the city</a></li> 
 
</ul> 
</li> 
<li id="btn_vision"><a href="/vision"><span class="btn_text">Vision</span></a> 
<ul> 
<li><a href="/vision">vision/mission</a></li> 
<li><a href="/vision/pcs-impact-study">PCS impact study</a></li> 
<li><a href="/vision/pcs-sustainable-design">PCS &amp; sustainable design</a></li> 
<li><a href="/vision/jobs" style="display: block;">jobs</a></li> 
<li><a href="/vision/why-were-nonprofit" style="display: block;">why we're nonprofit</a></li> 
<li><a href="/vision/history" style="display: block;">history</a></li> 
<li><a href="/vision/our-people" style="display: block;">our people</a></li> 
<li><a href="/vision/give-today" style="display: block;">give today!</a></li> 
<li><a href="/vision/press-room" style="display: block;">press room</a></li> 
</ul> 
</li> 
</ul>		</div> 
<div class="cont_pic"><img src="/sites/all/themes/images/interior/rotate.php" alt="PhillyCarShare" /></div> 
</div>	
<div class="content_wrapper"> 
 
        <div id="content-area"> 
          <div id="node-23" class="node node-type-page"><div class="node-inner"> 
 
  
  
  
  
  <div class="content"> 
    <div class="cont_pic"><img src="/sites/all/themes/images/cont_pic_ktc.jpg" alt="PhillyCarShare" /> 
</div>	
 
<div class="content_wrapper"> 
<div class="cont_col_1"> 
 
<div class="breadcrumb"> 
<p><em>News</em> 
:&nbsp;&nbsp;&nbsp;&nbsp;
<a href="/promos/sell-car-drive-free">sell your car, drive for free</a>&nbsp;&nbsp;:&nbsp;&nbsp;
<a href="/promos/press-room">roaming memberships</a>&nbsp;&nbsp;:&nbsp;&nbsp;
<a href="/promos/phillyaptco">the philly apartment co</a>&nbsp;&nbsp;:&nbsp;&nbsp;
<a href="/promos/referrals">refer a friend</a>&nbsp;&nbsp;:&nbsp;&nbsp;
<a href="/promos/gift-certificates">gift certificates</a>&nbsp;&nbsp;:&nbsp;&nbsp;
<a href="/promos/share-haul-save">share it, haul it, save it</a>&nbsp;&nbsp;:&nbsp;&nbsp;
<a href="/promos/free-rail-to-phillycarshare">free rail to PhillyCarShare</a>&nbsp;&nbsp;:&nbsp;&nbsp;
<a href="/promos/key-to-the-city"><strong>key to the city</strong></a>&nbsp;&nbsp;&nbsp;&nbsp;
</div> 
 
<h1>Key to the City</h1> 
 
<p>PhillyCarShare&#39;s Key to the City provides our members with exclusive discounts to participating Philadelphia retailers. Just present your incentive tag and receive the following cool deals available to only PhillyCarShare members. Click on a category for more information on local businesses.</p> 
<div style="text-align: center"><img src="/sites/all/themes/images/keytothecity.jpg" alt="" width="211" height="83" /></div> 
<p>&nbsp;</p> 
<div align="center"><a href="/promos/key-to-the-city/a-e">A&amp;E</a> : <a href="/promos/key-to-the-city/food-and-beverage">Food and Beverage</a> : <a href="/promos/key-to-the-city/nightlife">Nightlife</a> : <a href="/promos/key-to-the-city/places-to-shop">Places to Shop</a> : <a href="/promos/key-to-the-city/upcoming-events">Upcoming Events</a> : <a href="/promos/key-to-the-city/terms">Terms</a></div><p align="center"><a href="/promos/key-to-the-city/health-and-fitness">Health Fitness and Well Being</a> : <a href="/promos/key-to-the-city/pet-care">Pet Care</a>  : <a href="/promos/key-to-the-city/professional-services">Professional Services </a><br /></p> 
 
<hr />     
<p>Here are some of our newest partners...</p> 
 
<table border="0" cellspacing="0" cellpadding="5" width="554" height="359">               
<tbody> 
 
 
<tr><td align="center"> 
<a href="http://www.harvestlocalfoods.com" target="_blank"><img src="/sites/all/themes/images/key/key-harvestlogo.jpg" border="0" alt="" width="200" height="268" /></a> 
</td> 
<td align="center"> 
<a href="http://www.hydrosbottle.com/" target="_blank"><img src="http://www.phillycarshare.org/sites/default/files/newsletters/201005/hydrosbottle.png" alt="" border="0" align="middle" /></a> 
</td> 
 
</tr> 
<tr> 
<td align="center"> 
<p>Working with over 40 local family farmers and food artisans. Shop online from a selection of seasonal products year-round. Door-to-door delivery. PCS members get free delivery on their first order. <br /><a href="http://www.harvestlocalfoods.com" target="_blank">www.harvestlocalfoods.com</a> 
</p> 
 
<p>&nbsp;</p> 
</td> 
<td align="center"> 
<p>Never buy bottled water again! &nbsp;The <strong>Hydros Bottle</strong> is a reusable water bottle with a built-in filter designed to give you crisp, refreshing water on the go.</p> 
                                   <p>All PhillyCarShare users receive a 10% discount on your order at <a title="http://www.hydrosbottle.com/" href="http://www.hydrosbottle.com" target="_blank">www.hydrosbottle.com</a>.</p> 
                                   <p>Enter: "PCSCITYKEY"</p> 
</td> 
</tr> 
 
<tr><td align="center"> <a href="http://www.whitedog.com/"><img src="/sites/default/files/newsletters/201004/whitedog.jpg" alt="" /></a></td> 
<td align="center"> <a href="http://www.franklinfountain.com/" target="_blank"><img src="/sites/default/files/newsletters/201004/franklin-fountain.jpg" alt="" /></a></td><td>&nbsp;</td> 
</tr> 
 
<tr> 
<td align="center"><p> <a href="http://www.whitedog.com/" target="_blank"><strong><font face="Times New Roman" size="2" style="font-weight: bold; font-size: 11pt">White Dog Caf&eacute;</font></strong></a><br /></p> 
<p>Located in three adjacent Victorian brownstones in the University City section of Philadelphia, <strong>The White Dog Caf&eacute;</strong> is a local favorite known for its unusual blend of award-winning contemporary American cuisine, civic engagement and environmental sustainability.</p> 
                                   <p>10% off food purchases (alcohol not included)<br /> 
                                   <a href="http://www.whitedog.com/" target="_blank">www.whitedog.com</a></p> 
</td> 
<td align="center"><p align="center"><a href="http://www.franklinfountain.com/" target="_blank"><strong><font face="Times New Roman" size="2" style="font-weight: bold; font-size: 11pt">The Franklin Fountain</font></strong></a></p> 
<p>aims to serve an experience steeped in ideals, drizzled with drollery,  and sprinkled with the forgotten flavors of the American past.</p> 
                                   <p>10% off all Ice Cream, Sodas & Desserts from The Franklin Fountain. Offer limited to one use per month, per member.</p> 
                                   <p>116 Market Street<br /> 
                                   <a href="http://www.franklinfountain.com/" target="_blank">www.franklinfountain.com</a> 
                                   <br /> 
                                   215-627-1899
</p> 
<p>&nbsp;</p></td> 
</tr> 
 
<tr><td align="center"> <a href="http://www.playsandplayers.org/"><img src="/sites/default/files/newsletters/201003/playsandplayers.jpg" alt="" width="200" height="42" /></a></td> 
<td align="center"> <a href="http://www.wulffarchitects.com/" target="_blank"><img src="/sites/default/files/newsletters/201003/wulffarchitects.jpg" alt="" width="225" height="90" /></a></td><td>&nbsp;</td> 
</tr> 
 
<tr> 
<td align="center"><p> <a href="http://www.playsandplayers.org" target="_blank"><strong><font face="Times New Roman" size="2" style="font-weight: bold; font-size: 11pt">Plays and Players Theater</font></strong></a><br /></p> 
<p>is an historic company existing in a vibrant arts scene, where artists young and old can continue to practice and perform their craft.</p> 
<p>Buy One Get One for Opening Weekend (Thurs-Sun) and any Thursday evening performances throughout the season.
</p></td> 
<td align="center"><p align="center"><a href="http://www.wulffarchitects.com/" target="_blank"><strong><font face="Times New Roman" size="2" style="font-weight: bold; font-size: 11pt">Wulff Architects</font></strong></a></p> 
<p>is a regionally recognized firm located in Center City and specializing in Architectural Design, Interior Design, LEED, Project Management, Feasibility Studies, Furniture and Finish Selections and Site/Master/Urban Planning. Since its inception, Wulff Architects has maintained a repeat clientele through a reputation for competitive pricing and a commitment to design excellence.</p> 
<p>We want to be a part of your next commercial or residential project.
Members receive a Free Consultation, please ask for Erin Smith.
</p> 
<p>&nbsp;</p></td> 
</tr> 
 
<tr> 
<td align="center" valign="middle"><a href="http://www.philadelphia-acupuncture.com" target="_blank"><img src="/sites/all/themes/images/key-empirical.jpg" alt="Empirical Point Acupuncture"  border="0" align="middle" longdesc="http://www.philadelphia-acupuncture.com"></a> </td> 
<td align="center"><a href="http://www.dibruno.com/" target="_blank"><img src="/sites/default/files/newsletters/201003/dibruno.jpg" border="0" /></a> 
</td> 
<td>&nbsp;</td> 
</tr> 
<tr><td align="center" valign="middle"> 
<p><a href="http://www.philadelphia-acupuncture.com" target="_blank" title="http://www.philadelphia-acupuncture.com/"><strong><font face="Times New Roman" size="2" style="font-weight: bold; font-size: 11pt">Empirical  Point Acupuncture</font></strong></a></p> 
<p>Comprehensive, individualized care distinguishes Empirical Point as a premier  center for acupuncture and Oriental medicine in Philadelphia. With 9 years of study and  practice, Sharon Sherman creates a supportive environment in which symptoms,  diagnosis and treatment can be thoroughly addressed. PhillyCarShare members  receive 10% off their first appointment.</p></td> 
<td align="center"> 
<p><a href="http://www.dibruno.com/" target="_blank" title="http://www.dibruno.com/"><strong><font face="Times New Roman" size="2" style="font-weight: bold; font-size: 11pt">Di Bruno Bros.</font></strong></a></p> 
<p>is celebrating their 70th year of culinary pioneering in the great city of Philadelphia!  Di Bruno's specializes in imported meats and cheeses, oils and vinegars and a plethora of other fine international ingredients.  Most recently, Di Bruno's has launched a catering division, offering food services ranging from wine and cheese parties for 15 guests to extravagant cocktail parties for 500.</p> 
<p> 
Place a catering order of $150 or more and receive a gift card in the amount of $15 to use anywhere in our Chestnut Street store. Use promo code PCS; expires 9/30/10.</p> 
</p> 
</td> 
</tbody> 
</table>  
<p>&nbsp;</p> 
<p align="center">Check back often for the latest on our partners and discounts!</p> 
<p><em>If you are a business and would like to be a part of the program, please contact <a href="mailto:heather@phillycarshare.org?subject=Key%20to%20the%20City" target="_blank">heather@phillycarshare.org</a></em>.</p> 
 
</div> 
 
 
 
 
 
<div class="cont_col_2"> 
<iframe src="https://reservations.phillycarshare.org/my_mini_login.php" width="0" height="0"  frameborder="0" marginwidth="0" scrolling="No" marginheight="0"><!-- --></iframe> 
<form id="login" name="login" method="post" action="https://reservations.phillycarshare.org/index.php" target="_top"> 
<table cellpadding="3" cellspacing="0" width="80%" align="center"> 
<tr> 
<td class="label"><strong>Member ID:</strong> </td> 
</tr> 
<tr> 
<td><input type="text" class="text" size="20" name="login[name]" id="login_name_" /></td> 
</tr> 
<tr> 
<td class="label"><strong>Password:</strong> </td> 
 
</tr> 
<tr> 
<td><input type="password" class="text" size="20" name="login[password]" id="login_password_" /></td> 
</tr> 
<tr> 
<td><input type="hidden" name="mv_action" value="login"/><input type="image" src="/sites/all/themes/images/btn_signin_home.gif" value="submit" /></td> 
</tr> 
</table> 
<input id="login_tid_" type="hidden" name="login[tid]" value="1"/> 
</form> 
<p style="text-align:center;"><a href="https://reservations.phillycarshare.org/index.php?mv_action=password" style="color:#29296e;">Forgot Password?</a></p> 
<!-- <p><strong>Jonathan Smith</strong><br />you are signed in <br />(Residential Account)</p>
<p align="right"><a href=""><img src="/sites/all/themes/images/btn_signout.gif" alt="Sign Out" /></a></p> --> 
<div class="buttons"> 
<a href="/residents"><img src="/sites/all/themes/images/btn_works_cont.gif" alt="How it Works" class="works" /></a><a href="/join"><img src="/sites/all/themes/images/btn_join_cont.gif" alt="Join Now" class="join" /></a><a href="/refer"><img src="/sites/all/themes/images/btn_refer_cont.gif" alt="Refer a friend" class="refer" /></a> 
</div> 
<div class="testimonial"> 
 
</div> 
</div> 
<div style="clear:both;"></div>	  </div> 
 
  
</div></div> <!-- /node-inner, /node --> 
        </div> 
 
<div id="main_body"> 
	 </div></div> 
</div>			<div id="footer"> 
<table width="100" border="0" align="right" cellpadding="0" cellspacing="2"> 
  <tr> 
    <td align="center"><a href="http://www.facebook.com/phillycarshare/" target="_blank"><img src="/sites/all/themes/images/facebook-small.png" alt="facebook" width="25" border="0" /></a></td> 
    <td align="center"><a href="http://twitter.com/phillycarshare" target="_blank"><img src="/sites/all/themes/images/twitter-small.png" alt="twitter" width="25" border="0" /></a></td> 
    <td align="center"><a href="http://www.linkedin.com/companies/64730/PhillyCarShare?trk=pp_icon" target="_blank"><img src="/sites/all/themes/images/linkedin-small.png" alt="linkedin" width="27" border="0" /></a></td> 
  </tr> 
</table> 
<p>Join us on <a href="http://www.facebook.com/phillycarshare/" target="_blank">facebook</a>, <a href="http://twitter.com/phillycarshare" target="_blank">twitter</a>, and <a href="http://www.linkedin.com/companies/64730/PhillyCarShare?trk=pp_icon" target="_blank">linkedin</a>!</p> 
<h3><a href="/partnerships">partnerships:</a></h3> <p style="display:inline;"><a href="/partnerships/developers">Developers</a>&nbsp;&nbsp;&nbsp;<a href="/partnerships/property-managers">Property Managers</a>&nbsp;&nbsp;&nbsp;<a href="/partnerships/universities">Universities</a>&nbsp;&nbsp;&nbsp;<a href="/contact-us">Contact Us</a></p> 
<p>Our vision is a Philadelphia in which nonprofit car sharing exceeds the convenience, flexibility, and affordability of car ownership.<br /> 
<table width="95%" border="0" align="right" cellpadding="0" cellspacing="2"> 
  <tr> 
    <td align="center">phillycarshare &middot; a non-profit organization &middot; (215) 730-0988</td> 
    <td align="right"><a href="http://www.dreamhost.com/green.cgi" target="_blank"> 
<img border="0" alt="Green Web Hosting! This site hosted by DreamHost." src="https://secure.newdream.net/green3.gif" height="15" width="80" /></a> 
    </td> 
  </tr> 
</table> 
</p> 
</div>			<div style="clear:both;"></div> 
</div> 
 
<p class="credit">Copyright &copy; PhillyCarShare 2007 - 2010
</p> 
<p class="credit">design: <a href="http://www.northfound.com" target="_blank">northfound</a>&nbsp;&nbsp;|&nbsp;&nbsp;development: <a href="http://www.thoughtprocessinteractive.com" target="_blank">TPI</a></p> 
      </div></div> <!-- /#content-inner, /#content --> 
 
      
      
      
    </div></div> <!-- /#main-inner, /#main --> 
 
    
  </div></div> <!-- /#page-inner, /#page --> 
 
  
  <script type="text/javascript" src="/sites/default/files/js/js_c23fb57b3b2601f44bc0f204c65ad209.js"></script> 
<script type="text/javascript"> 
<!--//--><![CDATA[//><!--
try{var pageTracker = _gat._getTracker("UA-16737291-1");pageTracker._trackPageview();} catch(err) {}
//--><!]]>
</script> 
 
</body> 
</html> '''
