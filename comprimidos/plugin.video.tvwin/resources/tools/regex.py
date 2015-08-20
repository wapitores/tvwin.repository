# -*- coding: utf-8 -*-
#------------------------------------------------------------
# PalcoTV Regex de cast247
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
def castdos(params):
    plugintools.log('[%s %s].Regex cast247 %s' % (addonName, addonVersion, repr(params)))    
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

    if url_user.get("pageurl").find("domain=") <= 0:
        plugintools.log("URL_user dict= "+repr(url_user))
        pageurl = url_user.get("pageurl")
        body = gethttp_headers(pageurl)
        
        # Controlamos el caso de canal privado (requiere referer, por implementar)
        if body.find("Private Channel!") > 0 :
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "Canal privado", 3 , art+'icon.png'))
            return 0
        else:
            pageurl = re.compile('var sURL = \"(.*?)=\"').findall(body)
            pageurl = 'http://www.cast247.tv/' + pageurl[0]
            real_token = gethttp_headers(pageurl)

        # Iniciamos captura de parámetros
        streamer = re.compile('streamer: "(.*?)"').findall(body)
        file = re.compile('file: "(.*?)"').findall(body)

        url_user["rtmp"] = streamer[0]
        url_user["playpath"] = file[0]
        url_user["pageurl"] = pageurl
                
        # Construimos la URL original
        url = url_user.get("rtmp") + ' playpath=' + url_user.get("playpath") + ' live=1 timeout=20'
        url = url.strip()
        plugintools.log("url= "+url)
        plugintools.play_resolved_url(url)
        
    else:
        plugintools.log("URL_user dict= "+repr(url_user))
        # http://www.cast247.tv/embed.php?channel=plusjdskaks?&amp;width=670&amp;height=400&amp;domain=streamingfreetv.net
        # http://www.cast247.tv/embed.php?channel=plusjdskaks&width=670&height=400&domain=streamingfreetv.net (url_user)
        pageurl = url_user.get("pageurl")
        url_user["referer"]=pageurl
        width = plugintools.find_single_match(pageurl, 'width=(.*?)\&')
        height = plugintools.find_single_match(pageurl, 'height=(.*?)&')
        playpath = plugintools.find_single_match(pageurl, 'channel=(.*?\&')
        # playpath = url_user.get("playpath").split("?")
        playpath = re.compile('channel=(.*?)&').findall(pageurl)
        print 'width',width
        print 'height',height
        print 'channel',playpath
        new_playpath = playpath[0]
        domain = pageurl.split("=")
        i = len(domain)
        domain = domain[int(i)-1]
        new_pageurl = 'http://www.cast247.tv/embed.php?channel=' + new_playpath + '&width=' + width + '&height=' + height + '&domain=' + domain
        plugintools.log("new_pageurl= "+new_pageurl)
        url_user["pageurl"]=new_pageurl
        body = gethttp_referer_headers(url_user)
        plugintools.log("body= "+body)

        pageurl = re.compile('var sURL = \"(.*?)=\"').findall(body)
        pageurl = 'http://www.cast247.tv/' + pageurl[0]
        real_token = gethttp_headers(pageurl)        

        # Iniciamos captura de parámetros
        streamer = re.compile('streamer: "(.*?)"').findall(body)
        print 'streamer',streamer
        playpath = re.compile('file: "(.*?)"').findall(body)
        print 'playpath',playpath        
        url_user["rtmp"] = streamer[0]
        url_user["playpath"] = playpath[0]        

        # Construimos la URL original
        url = url_user.get("rtmp") + ' playpath=' + url_user.get("playpath") + ' live=1 timeout=20'
        url = url.strip()
        plugintools.log("url= "+url)
        plugintools.play_resolved_url(url)        
        


def castalba(params):
    plugintools.log("[PalcoTV-0.3.0].castalba "+repr(params))

    url = params.get("url")
    plugintools.play_resolved_url(url)


