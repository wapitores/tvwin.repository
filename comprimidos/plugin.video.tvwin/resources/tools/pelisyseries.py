# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Parser de pelis y series
# Version 0.1 (22/05/2015)
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Gracias a las librerías de pelisalacarta de Jesús (www.mimediacenter.info) y juarrox de palcotv 


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



addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")

music = 'http://3.bp.blogspot.com/-nTyqSSBdeDo/TujJSjNyYuI/AAAAAAAACbU/IqffXgbfpZo/s1600/megapost_peliculas.png'
referer = 'http://pacific1469.serverprofi24.eu:32400/library/sections/5/all?X-Plex-Token=yK9PAhXdNKo3ywoDx9b7'
pel = 'http://k32.kn3.net/taringa/D/7/6/7/5/0/niad/E10.jpg'
pel2 = 'http://images6.alphacoders.com/405/405735.jpg'
ser = 'http://pacific1469.serverprofi24.eu:32400'
ser2 = 'http://pacific1469.serverprofi24.eu:32400/library/parts/'
token = '?X-Plex-Token=yK9PAhXdNKo3ywoDx9b7'

art = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.tvwin/art', ''))




def seriecatcher(params):
    plugintools.log('[%s %s] seriecatcher %s' % (addonName, addonVersion, repr(params)))
    
	
    url = params.get("url")
    referer = 'http://pacific1469.serverprofi24.eu:32400/library/sections/5/all?X-Plex-Token=yK9PAhXdNKo3ywoDx9b7'
    data = gethttp_referer_headers(url,referer)
    plugintools.log("data= "+data)
    matches = plugintools.find_multiple_matches(data, '<Directory(.*?)</Directory>')
    for entry in matches:
        title = scrapertools.find_single_match(entry, 'type="show" title="(.*?)"')
        cover = plugintools.find_single_match(entry, 'banner="([^"]+)"')
        cover = ser + cover + token
        plugintools.log("cover= "+cover)
        url = plugintools.find_single_match(entry, 'key="([^"]+)"')
        url = ser + url + token
        plugintools.log("url= "+url)
        fondo = plugintools.find_single_match(entry, 'thumb="([^"]+)"')
        fondo = ser + fondo + token 
        plugintools.add_item(action="series", title = title , thumbnail = fondo , url = url , fanart = cover , folder = True , isPlayable = False)
    
	


def series(params):
   plugintools.log('[%s %s] series %s' % (addonName, addonVersion, repr(params)))  
   url = params.get("url")
   referer = url
   data = gethttp_referer_headers(url,referer)  
   plugintools.log("data= "+data)
   temp = plugintools.find_multiple_matches(data, '<Directory ra(.*?)</Directory>')
   for entry in temp:
    server_url2 = plugintools.find_single_match(entry, 'key="([^"]+)"')
    server_url2 = ser + server_url2 + token
    plugintools.log("server_url2= "+server_url2)
    mini_url = plugintools.find_single_match(entry, 'thumb="([^"]+)"')
    mini_url = ser + mini_url + token
    plugintools.log("mini_url= "+mini_url)
    server_title = plugintools.find_single_match(entry, 'title="([^"]+)"')
    plugintools.add_item(action="url_play13", title = server_title , thumbnail = mini_url , url = server_url2 , fanart = pel, folder = True, isPlayable = False)
    

def url_play12(params):
   plugintools.log('[%s %s] url_play12 %s' % (addonName, addonVersion, repr(params)))  
   url = params.get("url")
   referer = url
   data = gethttp_referer_headers(url,referer)  
   plugintools.log("data= "+data)
   temp = plugintools.find_multiple_matches(data, '<Video(.*?)</Video>')
   for entry in temp:
    url2 = plugintools.find_single_match(entry, 'title="([^"]+)"')
    play32 = plugintools.find_single_match(entry, ' key="/library/parts/([^"]+)"')
    play32 = ser2 + play32 + token
    tum = plugintools.find_single_match(entry, 'thumb="([^"]+)"')
    tum = ser + tum + token
    plugintools.add_item(action="notipeli", title = url2 , thumbnail = tum , url = play32 , fanart = pel2 , folder = False , isPlayable = 	True)

def url_play13(params):
   plugintools.log('[%s %s] url_play12 %s' % (addonName, addonVersion, repr(params)))  
   url = params.get("url")
   referer = url
   data = gethttp_referer_headers(url,referer)  
   plugintools.log("data= "+data)
   temp = plugintools.find_multiple_matches(data, '<Video(.*?)</Video>')
   for entry in temp:
    url2 = plugintools.find_single_match(entry, 'title="([^"]+)"')
    play32 = plugintools.find_single_match(entry, ' key="/library/parts/([^"]+)"')
    play32 = ser2 + play32 + token
    tum = plugintools.find_single_match(entry, 'thumb="([^"]+)"')
    tum = ser + tum + token
    plugintools.add_item(action="play2", title = url2 , thumbnail = tum , url = play32 , fanart = music , folder = False , isPlayable = 	True)	
	
	
def play2(params):    
    plugintools.log('[%s %s].play %s' % (addonName, addonVersion, repr(params)))
    url = params.get("url")
    plugintools.play_resolved_url(url)
    xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Tvwin', "Cargando Capitulo......", 1 , art+'s.png'))
	
	
def notipeli(params):    
    plugintools.log('[%s %s].play %s' % (addonName, addonVersion, repr(params)))
    url = params.get("url")
    plugintools.play_resolved_url(url)
    xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Tvwin', "Cargando Pelicula......", 1 , art+'s.png'))

	
def gethttp_referer_headers(url,referer):
    plugintools.log("gethttp_referer_headers "+url)

    request_headers=[]
    request_headers.append(["User-Agent","Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:16.0.1) Gecko/20121011 Firefox/16.0.1"])
    request_headers.append(["Referer", referer])    
    body,response_headers = plugintools.read_body_and_headers(url, headers=request_headers);print response_headers
    return body