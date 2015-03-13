# -*- coding: utf-8 -*-
#------------------------------------------------------------
# PalcoTV Regex de 9straem
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
import math


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
def ninestreams(params):
    plugintools.log("[PalcoTV-0.3.0].ninestreams "+repr(params))
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
    if referer is None:
        referer = 'http://verdirectotv.com/tv/documentales/history.html'
    channel_id = re.compile('channel=([^&]*)').findall(pageurl)
    print channel_id
    channel_id = channel_id[0]
    # http://www.9stream.com/embedplayer.php?width=650&height=400&channel=143&autoplay=true

    if pageurl.find("embedplayer.php") >= 0:
        pageurl = 'http://www.9stream.com/embedplayer.php?width=650&height=400&channel=' + channel_id + '&autoplay=true'
        url_user["pageurl"]=pageurl
        print 'pageurl',pageurl
        print 'referer',referer
        body = gethttp_headers(pageurl, referer)
        body = ioncube1(body)
        getparams_ninestream(url_user, body)
        url = 'rtmp://' + url_user.get("ip") + ':1935/verdirectotvedge/_definst_/ app=verdirectotvedge/_definst_/?xs=' + url_user.get("ninetok") + ' playpath=' + url_user.get("playpath") + ' token=' + url_user.get("token") + ' flashver=WIN%2011,9,900,117 swfUrl=http://www.9stream.com/player/player_orig_XXXXX.swf pageUrl=' + url_user.get("pageurl") + ' live=1 swfVfy=1 timeout=10'
        plugintools.play_resolved_url(url)        
    else:
        pageurl = 'http://www.9stream.com/embedplayer_2.php?width=650&height=400&channel=' + channel_id + '&autoplay=true'
        url_user["pageurl"]=pageurl
        print 'pageurl',pageurl
        print 'referer',referer
        body = gethttp_headers(pageurl, referer)
        plugintools.log("body= "+body)
        body = ioncube1(body)
        getparams_ninestream(url_user, body)
        url = 'rtmp://' + url_user.get("ip") + ':1935/verdirectotvedge/_definst_/ app=verdirectotvedge/_definst_/?xs=' + url_user.get("ninetok") + ' playpath=' + url_user.get("playpath") + ' token=' + url_user.get("token") + ' flashver=WIN%2011,9,900,117 swfUrl=http://www.9stream.com/player/player_orig_XXXXX.swf pageUrl=' + url_user.get("pageurl") + ' live=1 swfVfy=1 timeout=10'
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
def getparams_ninestream(url_user, body):
    plugintools.log("[PalcoTV-0.3.0].getparams_ninestream " + repr(url_user) )

    # Construimos el diccionario de 9stream
    entry = plugintools.find_single_match(body, 'setStream(token) {(.*?)}')
    ip = re.compile('rtmp:....([^:]*)').findall(body)   
    url_user["ip"]=str(ip[0])
    plugintools.log("IP= "+str(ip[0]))
    xs = re.compile('xs=(.*?)"').findall(body)
    ninetok = xs[0]
    url_user["xs"] = ninetok
    decoded = url_user.get("pageurl")
    playpath = getfile_ninestream(url_user, decoded, body)   
    playpath = playpath[0]
    # ninetok = xs[0] + './' + playpath
    ninetok = xs[0]
    url_user["ninetok"]=ninetok
    plugintools.log("xs= "+ninetok)
    url_user["xs"] = ninetok
    url_user["playpath"]=playpath
    decoded=re.compile('getJSON\("(.*?)"').findall(body)
    decoded=decoded[0]
    print url_user
    token = get_fileserver(decoded, url_user)
    token = token[0]
    url_user["token"]=token



 

# Vamos a capturar el playpath
def getfile_ninestream(url_user, decoded, body):
    plugintools.log("PalcoTV getfile_ninestream( "+repr(url_user))
    referer = url_user.get("referer")
    req = urllib2.Request(decoded)
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36')
    req.add_header('Referer', referer)
    response = urllib2.urlopen(req)
    print response
    data = response.read()
    print data
    file = re.compile("file': '([^.]*)").findall(data)
    print 'file',file
    return file


# Vamos a capturar el fileserver.php (token del server)
def get_fileserver(decoded, url_user):
    plugintools.log("PalcoTV fileserver "+repr(url_user))
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


def ioncube1(body):
    plugintools.log("[PalcoTV-0.3.03.ioncube ")
    p = re.compile(ur'<script language=javascript>(.*?)<\/script>')
    result=re.findall(p, body)
    p = re.compile(ur'eval\(unescape\(\'?"?"(.*?)\'?"?\)\)')
    result=re.findall(p, str(result))
    import urllib
    result = urllib.unquote_plus(str(result))
    plugintools.log("result= "+result)
    p = re.compile('c="([^"]+)')
    valc=re.findall(p, body)
    valc=valc[0]
    plugintools.log("valc= "+valc)
    p = re.compile('x\("([^"]+)')
    valx=re.findall(p, body);
    valx=valx[0];
    plugintools.log("valx= "+valx)
    d="";
    int1 = 0;
    while int1 < len(valc):
        if int1%3==0:
            d+="%";
        else:
            d+=valc[int1];
            
        int1 += 1
        plugintools.log("d= "+d)
        
    valc=urllib.unquote_plus(str(d))
    print 'valc',valc
    plugintools.log("valc= "+valc)
    valt=re.compile('t=Array\(([0-9,]+)\)').findall(valc)
    print 'valt',valt
    valz=valez(valx,valt);
    print 'valz',valz
    p=re.compile('(getJSON\(|streamer|file|flash\'?"?,?\s?src)\'?"?\s?:?\s?\'?"?([^\'"]+)')
    vals=re.findall(p,valz)
    print 'vals',vals
    tkserv=vals[0][1]
    strmr=vals[1][1].replace("\/","/")
    plpath=vals[2][1].replace(".flv","");
    swf=vals[3][1];
    print tkserv+"\n"+strmr+"\n"+plpath+"\n"+swf
    print vals;
    print valz;
    print "DATA = "+valz;
        
        
def valez(valx,tS,b=1024,p=0,s=0,w=0):
    print 'tS',tS
    l=len(valx)
    tS = tS[0]
    valt=tS.split(',')
    valr=[]

    for j in range(int(math.ceil(l/b)),0, -1):
        for i in range(min(l,b),0, -1):
            w |= int(valt[ord(valx[p])-48]) << s
            p += 1
            if (s):
                valr.append(chr(165 ^ w & 255))
                w >>= 8
                s -= 2
            else:
                s = 6
                l -=1

        valr = ''.join(valr)
        plugintools.log("valr= "+valr)
        return valr
	    
#6ik3cdsewu48nt1

    


