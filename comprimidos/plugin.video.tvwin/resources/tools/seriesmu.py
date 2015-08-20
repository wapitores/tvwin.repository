# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Parser 
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

import plugintools, scrapertools
from resources.tools.resolvers import *


addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")


fanart = 'http://st-listas.20minutos.es/images/2012-06/335200/list_640px.jpg?1368294762'
referer = 'http://peliculasaudiolatino.com/'







def pelis0(params):
    plugintools.log('[%s %s] lista_capis %s' % (addonName, addonVersion, repr(params)))

    
    
    url = params.get("url")
    referer = 'http://peliculasaudiolatino.com/ultimas-agregadas.html'
    data = gethttp_referer_headers(url,referer)

    plugintools.log("data= "+data)
    
    matches = plugintools.find_multiple_matches(data, '<div class="top">(.*?)</div>')
    for entry in matches:
        title = scrapertools.find_single_match(entry, '" alt="(.*?)"></a>')
        #plugintools.log("title= "+title)
        cover = plugintools.find_single_match(entry, '<img src="([^"]+)')
        #plugintools.log("cover= "+cover)
        url = plugintools.find_single_match(entry, '<a href="([^"]+)"><img ')
        #plugintools.log("url= "+url)
        plugintools.add_item(action="pelis1", title = title , thumbnail = cover , url = url , fanart = fanart , folder = True , isPlayable = False)
    
    next_page = scrapertools.find_single_match(data,'</a></li><li><a href="([^"]+)"><span class="icon-chevron-right"></span></a>')
    if next_page!="":
        plugintools.add_item(action="pelis0", title =">> Página siguiente" , thumbnail = "", url = next_page, fanart = fanart , folder = True)

    return plugintools.add_item
  
		


def pelis1(params):
   plugintools.log('[%s %s] enlaces_capi %s' % (addonName, addonVersion, repr(params)))  
   url = params.get("url")
   referer = url
   data = gethttp_referer_headers(url,referer)  
   #plugintools.log("data= "+data)
   temps = plugintools.find_multiple_matches(data, '</tr><tr><th class="headtable"(.*?)</div>')
   for entry in temps:
    server = plugintools.find_single_match(entry, 'http://peliculasaudiolatino.com/movies/([^"]+).html')
    server = 'http://peliculasaudiolatino.com/movies/'+ server +  ".html"
    title_url = plugintools.find_single_match(entry, '</th><th class="headmovil" align="left"><img src="([^"]+)" width="22"')
    #plugintools.log("title_url= "+title_url)
    server_title = plugintools.find_single_match(entry, '"/>([^"]+)</th><th')
    if server_title.find("allmyvideos") >=0:
       server_title = "[Server allmyvideos]"
       plugintools.add_item(action="pelis2", title = params.get("title") + " "   +server_title , thumbnail = title_url  , url = server ,  fanart = "" , folder = False, isPlayable = True)
    elif server_title.find("played.to") >= 0:
       server_title = "[Server played.to]"
       plugintools.add_item(action="playedlink", title = params.get("title") + " "   +server_title , thumbnail = title_url  , url = server ,  fanart = "" , folder = False, isPlayable = True)
    elif server_title.find("streamin.to") >= 0:
       server_title = "[Server streaminto]"
       plugintools.add_item(action="streamintolink", title = params.get("title") + " "   +server_title , thumbnail = title_url  , url = server ,  fanart = "" , folder = False, isPlayable = True)
    elif server_title.find("nowvideo.sx") >= 0:
       server_title = "[Server nowvideo]"
       plugintools.add_item(action="nowvideolink", title = params.get("title") + " "   +server_title , thumbnail = title_url  , url = server ,  fanart = "" , folder = False, isPlayable = True)
	   
	   
	   
	   
	   
	   
def playedlink(params):
    plugintools.log('[%s %s] playedlink %s' % (addonName, addonVersion, repr(params))) 
    url = params.get("url")
    referer = url
    data = gethttp_referer_headers(url,referer)  
    plugintools.log("data= "+data)
    final2 = plugintools.find_single_match(data, 'url=(.*?)"></iframe>')
    final2 = 'http://played.to/'+final2
    plugintools.log("final2 = "+final2 )
    params = plugintools.get_params()
    params["url"]=final2
    getlink(params)
	
def streamintolink(params):
    plugintools.log('[%s %s] streamintolink %s' % (addonName, addonVersion, repr(params))) 
    url = params.get("url")
    referer = url
    data = gethttp_referer_headers(url,referer)  
    plugintools.log("data= "+data)
    final2 = plugintools.find_single_match(data, 'url=(.*?)"></iframe>')
    final2 = 'http://streamin.to/'+final2
    plugintools.log("final2 = "+final2 )
    params = plugintools.get_params()
    params["url"]=final2
    getlink(params)
	
def nowvideolink(params):
    plugintools.log('[%s %s] streamintolink %s' % (addonName, addonVersion, repr(params))) 
    url = params.get("url")
    referer = url
    data = gethttp_referer_headers(url,referer)  
    plugintools.log("data= "+data)
    final2 = plugintools.find_single_match(data, 'url=(.*?)"></iframe>')
    final2 = 'http://www.nowvideo.sx/video/'+final2
    plugintools.log("final2 = "+final2 )
    params = plugintools.get_params()
    params["url"]=final2
    getlink(params)
	

	

	
	
def getlink(params):
    plugintools.log("GetLink for pelis "+repr(params))
    final2 = params.get("url")
    
    if final2.find("http://played.to/") >= 0:
        params["url"]=final2
        playedto(params)
    elif final2.find("http://streamin.to/") >= 0:
        params["url"]=final2
        streaminto(params)
    elif final2.find("http://www.nowvideo.sx/video/") >= 0:
        params["url"]=final2
        nowvideo(params)
   
	




    
	
	
	
	
def gethttp_referer_headers(url,referer):
    plugintools.log("gethttp_referer_headers "+url)

    request_headers=[]
    request_headers.append(["User-Agent","Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:16.0.1) Gecko/20121011 Firefox/16.0.1"])
    request_headers.append(["Referer", referer])    
    body,response_headers = plugintools.read_body_and_headers(url, headers=request_headers);print response_headers
    return body

