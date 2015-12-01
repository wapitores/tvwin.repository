# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Parser de music
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


referer = 'http://www.seriesflv.com/'
art = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.tvwin/art', ''))
thumbnail = 'http://aldocarranza.hol.es/wp-content/uploads/2014/07/iTunes-icon-150x150.png'
fanart = 'https://scontent-dfw1-1.xx.fbcdn.net/hphotos-xft1/v/t34.0-12/12285778_985198441503202_2143109109_n.jpg?oh=dc0f1b7faa87f9f35811587fb8796dd6&oe=565B4C2D'
lista = 'http://icon-icons.com/icons2/159/PNG/256/list_tasks_22372.png'




def search5(params):
    dialog = xbmcgui.Dialog()
    selector = dialog.select('TvWin', ['Busqueda por cancion', 'Busqueda por artista'])
    if selector == 0:
        texto = plugintools.keyboard_input()
        plugintools.set_setting("last_search",texto)
        busqueda = 'http://www.goear.com/apps/android/search_songs_json.php?q='+ texto
        busqueda  = busqueda.replace(' ', "+")
        data = gethttp_referer_headers(busqueda,referer)
        if "id" in data:
           plugintools.log("busqueda= "+busqueda)
           songs = plugintools.find_multiple_matches(data, '{(.*?)}')
           for entry in songs:
            plugintools.log("entry= "+entry)
            id_song = plugintools.find_single_match(entry, '"id":"([^"]+)')
            plugintools.log("id_song= "+id_song)
            title_song = plugintools.find_single_match(entry, '"title":"([^"]+)')
            title_song = title_song.upper()
            plugintools.log("title_song= "+title_song)
            songtime = plugintools.find_single_match(entry, '"songtime":"([^"]+)')
            plugintools.log("songtime= "+songtime)
            url='http://www.goear.com/action/sound/get/'+id_song
            plugintools.log("url= "+url)
            plugintools.add_item(action="play", title = title_song + " " +'[COLOR orange] ('+songtime+')[/COLOR]', url=url, thumbnail = thumbnail , fanart = fanart , folder = False, isPlayable = True)
        elif "0" in data:
             errormsg = plugintools.message("TvWin","Sin resultados")
             search5(params)
    if selector == 1:
        texto = plugintools.keyboard_input()
        plugintools.set_setting("last_search",texto)
        url = 'http://www.goear.com/apps/android/search_playlist_json.php?q='+texto
        plugintools.log("url= "+url)
        url2  = url.replace(' ', "+")
        data = gethttp_referer_headers(url2,referer)
        if "id" in data:
           songs = plugintools.find_multiple_matches(data, '{(.*?)}')
           i = 1
           for entry in songs:
            plugintools.log("entry= "+entry)
            id_song = plugintools.find_single_match(entry, '"id":"([^"]+)')
            plugintools.log("id_song= "+id_song)
            url = 'http://www.goear.com/apps/android/playlist_songs_json.php?v='+id_song 
            title_song = plugintools.find_single_match(entry, '"title":"([^"]+)')
            title_song = title_song.upper()			
            plugintools.log("title_song= "+title_song)
            plsongs = plugintools.find_single_match(entry, '"plsongs":"([^"]+)"')
            songtime = plugintools.find_single_match(entry, '"songtime":"([^"]+)')
            plugintools.add_item(action="songs2", title = title_song + " " + '[COLOR red]('+ plsongs +')[/COLOR]' + 'ITEMS' + '[COLOR orange] ('+songtime+')[/COLOR]' +  'DURACION'  , url = url , thumbnail = lista , fanart = fanart  , folder = True, isPlayable = False)
            i = i + 1			
        elif "0" in data:
             errormsg = plugintools.message("TvWin","Sin resultados")
             search5(params)		
           

		   
		   
def songs2(params):
        url = params.get("url")
        data = gethttp_referer_headers(url,referer)
        songs2 = plugintools.find_multiple_matches(data, '{(.*?)}')
        i = 1
        for entry in songs2:
            plugintools.log("entry= "+entry)
            id_song = plugintools.find_single_match(entry, '"id":"([^"]+)')
            plugintools.log("id_song= "+id_song)
            title_song = plugintools.find_single_match(entry, '"title":"([^"]+)')
            title_song = title_song.upper()
            plugintools.log("title_song= "+title_song)
            songtime = plugintools.find_single_match(entry, '"songtime":"([^"]+)')
            plugintools.log("songtime= "+songtime)
            url='http://www.goear.com/action/sound/get/'+id_song
            plugintools.log("url= "+url)
            plugintools.add_item(action="play", title = title_song + " " +'[COLOR orange] ('+songtime+')[/COLOR]', url=url, thumbnail = thumbnail , fanart = fanart , folder = False, isPlayable = True)
            i = i + 1


def karao(params):
    url = params.get("url")
    data = gethttp_referer_headers(url,referer)
    SongLists = plugintools.find_multiple_matches(data, '<li><a(.*?)</a>')
    for entry in SongLists:
            
            id_song = plugintools.find_single_match(entry, '"id":"([^"]+)')
            plugintools.log("id_song= "+id_song)
            url = plugintools.find_single_match(entry, '"title":"([^"]+)')
            title_song = title_song.upper()
            plugintools.log("title_song= "+title_song)
            songtime = plugintools.find_single_match(entry, '"songtime":"([^"]+)')
            plugintools.log("songtime= "+songtime)
            url='http://www.goear.com/action/sound/get/'+id_song
            plugintools.log("url= "+url)
            plugintools.add_item(action="play", title = title , url = url, thumbnail = thumbnail , fanart = fanart , folder = False, isPlayable = True)
           





def gethttp_referer_headers(url,referer):    
    request_headers=[]
    request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
    request_headers.append(["Referer", referer])    
    body,response_headers = plugintools.read_body_and_headers(url, headers=request_headers)
    return body