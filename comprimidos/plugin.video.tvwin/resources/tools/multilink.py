# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Arena+ - XBMC Add-on by Juarrox (juarrox@gmail.com)
# Version 0.2.99 (17.10.2014)
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Gracias a la librería plugintools de Jesús (www.mimediacenter.info

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

import plugintools, nstream, ioncube

from framescrape import *
from resources.tools.resolvers import *
from resources.tools.update import *
from resources.tools.vaughnlive import *
from resources.tools.ninestream import *
from resources.tools.vercosas import *
from resources.tools.directwatch import *
from resources.tools.freetvcast import *
from resources.tools.freebroadcast import *
from resources.tools.shidurlive import *
from resources.tools.updater import *
from resources.tools.castalba import *
from resources.tools.castdos import *
from resources.tools.updater import *
from resources.tools.resolvers import *
from resources.tools.mundoplus import *


icon = art + 'icon.png'
fanart = 'fanart.jpg'



def get_server(params):
    plugintools.log('[%s %s].get_server %s' % (addonName, addonVersion, repr(params)))

    show = params.get("page")
    if show == "":
        show = "list"            
    plugintools.modo_vista(show)
    
    url = params.get("url")

    
    if url.find("iguide.to") >= 0:
        iguide(params)

    elif url.find("freetvcast.pw") >= 0:
        from resources.tools.freetvcast import *		
        freetvcast(params)  
		
    elif url.find("streamingfreetv") >= 0:
        from resources.tools.streamingfreetv import *	
        streamingfreetv(params)  		

    elif url.find("9stream") >= 0:
        from resources.tools.ninestream import *
        ninestreams(params)

    elif url.find("freebroadcast") >= 0:
        from resources.tools.freebroadcast import *	
        freebroadcast(params)   

    elif url.find("cast247") >= 0:
        from resources.tools.castdos import *
        castdos(params)

    elif url.find("castalba") >= 0:
        from resources.tools.castalba import *
        castalba(params)     

    elif url.find("direct2watch") >= 0:
        from resources.tools.directwatch import *
        directwatch(params)
    
    elif url.find("vaughnlive") >= 0:
        from resources.tools.vaughnlive import *
        resolve_vaughnlive(params)

    elif url.find("shidurlive") >= 0:
        from resources.tools.shidurlive import *
        shidurlive(params)      
    
    elif url.find("vercosas") >= 0:
        from resources.tools.vercosas import *
        vercosasgratis(params)
        
    elif url.startswith("serie") >= 0:
        if url.find("seriesadicto") >= 0:
            from resources.tools.seriesadicto import *
            seriecatcher(params)
            
        elif url.find("seriesflv") >= 0:
            from resources.tools.seriesflv import *
            lista_capis(params)

        elif url.find("seriesyonkis") >= 0:
            from resources.tools.seriesyonkis import *
            serie_capis(params)

        elif url.find("seriesblanco") >= 0:
            from resources.tools.seriesblanco import *
            seriesblanco0(params)

        elif url.find("seriesmu") >= 0:
            from resources.tools.seriesblanco import *
            seriesmu0(params)            

    elif url.startswith("wuarron") >= 0:
        from resources.tools.wuarron import *
        url = url.strip()
        params["url"]=url
        wuarron_token(params)

    elif url.startswith("bum") >= 0:
        from resources.tools.bum import *
        url = url.strip()
        title = title.replace(" [COLOR lightyellow][I][BUM+][/COLOR]", "").strip()
        params["title"]=title
        params["url"]=url
        bum_multiparser(params)
 
    else:
	plugintools.play_resolved_url(url)




def play_url(url):
    plugintools.log("[PalcoTV-0.3.0].play "+url)

    params = plugintools.get_params()
    show = params.get("page")
    if show == "":
        show = "list"
    plugintools.modo_vista(show)
    
    # Notificación de inicio de resolver en caso de enlace RTMP
    url = url.strip()

    if url.startswith("http") == True:
        if url.find("allmyvideos") >= 0 :
            params = plugintools.get_params()
            params["url"]=url
            allmyvideos(params)
        elif url.find("streamcloud") >= 0 :
            params["url"]=url
            params["title"]=title
            params = plugintools.get_params() 
            streamcloud(params)
        elif url.find("vidspot") >= 0 :
            params = plugintools.get_params()
            params["url"]=url
            vidspot(params)
        elif url.find("played.to") >= 0 :
            params = plugintools.get_params()
            params["url"]=url
            playedto(params)
        elif url.find("vk.com") >= 0 :
            params = plugintools.get_params()
            params["url"]=url
            vk(params)
        elif url.find("nowvideo") >= 0 :
            params = plugintools.get_params()
            params["url"]=url
            nowvideo(params)
        elif url.find("tumi") >= 0 :
            params = plugintools.get_params()
            params["url"]=url
            tumi(params)
        elif url.find("streamin.to") >= 0 :
            params = plugintools.get_params()
            params["url"]=url
            streaminto(params)
        elif url.find("veehd") >= 0 :
            params = plugintools.get_params()
            params["url"]=url
            veehd(params)             
        else:
            url = url.strip()
            plugintools.play_resolved_url(url)

    elif url.startswith("rtp") >= 0:  # Control para enlaces de Movistar TV
        plugintools.play_resolved_url(url)
       
    else:
        plugintools.play_resolved_url(url)


        
       

def url_analyzer(url):
    plugintools.log("[Arena+ URL_Analyzer] "+url)

    params = plugintools.get_params()
    plugintools.log("params = "+repr(params))

    if url == "mundoplus":
        mundoplus_guide(params)
    
    elif url.startswith("goear") == True:
        id_goear = url.replace("goear:", "").replace('"', "").strip()
        url = 'http://www.goear.com/action/sound/get/'+id_goear
        plugintools.log("url= "+url)
        params["url"]=url.strip()
        play_resolved_url(url)
        
    elif url.startswith("serie") == True:
        if url.find("seriesflv") >= 0:
            from resources.tools.seriesflv import *
            url = url.replace("serie:", "")
            show = plugintools.get_setting("series_id")
            params = plugintools.get_params()
            params["url"]=url.strip()
            params["page"]=show
            plugintools.modo_vista(show)            
            lista_capis(params)
        elif url.find("seriesyonkis") >= 0:
            from resources.tools.seriesyonkis import *
            url = url.replace("serie:", "")
            show = plugintools.get_setting("series_id")
            params = plugintools.get_params()
            params["url"]=url.strip()
            plugintools.modo_vista(show)
            serie_capis(params)
        elif url.find("seriesadicto") >= 0:
            from resources.tools.seriesadicto import *
            url = url.replace("serie:", "")
            show = plugintools.get_setting("series_id")
            params = plugintools.get_params()
            params["url"]=url.strip()
            plugintools.modo_vista(show)            
            seriecatcher(params)
        elif url.find("seriesblanco") >= 0:
            from resources.tools.seriesblanco import *
            url = url.replace("serie:", "")
            show = plugintools.get_setting("series_id")
            params = plugintools.get_params()
            params["url"]=url.strip()
            plugintools.modo_vista(show)            
            seriesblanco0(params)
        elif url.find("series.mu") >= 0:
            from resources.tools.seriesmu import *
            url = url.replace("serie:", "")
            show = plugintools.get_setting("series_id")
            params = plugintools.get_params()
            params["page"]=show            
            params["url"]=url.strip()
            plugintools.modo_vista(show)            
            seriesmu0(params)            
        
    elif url.startswith("http") == True:        
        if url.find("allmyvideos") >= 0:
            params = plugintools.get_params()
            params["url"]=url
            allmyvideos(params)

        elif url.find("streamcloud") >= 0:                        
            params = plugintools.get_params()
            params["url"]=url
            streamcloud(params)

        elif url.find("vidspot") >= 0:
            params = plugintools.get_params()
            params["url"]=url
            vidspot(params)

        elif url.find("played.to") >= 0:
            params = plugintools.get_params()
            params["url"]=url
            playedto(params)       

        elif url.find("vk.com") >= 0:
            params = plugintools.get_params()
            params["url"]=url
            vk(params)

        elif url.find("nowvideo") >= 0:
            params = plugintools.get_params()
            params["url"]=url
            nowvideo(params)          
        
        elif url.find("tumi") >= 0:
            params = plugintools.get_params()
            params["url"]=url
            tumi(params)

        elif url.find("streamin.to") >= 0:
            params = plugintools.get_params()
            params["url"]=url
            streaminto(params)
            
        elif url.find("veehd") >= 0:
            params = plugintools.get_params()
            params["url"]=url
            veehd(params)              

        elif url.find("www.youtube.com") >= 0:
            plugintools.log("Youtube: "+url)
            videoid = url.replace("https://www.youtube.com/watch?v=", "")
            url = 'plugin://plugin.video.youtube/play/?video_id='+videoid
            url = url.strip()
            play_url(url)

        elif url.find(".m3u8") >= 0:
            plugintools.log("M3u8: "+url)
            url = url.strip()
            play_url(url)

        else:
            play_resolved_url(url)
            
    elif url.startswith("udp") == True:
        plugintools.log("UDP: "+url)
        url = url.strip()
        play_url(url)         
    
    elif url.startswith("rtp") == True:
        plugintools.log("RTP: "+url)
        url = url.strip()
        play_url(url)             
    
    elif url.startswith("mms") == True:
        plugintools.log("mms: "+url)
        url = url.strip()
        play_url(url)       

    elif url.startswith("plugin") == True:
        if url.find("youtube") >= 0 :
            plugintools.log("Youtube: "+url)
            url = url.strip()
            play_url(url)               
            
        elif url.find("mode=1") >= 0 :
            plugintools.log("Acestream: "+url)
            url = url.strip()
            play_url(url)
            
        elif url.find("mode=2") >= 0 :
            plugintools.log("Sopcast: "+url)
            url = url.strip()
            play_url(url)                
    elif url.startswith("magnet") == True:
        plugintools.log("Magnet link: "+url)
        url_fixed = urllib.quote_plus(data)
        url = 'plugin://plugin.video.xbmctorrent/play/' + url_fixed
        url = url.strip()
        play_url(url)

    elif url.startswith("sop") == True:
        plugintools.log("Sopcast: "+url)
        # plugin://plugin.video.p2p-streams/?url=sop://124.232.150.188:3912/11265&mode=2&name=Titulo+canal+Sopcast
        url = 'plugin://plugin.video.p2p-streams/?url=' + data + '&mode=2&name=' + title_fixed
        url = url.strip()
        play_url(url)
        
    elif url.startswith("ace") == True:
        plugintools.log("Acestream: "+url)
        url = url.replace("ace:", "")
        url = url.strip()
        url = 'plugin://plugin.video.p2p-streams/?url=' + url + '&mode=1&name='
        url = url.strip()
        play_url(url)                                         

    elif url.startswith("yt") == True:
        if url.startswith("yt_playlist") == True:
            plugintools.log("Youtube playlist: "+url)
            youtube_playlist = url.replace("yt_playlist(", "")
            youtube_playlist = youtube_playlist.replace(")", "")
            url = 'http://gdata.youtube.com/feeds/api/playlists/' + youtube_playlist
            url = url.strip()
            youtube_videos(url)            

        elif url.startswith("yt_channel") == True:
            plugintools.log("Youtube channel: "+url)
            youtube_channel = url.replace("yt_channel(", "")
            youtube_channel = youtube_channel.replace(")", "")
            url = 'http://gdata.youtube.com/feeds/api/users/' + youtube_channel + '/playlists?v=2&start-index=1&max-results=30'
            url = url.strip()
            youtube_playlists(url)
            
    elif url.startswith("rtmp") == True or url.startswith("rtsp") == True:
        params = plugintools.get_params()
        print params
        url = parse_url(url, show)
        params = plugintools.get_params()
        params["url"]=url
        get_server(params)
		
    elif url.startswith("wuarron") == True:
        url = url.replace("wuarron:", "")
        #url = parse_url(url, show)
        params = plugintools.get_params()
        params["url"]=url                
        get_server(params)
        from resources.tools.wuarron import *
        wuarron_token(params)

    elif url.startswith("bum") == True:
        params = plugintools.get_params()
        title = params.get("title")
        show = "list"
        title = multiparse_title(title, url, show)
        get_server(params)
        from resources.tools.bum import *
        bum_multiparser(params)
	
        
        

def youtube_playlists(url):
    plugintools.log('[%s %s].youtube_playlists %s' % (addonName, addonVersion, repr(params)))
    
    data = plugintools.read(url)
        
    pattern = ""
    matches = plugintools.find_multiple_matches(data,"<entry(.*?)</entry>")
    
    for entry in matches:
        plugintools.log("entry="+entry)
        
        title = plugintools.find_single_match(entry,"<titl[^>]+>([^<]+)</title>")
        plot = plugintools.find_single_match(entry,"<media\:descriptio[^>]+>([^<]+)</media\:description>")
        thumbnail = plugintools.find_single_match(entry,"<media\:thumbnail url='([^']+)'")           
        url = plugintools.find_single_match(entry,"<content type\='application/atom\+xml\;type\=feed' src='([^']+)'/>")
        fanart = art + 'youtube.png'
        
        plugintools.add_item( action="youtube_videos" , title=title , plot=plot , url=url , thumbnail=thumbnail , fanart=fanart , folder=True )
        plugintools.log("fanart= "+fanart)


# Muestra todos los vídeos del playlist de Youtube
def youtube_videos(url):
    plugintools.log("[Arena+ 0.3.2].youtube_videos "+url)
    
    # Fetch video list from YouTube feed
    data = plugintools.read(url)
    plugintools.log("data= "+data)
    
    # Extract items from feed
    pattern = ""
    matches = plugintools.find_multiple_matches(data,"<entry(.*?)</entry>")
    
    for entry in matches:
        plugintools.log("entry="+entry)
        
        # Not the better way to parse XML, but clean and easy
        title = plugintools.find_single_match(entry,"<titl[^>]+>([^<]+)</title>")
        title = title.replace("I Love Handball | ","")
        plot = plugintools.find_single_match(entry,"<summa[^>]+>([^<]+)</summa")
        thumbnail = plugintools.find_single_match(entry,"<media\:thumbnail url='([^']+)'")
        fanart = art+'youtube.png'
        video_id = plugintools.find_single_match(entry,"http\://www.youtube.com/watch\?v\=([0-9A-Za-z_-]{11})")
        url = "plugin://plugin.video.youtube/?path=/root/video&action=play_video&videoid="+video_id

        # Appends a new item to the xbmc item list
        plugintools.add_item( action="play" , title=title , plot=plot , url=url , thumbnail=thumbnail , fanart=fanart , isPlayable=True, folder=False )


def parse_url(url, show):
    plugintools.modo_vista(show)
    if url != "":
        url = url.strip()
        url = url.replace("rtmp://$OPT:rtmp-raw=", "")        
        return url
    
    else:
        plugintools.log("error en url= ")  # Mostrar diálogo de error al parsear url (por no existir, por ejemplo)


def multiparser(params):
    plugintools.log('[%s %s].Multiparser %s' % (addonName, addonVersion, repr(params)))
    dialog = xbmcgui.Dialog()

    show = params.get("page")  # Control de modo de vista predefinido
    if show == "":
        show = "list"
    else:
        plugintools.modo_vista(show)

    #info_plot = params["info_labels"]
    #print 'info_plot',info_plot

    filename = params.get("extra")
    plugintools.log("filename= "+filename)
    file = open(playlists + filename, "r")
    file.seek(0)
    title = params.get("title").replace("[Multiparser]", "").strip()
    title = parser_title(title)
    
    if title.find("  ") >= 0:
        title = title.split("  ")
        title = title[0].strip()
        title = "@"+title  # En la lista aparecerá el título precedido por el símbolo @
        plugintools.log("title_epg= "+title)
    
    encuentra = '#EXTINF:-1,' + title.replace(" [COLOR lightyellow][Multiparser][/COLOR]","")
    plugintools.log("*** Texto a buscar= "+encuentra)
    i = 0
    data = file.readline()
    print data
    while i <=8:  # Control para EOF
        if data == "":
            i = i + 1
            data = file.readline().strip()
            #print data
            continue
        else:
            i = 0
            if data.startswith(encuentra) == True:
                data = file.readline().strip()
                print data
                if data == "#multiparser":
                    #Leemos número de enlaces
                    i = 1  # Variable contador desde 1 porque nos servirá para nombrar los títulos
                    # Recopilamos enlaces en una lista
                    linea_url = file.readline().strip()
                    if linea_url.startswith("desc") == True:
                        linea_url = file.readline().strip()
                    
                    menu_seleccion = []                       
                    while linea_url != "#multiparser" :                         
                        linea_url = linea_url.strip().split(",")
                        url_option = linea_url[1]
                        title_option = linea_url[0]
                        
                        title_option = str(i) + ': ' + title_option
                        title_fixed = multiparse_title(title_option, url_option, show)
                        title_option = title_fixed
                        plugintools.log("title= "+title_option)
                        i = i + 1
                        menu_seleccion.append([title_option,url_option])
                        linea_url = file.readline()
                        linea_url = linea_url.strip()
                print menu_seleccion
                num_items = i - 1
                plugintools.log("Núm. items= "+str(num_items))
            else:                
                data = file.readline().strip()                
                
    # De una lista de 6 elementos, queremos meter en la lista items los elementos 0, 2 y 4 (pares) y en la lista urls los elementos 1, 3 y 5 (impares)
    i = 0
    channels = []
    items = []
       
    if num_items == 0:
        print "No hay enlaces"
    elif num_items == 1:
        print "Solo un enlace"
        selector = dialog.select(title, [menu_seleccion[0][0]])
    elif num_items == 2:
        selector = dialog.select(title, [menu_seleccion[0][0] , menu_seleccion[1][0]])
    elif num_items == 3:
        selector = dialog.select(title, [menu_seleccion[0][0] , menu_seleccion[1][0] , menu_seleccion[2][0]])
    elif num_items == 4:
        selector = dialog.select(title, [menu_seleccion[0][0] , menu_seleccion[1][0] , menu_seleccion[2][0] , menu_seleccion[3][0]])
    elif num_items == 5:
        selector = dialog.select(title, [menu_seleccion[0][0] , menu_seleccion[1][0] , menu_seleccion[2][0] , menu_seleccion[3][0] , menu_seleccion[4][0]])
    elif num_items == 6:
        selector = dialog.select(title, [menu_seleccion[0][0] , menu_seleccion[1][0] , menu_seleccion[2][0] , menu_seleccion[3][0] , menu_seleccion[4][0] , menu_seleccion[5][0]])
    elif num_items == 7:
        selector = dialog.select(title, [menu_seleccion[0][0] , menu_seleccion[1][0] , menu_seleccion[2][0] , menu_seleccion[3][0] , menu_seleccion[4][0] , menu_seleccion[5][0] , menu_seleccion[6][0]])
    elif num_items == 8:
        selector = dialog.select(title, [menu_seleccion[0][0] , menu_seleccion[1][0] , menu_seleccion[2][0] , menu_seleccion[3][0] , menu_seleccion[4][0] , menu_seleccion[5][0] , menu_seleccion[6][0] , menu_seleccion[7][0]])
    elif num_items == 9:
        selector = dialog.select(title, [menu_seleccion[0][0] , menu_seleccion[1][0] , menu_seleccion[2][0] , menu_seleccion[3][0] , menu_seleccion[4][0] , menu_seleccion[5][0] , menu_seleccion[6][0] , menu_seleccion[7][0] , menu_seleccion[8][0]])
    elif num_items == 10:
        selector = dialog.select(title, [menu_seleccion[0][0] , menu_seleccion[1][0] , menu_seleccion[2][0] , menu_seleccion[3][0] , menu_seleccion[4][0] , menu_seleccion[5][0] , menu_seleccion[6][0] , menu_seleccion[7][0] , menu_seleccion[8][0] , menu_seleccion[9][0]])
    elif num_items == 11:
        selector = dialog.select(title, [menu_seleccion[0][0] , menu_seleccion[1][0] , menu_seleccion[2][0] , menu_seleccion[3][0] , menu_seleccion[4][0] , menu_seleccion[5][0] , menu_seleccion[6][0] , menu_seleccion[7][0] , menu_seleccion[8][0] , menu_seleccion[9][0] , menu_seleccion[10][0]])
    elif num_items == 12:
        selector = dialog.select(title, [menu_seleccion[0][0] , menu_seleccion[1][0] , menu_seleccion[2][0] , menu_seleccion[3][0] , menu_seleccion[4][0] , menu_seleccion[5][0] , menu_seleccion[6][0] , menu_seleccion[7][0] , menu_seleccion[8][0] , menu_seleccion[9][0] , menu_seleccion[10][0], menu_seleccion[11][0]])
  
    if selector == 0:
        url_analyzer(menu_seleccion[0][1])
    elif selector == 1:
        url_analyzer(menu_seleccion[1][1])
    elif selector == 2:
        url_analyzer(menu_seleccion[2][1])
    elif selector == 3:
        url_analyzer(menu_seleccion[3][1])
    elif selector == 4:
        url_analyzer(menu_seleccion[4][1])
    elif selector == 5:
        url_analyzer(menu_seleccion[5][1])
    elif selector == 6:
        url_analyzer(menu_seleccion[6][1])
    elif selector == 7:
        url_analyzer(menu_seleccion[7][1])
    elif selector == 8:
        url_analyzer(menu_seleccion[8][1])
    elif selector == 9:
        url_analyzer(menu_seleccion[9][1])
    elif selector == 10:
        url_analyzer(menu_seleccion[10][1])

    plugintools.modo_vista(show)


# Esta función añade coletilla de tipo de enlace a los multilink
def multiparse_title(title, url, show):
    
    if show == "":
        show = "list"
        plugintools.modo_vista(show)

    if url == "mundoplus":
        title = title + ' [COLOR lightyellow][I][Agenda[B]TV[/B]][/I][/COLOR]' 

    elif url.startswith("serie") == True:
        if url.find("seriesflv") >= 0:
            title = title + ' [COLOR lightyellow][I][Series[B]FLV[/B]][/I][/COLOR]'
        if url.find("seriesyonkis") >= 0:
            title = title + ' [COLOR lightyellow][I][Series[B]Yonkis[/B]][/I][/COLOR]'
        if url.find("seriesadicto") >= 0:
            title = title + ' [COLOR lightyellow][I][Series[B]Adicto[/B]][/I][/COLOR]'
        if url.find("seriesblanco") >= 0:
            title = title + ' [COLOR lightyellow][I][Series[B]Blanco[/B]][/I][/COLOR]'
        if url.find("series.mu") >= 0:
            title = title + ' [COLOR lightyellow][I][Series[B].Mu[/B]][/I][/COLOR]'            

    elif url.startswith("wuarron") == True:
        title = title + ' [COLOR lightyellow][I][Wuarron][/I][/COLOR]'            

    elif url.startswith("goear") == True:
        title = title + ' [COLOR lightyellow][I][goear][/I][/COLOR]'        

    elif url.startswith("http") == True:        
        if url.find("allmyvideos") >= 0:
            title = title + ' [COLOR lightyellow][I][Allmyvideos][/I][/COLOR]'

        elif url.find("streamcloud") >= 0:
            title = title + ' [COLOR lightyellow][I][Streamcloud][/I][/COLOR]'

        elif url.find("vidspot") >= 0:
            title = title + ' [COLOR lightyellow][I][Vidspot][/I][/COLOR]'
            
        elif url.find("played.to") >= 0:
            title = title + ' [COLOR lightyellow][I][Played.to][/I][/COLOR]'       

        elif url.find("vk.com") >= 0:
            title = title + ' [COLOR lightyellow][I][Vk][/I][/COLOR]'

        elif url.find("nowvideo") >= 0:
            title = title + ' [COLOR lightyellow][I][Nowvideo.sx][/I][/COLOR]'            
        
        elif url.find("tumi") >= 0:
            title = title + ' [COLOR lightyellow][I][Tumi][/I][/COLOR]'

        elif url.find("streamin.to") >= 0:
            title = title + ' [COLOR lightyellow][I][Streamin.to][/I][/COLOR]'

        elif url.find("veehd") >= 0:
            title = title + ' [COLOR lightyellow][I][Veehd][/I][/COLOR]'            

        elif url.find("www.youtube.com") >= 0:
            title = title + ' [COLOR lightyellow][I][Youtube][/I][/COLOR]'

        elif url.find(".m3u8") >= 0:
            title = title + ' [COLOR lightyellow][I][M3u8][/I][/COLOR]'
            
    elif url.startswith("udp") == True:
        title = title + ' [COLOR lightyellow][I][udp][/I][/COLOR]'         
    
    elif url.startswith("rtp") == True:
        title = title + ' [COLOR lightyellow][I][rtp][/I][/COLOR]'            
    
    elif url.startswith("mms") == True:
        title = title + ' [COLOR lightyellow][I][mms][/I][/COLOR]'      

    elif url.startswith("plugin") == True:
        if url.find("youtube") >= 0 :
            title = title + ' [COLOR lightyellow][I][Youtube][/I][/COLOR]'
            
        elif url.find("mode=1") >= 0 :
            title = title + ' [COLOR lightyellow][I][Acestream][/I][/COLOR]'
            
        elif url.find("mode=2") >= 0 :
            title = title + ' [COLOR lightyellow][I][Sopcast][/I][/COLOR]'
            
    elif url.startswith("magnet") == True:
        title = title + ' [COLOR lightyellow][I][Torrent][/I][/COLOR]'

    elif url.startswith("sop") == True:
        title = title + ' [COLOR lightyellow][I][Sopcast][/I][/COLOR]'        
        
    elif url.startswith("ace") == True:
        title = title + ' [COLOR lightyellow][I][Acestream][/I][/COLOR]'

    elif url.startswith("yt") == True:
        if url.startswith("yt_playlist") == True:
            title = title + ' [COLOR lightyellow][I][Youtube Playlist][/I][/COLOR]'

        elif url.startswith("yt_channel") == True:
            title = title + ' [COLOR lightyellow][I][Youtube Channel][/I][/COLOR]'
            
    elif url.startswith("rtmp") == True or url.startswith("rtsp") == True:
        
        if url.find("iguide.to") >= 0:
            title = title + ' [COLOR lightyellow][I][iguide][/I][/COLOR]'
        elif url.find("freetvcast.pw") >= 0:
            title = title + ' [COLOR lightyellow[I][freetvcast][/I][/COLOR]'
        elif url.find("streamingfreetv") >= 0:
            title = title + ' [COLOR lightyellow][I][streamingfreetv][/I][/COLOR]'
        elif url.find("9stream") >= 0:
            title = title + ' [COLOR lightyellow][I][9stream][/I][/COLOR]'
        elif url.find("freebroadcast") >= 0:
            title = title + ' [COLOR lightyellow][I][freebroadcast][/I][/COLOR]'
        elif url.find("cast247") >= 0:
            title = title + ' [COLOR lightyellow][I][cast247][/I][/COLOR]'
        elif url.find("castalba") >= 0:
            title = title + ' [COLOR lightyellow][I][castalba][/I][/COLOR]'
        elif url.find("direct2watch") >= 0:
            title = title + ' [COLOR lightyellow][I][direct2watch][/I][/COLOR]'
        elif url.find("vaughnlive") >= 0:
            title = title + ' [COLOR lightyellow][I][vaughnlive][/I][/COLOR]'
        elif url.find("sawlive") >= 0:
            title = title + ' [COLOR lightyellow][I][sawlive][/I][/COLOR]'        
        elif url.find("shidurlive") >= 0:
            title = title + ' [COLOR lightyellow][I][shidurlive][/I][/COLOR]'
        elif url.find("vercosas") >= 0:
            title = title + ' [COLOR lightyellow][I][vercosas][/I][/COLOR]'
        else:
            title = title + ' [COLOR lightyellow][I][rtmp][/I][/COLOR]'

    elif url.startswith("bum") == True:
        title_fixed = title
        title = title + ' [COLOR lightyellow][I][BUM+][/I][/COLOR]'        
        params = plugintools.get_params()
        params["title"] = title_fixed
        plugintools.log("params_fixed = "+repr(params))
        
    else:
        title = title + ' [COLOR lightyellow][I][Unknown][/I][/COLOR]'

    plugintools.log("title_fixed= "+title)
    plugintools.log("url= "+url)
    return title