# Función que guía el proceso de elaboración de la URL original
def castalba(params):
    plugintools.log("[PalcoTV-0.3.0].castalba "+repr(params))
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
    body = gethttp_headers(pageurl)


    # Controlamos el caso de canal privado (requiere referer, por implementar)
    if body.find("THIS CHANNEL IS CURRENTLY OFFLINE") > 0 :
        xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "Canal offline", 3 , art+'icon.png'))
        return 0
    else:
    
        # Iniciamos captura de parámetros
        file = re.compile('file\': \'(.*?)\',').findall(body)
        if file[0].endswith("m3u8"):
            plugintools.play_resolved_url(file[0])
        else:
            streamer = re.compile('streamer\': \'(.*?)\',').findall(body)
            print 'file',file
            print 'streamer',streamer
            url_user["playpath"] = file[0]
            url_user["rtmp"] = streamer[0]            
            # Construimos la URL original
            url = url_user.get("rtmp") + ' playpath=' + url_user.get("playpath") + ' swfUrl=http://static.castalba.tv/player5.9.swf pageUrl=' + url_user.get("pageurl") + ' live=true timeout=15'
            url = url.strip()
            plugintools.log("url= "+url)
            plugintools.play_resolved_url(url)



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
        referer = 'http://www.vipracing.org'

    ref = referer
    body = gethttp_headers(pageurl, ref)
    
    nstr(pageurl,ref,body)



def nstr(pageurl,ref,body):
    plugintools.log("[PalcoTV 0.3.0].nstr")
    print 'pageurl',pageurl
    # http://www.direct2watch.com/embedplayer.php?width=653&height=410&channel=14&autoplay=true

    p1 = re.compile(ur'channel=?\'?"?([^\'"\&,;]+)')
    p2 = re.compile(ur'width=?\'?"?([^\'"\&,;]+)')
    p3 = re.compile(ur'height=?\'?"?([^\'"\&,;]+)')
    f1=re.findall(p1, pageurl);f2=re.findall(p2, pageurl);f3=re.findall(p3, pageurl);#res=list(set(f));
    print 'f1',f1
    print 'f2',f2
    print 'f3',f3
    c=f1[0];w=f2[0];h=f3[0]
    url='http://www.direct2watch.com/embedplayer.php?width='+w+'&height='+h+'&channel='+c+'&autoplay=true';body=''
    plugintools.log("url= "+url)
    plugintools.log("referer= "+ref)
    bodi=curl_frame(url,ref,body)
    print "\nURLXXX = "+url+"\nREFXXX = "+ref#+"\n"+bodi
    tkserv='';strmr='';plpath='';swf='';vala='';
    vals=ioncube.ioncube1(bodi)
    print "URL = "+url;print "REF = "+ref;
    tkserv=vals[0][1];strmr=vals[1][1].replace("\/","/");plpath=vals[2][1].replace(".flv","");swf=vals[3][1];
    ref=url;url=tkserv;bodi=curl_frame(url,ref,body);
    p='token":"([^"]+)';token=plugintools.find_single_match(bodi,p);#print token
    media_url = strmr+'/'+plpath+' swfUrl='+swf+' token='+token+' live=1 timeout=15 swfVfy=1 pageUrl='+ref
    plugintools.play_resolved_url(media_url)
    print media_url    

		
def curl_frame(url,ref,body):
	request_headers=[];
	request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
	request_headers.append(["Referer",ref])
	body,response_headers=plugintools.read_body_and_headers(url, headers=request_headers);
	return body

                                               

# Vamos a hacer una llamada a la página que nos dará el token
def gethttp_headers(pageurl):      
    request_headers=[]
    request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
    body,response_headers = plugintools.read_body_and_headers(pageurl, headers=request_headers)      
    plugintools.log("body= "+body)
    return body

	
def gethttp_referer_headers(url_user):
    pageurl = url_user.get("pageurl")
    referer = url_user.get("referer")
    print 'referer',referer
    request_headers=[]
    request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
    request_headers.append(["Referer", referer])
    body,response_headers = plugintools.read_body_and_headers(pageurl, headers=request_headers)      
    plugintools.log("body= "+body)
    return body
