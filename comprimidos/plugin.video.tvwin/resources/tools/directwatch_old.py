# -*- coding: utf-8 -*-
#------------------------------------------------------------
# PalcoTV Regex de direct2watch
# Version 0.1 (17.10.2014)
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


home = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.palcotv-wip/', ''))
tools = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.palcotv-wip/resources/tools', ''))
addons = xbmc.translatePath(os.path.join('special://home/addons/', ''))
resources = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.palcotv-wip/resources', ''))
art = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.palcotv-wip/art', ''))
tmp = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.palcotv-wip/tmp', ''))
playlists = xbmc.translatePath(os.path.join('special://home/addons/playlists', ''))

icon = art + 'icon.png'
fanart = 'fanart.jpg'


# Función que guía el proceso de elaboración de la URL original
def directwatch(params):
    plugintools.log("[PalcoTV-0.3.0].directwatch "+repr(params))
    url_user = {}
    url_user["token"]='KUidj872jf9867123444'
    url_user["rtmp"]='rtmp://watch.direct2watch.com/direct2watch'
    url_user["swfurl"]='http://www.direct2watch.com/player/player2.swf'    
    
    
    # Construimos diccionario...
    url = params.get("url")
    url_extracted = url.split(" ")
    for entry in url_extracted:
        if entry.startswith("playpath"):
            entry = entry.replace("playpath=", "")
            url_user["playpath"]=entry            
        elif entry.startswith("pageUrl"):
            pageurl = entry.replace("pageUrl=", "")
            pageurl = pageurl.replace("&amp;", "&")
            url_user["pageurl"]=pageurl          
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
    if referer is None:
        referer = 'http://www.direct2watch.com'

    print 'pageurl',pageurl
    print 'referer',referer
    body = gethttp_headers(pageurl, referer)
    getparams_directwatch(url_user, body)



# Vamos a hacer una llamada al pageUrl
def gethttp_headers(pageurl, referer):
    plugintools.log("[PalcoTV-0.3.0].gethttp_headers")
      
    request_headers=[]
    request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
    request_headers.append(["Referer",referer])
    body,response_headers = plugintools.read_body_and_headers(pageurl, headers=request_headers)      
    plugintools.log("body= "+body)
    return body


                
