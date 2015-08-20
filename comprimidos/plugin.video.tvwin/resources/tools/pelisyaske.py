# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Parser de pelis 
# Version 0.1 (22/05/2015)
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Gracias a las librerías de pelisalacarta de Jesús y juarrox de palcotv (www.mimediacenter.info)


import os
import sys
import urllib
import urllib2
import re


import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin

import re,urllib,urllib2,sys


import plugintools, scrapertools
from resources.tools.resolvers import *


addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")

fanart = "http://socialgeek.co/wp-content/uploads/2013/06/series-TV-Collage-television-10056729-2560-1600.jpg"
referer = 'http://www.yaske.to/'








def seriecatcher(params):
    plugintools.log('[%s %s] seriecatcher %s' % (addonName, addonVersion, repr(params)))
    
	
    url = params.get("url")
    referer = 'http://www.yaske.to/es/peliculas/custom/?gender=premieres'
    data = gethttp_referer_headers(url,referer)
    plugintools.log("data= "+data)
    matches = plugintools.find_multiple_matches(data, '<li class="item-movies(.*?)<div class="view">')
    for entry in matches:
        title = scrapertools.find_single_match(entry, '" alt="(.*?)" width="140" height="200" />')
        cover = plugintools.find_single_match(entry, '<img src="([^"]+)')
        url = plugintools.find_single_match(entry, '<a href="([^"]+)')
        plugintools.log("url= "+url)
        plugintools.add_item(action="pelisya", title = title , thumbnail = cover , url = url , fanart = fanart , folder = True , isPlayable = False)
    
	next_page = scrapertools.find_single_match(data,"href='http://www.yaske.to/es/peliculas/page/(.*?)'>")
    next_page = next_page.replace('("', "").replace('")', "")
    next_page = 'http://www.yaske.to/es/peliculas/page/'+next_page
    plugintools.log("next_page= "+next_page)
    if next_page!="":
        plugintools.add_item(action="seriecatcher", title =">> siguiente" , thumbnail = "", url = next_page, fanart = fanart , folder = True)

    return plugintools.add_item


	

def pelisya(params):
   plugintools.log('[%s %s] pelisya %s' % (addonName, addonVersion, repr(params)))  
   url = params.get("url")
   referer = url
   data = gethttp_referer_headers(url,referer)  
   plugintools.log("data= "+data)
   temp = plugintools.find_multiple_matches(data, '<tr bgcolor="">(.*?)<ul class="star"><li class="curr" style="width:')
   for entry in temp:
    server_url2 = plugintools.find_single_match(entry, 'u=([^"]+)"><i')
    plugintools.log("server_url2= "+server_url2)
    mini_url = plugintools.find_single_match(entry, '<td align="center"><img src="([^"]+)" width="22"></td>')
    plugintools.log("mini_url= "+mini_url)
    server_title = plugintools.find_single_match(entry, '" />([^"]+)</td>')
    if server_title.find("allmyvideos") >=0:
       server_title = "[Server allmyvideos]"
       plugintools.add_item(action="allmyvideos", title = params.get("title") + " "   +server_title , thumbnail = mini_url  , url = server_url2 ,  fanart = "" , folder = False, isPlayable = True)
    elif server_title.find("played.to") >= 0:
       server_title = "[Server played.to]"
       plugintools.add_item(action="playedlink", title = params.get("title") + " "   +server_title , thumbnail = mini_url , url = server_url2 ,  fanart = "" , folder = False, isPlayable = True)
    elif server_title.find("streamin.to") >= 0:
       server_title = "[Server streaminto]"
       plugintools.add_item(action="streamintolink", title = params.get("title") + " "   +server_title , thumbnail = mini_url  , url = server_url2 ,  fanart = "" , folder = False, isPlayable = True)
    elif server_title.find("nowvideo") >= 0:
       server_title = "[Server nowvideo]"
       plugintools.add_item(action="nowvideo", title = params.get("title") + " "   +server_title , thumbnail = mini_url  , url = server_url2 ,  fanart = "" , folder = False, isPlayable = True)
	
	
def gethttp_referer_headers(url,referer):
    plugintools.log("gethttp_referer_headers "+url)

    request_headers=[]
    request_headers.append(["User-Agent","Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:16.0.1) Gecko/20121011 Firefox/16.0.1"])
    request_headers.append(["Referer", referer])    
    body,response_headers = plugintools.read_body_and_headers(url, headers=request_headers);print response_headers
    return body