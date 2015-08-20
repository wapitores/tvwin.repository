# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Regex de Shidurlive para PalcoTV
# Version 0.1 (15.10.2014)
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Gracias a la librería plugintools de Jesús (www.mimediacenter.info)


import os
import sys
import urllib
import urllib2
import re
import shutil
import zipfile
import time

import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin

import plugintools
import json



addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")

home = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.palcotv/', ''))
tools = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.palcotv/resources/tools', ''))
addons = xbmc.translatePath(os.path.join('special://home/addons/', ''))
resources = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.palcotv/resources', ''))
art = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.palcotv/art', ''))
tmp = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.palcotv/tmp', ''))
playlists = xbmc.translatePath(os.path.join('special://home/addons/playlists', ''))


icon = art + 'icon.png'
fanart = 'fanart.jpg'



# Función que guía el proceso de elaboración de la URL original
def shidurlive(params):
    plugintools.log('[%s %s].Regex Shidurlive %s' % (addonName, addonVersion, repr(params))) 
    url_user = {}
    
    # Construimos diccionario...
    url = params.get("url")
    url_extracted = url.split(" ")
    for entry in url_extracted:
        if entry.startswith("rtmp"):
            entry = entry.replace("rtmp=", "")         
            url_user["rtmp"]=entry
        elif entry.startswith("playpath"):
            entry = entry.replace("playpath=", "")
            url_user["playpath"]=entry            
        elif entry.startswith("swfUrl"):
            entry = entry.replace("swfUrl=", "")
            url_user["swfurl"]=entry
        elif entry.startswith("pageUrl"):
            entry = entry.replace("pageUrl=", "")
            url_user["pageurl"]=entry          
        elif entry.startswith("token"):
            entry = entry.replace("token=", "")
            url_user["token"]=entry
        elif entry.startswith("referer"):
            entry = entry.replace("referer=", "")
            url_user["referer"]=entry

    plugintools.log("URL_user dict= "+repr(url_user)) 
    pageurl = url_user.get("pageurl")
    
    # Controlamos ambos casos de URL: Único link (pageUrl) o link completo rtmp://...
    if pageurl is None:
        pageurl = url_user.get("url")
        
    referer= url_user.get("referer")
    url_user["pageurl"]=pageurl
    print 'pageurl',pageurl
    print 'referer',referer
    body = gethttp_headers(pageurl, referer)
    plugintools.log("body= "+body)

    #src=http://www.shidurlive.com/stream/4e6a51324f54637a4e6a4d325a6a63324e6a55334d6a63354d7a453d/706c381d1202    
    src = re.compile('src=\"(.*?)\"').findall(body)
    print 'src',src
    url_user["pageurl"]=src[0]
    pageurl = url_user.get("pageurl")
    referer = url_user.get("referer")
    body = gethttp_headers(pageurl, referer)
    plugintools.log("body= "+body)
    getparams_shidurlive(url_user, body)
    url = url_user.get("rtmp") + ' playpath=' + url_user.get("playpath") + ' swfUrl=http://cdn.shidurlive.com/player.swf pageUrl=' + url_user.get("pageurl") + ' live=true timeout=15'
    plugintools.play_resolved_url(url)


# Vamos a hacer una llamada al pageUrl
def gethttp_headers(pageurl, referer):
      
    request_headers=[]
    request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
    request_headers.append(["Referer",referer])
    body,response_headers = plugintools.read_body_and_headers(pageurl, headers=request_headers)      
    plugintools.log("body= "+body)
    return body


# Iniciamos protocolo de elaboración de la URL original
# Capturamos parámetros correctos
def getparams_shidurlive(url_user, body):
    plugintools.log('[%s %s] getparams_shidurlive %s' % (addonName, addonVersion, repr(url_user))) 

    # Construimos el diccionario de 9stream
    streamer = re.compile("'streamer', '([^']*)").findall(body)
    url_user["rtmp"]=streamer[0]
    file = re.compile("'file', '([^']*)").findall(body)
    url_user["playpath"]=file[0]                          

    