# Iniciamos protocolo de elaboración de la URL original
# Capturamos parámetros correctos
def getparams_directwatch(url_user, body):
    plugintools.log("[PalcoTV-0.3.0].getparams_direct2watch " + repr(url_user) )

    # Construimos el diccionario de 9stream
    entry = plugintools.find_single_match(body, 'setStream(token) {(.*?)}')
    ip = re.compile('rtmp:....([^:]*)').findall(body)
    url_user["ip"]=str(ip[0])
    print 'ip',ip
    # plugintools.log("IP= "+str(ip[0]))
    xs = re.compile('xs=(.*?)"').findall(body)
    directwatchtok = xs[0]
    streamer = re.compile('streamer\': \"(.*?)\"').findall(body)
    print 'streamer',streamer
    streamer = streamer[0]
    streamer = streamer.split("xs=")
    url_user["rtmp"]=streamer[1]
    directwatchtok = xs[0]    
    url_user["xs"] = directwatchtok
    plugintools.log("xs= "+directwatchtok)
    decoded = url_user.get("pageurl")
    playpath = getfile_directwatch(url_user, decoded, body)   
    print 'playpath',playpath
    
    decoded=re.compile('getJSON\("(.*?)"').findall(body)
    decoded=decoded[0]
    token = get_fileserver(decoded, url_user)
    url_user["token"]=token[0]
    
    print url_user.get("playpath")
    print url_user.get("pageurl")
    print url_user.get("swfurl")
    print url_user.get("token")
    print url_user.get("rtmp")

    # rtmp://watch1.direct2watch.com:1935/direct2watch/_definst_/ app=direct2watch/_definst_/?xs=_we_dmh4OTZ5Y2ttcGF4cHE1fDE0MTI5ODUyMDR8ODMuNTcuMTcuNTd8NTQzODYzNjQ0OGE5MXw0M2U1MTMxYWMxZTQ4ZGNkZjU5ZDI4Yzg5NTUyZDhjZjAwMDYwN2Y4 playpath=vhx96yckmpaxpq5 token=h3736e224cac18ec4c393c393029e0c1 swfUrl=http://www.direct2watch.com/player/player_embed_iguide.swf pageUrl=http://www.direct2watch.com/embedplayer.php?width=653&height=400&channel=10&autoplay=true live=1 swfVfy=true timeout=10
    # rtmp://watch1.direct2watch.com:1935/direct2watch/_definst_/ app=directwatch/_definst_/?xs=_we_fDE0MTI5ODY5NDB8ODMuNTcuMTcuNTd8NTQzODZhMmM2YjBlMHxjNTA0ZjVhMDE4ZGY5ZWY4M2RhZWEwNDY5YzAzNDE5Y2ZmNTU2NzA0 playpath=vhx96yckmpaxpq5 token=se069e8f077eca5372c878eff5bd273c swfUrl=http://www.direct2watch.com/player/player2.swf pageUrl=http://www.direct2watch.com/embedplayer.php?width=653&amp;height=400&amp;channel=10&amp;autoplay=true live=1 swfVfy=truetimeout=10
    # rtmp://watch1.direct2watch.com:1935/direct2watch/_definst_/ app=direct2watch/_definst_/?xs=_we_dmh4OTZ5Y2ttcGF4cHE1fDE0MTI5ODcyMjl8ODMuNTcuMTcuNTd8NTQzODZiNGQ0YWI0NnxjYmVkODk3MzQzY2MyNWJiOWZiODgzNGI5MjhlYTJmNDY1MmZhNDA3 playpath=vhx96yckmpaxpq5 token=se069e8f077eca5372c878eff5bd273c swfUrl=http://www.direct2watch.com/player/player_embed_iguide.swf pageUrl=http://www.direct2watch.com/embedplayer.php?width=653&height=400&channel=10&autoplay=true live=1 swfVfy=true timeout=10
    # rtmp://watch1.direct2watch.com:1935/direct2watch/_definst_/ app=directwatch/_definst_/?xs=_we_fDE0MTI5ODczNDJ8ODMuNTcuMTcuNTd8NTQzODZiYmVlN2QxMHwzZmU0Mjc0NzkyMGI3MDg3YjI1Y2NiMGUxMjdhY2U3ZjM2ZGZmNWYz playpath=vhx96yckmpaxpq5 token=se069e8f077eca5372c878eff5bd273c swfUrl=http://www.direct2watch.com/player/player_embed_iguide.swf                      pageUrl=http://www.direct2watch.com/embedplayer.php?width=653&amp;height=400&amp;channel=10&amp;autoplay=true live=1 swfVfy=true timeout=10




    url = 'rtmp://watch1.direct2watch.com:1935/direct2watch/_definst_/ app=direct2watch/_definst_/?xs=' + url_user.get("rtmp") + ' playpath=' + url_user.get("playpath") + ' token=' + url_user.get("token") + ' swfUrl=http://www.direct2watch.com/player/player_embed_iguide.swf pageUrl=' + url_user.get("pageurl") + ' live=1 swfVfy=true timeout=10'
    plugintools.play_resolved_url(url)
 

# Vamos a capturar el playpath
def getfile_directwatch(url_user, decoded, body):
    plugintools.log("[PalcoTV-0.3.0].getfile_directwatch( "+repr(url_user))
    referer = url_user.get("referer")
    req = urllib2.Request(decoded)
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36')
    req.add_header('Referer', referer)
    response = urllib2.urlopen(req)
    print response
    data = response.read()
    print data
    file = re.compile('file(.*?)').findall(data)
    print 'file1',file
    return file


# Vamos a capturar el fileserver.php (token del server)
def get_fileserver(decoded, url_user):
    plugintools.log("PalcoTV get_fileserver "+repr(url_user))
    referer=url_user.get("pageurl")
    req = urllib2.Request(decoded)
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36')
    req.add_header('Referer',referer)
    response = urllib2.urlopen(req)
    print response
    data = response.read()
    print data
    token = re.compile('token":"(.*)"').findall(data)
    print 'token',token
    return token

def getfile_directwatch(url_user, decoded, body):
    plugintools.log("PalcoTV getfile_directwatch( "+repr(url_user))
    referer = url_user.get("referer")
    req = urllib2.Request(decoded)
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36')
    req.add_header('Referer', referer)
    response = urllib2.urlopen(req)
    print response
    data = response.read()
    print data
    file = re.compile("file': '([^.]*)").findall(data)
    print 'file2',file
    return file

    


