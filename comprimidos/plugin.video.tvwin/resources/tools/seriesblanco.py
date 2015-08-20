# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Parser de SeriesMu para PalcoTV
# Version 0.1 (22.05.2015)
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Gracias a las librerías de pelisalacarta de Jesús (www.mimediacenter.info)


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

import plugintools
from resources.tools.resolvers import *


addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")


fanart = 'http://st-listas.20minutos.es/images/2012-06/335200/list_640px.jpg?1368294762'





	#<div id="selectable">		
		#<div class="text"><ol><li class="li1"><div class="de1">#EXTM3U</div></li>
#<li class="li2"><div class="de2">#EXTINF:-1tvg-logo=&quot;http://www.totalplay.com.mx/images/logos/canales/fox/fox-movies-hd.png&quot;,Fox Movies HD</div></li>
#<li class="li1"><div class="de1">http://200.38.126.38:8081/TPMHLSWeb/M3U8LiveFile?a=Zm9ybWF0PTImcHJvZmlsZT0zMDUmbGFuPTImcm93cz0yMCZzZXNzaW9uPXRudTJoczYwcmk0c2c5aw==&amp;f=.m3u8</div></li>
#<li class="li2"><div class="de2">&nbsp;</div></li>
#<li class="li1"><div class="de1">&nbsp;</div></li>
#<li class="li2"><div class="de2">#EXTINF:-1 tvg-logo=&quot;http://www.totalplay.com.mx/images/logos/canales/fox/fox-1-hd.png&quot;,Fox 1 HD</div></li>
#<li class="li1"><div class="de1">http://200.38.126.38:8081/TPMHLSWeb/M3U8LiveFile?a=Zm9ybWF0PTImcHJvZmlsZT0yOTcmbGFuPTImcm93cz0yMCZzZXNzaW9uPXRudTJoczYwcmk0c2c5aw==&amp;f=.m3u8</div></li>
#<li class="li2"><div class="de2">&nbsp;</div></li>
#<li class="li1"><div class="de1">&nbsp;</div></li>
#<li class="li2"><div class="de2">#EXTINF:-1 tvg-logo=&quot;http://www.totalplay.com.mx/images/logos/canales/fox/fox-action-oeste.png&quot;,Fox Action HD</div></li>
#<li class="li1"><div class="de1">http://200.38.126.38:8081/TPMHLSWeb/M3U8LiveFile?a=Zm9ybWF0PTImcHJvZmlsZT0zMDEmbGFuPTImcm93cz0yMCZzZXNzaW9uPXRudTJoczYwcmk0c2c5aw==&amp;f=.m3u8</div></li>
#<li class="li2"><div class="de2">&nbsp;</div></li>
#<li class="li1"><div class="de1">&nbsp;</div></li>
#<li class="li2"><div class="de2">#EXTINF:-1 tvg-logo=&quot;http://www.totalplay.com.mx/images/logos/canales/fox/fox-family-hd.png&quot;,Fox Family</div></li>
#<li class="li1"><div class="de1">http://200.38.126.38:8081/TPMHLSWeb/M3U8LiveFile?a=Zm9ybWF0PTImcHJvZmlsZT0zNDEmbGFuPTImcm93cz0yMCZzZXNzaW9uPXRudTJoczYwcmk0c2c5aw==&amp;f=.m3u8</div></li>
#<li class="li2"><div class="de2">&nbsp;</div></li>
#<li class="li1"><div class="de1">&nbsp;</div></li>
#<li class="li2"><div class="de2">#EXTINF:-1tvg-logo=&quot;http://www.totalplay.com.mx/images/logos/canales/fox/fox-classics.png&quot;,Fox Clásico</div></li>
#<li class="li1"><div class="de1">http://200.38.126.38:8081/TPMHLSWeb/M3U8LiveFile?a=Zm9ybWF0PTImcHJvZmlsZT0zNDUmbGFuPTImcm93cz0yMCZzZXNzaW9uPXRudTJoczYwcmk0c2c5aw==&amp;f=.m3u8</div></li>




def seriesblanco0(params):
    plugintools.log('[%s %s] lista_capis %s' % (addonName, addonVersion, repr(params)))

    
    
      
        
    url = params.get("url")
    referer = 'http://pastebin.com/raw.php?i=aF32H93w'
    data = gethttp_referer_headers(url,referer)
	

    
    
    matches = plugintools.find_multiple_matches(data, '<div class="de1">canal</div></li>(.*?)<li class="li1"><div class="de1">canalfin')
    for entry in matches:
        title = scrapertools.find_single_match(entry, '<div class="de2">name=([^"]+)</div></li>')
        plugintools.log("title= "+title)
        cover = plugintools.find_single_match(entry, 'class="de1">logo=([^"]+)</div></li>')
        plugintools.log("cover= "+cover)
	
        url_channel = plugintools.find_single_match(entry, 'server=([^"]+)</div></li>')
        plugintools.log("url_channel = "+url_channel)
        plugintools.add_item(action="key", title = title , thumbnail = cover , url = url_channel , fanart = fanart , folder = False , isPlayable = False)



		
def key(params):
    plugintools.log('[%s %s] obtener key %s' % (addonName, addonVersion, repr(params)))
    url = params.get("url")
    referer = 'http://guiatvpro.com/admin/api.php?method=news&app_version=39&lang=es&test=1'
    data = gethttp_referer_headers(url,referer)
    plugintools.log("data= "+data)
    key_v = scrapertools.find_single_match(data, '/\/200.38.126.38:8081\/TPMHLSWeb\/M3U8LiveFile?a=Zm9ybWF0PTEmcHJvZmlsZT00MDcmbGFuPTImcm93cz00MCZzZXNzaW9u(.*?)==&f=.m3u8"')
    plugintools.log("key_v= "+key_v)
    plugintools.add_item(action="key", title = title , thumbnail = cover , url = key_v , fanart = fanart , folder = True , isPlayable = False)
	

    
        

def gethttp_referer_headers(url,referer):
    plugintools.log("gethttp_referer_headers "+url)

    request_headers=[]
    request_headers.append(["User-Agent","Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:16.0.1) Gecko/20121011 Firefox/16.0.1"])
    request_headers.append(["Referer", referer])    
    body,response_headers = plugintools.read_body_and_headers(url, headers=request_headers);print response_headers
    return body
	

	
def play(params):
    plugintools.play_resolved_url( params.get("url") )
