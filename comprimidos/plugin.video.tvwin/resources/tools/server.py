# -*- coding: utf-8 -*-
#------------------------------------------------------------
# PalcoTV - XBMC Add-on by Juarrox (juarrox@gmail.com)
# Conectores multimedia para PalcoTV
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Gracias a las librerías de pelisalacarta de Jesús (www.mimediacenter.info)


import os
import sys
import urllib
import urllib2
import re
import string
import shutil
import zipfile
import time
import urlparse
import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin
import scrapertools, plugintools, unwise, unpackerjs

addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")

home = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.tvwin/', ''))
tools = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.tvwin/resources/tools', ''))
addons = xbmc.translatePath(os.path.join('special://home/addons/', ''))
resources = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.tvwin/resources', ''))
art = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.tvwin/art', ''))
tmp = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.tvwin/tmp', ''))
playlists = xbmc.translatePath(os.path.join('special://home/addons/playlists', ''))


icon = art + 'icon.png'
fanart = 'fanart.jpg'




    



def streaminto(params):
    plugintools.log('[%s %s] streaminto %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")
    if page_url.startswith("http://streamin.to/embed-") == False:
        videoid = plugintools.find_single_match(page_url,"streamin.to/([a-z0-9A-Z]+)")
        page_url = "http://streamin.to/embed-"+videoid+".html"

    plugintools.log("page_url= "+page_url)
    
    # Leemos el código web
    headers = {'user-agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14'}
    r = requests.get(page_url, headers=headers)
    data = r.text
        
    plugintools.log("data= "+data)
    if data == "File was deleted":
        xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "Archivo borrado!", 3 , art+'icon.png'))        
    else:        
        # TODO: Si "video not found" en data, mostrar mensaje "Archivo borrado!"
        patron_flv = 'file: "([^"]+)"'    
        patron_jpg = 'image: "(http://[^/]+/)'    
    try:
        host = scrapertools.get_match(data, patron_jpg)
        plugintools.log("[streaminto.py] host="+host)
        flv_url = scrapertools.get_match(data, patron_flv)
        plugintools.log("[streaminto.py] flv_url="+flv_url)
        flv = host+flv_url.split("=")[1]+"/v.flv"
        plugintools.log("[streaminto.py] flv="+flv)
        page_url = flv
    except:
        plugintools.log("[streaminto] opcion 2")
        op = plugintools.find_single_match(data,'<input type="hidden" name="op" value="([^"]+)"')
        plugintools.log("[streaminto] op="+op)
        usr_login = ""
        id = plugintools.find_single_match(data,'<input type="hidden" name="id" value="([^"]+)"')
        plugintools.log("[streaminto] id="+id)
        fname = plugintools.find_single_match(data,'<input type="hidden" name="fname" value="([^"]+)"')
        plugintools.log("[streaminto] fname="+fname)
        referer = plugintools.find_single_match(data,'<input type="hidden" name="referer" value="([^"]*)"')
        plugintools.log("[streaminto] referer="+referer)
        hashstring = plugintools.find_single_match(data,'<input type="hidden" name="hash" value="([^"]*)"')
        plugintools.log("[streaminto] hashstring="+hashstring)
        imhuman = plugintools.find_single_match(data,'<input type="submit" name="imhuman".*?value="([^"]+)"').replace(" ","+")
        plugintools.log("[streaminto] imhuman="+imhuman)
            
        import time
        time.sleep(10)
            
        # Lo pide una segunda vez, como si hubieras hecho click en el banner
        #op=download1&usr_login=&id=z3nnqbspjyne&fname=Coriolanus_DVDrip_Castellano_by_ARKONADA.avi&referer=&hash=nmnt74bh4dihf4zzkxfmw3ztykyfxb24&imhuman=Continue+to+Video
        post = "op="+op+"&usr_login="+usr_login+"&id="+id+"&fname="+fname+"&referer="+referer+"&hash="+hashstring+"&imhuman="+imhuman
        request_headers.append(["Referer",page_url])
        data_video = plugintools.read_body_and_headers( page_url , post=post, headers=request_headers )
        data_video = data_video[0]
        rtmp = plugintools.find_single_match(data_video, 'streamer: "([^"]+)"')
        print 'rtmp',rtmp
        video_id = plugintools.find_single_match(data_video, 'file: "([^"]+)"')
        print 'video_id',video_id
        swf = plugintools.find_single_match(data_video, 'src: "(.*?)"')
        print 'swf',swf
        page_url = rtmp+' swfUrl='+swf + ' playpath='+video_id+"/v.flv"  

    plugintools.play_resolved_url(page_url)    
    



