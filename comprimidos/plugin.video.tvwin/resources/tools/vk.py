# -*- coding: utf-8 -*-
#------------------------------------------------------------
# tvwin - XBMC Add-on by 19hdz19
# Version 0.1.0 (18.07.2014)
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Librerías Plugintools por Jesús (www.mimediacenter.info)


import os
import sys
import urllib
import urllib2
import re
import shutil
import zipfile

import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin

import plugintools


home = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.tvwin/', ''))
tools = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.tvwin/resources/tools', ''))
addons = xbmc.translatePath(os.path.join('special://home/addons/', ''))
resources = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.tvwin/resources', ''))
art = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.tvwin/art', ''))
tmp = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.tvwin/tmp', ''))
playlists = xbmc.translatePath(os.path.join('special://home/addons/playlists', ''))

icon = art + 'icon.png'
fanart = 'fanart.jpg'


def vk(params):
    plugintools.log("[tvwin-0.1.0].vk " + repr(params))

    # http://vk.com/video_ext.php?oid=238208017&id=169663934&hash=1fc3ef827b751943&hd=1

    data = plugintools.read(params.get("url"))
    data = data.replace("amp;", "")
    
    if "This video has been removed from public access" in data:
        xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('TvWin', "El archivo ya no está disponible", 3 , art+'s.png'))
    else:
        match = plugintools.find_single_match(data, '<param name="flashvars"(.*?)</param>')
        plugintools.log("match= "+match)
        matches = plugintools.find_multiple_matches(match, 'vkid(.*?)&')
        for entry in matches:
            plugintools.log("match= "+entry)

        video_host = plugintools.find_single_match(data, 'var video_host = \'(.*?)\';')
        print 'video_host',video_host
        video_uid = plugintools.find_single_match(data, 'var video_uid = \'(.*?)\';')
        print 'video_uid',video_uid        
        video_vtag = plugintools.find_single_match(data, 'var video_vtag = \'(.*?)\';')
        print 'video_vtag',video_vtag        
        video_no_flv = plugintools.find_single_match(data, 'var video_no_flv = \'(.*?)\';')
        print 'video_no_flv',video_no_flv        
        video_max_hd = plugintools.find_single_match(data, 'var video_max_hd = \'(.*?)\';')
        print 'video_max_hd',video_max_hd

        if video_no_flv.strip() == "0" and video_uid != "0":
            media = 'flv'

        url_sintax = video_host + video_uid + '/video/' + video_vtag
        plugintools.log("url_sintax= "+url_sintax)

        # Control para el caso en que no se encuentren los parámetros por "Acceso prohibido o restringido"
        if url_sintax == "/video":
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('TvWin', "El archivo ya no está disponible", 3 , art+'s.png'))
        else:            
            url_1 = url_sintax + '.240.mp4'
            url_extended_1 = plugintools.find_single_match(match, 'url240=(.*?)\&')
            url_2 = url_sintax + '.360.mp4'
            url_extended_2 = plugintools.find_single_match(match, 'url360=(.*?)\&')
            url_3 = url_sintax + '.480.mp4'
            url_extended_3 = plugintools.find_single_match(match, 'url480=(.*?)\&')
            url_4 = url_sintax + '.720.mp4'
            url_extended_4 = plugintools.find_single_match(match, 'url720=(.*?)\&')

            video_urls = [url_extended_1, url_extended_2, url_extended_3, url_extended_4]
            print video_urls
            
            dialog_vk = xbmcgui.Dialog()
            selector = ""        
            
            if video_max_hd == "0":
                selector = dialog_vk.select('tvwin', ['240'])

            if video_max_hd == "1":
                selector = dialog_vk.select('tvwin', ['240', '360'])

            if video_max_hd == "2":
                selector = dialog_vk.select('tvwin', ['240', '360', '480'])

            if video_max_hd == "3":
                selector = dialog_vk.select('tvwin', ['240', '360', '480', '720'])                      

            i = 0
            while i<= video_max_hd :
                if selector == i:
                    plugintools.log("URL_vk= "+video_urls[i])
                    url = video_urls[i]
                    if selector == "":
                        xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('TvWin', "El archivo ya no está disponible", 3 , art+'s.png'))
                    else:
                        plugintools.play_resolved_url(url)
                        xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Tvwin', "Cargando Capitulo......", 1 , art+'s.png'))
                i = i + 1


