# -*- coding: utf-8 -*-
#------------------------------------------------------------
# TvWin - Kodi Addon 
# Version 2.1.0 (22.04.2015)
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Gracias a las librerías de Jesús para pelisalacarta (www.mimediacenter.info)


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

import plugintools, nstream, ioncube, scrapertools, unwise
import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmc,xbmcaddon,HTMLParser,os,sys,time,random  # PDF Reader
h = HTMLParser.HTMLParser()

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
from resources.tools.streamingfreetv import *
from resources.tools.dailymotion import *

from resources.tools.getposter import *
from resources.tools.yt_playlist import *
from resources.tools.seriesflv import *
from resources.tools.pelisyaske import *
from resources.tools.seriesblanco import *
from resources.tools.seriesmu import *

from resources.tools.sawlive import *
from resources.tools.goear import *
from resources.tools.moviedb import *
from resources.tools.mundoplus import *
from resources.tools.server import *




addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")
                                     
home = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.tvwin/', ''))
tools = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.tvwin/resources/tools', ''))
addons = xbmc.translatePath(os.path.join('special://home/addons/', ''))
art = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.tvwin/art', ''))
cbx_pages = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.tvwin/art/cbx', ''))
tmp = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.tvwin/tmp', ''))
playlists = xbmc.translatePath(os.path.join('special://home/addons/playlists', ''))


icon = art + 'icon.png'
fanart = 'fanart.jpg'

LIST = "list"
THUMBNAIL = "thumbnail"
MOVIES = "movies"
TV_SHOWS = "tvshows"
SEASONS = "seasons"
EPISODES = "episodes"
OTHER = "other"


# Entry point
def run():
    plugintools.log('[%s %s] Initializing... ' % (addonName, addonVersion))
    plugintools.set_view(THUMBNAIL)

    # Obteniendo parámetros...
    params = plugintools.get_params()

    if params.get("action") is None:
        main_list(params)
    else:
       action = params.get("action")
       url = params.get("url")
       exec action+"(params)"

    if not os.path.exists(playlists) :
        os.makedirs(playlists)

    plugintools.close_item_list()



# Main menu

def main_list(params):
    plugintools.log('[%s %s].main_list %s' % (addonName, addonVersion, repr(params)))

    # Control del skin de TvWin
    mastermenu = xml_skin()
    plugintools.log("XML menu: "+mastermenu)
    try:
        data = plugintools.read(mastermenu)
    except:
        xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('TvWin', "Usuario no reconocido...", 3 , art+'icon.png'))
        mastermenu = 'http://pastebin.com/raw.php?i=maCUftFJ'
        data = plugintools.read(mastermenu)

    matches = plugintools.find_multiple_matches(data,'<menu_info>(.*?)</menu_info>')
    for entry in matches:
        title = plugintools.find_single_match(entry,'<title>(.*?)</title>')
        date = plugintools.find_single_match(entry,'<date>(.*?)</date>')
        thumbnail = plugintools.find_single_match(entry,'<thumbnail>(.*?)</thumbnail>')
        fanart = plugintools.find_single_match(entry,'<fanart>(.*?)</fanart>')
        plugintools.add_item( action="" , title = title + date , fanart = fanart , thumbnail=thumbnail , folder = False , isPlayable = False )

    data = plugintools.read(mastermenu)
    matches = plugintools.find_multiple_matches(data,'<channel>(.*?)</channel>')
    for entry in matches:
        title = plugintools.find_single_match(entry,'<name>(.*?)</name>')
        thumbnail = plugintools.find_single_match(entry,'<thumbnail>(.*?)</thumbnail>')
        fanart = plugintools.find_single_match(entry,'<fanart>(.*?)</fanart>')
        action = plugintools.find_single_match(entry,'<action>(.*?)</action>')
        last_update = plugintools.find_single_match(entry,'<last_update>(.*?)</last_update>')
        url = plugintools.find_single_match(entry,'<url>(.*?)</url>')
        date = plugintools.find_single_match(entry,'<last_update>(.*?)</last_update>')

        # Control paternal
        pekes_no = plugintools.get_setting("pekes_no")
        if pekes_no == "true" :
            print "Control paternal en marcha"
            if title.find("Adultos") >= 0 :
                plugintools.log("Activando control paternal...")
            else:
                fixed = title
                plugintools.log("fixed= "+fixed)
                if fixed == "Actualizaciones":
                    plugintools.add_item( action = action , plot = fixed , title = '[COLOR red]' + fixed + '[/COLOR]' , fanart = fanart , thumbnail = thumbnail , url = url , folder = True , isPlayable = False )
                elif fixed == 'Agenda TV':
                    plugintools.add_item( action = action , plot = fixed , title = '[COLOR red]' + fixed + '[/COLOR]' , fanart = fanart , thumbnail = thumbnail , url = url , folder = True , isPlayable = False )
                elif fixed == 'Configuración':
                    plugintools.add_item( action = action , plot = fixed , title = '[COLOR red]' + fixed + '[/COLOR]' , fanart = fanart , thumbnail = thumbnail , url = url , folder = False , isPlayable = False )                    
                else:
                    plugintools.add_item( action = action , plot = fixed , title = '[COLOR lightyellow]' + fixed + '[/COLOR]' , fanart = fanart , thumbnail = thumbnail , url = url , folder = True , isPlayable = False )
        else:
            fixed = title
            if fixed == "Actualizaciones":
                plugintools.add_item( action = action , plot = fixed , title = '[COLOR red]' + fixed + '[/COLOR]' , fanart = fanart , thumbnail = thumbnail , url = url , folder = True , isPlayable = False )
            elif fixed == "Agenda TV":
                plugintools.add_item( action = action , plot = fixed , title = '[COLOR red]' + fixed + '[/COLOR]' , fanart = fanart , thumbnail = thumbnail , url = url , folder = True , isPlayable = False )
            else:
                plugintools.add_item( action = action , plot = fixed , title = '[COLOR lightyellow]' + fixed + '[/COLOR]' , fanart = fanart , thumbnail = thumbnail , url = url , folder = True , isPlayable = False )




	
def play(params):    
    plugintools.log('[%s %s].play %s' % (addonName, addonVersion, repr(params)))
    url = params.get("url")
    plugintools.play_resolved_url(url)

    

    




def runPlugin(url):
    xbmc.executebuiltin('XBMC.RunPlugin(' + url +')')


def live_items_withlink(params):
    plugintools.log('[%s %s].live_items_withlink %s' % (addonName, addonVersion, repr(params)))
    
    data = plugintools.read(params.get("url"))    
    header_xml(params)  # ToDo: Agregar función lectura de cabecera (fanart, thumbnail, título, últ. actualización)

    fanart = plugintools.find_single_match(data, '<fanart>(.*?)</fanart>')  # Localizamos fanart de la lista
    if fanart == "":
        fanart = art + 'fanart.jpg'

    author = plugintools.find_single_match(data, '<poster>(.*?)</poster>')  # Localizamos autor de la lista (encabezado)

    matches = plugintools.find_multiple_matches(data,'<item>(.*?)</item>')
    for entry in matches:
        title = plugintools.find_single_match(entry,'<title>(.*?)</title>')
        title = title.replace("<![CDATA[", "")
        title = title.replace("]]>", "")
        thumbnail = plugintools.find_single_match(entry,'<thumbnail>(.*?)</thumbnail>')
        url = plugintools.find_single_match(entry,'<link>(.*?)</link>')
        url = url.replace("<![CDATA[", "")
        url = url.replace("]]>", "")
        plugintools.add_item(action = "play" , title = title , url = url , fanart = fanart , thumbnail = thumbnail , folder = False , isPlayable = True )




def simpletv_items(params):
    plugintools.log('[%s %s].simpletv_items ' % (addonName, addonVersion))

    saving_url = 0  # Interruptor para scraper de pelis
    datamovie = {}  # Creamos lista de datos película
    follower = 0

    show = "thumbnail"
    params["show"]=show
    
    # Obtenemos fanart y thumbnail del diccionario
    thumbnail = params.get("thumbnail")
   # plugintools.log("thumbnail= "+thumbnail)
    if thumbnail == "" :
        thumbnail = art + ''

    # Parche para solucionar un bug por el cuál el diccionario params no retorna la variable fanart
    fanart = params.get("extra")
    if fanart == " " :
        fanart = params.get("fanart")
        if fanart == " " :
            fanart = art + 'fanart.png'
        
    title = params.get("plot")
    texto= params.get("texto")
    busqueda = ""
    if title == 'search':
        title = title + '.txt'
        #plugintools.log("title= "+title)
    else:
        title = title + '.m3u'

    if title == 'search.txt':
        busqueda = 'search.txt'
        filename = title
        file = open(tmp + 'search.txt', "r")
        file.seek(0)
        data = file.readline()
        if data == "":
            ok = plugintools.message("TvWin", "Sin resultados")
            return ok
    else:
        title = params.get("title")
        title = parser_title(title)
        ext = params.get("ext")
        title_plot = params.get("plot")
        if title_plot == "":
            filename = title + "." + ext

        if ext is None:
            filename = title
        else:
            #plugintools.log("ext= "+ext)
            filename = title + "." + ext
            
        file = open(playlists + filename, "r")
        file.seek(0)
        data = file.readline().strip()
        
             
            
    if data == "":
        print "No es posible leer el archivo!"
        data = file.readline()
        #plugintools.log("data= "+data)
    else:
        file.seek(0)
        num_items = len(file.readlines())
        print num_items
        #plugintools.log("filename= "+filename)
        plugintools.add_item(action="" , title = ''+ filename + '' , url = playlists + title , fanart = fanart , thumbnail = thumbnail , folder = False , isPlayable = False)
            
       
    plot = "."   # Control canal sin EPG (plot is null)
    file.seek(0)
    data = file.readline()
    i = -1
    while i <= num_items:
        if data.startswith("#EXTINF:-1") == True:
            title = data.replace("#EXTINF:-1", "")
            title = title.replace(",", "")
            title = title.replace("-AZBOX *", "")
            title = title.replace("-AZBOX-*", "")
            
           
                
                

            # Control de la línea del título en caso de búsqueda 
            if busqueda == 'search.txt':
                title_search = title.split('"')
                print 'title',title
                titulo = title_search[0]
                titulo = titulo.strip()
                origen = title_search[1]
                origen = origen.strip()
                data = file.readline()
                i = i + 1      
            else:
                images = m3u_items(title)
                print 'images',images
                #plugintools.modo_vista(show)  # Para no perder el modo de vista predefinido tras llamar a la función m3u_items
                thumbnail = images[0]
                fanart = images[1]
                cat = images[2]
                title = images[3]
                
                
                
               
                
                origen = title.split(",")                
                title = title.strip()
               # plugintools.log("title= "+title)
                data = file.readline()
                i = i + 1

            if title.startswith("#") == True:  # Control para comentarios
                title = title.replace("#", "")
                #plugintools.log("desc= "+data)                
                if data.startswith("desc") == True:
                    plot = data.replace("desc=", "").replace('"',"")
                    plugintools.add_item(action="", title = title , url = "", plot = plot , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = False)
                else:                    
                    plugintools.add_item(action="", title = title , url = "", thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = False)
                data = file.readline()
                i = i + 1
                continue                

          
                    
                    
                        
            # Control para determinadas listas de decos sat
            if title.startswith(' $ExtFilter="') == True:
                if busqueda == 'search.txt':
                    title = title.replace('$ExtFilter="', "")
                    title_search = title.split('"')
                    titulo = title_search[1]
                    origen = title_search[2]
                    origen = origen.strip()
                    data = file.readline()
                    i = i + 1                    
                else:
                    title = title.replace('$ExtFilter="', "")
                    category = title.split('"')
                    tipo = category[0]
                    tipo = tipo.strip()
                    title = category[1]
                    title = title.strip()
                    print title
                    data = file.readline()
                    i = i + 1
              
            if data != "":
                title = title.replace("radio=true", "")
                url = data.strip()
                if url == "#multilink":
                    # Control para info de canal o sinopsis de película
                    #data = file.readline()
                    plugintools.log("linea= "+data)
                    if data.startswith("desc") == True:                        
                        plot = data.replace("desc=", "").replace('"',"")
                        plugintools.log("sinopsis= "+data)
                    if cat == "":
                        if busqueda == 'search.txt':
                            plugintools.add_item( action = "multilink" , plot = plot , extra = filename , title = '[COLOR white]' + title + ' [COLOR lightyellow][Multilink][/COLOR][COLOR white][I] (' + origen + ')[/I][/COLOR]', show = show , page = show , url = url , info_labels = datamovie , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )                            
                            plot = ""
                        else:
                            plugintools.add_item( action = "multilink" , plot = plot , extra = filename , title = '[COLOR white]' + title + ' [COLOR lightyellow][Multilink][/COLOR]', url = url ,  thumbnail = thumbnail, info_labels = datamovie , show = show , page = show , fanart = fanart , folder = False , isPlayable = True )
                            if saving_url == 1:
                                plugintools.log("URL= "+url)
                                save_multilink(url, filename)
                                while url != "":
                                    url = file.readline().strip()
                                    plugintools.log("URL= "+url)
                                    save_multilink(url, filename)
                                    i = i + 1
                                saving_url = 0                            
                            plot = ""
                    else:                        
                        if busqueda == 'search.txt':
                            plugintools.add_item( action = "multilink" , plot = plot , extra = filename , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + ' [COLOR purple][Multilink][/COLOR][COLOR white][I] (' + origen + ')[/I][/COLOR]' , url = url , info_labels = datamovie , thumbnail = thumbnail, show = show, page = show , fanart = fanart , folder = False , isPlayable = True )                           
                            plot = ""
                        else:
                            plugintools.add_item( action = "multilink" , plot = plot , extra = filename , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + ' [COLOR purple][Multilink][/COLOR]' , url = url , info_labels = datamovie , thumbnail = thumbnail, show = show, page = show , fanart = fanart , folder = False , isPlayable = True )
                            if saving_url == 1:
                                save_multilink(url, filename)
                                while url != "":
                                    url = file.readline().strip()
                                    save_multilink(url, filename)
                                    i = i + 1
                                saving_url = 0                            
                            plot = ""

                elif url == "#multiparser":
                    # Control para info de canal o sinopsis de película
                    data = file.readline()
                    plugintools.log("linea= "+data)
                    if data.startswith("desc") == True:                        
                        plot = data.replace("desc=", "").replace('"',"")
                        plugintools.log("sinopsis= "+data)
                    if cat == "":
                        if busqueda == 'search.txt':
                            plugintools.add_item( action = "multiparser" , plot = datamovie["Plot"] , extra = filename , title = '[COLOR white]' + title + ' [COLOR lightyellow][Multiparser][/COLOR][COLOR white][I] (' + origen + ')[/I][/COLOR]', show = show , page = show , url = url , info_labels = datamovie , thumbnail = thumbnail , fanart = fanart , folder = True , isPlayable = False )
                            plot = ""
                        else:
                            plugintools.add_item( action = "multiparser" , plot = datamovie["Plot"] , extra = filename , title = '[COLOR white]' + title + ' [COLOR lightyellow][Multiparser][/COLOR]', url = url ,  thumbnail = thumbnail, info_labels = datamovie , show = show , page = show , fanart = fanart , folder = True , isPlayable = False )
                            if saving_url == 1:
                                save_url(url, filename)
                                data = file.readline()
                                i = i + 1
                                while url != "":
                                    url = file.readline().strip()
                                    save_url(url, filename)
                                    i = i + 1
                                saving_url = 0                            
                            plot = ""
                    else:                        
                        if busqueda == 'search.txt':
                            plugintools.add_item( action = "multiparser" , plot = datamovie["Plot"] , extra = filename , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + ' [COLOR purple][Multiparser][/COLOR][COLOR white][I] (' + origen + ')[/I][/COLOR]' , url = url , info_labels = datamovie , page = show , thumbnail = thumbnail, show = show, fanart = fanart , folder = True , isPlayable = False )                           
                            plot = ""
                        else:
                            plugintools.add_item( action = "multiparser" , plot = datamovie["Plot"] , extra = filename , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + ' [COLOR purple][Multiparser][/COLOR]' , url = url , info_labels = datamovie , thumbnail = thumbnail, show = show, page = show, fanart = fanart , folder = True , isPlayable = False )
                            if saving_url == 1:
                                save_url(url, filename)
                                saving_url = 0                            
                            plot = ""

                elif url.startswith("img") == True:
                    url = data.strip()
                    plugintools.add_item( action = "show_image" , plot = datamovie["Plot"] , extra = filename , title = '[COLOR white] ' + title + ' [COLOR lightyellow][IMG][/COLOR]' , url = url , info_labels = datamovie , thumbnail = thumbnail, show = show, page = show, fanart = fanart , folder = False , isPlayable = False )
                    data = file.readline()
                    i = i + 1
                    continue                                       
                            
                elif url.startswith("serie") == True:
                    url = data.strip()
                    if cat == "":
                        if busqueda == 'search.txt':                            
                            url = url.replace("serie:", "")
                            params["fanart"] = fanart
                            if url.find("www.yaske.cc") >= 0:
                                plugintools.add_item( action = "seriecatcher" , title = '[COLOR white]' + title + ' [COLOR lightgreen][B][Series[/B]adicto][/COLOR][COLOR white][I] (' + origen + ')[/I][/COLOR]', url = url , thumbnail = thumbnail , fanart = fanart , folder = True , isPlayable = False )
                                data = file.readline()
                                i = i + 1
                                continue
                            elif url.find("seriesflv") >= 0:
                                plugintools.add_item( action = "lista_capis" , title =  + title +  origen , url = url , thumbnail = thumbnail , fanart = fanart , folder = True , isPlayable = False )
                                data = file.readline()
                                i = i + 1
                                continue
                            elif url.find("peliculasaudiolatino") >= 0:
                                plugintools.add_item( action = "pelis0" , title = '[COLOR white]' + title + ' [COLOR lightgreen][B][Series[/B]Yonkis][/COLOR][COLOR white][I] (' + origen + ')[/I][/COLOR]', url = url , thumbnail = thumbnail , fanart = fanart , folder = True , isPlayable = False )
                                data = file.readline()
                                i = i + 1
                                continue
                            elif url.find("pastebin.com") >= 0:
                                plugintools.add_item( action = "seriesblanco0" , title = '[COLOR white]' + title + ' [COLOR lightgreen][B][Series[/B]Blanco][/COLOR][COLOR white][I] (' + origen + ')[/I][/COLOR]', url = url , thumbnail = thumbnail , fanart = fanart , folder = True , isPlayable = False )
                                data = file.readline()
                                i = i + 1
                                continue
                            elif url.find("peliculasaudiolatino") >= 0:
                                plugintools.add_item( action = "pelis0" , title = '[COLOR white]' + title + ' [COLOR lightgreen][B][Series[/B].Mu][/COLOR][COLOR white][I] (' + origen + ')[/I][/COLOR]', url = url , thumbnail = thumbnail , fanart = fanart , folder = True , isPlayable = False )
                                data = file.readline()
                                i = i + 1
                                continue                              
                            data = file.readline()
                            i = i + 1
                            continue
                        else:
                            url = url.replace("serie:", "")
                            params["fanart"] = fanart
                            if url.find("www.yaske.cc") >= 0:
                                plugintools.add_item( action = "seriecatcher" , title = title , url = url , thumbnail = thumbnail , show = show, fanart = fanart , folder = True , isPlayable = False )
                                data = file.readline()
                                i = i + 1
                                continue
                            elif url.find("seriesflv") >= 0:
                                plugintools.add_item( action = "lista_capis" , title =  title  , url = url , thumbnail = thumbnail , fanart = fanart , folder = True , isPlayable = False )
                                data = file.readline()
                                i = i + 1
                                continue
                            elif url.find("peliculasaudiolatino") >= 0:
                                plugintools.add_item( action = "pelis0" , title =  title , url = url , thumbnail = thumbnail , fanart = fanart , folder = True , isPlayable = False )
                                data = file.readline()
                                i = i + 1
                                continue
                            elif url.find("pastebin.com") >= 0:
                                plugintools.add_item( action = "seriesblanco0" , title = '[COLOR white]' + title + ' [COLOR lightgreen][B][Series[/B]Blanco][/COLOR]', url = url , thumbnail = thumbnail , fanart = fanart , folder = True , isPlayable = False )
                                data = file.readline()
                                i = i + 1
                                continue
                            elif url.find("peliculasaudiolatino") >= 0:
                                plugintools.add_item( action = "pelis0" , title = '[COLOR white]' + title + ' [COLOR lightgreen][B][Series[/B].Mu][/COLOR]', url = url , thumbnail = thumbnail , fanart = fanart , folder = True , isPlayable = False )
                                data = file.readline()
                                i = i + 1
                                continue                               
                    else:
                        if busqueda == 'search.txt':
                            plugintools.add_item( action = "play" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + ' [COLOR purple][Serie online][/COLOR][COLOR white][I] (' + origen + ')[/I][/COLOR]' , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                            data = file.readline()
                            i = i + 1
                            continue
                        else:
                            plugintools.add_item( action = "play" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + ' [COLOR purple][Serie online][/COLOR]' , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                            data = file.readline()
                            i = i + 1
                            continue

                

                                     

                elif url.startswith("short") == True:
                    if busqueda == 'search.txt':
                        url = url.replace("short:", "").strip()
                        plugintools.add_item( action = "longurl" , title = '[COLOR white]' + title + '[COLOR lightblue] [shortlink][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url , extra = show , show = show , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                        data = file.readline()
                        i = i + 1
                        continue
                    else:
                        url = url.replace("short:", "").strip()
                        plugintools.add_item( action = "longurl" , title = '[COLOR white]' + title + '[COLOR lightblue] [shortlink][/COLOR]', url = url , extra = show , show = show , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                        data = file.readline()
                        i = i + 1
                        continue

                elif data.startswith("http") == True:
                    url = data.strip()
                    if cat != "":  # Controlamos el caso de subcategoría de canales
                        if busqueda == 'search.txt':
                            if url.startswith("serie") == True:
                                url = url.replace("serie:", "")
                                params["fanart"] = fanart
                                plugintools.add_item( action = "seriecatcher" , title = '[COLOR white]' + title + ' [COLOR purple][Serie online][/COLOR][COLOR lightsalmon](' + origen + ')[/I][/COLOR]' , url = url , thumbnail = thumbnail , show = show, fanart = fanart , folder = True , isPlayable = False )
                                data = file.readline()
                                i = i + 1
                                continue
                          
                            elif url.find("allmyvideos") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()
                                plugintools.add_item( action = "allmyvideos" , title = '[COLOR white]' + title + '[COLOR lightyellow] [Allmyvideos][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url , thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("streamcloud") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                            
                                plugintools.add_item( action = "streamcloud" , title = '[COLOR white]' + title + '[COLOR lightskyblue] [Streamcloud][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )                          
                                data = file.readline()
                                i = i + 1
                                continue                        

                            elif url.find("vidspot") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                            
                                plugintools.add_item( action = "vidspot" , title = '[COLOR white]' + title + '[COLOR palegreen] [Vidspot][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("played.to") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                            
                                plugintools.add_item( action = "playedto" , title = '[COLOR white]' + title + '[COLOR lavender] [Played.to][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("vk.com") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                            
                                plugintools.add_item( action = "vk" , title = '[COLOR white]' + title + '[COLOR royalblue] [Vk][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("nowvideo") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                            
                                plugintools.add_item( action = "nowvideo" , title = '[COLOR white]' + title + '[COLOR red] [Nowvideo][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue
                            
                            elif url.find("tumi") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                            
                                plugintools.add_item( action = "tumi" , title = '[COLOR white]' + title + '[COLOR forestgreen] [Tumi][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("veehd") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                            
                                plugintools.add_item( action = "veehd" , title = '[COLOR white]' + title + '[COLOR orange] [Veehd][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("streamin.to") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                            
                                plugintools.add_item( action = "streaminto" , title = '[COLOR white]' + title + '[COLOR orange] [Streamin.to][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("powvideo") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                            
                                plugintools.add_item( action = "powvideo" , title = '[COLOR white]' + title + '[COLOR orange] [powvideo][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("mail.ru") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                            
                                plugintools.add_item( action = "mailru" , title = '[COLOR white]' + title + '[COLOR orange] [Mail.ru][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("novamov") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                            
                                plugintools.add_item( action = "novamov" , title = '[COLOR white]' + title + '[COLOR orange] [Novamov][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("gamovideo") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                            
                                plugintools.add_item( action = "gamovideo" , title = '[COLOR white]' + title + '[COLOR orange] [Gamovideo][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("moevideos") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                            
                                plugintools.add_item( action = "moevideos" , title = '[COLOR white]' + title + '[COLOR orange] [Moevideos][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("movshare") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                            
                                plugintools.add_item( action = "movshare" , title = '[COLOR white]' + title + '[COLOR orange] [Movshare][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("movreel") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                            
                                plugintools.add_item( action = "movreel" , title = '[COLOR white]' + title + '[COLOR orange] [Movreel][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("videobam") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                            
                                plugintools.add_item( action = "videobam" , title = '[COLOR white]' + title + '[COLOR orange] [Videobam][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue                              

                            elif url.find("www.youtube.com") >= 0:  # Video youtube
                                plugintools.log("linea titulo= "+title_search)
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()
                                videoid = url.replace("https://www.youtube.com/watch?=", "")
                                url = 'plugin://plugin.video.youtube/play/?video_id='+videoid
                                url = url.strip()
                                plugintools.add_item( action = "play" , title = '[COLOR white]' + title + ' [[COLOR red]You[COLOR white]tube Video][I] (' + origen + ')[/I][/COLOR]', url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("www.dailymotion.com/playlist") >= 0:  # Playlist
                                id_playlist = dailym_getplaylist(url)
                                if id_playlist != "":
                                    url = "https://api.dailymotion.com/playlist/"+id_playlist+"/videos"
                                    if thumbnail == "":
                                        thumbnail = 'http://press.dailymotion.com/wp-old/wp-content/uploads/logo-Dailymotion.png'
                                    plugintools.add_item( action="dailym_pl" , title=title + ' [COLOR lightyellow][B][Dailymotion[/B] playlist][/COLOR]' , fanart=fanart, show = show, thumbnail=thumbnail, url=url , folder=True, isPlayable=False)
                                else:
                                    data = file.readline()
                                    i = i + 1
                                    continue

                            elif url.find("dailymotion.com/video") >= 0:
                                video_id = dailym_getvideo(url)
                                if video_id != "":
                                    thumbnail = "https://api.dailymotion.com/thumbnail/video/"+video_id+""
                                    url = "plugin://plugin.video.dailymotion_com/?url="+video_id+"&mode=playVideo"
                                    # Appends a new item to the xbmc item list
                                    # API Dailymotion list of video parameters: http://www.dailymotion.com/doc/api/obj-video.html
                                    plugintools.add_item( action="play" , title=title + ' [COLOR lightyellow][B][Dailymotion[/B] video][/COLOR]' , url=url , thumbnail = thumbnail , show = show, fanart = fanart, isPlayable=True, folder=False )
                                    data = file.readline()
                                    i = i + 1
                                    continue
                                else:
                                    data = file.readline()
                                    i = i + 1
                                    continue        

                            elif url.endswith("m3u8") == True:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()
                                plugintools.add_item( action = "play" , title = '[COLOR white]' + title + '[COLOR purple][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url , info_labels = datamovie , thumbnail = thumbnail , extra = show , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.endswith("torrent") == True:  # Archivos torrents
                                # plugin://plugin.video.p2p-streams/?url=http://something.torrent&mode=1&name=acestream+title   
                                title_fixed = title.replace(" ", "+").strip()
                                url = 'plugin://plugin.video.p2p-streams/?url='+url+'&mode=1&name='+title_fixed                                
                                plugintools.add_item( action = "play" , title = '[COLOR white]' + title + '[COLOR gold] [Torrent][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url , plot = datamovie["Plot"], info_labels = datamovie , thumbnail = thumbnail , extra = show , show = show, fanart = fanart , folder = True , isPlayable = False )
                                data = file.readline()
                                i = i + 1
                                continue   
                            
                            else:
                                title = title_search.split('"')
                                title = title[0]
                                title = title.strip()
                                plugintools.add_item( action = "play" , title = '[COLOR white]' + title + '[COLOR lightblue] [HTTP][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', info_labels = datamovie , plot = datamovie["Plot"], url = url , extra = show , show = show , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue
                        else:
                            if url.startswith("serie") == True:
                                url = url.replace("serie:", "")
                                params["fanart"] = fanart
                                plugintools.add_item( action = "seriecatcher" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + ' [COLOR purple][Serie online][/COLOR]', url = url , thumbnail = thumbnail , info_labels = datamovie , show = show, fanart = fanart , folder = True , isPlayable = False )
                                data = file.readline()
                                i = i + 1
                                continue
                            
                            elif url.find("allmyvideos") >= 0:
                                listitem = xbmcgui.ListItem( title, iconImage="DefaultVideo.png", thumbnailImage=thumbnail )
                                plugintools.add_item( action = "allmyvideos" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR lightyellow] [Allmyvideos][/COLOR]' , url = url , thumbnail = thumbnail , info_labels = datamovie , show = show, fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    save_url(url, filename)
                                    saving_url = 0
                                data = file.readline()
                                i = i + 1
                                continue
                            
                            elif url.find("streamcloud") >= 0:                             
                                plugintools.add_item( action = "streamcloud" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR lightskyblue] [Streamcloud][/COLOR]' , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    save_url(url, filename)
                                    saving_url = 0
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("vidspot") == True:                             
                                plugintools.add_item( action = "vidspot" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR palegreen] [Vidspot][/COLOR]' , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    save_url(url, filename)
                                    saving_url = 0                                
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("played.to") >= 0:                            
                                plugintools.add_item( action = "playedto" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR lavender] [Played.to][/COLOR]' , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    save_url(url, filename)
                                    saving_url = 0                              
                                data = file.readline()
                                i = i + 1
                                continue
                            
                            elif url.find("vk") >= 0:                            
                                plugintools.add_item( action = "vk" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR royalblue] [Vk][/COLOR]' , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    save_url(url, filename)
                                    saving_url = 0                              
                                data = file.readline()
                                i = i + 1
                                continue                            

                            elif url.find("nowvideo") >= 0:                            
                                plugintools.add_item( action = "nowvideo" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR red] [Nowvideo][/COLOR]' , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    save_url(url, filename)
                                    saving_url = 0                               
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("tumi") >= 0:                            
                                plugintools.add_item( action = "tumi" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR forestgreen] [Tumi][/COLOR]' , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    save_url(url, filename)
                                    saving_url = 0                               
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("veehd") >= 0:                            
                                plugintools.add_item( action = "veehd" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR orange] [VeeHD][/COLOR]' , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    save_url(url, filename)
                                    saving_url = 0                               
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("streamin.to") >= 0:                            
                                plugintools.add_item( action = "streaminto" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR orange] [streamin.to][/COLOR]' , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    save_url(url, filename)
                                    saving_url = 0                           
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("mail.ru") >= 0:                            
                                plugintools.add_item( action = "mailru" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR orange] [Mail.ru][/COLOR]' , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    save_url(url, filename)
                                    saving_url = 0                              
                                data = file.readline()
                                i = i + 1
                                continue                            

                            elif url.find("powvideo") >= 0:                            
                                plugintools.add_item( action = "powvideo" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR orange] [Powvideo][/COLOR]' , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    save_url(url, filename)
                                    saving_url = 0                              
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("novamov") >= 0:                            
                                plugintools.add_item( action = "novamov" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR orange] [Novamov][/COLOR]' , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    save_url(url, filename)
                                    saving_url = 0                              
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("gamovideo") >= 0:                            
                                plugintools.add_item( action = "gamovideo" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR orange] [Gamovideo][/COLOR]' , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    save_url(url, filename)
                                    saving_url = 0                              
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("moevideos") >= 0:                            
                                plugintools.add_item( action = "moevideos" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR orange] [Moevideos][/COLOR]' , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    save_url(url, filename)
                                    saving_url = 0                              
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("movshare") >= 0:                            
                                plugintools.add_item( action = "movshare" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR orange] [Movshare][/COLOR]' , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    save_url(url, filename)
                                    saving_url = 0                              
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("movreel") >= 0:                            
                                plugintools.add_item( action = "movreel" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR orange] [Movreel][/COLOR]' , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    save_url(url, filename)
                                    saving_url = 0                              
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("videobam") >= 0:                            
                                plugintools.add_item( action = "videobam" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR orange] [Videobam][/COLOR]' , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    save_url(url, filename)
                                    saving_url = 0                              
                                data = file.readline()
                                i = i + 1
                                continue                               
   
                            elif url.find("www.youtube.com") >= 0:  # Video youtube
                                title = title.split('"')
                                title = title[0]
                                title =title.strip()
                                videoid = url.replace("https://www.youtube.com/watch?=", "")                                
                                url = 'plugin://plugin.video.youtube/play/?video_id='+videoid
                                plugintools.add_item( action = "play" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + ' [[COLOR red]You[COLOR white]tube Video][/COLOR]', url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    save_url(url, filename)
                                    saving_url = 0                                
                                data = file.readline()
                                i = i + 1
                                continue
                            
                            elif url.find("www.dailymotion.com/playlist") >= 0:  # Playlist
                                id_playlist = dailym_getplaylist(url)
                                if id_playlist != "":
                                    plugintools.log("id_playlist= "+id_playlist)
                                    if thumbnail == "":
                                        thumbnail = 'http://press.dailymotion.com/wp-old/wp-content/uploads/logo-Dailymotion.png'
                                    url = "https://api.dailymotion.com/playlist/"+id_playlist+"/videos"
                                    plugintools.add_item( action="dailym_pl" , title='[COLOR red][I]'+cat+' / [/I][/COLOR] '+title+' [COLOR lightyellow][B][Dailymotion[/B] playlist][/COLOR]', url=url , fanart = fanart , show = show, thumbnail=thumbnail , folder=True, isPlayable=False)
                                else:
                                    data = file.readline()
                                    i = i + 1
                                    continue

                            elif url.find("dailymotion.com/video") >= 0:
                                video_id = dailym_getvideo(url)
                                if video_id != "":
                                    thumbnail = "https://api.dailymotion.com/thumbnail/video/"+video_id+""
                                    url = "plugin://plugin.video.dailymotion_com/?url="+video_id+"&mode=playVideo"
                                    # Appends a new item to the xbmc item list
                                    # API Dailymotion list of video parameters: http://www.dailymotion.com/doc/api/obj-video.html
                                    plugintools.add_item( action="play" , title='[COLOR red][I]' + cat + ' / [/I][/COLOR] '+title+' [COLOR lightyellow][B][Dailymotion[/B] video][/COLOR]', url=url , thumbnail = thumbnail , show = show, fanart= fanart , isPlayable=True, folder=False )
                                    data = file.readline()
                                    i = i + 1
                                    continue
                                else:
                                    data = file.readline()
                                    i = i + 1
                                    continue
                                    
                                data = file.readline()
                                i = i + 1
                                continue  

                            elif url.endswith("m3u8") == True:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                            
                                plugintools.add_item( action = "play" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '', url = url , plot = plot , info_labels = datamovie , thumbnail = thumbnail , extra = show , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.startswith("cbz") == True:
                                if url.find("copy.com") >= 0:
                                    plugintools.log("CBZ Copy.com")
                                    #url = url.replace("cbz:", "").strip()
                                else:
                                    url = url.replace("cbz:", "").strip()
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                            
                                plugintools.add_item( action = "cbx_reader" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR gold] [CBZ][/COLOR]', url = url , plot = datamovie["Plot"] , info_labels = datamovie , thumbnail = thumbnail , extra = show , show = show, fanart = fanart , folder = True , isPlayable = False )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.startswith("cbr") == True:
                                if url.find("copy.com") >= 0:
                                    plugintools.log("CBR Copy.com")
                                    #url = url.replace("cbr:", "").strip()
                                else:
                                    url = url.replace("cbr:", "").strip()
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                            
                                plugintools.add_item( action = "cbx_reader" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR gold] [CBR][/COLOR]', url = url , plot = datamovie["Plot"], info_labels = datamovie , thumbnail = thumbnail , extra = show , show = show, fanart = fanart , folder = True , isPlayable = False )
                                data = file.readline()
                                i = i + 1
                                continue 

                            elif url.startswith("short") == True:
                                url.replace("short:", "").strip()
                                title = title_search.split('"')
                                title = title[0]
                                title = title.strip()
                                plugintools.add_item( action = "longurl" , title = '[COLOR white]' + title + '[COLOR green] [shortlink][/COLOR]', url = url , extra = show , show = show , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                                params["show"]=show
                                plugintools.log("show "+show)
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.endswith("torrent") == True:
                                # plugin://plugin.video.p2p-streams/?url=http://something.torrent&mode=1&name=acestream+title   
                                title_fixed = title.replace(" ", "+").strip()
                                url = 'plugin://plugin.video.p2p-streams/?url='+url+'&mode=1&name='+title_fixed                                
                                plugintools.add_item( action = "play" , title = '[COLOR white]' + title + '[COLOR gold] [Torrent][/COLOR]', url = url , plot = datamovie["Plot"], info_labels = datamovie , thumbnail = thumbnail , extra = show , show = show, fanart = fanart , folder = True , isPlayable = False )
                                data = file.readline()
                                i = i + 1
                                continue
                            
                            else:
                                plugintools.add_item( action = "play" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '' , url = url , plot = plot , info_labels = datamovie , extra = show , show = show , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )                                
                                data = file.readline()
                                i = i + 1
                                continue
                            
                    # Sin categoría de canales   
                    else:
                        if busqueda == 'search.txt':
                            if url.startswith("serie") == True:
                                url = url.replace("serie:", "")
                                params["fanart"] = fanart
                                plugintools.log("fanart= "+fanart)
                                plugintools.add_item( action = "seriecatcher" , title = '[COLOR white]' + title + ' [COLOR purple][Serie online][/COLOR][COLOR lightsalmon](' + origen + ')[/I][/COLOR]' , url = url , thumbnail = thumbnail , show = show, fanart = fanart , folder = True , isPlayable = False )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.startswith("goear") == True:
                                params["fanart"] = fanart
                                if show == "list":
                                    show = plugintools.get_setting("music_id")
                                    plugintools.log("show en config")
                                data = file.readline()
                                if data.startswith("desc") == True:
                                    datamovie["Plot"] = data.replace("desc=", "").replace('"',"")                                    
                                plugintools.add_item( action = "goear" , plot = plot , title = '[COLOR white]' + title + ' [COLOR blue][goear][/COLOR][COLOR lightsalmon](' + origen + ')[/I][/COLOR]' , url = url , thumbnail = thumbnail , info_labels = datamovie , extra = show , show = show, fanart = fanart , folder = True , isPlayable = False )
                                data = file.readline()                                    
                                i = i + 1
                                continue
                                                        
                            elif url.find("allmyvideos") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()
                                listitem = xbmcgui.ListItem( title, iconImage="DefaultVideo.png", thumbnailImage=thumbnail )
                                plugintools.add_item( action = "allmyvideos" , title = '[COLOR white]' + title + '[COLOR lightyellow] [Allmyvideos][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url , thumbnail = thumbnail , info_labels = datamovie , show = show, fanart = fanart , folder = False , isPlayable = True )                                                      
                                if saving_url == 1:
                                    save_url(url, filename)
                                    saving_url = 0
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("streamcloud") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                             
                                plugintools.add_item( action = "streamcloud" , title = '[COLOR white]' + titulo + '[COLOR lightskyblue] [Streamcloud][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue                        
                            
                            elif url.find("vidspot") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                             
                                plugintools.add_item( action = "vidspot" , title = '[COLOR white]' + title + '[COLOR palegreen] [Vidspot][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue
                            
                            elif url.find("played.to") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                             
                                plugintools.add_item( action = "playedto" , title = '[COLOR white]' + title + '[COLOR lavender] [Played.to][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("vk.com") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                             
                                plugintools.add_item( action = "vk" , title = '[COLOR white]' + title + '[COLOR royalblue] [Vk][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("nowvideo") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                             
                                plugintools.add_item( action = "nowvideo" , title = '[COLOR white]' + title + '[COLOR red] [Nowvideo][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("tumi.tv") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                             
                                plugintools.add_item( action = "tumi" , title = '[COLOR white]' + title + '[COLOR forestgreen] [Tumi][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("veehd") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                             
                                plugintools.add_item( action = "veehd" , title = '[COLOR white]' + title + '[COLOR orange] [VeeHD][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("streamin.to") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                             
                                plugintools.add_item( action = "streaminto" , title = '[COLOR white]' + title + '[COLOR orange] [streamin.to][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url , thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("powvideo") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                             
                                plugintools.add_item( action = "powvideo" , title = '[COLOR white]' + title + '[COLOR orange] [powvideo][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("mail.ru") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                             
                                plugintools.add_item( action = "mailru" , title = '[COLOR white]' + title + '[COLOR orange] [Mail.ru][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("novamov") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                             
                                plugintools.add_item( action = "novamov" , title = '[COLOR white]' + title + '[COLOR orange] [Novamov][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("moevideos") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                             
                                plugintools.add_item( action = "moevideos" , title = '[COLOR white]' + title + '[COLOR orange] [Moevideos][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue                             

                            elif url.find("www.youtube.com") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()
                                videoid = url.replace("https://www.youtube.com/watch?=", "")
                                url = 'plugin://plugin.video.youtube/play/?video_id='+videoid                       
                                plugintools.add_item( action = "youtube_videos" , title = '[COLOR white][' + title + ' [[COLOR red]You[/COLOR][COLOR white]tube Video][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("www.dailymotion.com/playlist") >= 0:  # Playlist
                                id_playlist = dailym_getplaylist(url)
                                if id_playlist != "":
                                    if thumbnail == "":
                                        thumbnail = 'http://press.dailymotion.com/wp-old/wp-content/uploads/logo-Dailymotion.png'                               
                                    url = "https://api.dailymotion.com/playlist/"+id_playlist+"/videos"
                                    plugintools.add_item( action="dailym_pl" , title=title+' [COLOR lightyellow][B][Dailymotion[/B] playlist][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url=url , fanart = fanart , show = show, thumbnail=thumbnail , folder=True, isPlayable=False)
                                else:
                                    data = file.readline()
                                    i = i + 1
                                    continue

                            elif url.find("dailymotion.com/video") >= 0:
                                video_id = dailym_getvideo(url)
                                if video_id != "":
                                    thumbnail = "https://api.dailymotion.com/thumbnail/video/"+video_id+""
                                    url = "plugin://plugin.video.dailymotion_com/?url="+video_id+"&mode=playVideo"
                                    # Appends a new item to the xbmc item list
                                    # API Dailymotion list of video parameters: http://www.dailymotion.com/doc/api/obj-video.html
                                    plugintools.add_item( action="play" , title=title+' [COLOR lightyellow][B][Dailymotion[/B] video][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url=url , fanart = fanart , show = show, thumbnail = thumbnail , isPlayable=True, folder=False )
                                    data = file.readline()
                                    i = i + 1
                                    continue
                                else:
                                    data = file.readline()
                                    i = i + 1
                                    continue
                                    
                                data = file.readline()
                                i = i + 1
                                continue                             
                            
                            elif url.endswith("m3u8") == True:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                            
                                plugintools.add_item( action = "play" , title = '[COLOR white]' + title + ' [COLOR purple][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url , info_labels = datamovie , thumbnail = thumbnail , extra = show , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.startswith("cbz:") == True:
                                if url.find("copy.com") >= 0:
                                    plugintools.log("CBZ Copy.com")
                                    #url = url.replace("cbz:", "").strip()
                                else:
                                    url = url.replace("cbz:", "").strip()
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                            
                                plugintools.add_item( action = "cbx_reader" , title = '[COLOR white]' + title + ' [COLOR gold][CBZ][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url , plot = datamovie["Plot"], info_labels = datamovie , thumbnail = thumbnail , extra = show , show = show, fanart = fanart , folder = True , isPlayable = False )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.startswith("cbr:") == True:
                                if url.find("copy.com") >= 0:
                                    plugintools.log("CBR Copy.com")
                                    #url = url.replace("cbr:", "").strip()
                                else:
                                    url = url.replace("cbr:", "").strip()
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                            
                                plugintools.add_item( action = "cbx_reader" , title = '[COLOR white]' + title + ' [COLOR gold][CBR][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url , plot = datamovie["Plot"], info_labels = datamovie , thumbnail = thumbnail , extra = show , show = show, fanart = fanart , folder = True , isPlayable = False )
                                data = file.readline()
                                i = i + 1
                                continue                            

                            elif url.find("mediafire") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                            
                                plugintools.add_item( action = "cbx_reader" , title = '[COLOR white]' + title + ' [COLOR gold][Mediafire][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url , info_labels = datamovie , thumbnail = thumbnail , extra = show , show = show, fanart = fanart , folder = True , isPlayable = False )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.endswith("torrent") == True:
                                # plugin://plugin.video.p2p-streams/?url=http://something.torrent&mode=1&name=acestream+title   
                                title_fixed = title.replace(" ", "+").strip()
                                url = 'plugin://plugin.video.p2p-streams/?url='+url+'&mode=1&name='+title_fixed
                                plugintools.add_item( action = "play" , title = '[COLOR white]' + title + '[COLOR gold] [Torrent][/COLOR]', url = url , plot = datamovie["Plot"], info_labels = datamovie , thumbnail = thumbnail , extra = show , show = show, fanart = fanart , folder = True , isPlayable = False )
                                data = file.readline()
                                i = i + 1
                                continue                            

                            elif url.startswith("short") == True:
                                url.replace("short:", "").strip()
                                title = title_search.split('"')
                                title = title[0]
                                title = title.strip()
                                plugintools.add_item( action = "longurl" , title = '[COLOR white]' + title + '[COLOR lightblue] [HTTP][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url , extra = show , show = show , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                                params["show"]=show
                                plugintools.log("show "+show)
                                data = file.readline()
                                i = i + 1
                                continue                             
                            
                            else:                      
                                title = title_search[0]
                                title = title.strip()                             
                                plugintools.add_item( action = "play" , title = '[COLOR white]' + title + ' [COLOR blue][HTTP][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url , extra = show , show = show , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                                params["show"]=show
                                plugintools.log("show "+show)
                                data = file.readline()
                                i = i + 1
                                continue

                        else:
                            if url.find("allmyvideos") >= 0:
                                listitem = xbmcgui.ListItem( title, iconImage="DefaultVideo.png", thumbnailImage=thumbnail )
                                plugintools.add_item( action = "allmyvideos" , title = '[COLOR white]' + title + ' [COLOR lightyellow][Allmyvideos][/COLOR]', url = url , thumbnail = thumbnail , info_labels = datamovie , show = show, fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    save_url(url, filename)
                                    saving_url = 0
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("streamcloud") >= 0:                             
                                plugintools.add_item( action = "streamcloud" , title = '[COLOR white]' + title + ' [COLOR lightskyblue][Streamcloud][/COLOR]', url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("vidspot") >= 0:                            
                                plugintools.add_item( action = "vidspot" , title = '[COLOR white]' + title + ' [COLOR palegreen][Vidspot][/COLOR]' , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue
                            
                            elif url.find("played.to") >= 0:                            
                                plugintools.add_item( action = "playedto" , title = '[COLOR white]' + title + ' [COLOR lavender][Played.to][/COLOR]' , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("vk.com") >= 0:                            
                                plugintools.add_item( action = "vk" , title = '[COLOR white]' + title + ' [COLOR royalblue][Vk][/COLOR]' , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("nowvideo") >= 0:                            
                                plugintools.add_item( action = "nowvideo" , title = '[COLOR white]' + title + '[COLOR red] [Nowvideo][/COLOR]' , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("tumi.tv") >= 0:                            
                                plugintools.add_item( action = "tumi" , title = '[COLOR white]' + title + '[COLOR forestgreen] [Tumi][/COLOR]' , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("VeeHD") >= 0:                            
                                plugintools.add_item( action = "veehd" , title = '[COLOR white]' + title + '[COLOR forestgreen] [VeeHD][/COLOR]' , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("streamin.to") >= 0:                            
                                plugintools.add_item( action = "streaminto" , title = '[COLOR white]' + title + '[COLOR forestgreen] [streamin.to][/COLOR]' , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue
                            
                            elif url.find("powvideo") >= 0:                            
                                plugintools.add_item( action = "powvideo" , title = '[COLOR white]' + title + '[COLOR forestgreen] [powvideo][/COLOR]' , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue
                            
                            elif url.find("mail.ru") >= 0:                            
                                plugintools.add_item( action = "mailru" , title = '[COLOR white]' + title + '[COLOR forestgreen] [Mail.ru][/COLOR]' , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("novamov") >= 0:                            
                                plugintools.add_item( action = "novamov" , title = '[COLOR white]' + title + '[COLOR forestgreen] [Novamov][/COLOR]' , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("gamovideo") >= 0:                            
                                plugintools.add_item( action = "gamovideo" , title = '[COLOR white]' + title + '[COLOR forestgreen] [Gamovideo][/COLOR]' , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("moevideos") >= 0:                            
                                plugintools.add_item( action = "moevideos" , title = '[COLOR white]' + title + '[COLOR forestgreen] [Moevideos][/COLOR]' , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("movshare") >= 0:                            
                                plugintools.add_item( action = "movshare" , title = '[COLOR white]' + title + '[COLOR forestgreen] [Movshare][/COLOR]' , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("movreel") >= 0:                            
                                plugintools.add_item( action = "movreel" , title = '[COLOR white]' + title + '[COLOR forestgreen] [Movreel][/COLOR]' , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("videobam") >= 0:                            
                                plugintools.add_item( action = "videobam" , title = '[COLOR white]' + title + '[COLOR forestgreen] [Videobam][/COLOR]' , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue                             

                            elif url.find("www.youtube.com") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()
                                videoid = url.replace("https://www.youtube.com/watch?v=", "")
                                print 'videoid',videoid
                                url = 'plugin://plugin.video.youtube/play/?video_id='+videoid                       
                                plugintools.add_item( action = "youtube_videos" , title = '[COLOR white]' + title + ' [[COLOR red]You[/COLOR][COLOR white]tube Video][/COLOR]', url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("www.dailymotion.com/playlist") >= 0:  # Playlist
                                id_playlist = dailym_getplaylist(url)
                                if id_playlist != "":
                                    plugintools.log("id_playlist= "+id_playlist)
                                    thumbnail=art+'/lnh_logo.png'
                                    url = "https://api.dailymotion.com/playlist/"+id_playlist+"/videos"
                                    #plugintools.log("url= "+url)
                                    plugintools.add_item( action="dailym_pl" , title=title + ' [COLOR lightyellow][B][Dailymotion[/B] playlist][/COLOR]' , url=url , fanart = fanart , show = show, thumbnail=thumbnail , folder=True)
                                else:
                                    data = file.readline()
                                    i = i + 1
                                    continue

                            elif url.find("dailymotion.com/video") >= 0:
                                video_id = dailym_getvideo(url)
                                if video_id != "":
                                    thumbnail = "https://api.dailymotion.com/thumbnail/video/"+video_id+""
                                    url = "plugin://plugin.video.dailymotion_com/?url="+video_id+"&mode=playVideo"
                                    #plugintools.log("url= "+url)
                                    # Appends a new item to the xbmc item list
                                    # API Dailymotion list of video parameters: http://www.dailymotion.com/doc/api/obj-video.html
                                    plugintools.add_item( action="play" , title=title + ' [COLOR lightyellow][B][Dailymotion[/B] video][/COLOR]' , url=url , thumbnail = thumbnail , show = show, fanart = fanart , isPlayable=True, folder=False )
                                    data = file.readline()
                                    i = i + 1
                                    continue
                                else:
                                    data = file.readline()
                                    i = i + 1
                                    continue
                                    
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("oneplay.tv/") >= 0:
                                #plugintools.add_item( action = "one2" , title = '[COLOR white]' + title + ' [COLOR red][Oneplay][/COLOR]', plot = plot , url = url , thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                plugintools.add_item( action = "play" , title = title , plot = plot , url = url , thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue                             
                            
                            elif url.endswith("m3u8") == True:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                            
                                plugintools.add_item( action = "play" , title = '[COLOR white]' + title + ' [COLOR purple][/COLOR]', plot = plot , url = url , info_labels = datamovie , thumbnail = thumbnail , extra = show , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.startswith("cbz:") == True:
                                if url.find("copy.com") >= 0:
                                    plugintools.log("CBZ Copy.com")
                                    #url = url.replace("cbz:", "").strip()
                                else:
                                    url = url.replace("cbz:", "").strip()
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                            
                                plugintools.add_item( action = "cbx_reader" , title = '[COLOR white]' + title + ' [COLOR gold][CBZ][/COLOR]', url = url , plot = datamovie["Plot"], info_labels = datamovie , thumbnail = thumbnail , extra = show , show = show, fanart = fanart , folder = True , isPlayable = False )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.startswith("cbr:") == True:
                                if url.find("copy.com") >= 0:
                                    plugintools.log("CBR Copy.com")
                                    #url = url.replace("cbr:", "").strip()
                                else:
                                    url = url.replace("cbr:", "").strip()
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                            
                                plugintools.add_item( action = "cbx_reader" , title = '[COLOR white]' + title + ' [COLOR gold][CBR][/COLOR]', url = url , plot = datamovie["Plot"], info_labels = datamovie , thumbnail = thumbnail , extra = show , show = show, fanart = fanart , folder = True , isPlayable = False )
                                data = file.readline()
                                i = i + 1
                                continue                            

                            elif url.find("mediafire") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                            
                                plugintools.add_item( action = "cbx_reader" , title = '[COLOR white]' + title + ' [COLOR gold][Mediafire][/COLOR]', plot = plot , url = url , info_labels = datamovie , thumbnail = thumbnail , extra = show , show = show, fanart = fanart , folder = True , isPlayable = False )
                                data = file.readline()
                                i = i + 1
                                continue                             

                            elif url.startswith("short") == True:
                                url.replace("short:", "").strip()
                                title = title_search.split('"')
                                title = title[0]
                                title = title.strip()
                                plugintools.add_item( action = "longurl" , title = '[COLOR white]' + title + '[COLOR lightblue] [shortlink][/COLOR]', url = url , extra = show , show = show , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                                params["show"]=show
                                plugintools.log("show "+show)
                                data = file.readline()
                                i = i + 1
                                continue
                            
                            else:
                                plugintools.add_item( action = "play" , title = '[COLOR red][I]' + '[/I][/COLOR][COLOR white]' + title + '[/COLOR]' , plot = plot , url = url , extra = show , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                                params["show"]=show
                                plugintools.log("show "+show)
                                data = file.readline()
                                i = i + 1
                                continue
              
                if data.startswith("rtmp") == True or data.startswith("rtsp") == True:
                    url = data
                    url = parse_url(url)
                    if cat != "":  # Controlamos el caso de subcategoría de canales
                        if busqueda == 'search.txt':
                            params["url"] = url
                            server_rtmp(params)                      
                            server = params.get("server")
                            plugintools.log("params en simpletv" +repr(params) )
                            url = params.get("url")                            
                            plugintools.add_item( action = "launch_rtmp" , title = '[COLOR white]' + titulo + '' + server + '' + origen + '', url = params.get("url") , thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                            params["server"] = server
                            print url                        
                            data = file.readline()
                            i = i + 1
                            continue
                        else:
                            params["url"] = url
                            server_rtmp(params)                         
                            server = params.get("server")
                            plugintools.log("params en simpletv" +repr(params) )
                            plugintools.log("fanart= "+fanart)
                            url = params.get("url")                            
                            plugintools.add_item( action = "launch_rtmp" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '' + server + '' , plot = plot , url = params.get("url") , info_labels = datamovie , thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                            print url                        
                            data = file.readline()
                            i = i + 1
                            continue
                            
                    else:
                        if busqueda == 'search.txt':
                            params["url"] = url
                            server_rtmp(params)                        
                            server = params.get("server")
                            plugintools.log("params en simpletv" +repr(params) )
                            url = params.get("url")
                            plugintools.add_item( action = "launch_rtmp" , title = '[COLOR white]' + titulo + '[COLOR green] [' + server + '][/COLOR][I][COLOR lightgreen] (' + origen + ')[/COLOR][/I]' , url = params.get("url") , info_labels = datamovie , thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                            print url                        
                            data = file.readline()
                            i = i + 1
                            continue
                        else:
                            params["url"] = url
                            server_rtmp(params)                         
                            server = params.get("server")
                            plugintools.log("fanart= "+fanart)
                            plugintools.log("params en simpletv" +repr(params) )
                            url = params.get("url")                            
                            plugintools.add_item( action = "launch_rtmp" , title = '[COLOR white]' + title + ''+ server + '[/COLOR]' , plot = plot , url = params.get("url") , info_labels = datamovie , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                            print url
                            data = file.readline()
                            i = i + 1
                            continue

                if data.startswith("udp") == True or data.startswith("rtp") == True:
                    # print "udp"
                    url = data
                    url = parse_url(url)
                    plugintools.log("url retornada= "+url)
                    if cat != "":  # Controlamos el caso de subcategoría de canales
                        if busqueda == 'search.txt':
                            plugintools.add_item( action = "play" , title = '[COLOR white]' + titulo + '[COLOR red] [UDP][/COLOR][I][COLOR lightgreen] (' + origen + ')[/COLOR][/I]', url = url , info_labels = datamovie , thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                            data = file.readline()
                            i = i + 1
                            continue
                        else:
                            plugintools.add_item( action = "play" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR red] [UDP][/COLOR]' , plot = plot , url = url , info_labels = datamovie , thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                            data = file.readline()
                            i = i + 1
                            continue
                            
                    else:
                        if busqueda == 'search.txt':
                            plugintools.add_item( action = "play" , title = '[COLOR white]' + titulo + '[COLOR red] [UDP][/COLOR][I][COLOR lightgreen] (' + origen + ')[/COLOR][/I]' , url = url , info_labels = datamovie , thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                            data = file.readline()
                            i = i + 1
                            continue
                        else:
                            plugintools.add_item( action = "play" , title = '[COLOR white]' + title + '[COLOR red] [UDP][/COLOR]' , plot = plot , url = url , info_labels = datamovie , thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                            data = file.readline()
                            i = i + 1
                            continue

                if data.startswith("mms") == True or data.startswith("rtp") == True:
                    # print "udp"
                    url = data
                    url = parse_url(url)
                    plugintools.log("url retornada= "+url)
                    if cat != "":  # Controlamos el caso de subcategoría de canales
                        if busqueda == 'search.txt':
                            plugintools.add_item( action = "play" , title = '[COLOR white]' + titulo + '[COLOR red] [MMS][/COLOR][I][COLOR lightgreen] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                            data = file.readline()
                            i = i + 1
                            continue
                        else:
                            plugintools.add_item( action = "play" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR red] [MMS][/COLOR]' , plot = plot , url = url , thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                            data = file.readline()
                            i = i + 1
                            continue
                            
                    else:
                        if busqueda == 'search.txt':
                            plugintools.add_item( action = "play" , title = '[COLOR white]' + titulo + '[COLOR red] [MMS][/COLOR][I][COLOR lightgreen] (' + origen + ')[/COLOR][/I]' , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                            data = file.readline()
                            i = i + 1
                            continue
                        else:                            
                            plugintools.add_item( action = "play" , title = '[COLOR white]' + title + '[COLOR red] [MMS][/COLOR]' , plot = plot , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                            data = file.readline()
                            i = i + 1
                            continue                      

                if data.startswith("plugin") == True:
                    title = title.split('"')
                    title = title[0]
                    title = title.strip()
                    title = title.replace("#EXTINF:-1,", "")
                    url = data
                    url = url.strip()
                    if url.startswith("plugin") == True:
                        if url.find("plugin.video.f4mTester") >= 0:
                            if cat != "":
                                if busqueda == 'search.txt':
                                    plugintools.add_item( action = "play" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR orange] [F4M][/COLOR][I][COLOR lightblue] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = art + "icon.png" , fanart = art + 'fanart.jpg' , show = show, folder = False , isPlayable = True )
                                    data = file.readline()
                                    i = i + 1
                                    continue
                                else:                                    
                                    plugintools.add_item( action = "play" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR orange] [F4M][/COLOR]', plot = plot , url = url , thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                    data = file.readline()
                                    i = i + 1
                                    continue
                            else:
                                if busqueda == 'search.txt':
                                    plugintools.add_item( action = "play" , title = '[COLOR white]' + title + '[COLOR orange] [F4M][/COLOR][I][COLOR lightblue] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = art + "icon.png" , fanart = art + 'fanart.jpg' , show = show, folder = False , isPlayable = True )
                                    data = file.readline()
                                    i = i + 1
                                    continue
                                else:                                    
                                    plugintools.add_item( action = "play" , title = '[COLOR white]' + title + '[COLOR orange] [F4M][/COLOR]', plot = plot , url = url , thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                    data = file.readline()
                                    i = i + 1
                                    continue

                    elif url.startswith("plugin://plugin.video.live.streamspro/") == True :
                        if cat != "":                      
                            if busqueda == 'search.txt':
                                plugintools.add_item( action = "play" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR orange] [Livestreams][/COLOR][I][COLOR lightblue] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = art + "icon.png" , fanart = art + 'fanart.jpg' , show = show, folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue
                            else:                                
                                plugintools.add_item( action = "play" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR orange] [Livestreams][/COLOR]', plot = plot , url = url , thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue
                        else:
                            if busqueda == 'search.txt':
                                plugintools.add_item( action = "play" , title = '[COLOR white]' + title + '[COLOR orange] [Livestreams][/COLOR][I][COLOR lightblue] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = art + "icon.png" , fanart = art + 'fanart.jpg' , show = show, folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue
                            else:                                
                                plugintools.add_item( action = "play" , title = '[COLOR white]' + title + '[COLOR orange] [Livestreams][/COLOR]', plot = plot , url = url , thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue
                            
                    elif url.find("plugin.video.youtube") >= 0 :
                        if cat != "":                      
                            if busqueda == 'search.txt':
                                plugintools.add_item( action = "play" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR white] [You[COLOR red]Tube[/COLOR][COLOR white] Video][/COLOR][I][COLOR lightblue] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = art + "icon.png" , fanart = art + 'fanart.jpg' , show = show, folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue
                            else:
                                plugintools.add_item( action = "play" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR white] [You[COLOR red]Tube[/COLOR][COLOR white] Video][/COLOR]', url = url , thumbnail = thumbnail , fanart = fanart , show = show, folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue
                        else:
                            if busqueda == 'search.txt':
                                plugintools.add_item( action = "play" , title = '[COLOR white] ' + title + '[COLOR white] [You[COLOR red]Tube[/COLOR][COLOR white] Video][/COLOR][I][COLOR lightblue] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = art + "icon.png" , fanart = art + 'fanart.jpg' , show = show, folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue
                            else:
                                plugintools.add_item( action = "play" , title = '[COLOR white] ' + title + '[COLOR white] [You[COLOR red]Tube[/COLOR][COLOR white] Video][/COLOR]', url = url , thumbnail = thumbnail , fanart = fanart , show = show, folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue                            
                        
                    elif url.find("mode=1") >= 0 :
                        if cat != "":
                            if busqueda == 'search.txt':
                                plugintools.add_item( action = "play" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + ' [COLOR lightblue] [Acestream][/COLOR][I][COLOR lightblue] (' + origen + ')[/COLOR][/I]' , url = url ,  thumbnail = thumbnail , fanart = fanart , show = show, folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue
                            else:
                                plugintools.add_item( action = "play" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR lightblue] [Acestream][/COLOR]' , plot = plot , url = url ,  thumbnail = thumbnail , fanart = fanart , show = show, folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue
                        else:
                            if busqueda == 'search.txt':
                                plugintools.add_item( action = "play" , title = '[COLOR white]' + title + ' [COLOR lightblue] [Acestream][/COLOR][I][COLOR lightblue] (' + origen + ')[/COLOR][/I]' , url = url ,  thumbnail = thumbnail , fanart = fanart , show = show, folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue
                            else:
                                plugintools.add_item( action = "play" , title = '[COLOR white]' + title + '[COLOR lightblue] [Acestream][/COLOR]' , plot = plot , url = url ,  thumbnail = thumbnail , fanart = fanart , show = show, folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue                            
                        
                    elif url.find("mode=2") >= 0 :
                        if cat != "":
                            if busqueda == 'search.txt':
                                plugintools.add_item( action = "play" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + ' [COLOR darkorange] [Sopcast][/COLOR][I][COLOR lightblue] (' + origen + ')[/COLOR][/I]' , url = url ,  thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue
                            else:                                
                                plugintools.add_item( action = "play" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR darkorange] [Sopcast][/COLOR]' , plot = plot , url = url ,  thumbnail = thumbnail , fanart = fanart , show = show, folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue
                        else:
                            if busqueda == 'search.txt':
                                plugintools.add_item( action = "play" , title = '[COLOR white] ' + title + ' [COLOR darkorange] [Sopcast][/COLOR][I][COLOR lightblue] (' + origen + ')[/COLOR][/I]' , url = url ,  thumbnail = thumbnail , fanart = fanart , show = show, folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue
                            else:                                
                                plugintools.add_item( action = "play" , title = '[COLOR white] ' + title + '[COLOR darkorange] [Sopcast][/COLOR]' , plot = plot , url = url ,  thumbnail = thumbnail , fanart = fanart , show = show, folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue

                elif data.startswith("magnet") == True:
                    if cat != "":
                        if busqueda == 'search.txt':
                            url = urllib.quote_plus(data)
                            title = parser_title(title)
                            url = launch_torrent(url)
                            plugintools.add_item( action = "play" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR orangered] [Torrent][/COLOR][I][COLOR lightblue] (' + origen + ')[/COLOR][/I]', url = url , thumbnail = thumbnail , fanart = fanart , show = show, folder = False , isPlayable = True )
                            data = file.readline()
                            i = i + 1
                            continue
                        else:
                            data = data.strip()
                            url = urllib.quote_plus(data).strip()                      
                            title = parser_title(title)
                            url = launch_torrent(url)
                            plugintools.add_item( action = "play" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + ' [COLOR orangered][Torrent][/COLOR]', url = url , thumbnail = thumbnail , fanart = fanart , show = show, folder = False , isPlayable = True )
                            data = file.readline()
                            i = i + 1
                            continue
                    else:
                        if busqueda == 'search.txt':
                            url = urllib.quote_plus(data)
                            url = launch_torrent(url)
                            title = parser_title(title)
                            plugintools.add_item( action = "play" , title = '[COLOR white]' + title + '[COLOR orangered] [Torrent][/COLOR][I][COLOR lightblue] (' + origen + ')[/COLOR][/I]', url = url , thumbnail = thumbnail , fanart = fanart , show = show, folder = False , isPlayable = True )
                            data = file.readline()
                            i = i + 1
                            continue
                        else:
                            title = parser_title(title)
                            data = data.strip()
                            url = urllib.quote_plus(data)
                            url = launch_torrent(url)
                            plugintools.add_item( action = "play" , title = '[COLOR white]' + title + ' [COLOR orangered][Torrent][/COLOR]', url = url , thumbnail = thumbnail , fanart = fanart , show = show, folder = False , isPlayable = True )
                            data = file.readline()
                            i = i + 1
                            continue

                elif data.startswith("torrent") == True:  # Torrent file (URL)
                    url = data.replace("torrent:", "").strip()
                    if cat != "":
                        if busqueda == 'search.txt':
                            title = parser_title(title)
                            url = launch_torrent(url)
                            plugintools.log("url= "+url)
                            plugintools.add_item( action = "play" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR orangered] [Torrent file][/COLOR][I][COLOR lightblue] (' + origen + ')[/COLOR][/I]', url = url , thumbnail = thumbnail , fanart = fanart , show = show, folder = False , isPlayable = True )
                            data = file.readline()
                            i = i + 1
                            continue
                        else:
                            data = data.strip()
                            title = parser_title(title)
                            url = launch_torrent(url)
                            plugintools.log("url= "+url)
                            plugintools.add_item( action = "play" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + ' [COLOR orangered][Torrent file][/COLOR]', url = url , thumbnail = thumbnail , fanart = fanart , show = show, folder = False , isPlayable = True )
                            data = file.readline()
                            i = i + 1
                            continue
                    else:
                        if busqueda == 'search.txt':                            
                            url = launch_torrent(url)
                            plugintools.log("url= "+url)
                            plugintools.add_item( action = "play" , title = '[COLOR white]' + title + '[COLOR orangered] [Torrent file][/COLOR][I][COLOR lightblue] (' + origen + ')[/COLOR][/I]', url = url , thumbnail = thumbnail , fanart = fanart , show = show, folder = False , isPlayable = True )
                            data = file.readline()
                            i = i + 1
                            continue
                        else:
                            title = parser_title(title)
                            data = data.strip()                            
                            url = launch_torrent(url)
                            plugintools.log("url= "+url)
                            plugintools.add_item( action = "play" , title = '[COLOR white]' + title + ' [COLOR orangered][Torrent file][/COLOR]', url = url , thumbnail = thumbnail , fanart = fanart , show = show, folder = False , isPlayable = True )
                            data = file.readline()
                            i = i + 1
                            continue                        
                        
                elif data.startswith("sop") == True:
                    if cat != "":
                        if busqueda == 'search.txt':
                            title = title.split('"')
                            title = title[0]
                            title = title.replace("#EXTINF:-1,", "")
                            # plugin://plugin.video.p2p-streams/?url=sop://124.232.150.188:3912/11265&mode=2&name=Titulo+canal+Sopcast
                            url = 'plugin://plugin.video.p2p-streams/?url=' + data + '&mode=2&name='
                            url = url.strip()
                            plugintools.add_item( action = "play" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR darkorange] [Sopcast][/COLOR][I][COLOR lightblue] (' + origen + ')[/COLOR][/I]', url = url , thumbnail = thumbnail , fanart = fanart , show = show, folder = False , isPlayable = True )
                            data = file.readline()
                            i = i + 1
                            continue
                        else:
                            title = title.split('"')
                            title = title[0]
                            title = title.replace("#EXTINF:-1,", "")
                            url = 'plugin://plugin.video.p2p-streams/?url=' + data + '&mode=2&name='
                            plugintools.add_item( action = "play" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + ' [COLOR darkorange][Sopcast][/COLOR]', plot = plot , url = url , thumbnail = thumbnail , fanart = fanart , show = show, folder = False , isPlayable = True )
                            data = file.readline()
                            i = i + 1
                            continue
                    else:
                        if busqueda == 'search.txt':
                            title = title.split('"')
                            title = title[0]
                            title = title.replace("#EXTINF:-1,", "")
                            url = 'plugin://plugin.video.p2p-streams/?url=' + data + '&mode=2&name='
                            plugintools.add_item( action = "play" , title = '[COLOR white]' + title + '[COLOR darkorange] [Sopcast][/COLOR][I][COLOR lightblue] (' + origen + ')[/COLOR][/I]', url = url , thumbnail = thumbnail , fanart = fanart , show = show, folder = False , isPlayable = True )
                            data = file.readline()
                            i = i + 1
                            continue
                        else:
                            title = title.split('"')
                            title = title[0]
                            title = title.replace("#EXTINF:-1,", "")
                            url = 'plugin://plugin.video.p2p-streams/?url=' + data + '&mode=2&name='
                            plugintools.add_item( action = "play" , title = '[COLOR white]' + title + ' [COLOR darkorange][Sopcast][/COLOR]', plot = plot , url = url , thumbnail = thumbnail , fanart = fanart , show = show, folder = False , isPlayable = True )
                            data = file.readline()
                            i = i + 1
                            continue                        

                elif data.startswith("ace") == True:
                    if cat != "":
                        if busqueda == 'search.txt':
                            # plugin://plugin.video.p2p-streams/?url=a55f96dd386b7722380802b6afffc97ff98903ac&mode=1&name=Sky+Sports+title
                            title = parser_title(title)
                            title = title.strip()
                            title_fixed = title.replace(" ", "+")
                            url = data.replace("ace:", "")
                            url = url.strip()
                            url = 'plugin://plugin.video.p2p-streams/?url=' + url + '&mode=1&name=' + title_fixed
                            plugintools.add_item(action="play" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + ' [COLOR lightblue][Acestream][/COLOR] [COLOR lightblue][I](' + origen + ')[/COLOR][/I]' , url = url, thumbnail = thumbnail , fanart = fanart , show = show, folder = False , isPlayable = True)
                            data = file.readline()
                            data = data.strip()
                            i = i + 1
                            continue
                        else:
                            title = parser_title(title)
                            print 'data',data
                            url = data.replace("ace:", "")
                            url = url.strip()
                            print 'url',url
                            url = 'plugin://plugin.video.p2p-streams/?url=' + url + '&mode=1&name='
                            plugintools.add_item(action="play" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + ' [COLOR lightblue][Acestream][/COLOR]' , plot = plot , url = url, thumbnail = thumbnail , fanart = fanart , show = show, folder = False , isPlayable = True)
                            data = file.readline()
                            data = data.strip()
                            i = i + 1
                            continue
                    else:
                        if busqueda == 'search.txt':
                            # plugin://plugin.video.p2p-streams/?url=a55f96dd386b7722380802b6afffc97ff98903ac&mode=1&name=Sky+Sports+title
                            title = parser_title(title)
                            url = data.replace("ace:", "")
                            url = url.strip()
                            url = 'plugin://plugin.video.p2p-streams/?url=' + url + '&mode=1&name='
                            plugintools.add_item(action="play" , title = '[COLOR white]' + title + ' [COLOR lightblue][Acestream][/COLOR] [COLOR lightblue][I](' + origen + ')[/COLOR][/I]' , url = url, thumbnail = thumbnail , fanart = fanart , show = show, folder = False , isPlayable = True)
                            data = file.readline()
                            data = data.strip()
                            i = i + 1
                            continue
                        else:
                            title = parser_title(title)
                            print 'data',data
                            url = data.replace("ace:", "")
                            url = url.strip()
                            print 'url',url
                            url = 'plugin://plugin.video.p2p-streams/?url=' + url + '&mode=1&name='                            
                            plugintools.add_item(action="play" , title = '[COLOR white]' + title + ' [COLOR lightblue][Acestream][/COLOR]' , plot = plot , url = url, thumbnail = thumbnail , fanart = fanart , show = show, folder = False , isPlayable = True)
                            data = file.readline()
                            data = data.strip()
                            i = i + 1
                            continue                        
                
                # Youtube playlist & channel    
                elif data.startswith("yt") == True:
                    if data.startswith("yt_playlist") == True:
                        if busqueda == 'search.txt':
                            title = title.split('"')
                            title = title[0]
                            title = title.replace("#EXTINF:-1,", "")
                            youtube_playlist = data.replace("yt_playlist(", "")
                            youtube_playlist = youtube_playlist.replace(")", "")
                            plugintools.log("youtube_playlist= "+youtube_playlist)
                            url = 'https://www.youtube.com/playlist?list='+youtube_playlist
                            plugintools.add_item( action = "yt_playlist" , title = '[[COLOR white]' + title + ' [COLOR red][You[COLOR white]Tube Playlist][/COLOR] [I][COLOR lightblue](' + origen + ')[/I][/COLOR]', url = url ,  thumbnail = thumbnail , fanart = fanart , show = show, folder = True , isPlayable = False )
                            data = file.readline()
                            i = i + 1
                            continue
                        else:
                            title = title.split('"')
                            title = title[0]
                            title = title.replace("#EXTINF:-1,", "")
                            plugintools.log("title= "+title)
                            youtube_playlist = data.replace("yt_playlist(", "")
                            youtube_playlist = youtube_playlist.replace(")", "")
                            plugintools.log("youtube_playlist= "+youtube_playlist)                    
                            url = 'https://www.youtube.com/playlist?list='+youtube_playlist                            
                            plugintools.add_item( action = "yt_playlist" , title = '[COLOR white]' + title + ' [COLOR red][You[COLOR white]Tube Playlist][/COLOR]', url = url ,  thumbnail = thumbnail , fanart = fanart , show = show, folder = True , isPlayable = False )
                            data = file.readline()
                            i = i + 1
                            continue                   

                    elif data.startswith("yt_channel") == True:
                        if busqueda == 'search.txt':
                            title = title.split('"')
                            title = title[0]
                            title = title.replace("#EXTINF:-1,", "")
                            youtube_channel = data.replace("yt_channel(", "")
                            youtube_channel = youtube_channel.replace(")", "")
                            plugintools.log("youtube_user= "+youtube_channel)
                            url = 'http://gdata.youtube.com/feeds/api/users/' + youtube_channel + '/playlists?v=2&start-index=1&max-results=30'
                            plugintools.add_item( action = "youtube_playlists" , title = '[[COLOR white]' + title + ' [COLOR red][You[COLOR white]Tube Channel][/COLOR] [I][COLOR lightblue](' + origen + ')[/I][/COLOR]', url = url ,  thumbnail = thumbnail , fanart = fanart , show = show, folder = True , isPlayable = False )
                            data = file.readline()
                            i = i + 1
                            continue
                        else:
                            title = title.split('"')
                            title = title[0]
                            title = title.replace("#EXTINF:-1,", "")
                            plugintools.log("title= "+title)
                            youtube_channel = data.replace("yt_channel(", "")
                            youtube_channel = youtube_channel.replace(")", "")
                            youtube_channel = youtube_channel.strip()                 
                            url = 'http://gdata.youtube.com/feeds/api/users/' + youtube_channel + '/playlists?v=2&start-index=1&max-results=30'
                            plugintools.log("url= "+url)                            
                            plugintools.add_item( action = "youtube_playlists" , title = '[COLOR white]' + title + ' [COLOR red][You[COLOR white]Tube Channel][/COLOR]', url = url ,  thumbnail = thumbnail , fanart = fanart , show = show, folder = True , isPlayable = False )
                            data = file.readline()
                            i = i + 1
                            continue
                        
                elif data.startswith("m3u") == True:
                    if busqueda == 'search.txt':
                        url = data.replace("m3u:", "")
                        data = file.readline()
                        if data.startswith("desc=") == True:
                            plot = data.replace("desc=", "")                            
                        else:
                            plot = ""
                        plugintools.add_item( action = "getfile_http" , title = title + ' [I][COLOR lightblue](' + origen + ')[/I][/COLOR]', url = url ,  thumbnail = thumbnail , fanart = fanart , show = show, folder = True , isPlayable = False )
                        data = file.readline()
                        i = i + 1
                        continue
                    else:
                        url = data.replace("m3u:", "")
                        data = file.readline()
                        if data.startswith("desc=") == True:
                            data = data.replace("desc=", "")
                            data = data.replace('"', "")
                            datamovie = {}
                            datamovie["Plot"] = data
                            #plugintools.log("SHOW= "+show)
                            if plugintools.get_setting("nolabel") == "true":
                                plugintools.add_item( action = "getfile_http" , title = title, info_labels = datamovie , url = url ,  thumbnail = thumbnail , fanart = fanart , show = show, folder = True , isPlayable = False )
                            else:
                                plugintools.add_item( action = "getfile_http" , title = title + ' [COLOR orange][Lista [B]M3U[/B]][/COLOR]', info_labels = datamovie , url = url , thumbnail = thumbnail , fanart = fanart , show = show, folder = True , isPlayable = False )
                            data = file.readline()
                            i = i + 1
                            continue
                        else:
                           # plugintools.log("SHOW= "+show)
                            if plugintools.get_setting("nolabel") == "true":
                                plugintools.add_item( action = "getfile_http" , title = title, url = url ,  thumbnail = thumbnail , fanart = fanart , show = show, folder = True , isPlayable = False )
                            else:
                                plugintools.add_item( action = "getfile_http" , title = title + ' [COLOR orange][Lista [B]M3U[/B]][/COLOR]', url = url ,  thumbnail = thumbnail , fanart = fanart , show = show, folder = True , isPlayable = False )                                                
                            i = i + 1
                            continue


                elif data.startswith("plx") == True:
                    if busqueda == 'search.txt':
                        url = data.replace("plx:", "")
                        # Se añade parámetro plot porque en las listas PLX no tengo en una función separada la descarga (FIX IT!)
                        plugintools.add_item( action = "plx_items" , plot = "" , title = title + ' [I][/COLOR][COLOR lightblue](' + origen + ')[/I][/COLOR]', url = url ,  thumbnail = thumbnail , fanart = fanart , show = show, folder = True , isPlayable = False )
                        data = file.readline()
                        i = i + 1
                        continue
                    else:
                        url = data.replace("plx:", "")
                        # Se añade parámetro plot porque en las listas PLX no tengo en una función separada la descarga (FIX IT!)                        
                        plugintools.add_item( action = "plx_items" , plot = "" , title = title + '', url = url ,  thumbnail = thumbnail , fanart = fanart , show = show, folder = True , isPlayable = False )
                        data = file.readline()
                        i = i + 1
                        continue

                elif data.startswith("goear") == True:
                    if busqueda == 'search.txt':
                        plugintools.add_item( action = "goear" , title = title + ' [I][/COLOR][COLOR lightblue](' + origen + ')[/I][/COLOR]', url = url ,  thumbnail = thumbnail , fanart = fanart , show = show, extra = show , folder = True , isPlayable = False )
                        data = file.readline()
                        i = i + 1
                        continue
                    else:
                        data = file.readline()
                        if show == "list":
                            show = plugintools.get_setting("music_id")
                            #plugintools.log("show en config")                        
                        if data.startswith("desc") == True:
                            datamovie["Plot"] = data.replace("desc=", "").replace('"',"").strip()                            
                        plugintools.add_item( action = "goear" , plot = plot , title = title + ' [COLOR blue][goear][/COLOR]', url = url , info_labels = datamovie , thumbnail = thumbnail , fanart = fanart , show = show, extra = show , folder = True , isPlayable = False )
                        data = file.readline()
                        i = i + 1
                        continue                    
                    
                
            else:
                data = file.readline()
                i = i + 1
                continue

        else:
            data = file.readline()
            i = i + 1
            
    
    file.close()
    plugintools.modo_vista(show)
    if title == 'search.txt':
            os.remove(tmp + title)

    plugintools.log("follower= "+str(follower))
    if follower == 1:
        if os.path.isfile(playlists + filename):
            os.remove(playlists + filename)
            print "Borrado correcto!"
        else:
            pass              



def myplaylists_m3u(params):  # Mis listas M3U
    plugintools.log('[%s %s].myplaylists_m3u %s' % (addonName, addonVersion, repr(params)))
    thumbnail = params.get("thumbnail")
    #plugintools.add_item(action="play" , title = "[COLOR lightyellow]Cómo importar listas M3U a mi biblioteca [/COLOR][COLOR lightblue][I][Youtube][/I][/COLOR]" , thumbnail = art + "icon.png" , url = "plugin://plugin.video.youtube/?path=/root/video&action=play_video&videoid=8i0KouM-4-U" , folder = False , isPlayable = True )
    plugintools.add_item(action="my_albums" , title = "[COLOR gold][B]Mis álbumes[/B][/COLOR][COLOR lightblue][I] (CBR/CBZ)[/I][/COLOR]" , thumbnail = art + "search.png" , fanart = art + 'fanart.jpg' , folder = True , isPlayable = False )
    plugintools.add_item(action="search_channel" , title = "[COLOR lightyellow]Buscador[/COLOR]" , thumbnail = art + "search.png" , fanart = art + 'fanart.jpg' , folder = True , isPlayable = False )

    # Agregamos listas online privadas del usuario
    add_playlist(params)

    ficheros = os.listdir(playlists)  # Lectura de archivos en carpeta /playlists. Cuidado con las barras inclinadas en Windows

    # Control paternal
    pekes_no = plugintools.get_setting("pekes_no")

    for entry in ficheros:
        plot = entry.split(".")
        plot = plot[0]
        plugintools.log("entry= "+entry)

        if pekes_no == "true" :
            print "Control paternal en marcha"
            if entry.find("XXX") >= 0 :
                plugintools.log("Activando control paternal...")

            else:
                if entry.endswith("plx") == True:  # Control para según qué extensión del archivo se elija thumbnail y función a ejecutar
                    entry = entry.replace(".plx", "")
                    plugintools.add_item(action="plx_items" , plot = plot , title = '[COLOR white]' + entry + '[/COLOR][COLOR green][B][I].plx[/I][/B][/COLOR]' , url = playlists + entry , thumbnail = art + 'plx3.png' , fanart = art + 'fanart.jpg' , folder = True , isPlayable = False )

                elif entry.endswith("p2p") == True:
                    entry = entry.replace(".p2p", "")
                    plugintools.add_item(action="p2p_items" , plot = plot , title = '[COLOR white]' + entry + '[COLOR blue][B][I].p2p[/I][/B][/COLOR]', url = playlists + entry , thumbnail = art + 'p2p.png' , fanart = art + 'fanart.jpg' , folder = True , isPlayable = False )

                elif entry.endswith("m3u") == True:
                    entry = entry.replace(".m3u", "")
                    plugintools.add_item(action="simpletv_items" , plot = plot , title = '[COLOR white]' + entry + '[COLOR red][B][I].m3u[/I][/B][/COLOR]', url = playlists + entry , thumbnail = art + 'm3u7.png' , fanart = art + 'fanart.jpg' , folder = True , isPlayable = False )

                elif entry.endswith("jsn") == True:
                    entry = entry.replace(".jsn", "")
                    plugintools.add_item(action="json_items" , plot = plot , title = '[COLOR white]' + entry + '[COLOR yellow][B][I].jsn[/I][/B][/COLOR]', url = playlists + entry , thumbnail = art + 'm3u7.png' , fanart = art + 'fanart.jpg' , folder = True , isPlayable = False )

        else:

                if entry.endswith("plx") == True:  # Control para según qué extensión del archivo se elija thumbnail y función a ejecutar
                    entry = entry.replace(".plx", "")
                    plugintools.add_item(action="plx_items" , plot = plot , title = '[COLOR white]' + entry + '[/COLOR][COLOR green][B][I].plx[/I][/B][/COLOR]' , url = playlists + entry , thumbnail = art + 'plx3.png' , fanart = art + 'fanart.jpg' , folder = True , isPlayable = False )

                elif entry.endswith("p2p") == True:
                    entry = entry.replace(".p2p", "")
                    plugintools.add_item(action="p2p_items" , plot = plot , title = '[COLOR white]' + entry + '[COLOR blue][B][I].p2p[/I][/B][/COLOR]', url = playlists + entry , thumbnail = art + 'p2p.png' , fanart = art + 'fanart.jpg' , folder = True , isPlayable = False )

                elif entry.endswith("m3u") == True:
                    entry = entry.replace(".m3u", "")
                    plugintools.add_item(action="simpletv_items" , plot = plot , title = '[COLOR white]' + entry + '[COLOR red][B][I].m3u[/I][/B][/COLOR]', url = playlists + entry , thumbnail = art + 'm3u7.png' , fanart = art + 'fanart.jpg' , folder = True , isPlayable = False )

                elif entry.endswith("jsn") == True:
                    entry = entry.replace(".jsn", "")
                    plugintools.add_item(action="json_items" , plot = plot , title = '[COLOR white]' + entry + '[COLOR yellow][B][I].jsn[/I][/B][/COLOR]', url = playlists + entry , thumbnail = art + 'm3u7.png' , fanart = art + 'fanart.jpg' , folder = True , isPlayable = False )


def my_albums(params):  # Mis listas M3U
    plugintools.log('[%s %s].my_albums %s' % (addonName, addonVersion, repr(params)))
    thumbnail = params.get("thumbnail")

    plugintools.add_item(action="" , title = "[COLOR gold][B]Mis álbumes[/B][/COLOR][COLOR lightblue][I] (CBR/CBZ)[/I][/COLOR]" , thumbnail = art + "albums_icon.png" , fanart = art + 'my_albums.jpg' , folder = False , isPlayable = False )
    ficheros = os.listdir(tmp)  # Lectura de archivos en carpeta /tmp. Cuidado con las barras inclinadas en Windows

    # Control paternal
    pekes_no = plugintools.get_setting("pekes_no")

    for entry in ficheros:
        plot = entry.split(".")
        plot = plot[0]
        plugintools.log("entry= "+entry)

        if pekes_no == "true" :
            print "Control paternal en marcha"
            if entry.find("XXX") >= 0 :
                plugintools.log("Activando control paternal...")

            else:
                if entry.endswith("cbr") == True:  # Control para según qué extensión del archivo se elija thumbnail y función a ejecutar
                    entry = entry.replace(".cbr", "")
                    plugintools.add_item(action="cbx_reader" , plot = plot , title = '[COLOR white]' + entry + '[/COLOR][COLOR green][B][I].cbr[/I][/B][/COLOR]' , extra = "my_albums", url = playlists + entry , thumbnail = art+'cbr.png' , fanart = art + 'my_albums.jpg' , folder = True , isPlayable = False )

                elif entry.endswith("cbz") == True:
                    entry = entry.replace(".cbz", "")
                    plugintools.add_item(action="cbx_reader" , plot = plot , title = '[COLOR white]' + entry + '[COLOR blue][B][I].cbz[/I][/B][/COLOR]', extra = "my_albums" , url = playlists + entry , thumbnail = art+'cbz.png' , fanart = art + 'my_albums.jpg' , folder = True , isPlayable = False )

        else:

                if entry.endswith("cbr") == True:  # Control para según qué extensión del archivo se elija thumbnail y función a ejecutar
                    entry = entry.replace(".cbr", "")
                    plugintools.add_item(action="cbx_reader" , plot = plot , title = '[COLOR white]' + entry + '[/COLOR][COLOR green][B][I].cbr[/I][/B][/COLOR]' , extra = "my_albums" , url = playlists + entry , thumbnail = art+'cbr.png' , fanart = art + 'my_albums.jpg' , folder = True , isPlayable = False )

                elif entry.endswith("cbz") == True:
                    entry = entry.replace(".cbz", "")
                    plugintools.add_item(action="cbx_reader" , plot = plot , title = '[COLOR white]' + entry + '[COLOR blue][B][I].cbz[/I][/B][/COLOR]', extra = "my_albums" , url = playlists + entry , thumbnail = art+'cbz.png' , fanart = art + 'my_albums.jpg' , folder = True , isPlayable = False )



def playlists_m3u(params):  # Biblioteca online
    plugintools.log('[%s %s].playlists_m3u %s' % (addonName, addonVersion, repr(params)))

    data = plugintools.read( params.get("url") )
    name_channel = params.get("plot")
    pattern = '<name>'+name_channel+'(.*?)</channel>'
    data = plugintools.find_single_match(data, pattern)
    online = '[COLOR yellowgreen][I][Auto][/I][/COLOR]'
    params["ext"] = 'm3u'
    plugintools.add_item( action="" , title=''+name_channel+'' , thumbnail= art + 'icon.png' , folder = False , isPlayable = False )
    subchannel = re.compile('<subchannel>([^<]+)<name>([^<]+)</name>([^<]+)<thumbnail>([^<]+)</thumbnail>([^<]+)<url>([^<]+)</url>([^<]+)</subchannel>').findall(data)
    # Sustituir por una lista!!!
    for biny, ciny, diny, winy, pixy, dixy, boxy in subchannel:
        if ciny == "Vcx7 IPTV":
            plugintools.add_item( action="getfile_http" , plot = ciny , title = '[COLOR lightyellow]' + ciny + '[/COLOR] ' + online , url= dixy , thumbnail = art + winy , fanart = art + 'fanart.jpg' , folder = True , isPlayable = False )
            params["ext"] = "m3u"
            title = ciny
            params["title"]=title
        elif ciny == "Largo Barbate M3U":
            plugintools.add_item( action="getfile_http" , plot = ciny , title = '[COLOR lightyellow]' + ciny + '[/COLOR] ' + online , url= dixy , thumbnail = art + winy , fanart = art + 'fanart.jpg' , folder = True , isPlayable = False )
            title = ciny
            params["title"]=title
        elif ciny == "XBMC Mexico":
            plugintools.add_item( action="getfile_http" , plot = ciny , title = '[COLOR lightyellow]' + ciny + '[/COLOR] ' + online , url= dixy , thumbnail = art + winy , fanart = art + 'fanart.jpg' , folder = True , isPlayable = False )
            title = ciny
            params["title"]=title
        elif ciny == "allSat":
            plugintools.add_item( action="getfile_http" , plot = ciny , title = '[COLOR lightyellow]' + ciny + '[/COLOR] ' + online , url= dixy , thumbnail = art + winy , fanart = art + 'fanart.jpg' , folder = True , isPlayable = False )
            title = ciny
            params["title"]=title
        elif ciny == "AND Wonder":
            plugintools.add_item( action="getfile_http" , plot = ciny , title = '[COLOR lightyellow]' + ciny + '[/COLOR] ' + online , url= dixy , thumbnail = art + winy , fanart = art + 'fanart.jpg' , folder = True , isPlayable = False )
            title = ciny
            params["title"]=title
        elif ciny == "FenixTV":
            plugintools.add_item( action="getfile_http" , plot = ciny , title = '[COLOR lightyellow]' + ciny + '[/COLOR] ' + online , url= dixy , thumbnail = art + winy , fanart = art + 'fanart.jpg' , folder = True , isPlayable = False )
            title = ciny
            params["title"]=title
        else:
            plot = ciny.split("[")
            plot = plot[0]
            plugintools.add_item( action="getfile_http" , plot = plot , title = '[COLOR lightyellow]' + ciny + '[/COLOR] ' , url= dixy , thumbnail = art + winy , fanart = art + 'fanart.jpg' , folder = True , isPlayable = False )

    plugintools.log('[%s %s].playlists_m3u %s' % (addonName, addonVersion, repr(params)))    



def getfile_http(params):  # Descarga de lista M3U + llamada a simpletv_items para que liste los items
    plugintools.log('[%s %s].getfile_http ' % (addonName, addonVersion))
    
    url = params.get("url")
    params["ext"] = "m3u"
    getfile_url(params)
    simpletv_items(params)

        


def parse_url(url):
    # plugintools.log("url entrante= "+url)

    if url != "":
        url = url.strip()
        url = url.replace("rtmp://$OPT:rtmp-raw=", "")
        return url

    else:
        plugintools.log("error en url= ")  # Mostrar diálogo de error al parsear url (por no existir, por ejemplo)



def getfile_url(params):
    plugintools.log('[%s %s].getfile_url ' % (addonName, addonVersion))
    ext = params.get("ext")
    title = params.get("title")

    if ext == 'plx':
        filename = parser_title(title)
        params["plot"]=filename
        filename = title + ".plx"  # El título del archivo con extensión (m3u, p2p, plx)
    elif ext == 'm3u':
        filename = params.get("plot")
        # Vamos a quitar el formato al texto para que sea el nombre del archivo
        filename = parser_title(title)
        filename = filename + ".m3u"  # El título del archivo con extensión (m3u, p2p, plx)
    else:
        ext == 'p2p'
        filename = parser_title(title)
        filename = filename + ".p2p"  # El título del archivo con extensión (m3u, p2p, plx)

    if filename.endswith("plx") == True :
        filename = parser_title(filename)

    plugintools.log("filename= "+filename)
    url = params.get("url")
    
    try:
        response = urllib2.urlopen(url)
        body = response.read()
    except:
        # Control si la lista está en el cuerpo del HTTP
        request_headers=[]
        request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
        body,response_headers = plugintools.read_body_and_headers(url, headers=request_headers)

    #open the file for writing
    fh = open(playlists + filename, "wb")

    # read from request while writing to file
    fh.write(body)

    fh.close()

    file = open(playlists + filename, "r")
    file.seek(0)
    data = file.readline()
    data = data.strip()

    lista_items = {'linea': data}
    file.seek(0)
    lista_items = {'plot': data}
    file.seek(0)






def header_xml(params):
    plugintools.log('[%s %s].header_xml %s' % (addonName, addonVersion, repr(params)))

    url = params.get("url")
    params.get("title")
    data = plugintools.read(url)
    # plugintools.log("data= "+data)
    author = plugintools.find_single_match(data, '<poster>(.*?)</poster>')
    author = author.strip()
    fanart = plugintools.find_single_match(data, '<fanart>(.*?)</fanart>')
    message = plugintools.find_single_match(data, '<message>(.*?)</message>')
    desc = plugintools.find_single_match(data, '<description>(.*?)</description>')
    thumbnail = plugintools.find_single_match(data, '<thumbnail>(.*?)</thumbnail>')

    if author != "":
        if message != "":
            plugintools.add_item(action="" , plot = author , title = '[COLOR green][B]' + author + '[/B][/COLOR][I] ' + message + '[/I]', url = "" , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = False )
            return fanart
        else:
            plugintools.add_item(action="" , plot = author , title = '[COLOR green][B]' + author + '[/B][/COLOR]', url = "" , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = False )
            return fanart
    else:
        if desc != "":
            plugintools.add_item(action="" , plot = author , title = '[COLOR green][B]' + desc + '[/B][/COLOR]', url = "" , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = False )
            return fanart
        else:
            return fanart


def search_channel(params):
    plugintools.log('[%s %s].search_channel %s' % (addonName, addonVersion, repr(params)))

    buscar = params.get("plot")
    if buscar == "":
        last_search = plugintools.get_setting("last_search")
        texto = plugintools.keyboard_input(last_search)
        plugintools.set_setting("last_search",texto)
        params["texto"]=texto
        texto = texto.lower()
        cat = ""
        if texto == "":
            errormsg = plugintools.message("TvWin","Por favor, introduzca el canal a buscar")
            return errormsg

    else:
        texto = buscar
        texto = texto.lower()
        plugintools.log("texto a buscar= "+texto)
        cat = ""

    results = open(tmp + 'search.txt', "wb")
    results.seek(0)
    results.close()

    # Listamos archivos de la biblioteca local
    ficheros = os.listdir(playlists)  # Lectura de archivos en carpeta /playlists. Cuidado con las barras inclinadas en Windows

    for entry in ficheros:
        if entry.endswith("m3u") == True:
            print "Archivo tipo m3u"
            plot = entry.split(".")
            plot = plot[0]  # plot es la variable que recoge el nombre del archivo (sin extensión txt)
            # Abrimos el primer archivo
            filename = plot + '.m3u'
            plugintools.log("Archivo M3U: "+filename)
            arch = open(playlists + filename, "r")
            num_items = len(arch.readlines())
            print num_items
            i = 0  # Controlamos que no se salga del bucle while antes de que lea el último registro de la lista
            arch.seek(0)
            data = arch.readline()
            data = data.strip()
            plugintools.log("data linea= "+data)
            texto = texto.strip()
            plugintools.log("data_antes= "+data)
            plugintools.log("texto a buscar= "+texto)

            data = arch.readline()
            data = data.strip()
            i = i + 1
            while i <= num_items :
                if data.startswith('#EXTINF:-1') == True:
                    data = data.replace('#EXTINF:-1,', "")  # Ignoramos la primera parte de la línea
                    data = data.replace(",", "")
                    title = data.strip()  # Ya tenemos el título

                    if data.find('$ExtFilter="') >= 0:
                        data = data.replace('$ExtFilter="', "")

                    if data.find(' $ExtFilter="') >= 0:
                        data = data.replace('$ExtFilter="', "")

                    title = title.replace("-AZBOX*", "")
                    title = title.replace("AZBOX *", "")

                    images = m3u_items(title)
                    plugintools.modo_vista(show)  # Para no perder el modo de vista predefinido tras llamar a la función m3u_items
                    print 'images',images
                    thumbnail = images[0]
                    fanart = images[1]
                    cat = images[2]
                    title = images[3]
                    plugintools.log("title= "+title)
                    minus = title.lower()
                    data = arch.readline()
                    data = data.strip()
                    i = i + 1

                    if minus.find(texto) >= 0:
                    # if re.match(texto, title, re.IGNORECASE):
                        # plugintools.log("Concidencia hallada. Obtenemos url del canal: " + texto)
                        if data.startswith("http") == True:
                            url = data.strip()
                            if cat != "":  # Controlamos el caso de subcategoría de canales
                                results = open(tmp + 'search.txt', "a")
                                results.write("#EXTINF:-1," + title + '"' + filename + '\n')
                                results.write(url + '\n\n')
                                results.close()
                                data = arch.readline()
                                i = i + 1
                                continue
                            else:
                                results = open(tmp + 'search.txt', "a")
                                results.write("#EXTINF:-1," + title + '"' + filename + '\n')
                                results.write(url + '\n\n')
                                results.close()
                                data = arch.readline()
                                i = i + 1
                                continue
                        if data.startswith("rtmp") == True:
                            url = data
                            url = parse_url(url)
                            if cat != "":   # Controlamos el caso de subcategoría de canales
                                results = open(tmp + 'search.txt', "a")
                                results.write("#EXTINF:-1," + title + '"' + filename + '\n')
                                results.write(url + '\n\n')
                                results.close()
                                data = arch.readline()
                                i = i + 1
                                continue
                            else:
                                results = open(tmp + 'search.txt', "a")
                                results.write("#EXTINF:-1," + title + '"' + filename + '\n')
                                results.write(url + '\n\n')
                                results.close()
                                data = arch.readline()
                                i = i + 1
                                continue
                        if data.startswith("yt") == True:
                            print "CORRECTO"
                            url = data
                            results = open(tmp + 'search.txt', "a")
                            results.write("#EXTINF:-1," + title + '"' + filename + '\n')
                            results.write(url + '\n\n')
                            results.close()
                            data = arch.readline()
                            i = i + 1
                            continue


                else:
                    data = arch.readline()
                    data = data.strip()
                    plugintools.log("data_buscando_title= "+data)
                    i = i + 1

            else:
                data = arch.readline()
                data = data.strip()
                plugintools.log("data_final_while= "+data)
                i = i + 1
                continue



    # Listamos archivos de la biblioteca local
    ficheros = os.listdir(playlists)  # Lectura de archivos en carpeta /playlists. Cuidado con las barras inclinadas en Windows

    for entry in ficheros:
        if entry.endswith('p2p') == True:
            plot = entry.split(".")
            plot = plot[0]  # plot es la variable que recoge el nombre del archivo (sin extensión txt)
            # Abrimos el primer archivo
            plugintools.log("texto a buscar= "+texto)
            filename = plot + '.p2p'
            arch = open(playlists + filename, "r")
            num_items = len(arch.readlines())
            plugintools.log("archivo= "+filename)
            i = 0  # Controlamos que no se salga del bucle while antes de que lea el último registro de la lista
            arch.seek(0)
            while i <= num_items:
                data = arch.readline()
                data = data.strip()
                title = data
                texto = texto.strip()
                plugintools.log("linea a buscar title= "+data)
                i = i + 1

                if data.startswith("#") == True:
                    data = arch.readline()
                    data = data.strip()
                    i = i + 1
                    continue

                if data.startswith("default=") == True:
                    data = arch.readline()
                    data = data.strip()
                    i = i + 1
                    continue

                if data.startswith("art=") == True:
                    data = arch.readline()
                    data = data.strip()
                    i = i + 1
                    continue

                if data != "":
                    title = data.strip()  # Ya tenemos el título
                    plugintools.log("title= "+title)
                    minus = title.lower()
                    if minus.find(texto) >= 0:
                        plugintools.log("title= "+title)
                        data = arch.readline()
                        i = i + 1
                        #print i
                        plugintools.log("linea a comprobar url= "+data)
                        if data.startswith("sop") == True:
                            # plugin://plugin.video.p2p-streams/?url=sop://124.232.150.188:3912/11265&mode=2&name=Titulo+canal+Sopcast
                            title_fixed = title.replace(" " , "+")
                            url = 'plugin://plugin.video.p2p-streams/?url=' + data + '&mode=2&name=' + title_fixed
                            url = url.strip()
                            results = open(tmp + 'search.txt', "a")
                            results.write("#EXTINF:-1," + title + '"' + filename + '\n')  # Hay que cambiar esto! No puede agregar #EXTINF:-1, si no es una lista m3u
                            results.write(url + '\n\n')
                            results.close()
                            data = arch.readline()
                            i = i + 1
                            continue

                        elif data.startswith("magnet") == True:
                            # magnet:?xt=urn:btih:6CE983D676F2643430B177E2430042E4E65427...
                            title_fixed = title.split('"')
                            title = title_fixed[0]
                            plugintools.log("title magnet= "+title)
                            url = data
                            plugintools.log("url magnet= "+url)
                            results = open(tmp + 'search.txt', "a")
                            results.write("#EXTINF:-1," + title + '"' + filename + '\n')
                            results.write(url + '\n\n')
                            results.close()
                            data = arch.readline()
                            i = i + 1
                            continue

                        elif data.find("://") == -1:
                            # plugin://plugin.video.p2p-streams/?url=a55f96dd386b7722380802b6afffc97ff98903ac&mode=1&name=Sky+Sports+title
                            title_fixed = title.split('"')
                            title = title_fixed[0]
                            title_fixed = title.replace(" " , "+")
                            url = 'plugin://plugin.video.p2p-streams/?url=' + data + '&mode=1&name=' + title_fixed
                            results = open(tmp + 'search.txt', "a")
                            results.write("#EXTINF:-1," + title + '"' + filename + '\n')  # Hay que cambiar esto! No puede agregar #EXTINF:-1, si no es una lista m3u
                            results.write(url + '\n\n')
                            results.close()
                            data = arch.readline()
                            i = i + 1
                            continue

                    else:
                        plugintools.log("no coinciden titulo y texto a buscar")


    for entry in ficheros:
        if entry.endswith('plx') == True:
            plot = entry.split(".")
            plot = plot[0]  # plot es la variable que recoge el nombre del archivo (sin extensión)
            # Abrimos el primer archivo
            plugintools.log("texto a buscar= "+texto)
            filename = plot + '.plx'
            plugintools.log("archivo PLX: "+filename)
            arch = open(playlists + filename, "r")
            num_items = len(arch.readlines())
            print num_items
            i = 0
            arch.seek(0)
            while i <= num_items:
                data = arch.readline()
                data = data.strip()
                i = i + 1
                print i

                if data.startswith("#") == True:
                    continue

                if (data == 'type=video') or (data == 'type=audio') == True:
                    data = arch.readline()
                    i = i + 1
                    print i
                    data = data.replace("name=", "")
                    data = data.strip()
                    title = data
                    minus = title.lower()
                    if minus.find(texto) >= 0:
                        plugintools.log("Título coincidente= "+title)
                        data = arch.readline()
                        plugintools.log("Siguiente linea= "+data)
                        i = i + 1
                        print i
                        print "Analizamos..."
                        while data <> "" :
                            if data.startswith("thumb") == True:
                                data = arch.readline()
                                plugintools.log("data_plx= "+data)
                                i = i + 1
                                print i
                                continue

                            if data.startswith("date") == True:
                                data = arch.readline()
                                plugintools.log("data_plx= "+data)
                                i = i + 1
                                print i
                                continue

                            if data.startswith("background") == True:
                                data = arch.readline()
                                plugintools.log("data_plx= "+data)
                                i = i + 1
                                print i
                                continue

                            if data.startswith("URL") == True:
                                data = data.replace("URL=", "")
                                data = data.strip()
                                url = data
                                parse_url(url)
                                plugintools.log("URL= "+url)
                                results = open(tmp + 'search.txt', "a")
                                results.write("#EXTINF:-1," + title + '"' + filename + '\n')
                                results.write(url + '\n\n')
                                results.close()
                                data = arch.readline()
                                i = i + 1
                                break




    arch.close()
    results.close()
    params["plot"] = 'search'  # Pasamos a la lista de variables (params) el valor del archivo de resultados para que lo abra la función simpletv_items
    params['texto']= texto  # Agregamos al diccionario una nueva variable que contiene el texto a buscar
    simpletv_items(params)








def plx_items(params):
    plugintools.log('[%s %s].plx_items %s' % (addonName, addonVersion, repr(params)))

    fanart = ""
    thumbnail = ""
    datamovie = {}
    show = "THUMBNAIL"

    # Control para elegir el título (plot, si formateamos el título / title , si no existe plot)
    if params.get("plot") == "":
        title = params.get("title").strip() + '.plx'
        title = parser_title(title)
        title = title.strip()
        filename = title
        params["plot"]=filename
        params["ext"] = 'plx'
        getfile_url(params)
        title = params.get("title")
    else:
        title = params.get("plot")
        title = title.strip()
        title = parser_title(title)
        plugintools.log("Lectura del archivo PLX")

    title = title.replace(" .plx", ".plx")
    title = title.strip()
    file = open(playlists + parser_title(title) + '.plx', "r")
    file.seek(0)
    num_items = len(file.readlines())
    print num_items
    file.seek(0)

    # Lectura del título y fanart de la lista
    background = art + 'fanart.jpg'
    logo = art + 'plx3.png'
    file.seek(0)
    data = file.readline()
    while data <> "":
        plugintools.log("data= "+data)
        if data.startswith("background=") == True:
            data = data.replace("background=", "")
            background = data.strip()
            plugintools.log("background= "+background)
            if background == "":
                background = params.get("extra")
                if background == "":
                    background = art + 'fanart.jpg'

            data = file.readline()
            continue

        if data.startswith("title=") == True:
            name = data.replace("title=", "")
            name = name.strip()
            plugintools.log("name= "+name)
            if name == "Select sort order for this list":
                name = "Seleccione criterio para ordenar ésta lista... "
            data = file.readline()
            continue

        if data.startswith("logo=") == True:
            data = data.replace("logo=", "")
            logo = data.strip()
            plugintools.log("logo= "+logo)
            title = parser_title(title)
            if thumbnail == "":
                thumbnail = art + 'plx3.png'

            plugintools.add_item(action="" , title = '[COLOR lightyellow][B][I]playlist / '+ title + '[/B][/I][/COLOR]', url = playlists + title , thumbnail = logo , fanart = background , folder = False , isPlayable = False)
            plugintools.log("fanart= "+fanart)
            plugintools.add_item(action="" , title = '[I][B]' + name + '[/B][/I]' , url = "" , thumbnail = logo , fanart = background , folder = False , isPlayable = False)

            data = file.readline()
            break

        else:
            data = file.readline()


    try:
        data = file.readline()
        plugintools.log("data= "+data)
        if data.startswith("background=") == True:
            data = data.replace("background=", "")
            data = data.strip()
            fanart = data
            background = fanart
            plugintools.log("fanart= "+fanart)
        else:
            # data = file.readline()
            if data.startswith("background=") == True:
                print "Archivo plx!"
                data = data.replace("background=", "")
                fanart = data.strip()
                plugintools.log("fanart= "+fanart)
            else:
                if data.startswith("title=") == True:
                    name = data.replace("title=", "")
                    name = name.strip()
                    plugintools.log("name= "+name)
    except:
        plugintools.log("ERROR: Unable to load PLX file")


    data = file.readline()
    try:
        if data.startswith("title=") == True:
            data = data.replace("title=", "")
            name = data.strip()
            plugintools.log("title= "+title)
            plugintools.add_item(action="" , title = '[COLOR lightyellow][B][I]playlist / '+ title +'[/I][/B][/COLOR]' , url = playlists + title , thumbnail = logo , fanart = fanart , folder = False , isPlayable = False)
            plugintools.add_item(action="" , title = '[I][B]' + name + '[/B][/I]' , url = "" , thumbnail = art + "icon.png" , fanart = fanart , folder = False , isPlayable = False)
    except:
        plugintools.log("Unable to read PLX title")


    # Lectura de items

    i = 0
    file.seek(0)
    while i <= num_items:
        data = file.readline()
        data = data.strip()
        i = i + 1
        print i

        if data.startswith("#") == True:
            continue
        elif data.startswith("rating") == True:
            continue
        elif data.startswith("description") == True:
            continue

        if (data == 'type=comment') == True:
            data = file.readline()
            i = i + 1
            print i

            while data <> "" :
                if data.startswith("name") == True:
                    title = data.replace("name=", "")
                    data = file.readline()
                    data = data.strip()
                    i = i + 1
                    print i
                    continue

                elif data.startswith("thumb") == True:
                    data = data.replace("thumb=", "")
                    data = data.strip()
                    thumbnail = data
                    if thumbnail == "":
                        thumbnail = logo
                    data = file.readline()
                    data = data.strip()
                    i = i + 1
                    print i
                    continue

                elif data.startswith("background") == True:
                    data = data.replace("background=", "")
                    fanart = data.strip()
                    if fanart == "":
                        fanart = background
                    data = file.readline()
                    data = data.strip()
                    i = i + 1
                    print i
                    continue

            plugintools.add_item(action="", title = title , url = "", thumbnail = thumbnail , fanart = fanart , folder = False, isPlayable = False)

        if (data == 'type=video') or (data == 'type=audio') == True:
            data = file.readline()
            i = i + 1
            print i

            while data <> "" :
                if data.startswith("#") == True:
                    data = file.readline()
                    data = data.strip()
                    i = i + 1
                    print i
                    continue
                elif data.startswith("description") == True:
                    data = file.readline()
                    data = data.strip()
                    i = i + 1
                    print i
                    continue
                elif data.startswith("rating") == True:
                    data = file.readline()
                    data = data.strip()
                    i = i + 1
                    print i
                    continue
                elif data.startswith("name") == True:
                    data = data.replace("name=", "")
                    data = data.strip()
                    title = data
                    if title == "[COLOR=FF00FF00]by user-assigned order[/COLOR]" :
                        title = "Seleccione criterio para ordenar ésta lista... "

                    if title == "by user-assigned order" :
                        title = "Según se han agregado en la lista"

                    if title == "by date added, oldest first" :
                        title = "Por fecha de agregación, las más antiguas primero"

                    if title == "by date added, newest first" :
                        title = "Por fecha de agregación, las más nuevas primero"

                    data = file.readline()
                    data = data.strip()
                    i = i + 1
                    print i
                elif data.startswith("thumb") == True:
                    data = data.replace("thumb=", "")
                    data = data.strip()
                    thumbnail = data
                    if thumbnail == "":
                        thumbnail = logo
                    data = file.readline()
                    data = data.strip()
                    i = i + 1
                    print i
                    continue
                elif data.startswith("date") == True:
                    data = file.readline()
                    i = i + 1
                    print i
                    continue
                elif data.startswith("background") == True:
                    data = data.replace("background=", "")
                    fanart = data.strip()
                    if fanart == "":
                        fanart = background
                    data = file.readline()
                    data = data.strip()
                    i = i + 1
                    print i
                    continue

                elif data.startswith("URL") == True:
                    # Control para el caso de que no se haya definido fanart en cada entrada de la lista => Se usa el fanart general
                    if fanart == "":
                        fanart = background
                    data = data.replace("URL=", "")
                    data = data.strip()
                    url = data
                    parse_url(url)
                    if url.startswith("yt_channel") == True:
                        youtube_channel = url.replace("yt_channel(", "")
                        youtube_channel = youtube_channel.replace(")", "")
                        url = 'http://gdata.youtube.com/feeds/api/users/' + youtube_channel + '/playlists?v=2&start-index=1&max-results=30'
                        plugintools.add_item(action="youtube_playlists" , title = title + ' [[COLOR red]You[COLOR white]tube Channel][/COLOR]', extra = show, url = url , thumbnail = thumbnail , fanart = fanart , folder = True , isPlayable = False)
                        break

                    elif url.startswith("yt_playlist") == True:
                        youtube_playlist = url.replace("yt_playlist(", "")
                        youtube_playlist = youtube_playlist.replace(")", "")
                        plugintools.log("youtube_playlist= "+youtube_playlist)
                        url = 'https://www.youtube.com/playlist?list='+youtube_playlist
                        plugintools.add_item( action = "yt_playlist" , title = title + ' [COLOR red][You[COLOR white]tube Playlist][/COLOR] [I][COLOR lightblue][/I][/COLOR]', extra = show, url = url , thumbnail = thumbnail , fanart = fanart , folder = True , isPlayable = False )
                        data = file.readline()
                        i = i + 1
                        break

                    elif url.startswith("serie") == True:
                        url = url.replace("serie:", "")
                        plugintools.log("URL= "+url)
                        plugintools.log("FANART = "+fanart)
                        plugintools.add_item(action="seriecatcher" , title = title + ' [COLOR purple][Serie online][/COLOR]' , show = show, url = url , thumbnail = thumbnail , fanart = fanart , extra = fanart , folder = True , isPlayable = False)
                        break

                    elif url.startswith("goear") == True:
                        plugintools.add_item(action="goear" , title = title + '' , show = show, url = url , thumbnail = thumbnail , fanart = fanart , extra = fanart , folder = True , isPlayable = False)
                        break

                    elif url.startswith("http") == True:
                        if url.find("allmyvideos") >= 0:
                            plugintools.add_item(action="allmyvideos" , title = title + ' [COLOR lightyellow][Allmyvideos][/COLOR]' , extra = show, url = url , info_labels = datamovie , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True)
                            plugintools.log("URL= "+url)
                            break

                        elif url.find("streamcloud") >= 0:
                            plugintools.add_item(action="streamcloud" , title = title + ' [COLOR lightskyblue][Streamcloud][/COLOR]' , extra = show, url = url , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True)
                            plugintools.log("URL= "+url)
                            plugintools.log("FANART = "+fanart)
                            break

                        elif url.find("played.to") >= 0:
                            plugintools.add_item(action="playedto" , title = title + ' [COLOR lavender][Played.to][/COLOR]' , url = url , extra = show, thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True)
                            plugintools.log("URL= "+url)
                            plugintools.log("FANART = "+fanart)
                            break

                        elif url.find("vidspot") >= 0:
                            plugintools.add_item(action="vidspot" , title = title + ' [COLOR palegreen][Vidspot][/COLOR]' , url = url , extra = show, thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True)
                            plugintools.log("URL= "+url)
                            plugintools.log("FANART = "+fanart)
                            break

                        elif url.find("vk.com") >= 0:
                            plugintools.add_item(action="vk" , title = title + ' [COLOR royalblue][Vk][/COLOR]' , url = url , extra = show, thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True)
                            plugintools.log("URL= "+url)
                            plugintools.log("FANART = "+fanart)
                            break

                        elif url.find("nowvideo") >= 0:
                            plugintools.add_item(action="nowvideo" , title = title + ' [COLOR red][Nowvideo][/COLOR]' , url = url , extra = show, thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True)
                            plugintools.log("URL= "+url)
                            break

                        elif url.find("tumi.tv") >= 0:
                            plugintools.add_item(action="tumi" , title = title + ' [COLOR forestgreen][Tumi][/COLOR]' , url = url , extra = show, thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True)
                            plugintools.log("URL= "+url)
                            break

                        elif url.find("veehd.com") >= 0:
                            plugintools.add_item(action="veehd" , title = title + ' [COLOR orange][VeeHD][/COLOR]' , url = url , extra = show, thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True)
                            plugintools.log("URL= "+url)
                            break

                        elif url.find("streamin.to") >= 0:
                            plugintools.add_item(action="streaminto" , title = title + ' [COLOR orange][streamin.to][/COLOR]' , url = url , thumbnail = thumbnail , extra = show, fanart = fanart , folder = False , isPlayable = True)
                            plugintools.log("URL= "+url)
                            break

                        elif url.find("powvideo") >= 0:
                            plugintools.add_item(action="powvideo" , title = title + ' [COLOR orange][powvideo][/COLOR]' , url = url , thumbnail = thumbnail , extra = show, fanart = fanart , folder = False , isPlayable = True)
                            plugintools.log("URL= "+url)
                            break

                        elif url.find("mail.ru") >= 0:
                            plugintools.add_item(action="mailru" , title = title + ' [COLOR orange][Mail.ru][/COLOR]' , url = url , thumbnail = thumbnail , extra = show, fanart = fanart , folder = False , isPlayable = True)
                            plugintools.log("URL= "+url)
                            break

                        elif url.find("novamov") >= 0:
                            plugintools.add_item(action="novamov" , title = title + ' [COLOR orange][Novamov][/COLOR]' , url = url , thumbnail = thumbnail , extra = show, fanart = fanart , folder = False , isPlayable = True)
                            plugintools.log("URL= "+url)
                            break

                        elif url.find("gamovideo") >= 0:
                            plugintools.add_item(action="gamovideo" , title = title + ' [COLOR orange][Gamovideo][/COLOR]' , url = url , thumbnail = thumbnail , extra = show, fanart = fanart , folder = False , isPlayable = True)
                            plugintools.log("URL= "+url)
                            break

                        elif url.find("moevideos") >= 0:
                            plugintools.add_item(action="moevideos" , title = title + ' [COLOR orange][Moevideos][/COLOR]' , url = url , thumbnail = thumbnail , extra = show, fanart = fanart , folder = False , isPlayable = True)
                            plugintools.log("URL= "+url)
                            break

                        elif url.find("movshare") >= 0:
                            plugintools.add_item(action="movshare" , title = title + ' [COLOR orange][Movshare][/COLOR]' , url = url , thumbnail = thumbnail , extra = show, fanart = fanart , folder = False , isPlayable = True)
                            plugintools.log("URL= "+url)
                            break

                        elif url.find("movreel") >= 0:
                            plugintools.add_item(action="movreel" , title = title + ' [COLOR orange][Movreel][/COLOR]' , url = url , thumbnail = thumbnail , extra = show, fanart = fanart , folder = False , isPlayable = True)
                            plugintools.log("URL= "+url)
                            break

                        elif url.find("videobam") >= 0:
                            plugintools.add_item(action="videobam" , title = title + ' [COLOR orange][Videobam][/COLOR]' , url = url , thumbnail = thumbnail , extra = show, fanart = fanart , folder = False , isPlayable = True)
                            plugintools.log("URL= "+url)
                            break                          

                        elif url.endswith("flv") == True:
                            plugintools.log("URL= "+url)
                            plugintools.log("FANART = "+fanart)
                            plugintools.add_item( action = "play" , title = title + ' [COLOR cyan][Flash][/COLOR]' , url = url ,  thumbnail = thumbnail , extra = show, fanart = fanart , folder = False , isPlayable = True )
                            break

                        elif url.endswith("m3u8") == True:
                            plugintools.log("URL= "+url)
                            plugintools.log("FANART = "+fanart)
                            plugintools.add_item( action = "play" , title = title + ' [COLOR purple][/COLOR]' , url = url , info_labels = datamovie , thumbnail = thumbnail , extra = show, fanart = fanart , folder = False , isPlayable = True )
                            break

                        elif url.startswith("cbr:") == True:
                            if url.find("copy.com") >= 0:
                                plugintools.log("CBR Copy.com")
                                #url = url.replace("cbr:", "").strip()
                            else:
                                url = url.replace("cbr:", "").strip()
                            plugintools.add_item( action = "cbx_reader" , title = '[COLOR white]' + title + ' [COLOR gold][CBR][/COLOR]', plot = plot , url = url , thumbnail = thumbnail , show = show, fanart = fanart , folder = True , isPlayable = False )                    
                            break

                        elif url.startswith("cbz:") == True:
                            if url.find("copy.com") >= 0:
                                plugintools.log("CBZ Copy.com")
                                #url = url.replace("cbr:", "").strip()
                            else:
                                url = url.replace("cbr:", "").strip()
                            plugintools.add_item( action = "cbx_reader" , title = '[COLOR white]' + title + ' [COLOR gold][CBZ][/COLOR]', plot = plot , url = url , thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                            break

                        elif url.find("mediafire") >= 0:                                
                            plugintools.add_item( action = "cbx_reader" , title = '[COLOR white]' + title + ' [COLOR gold][Mediafire][/COLOR]', plot = plot , url = url , thumbnail = thumbnail , show = show, fanart = fanart , folder = True , isPlayable = True )
                            break                     
                            
                        elif url.find("youtube.com") >= 0:
                            plugintools.log("URL= "+url)
                            plugintools.log("FANART = "+fanart)
                            videoid = url.replace("https://www.youtube.com/watch?v=", "")
                            url = 'plugin://plugin.video.youtube/?path=/root/video&action=play_video&videoid=' + videoid
                            plugintools.add_item( action = "play" , title = title + ' [[COLOR red]You[COLOR white]tube Video][/COLOR]', url = url , extra = show, thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                            break

                        elif url.endswith("torrent") == True:
                            # plugin://plugin.video.p2p-streams/?url=http://something.torrent&mode=1&name=acestream+title   
                            title_fixed = title.replace(" ", "+").strip()
                            url = 'plugin://plugin.video.p2p-streams/?url='+url+'&mode=1&name='+title_fixed                            
                            plugintools.add_item( action = "play" , title = '[COLOR white]' + title + '[COLOR gold] [Torrent][/COLOR]', url = url , plot = plot, info_labels = datamovie , thumbnail = thumbnail , fanart = fanart , folder = True , isPlayable = False )
                            break
                        
                        else:
                            plugintools.log("URL= "+url)
                            plugintools.add_item( action = "play" , title = title + '' , url = url ,  extra = show , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                            plugintools.log("show "+show)
                            break

                    elif url.startswith("rtmp") == True:
                        params["url"] = url
                        server_rtmp(params)
                        server = params.get("server")
                        url = params.get("url")
                        plugintools.add_item( action = "launch_rtmp" , title = title + '' + server + '' , extra = show, url = params.get("url") ,  thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                        break

                    elif url.startswith("rtsp") == True:
                        params["url"] = url
                        server_rtmp(params)
                        server = params.get("server")
                        url = params.get("url")
                        plugintools.add_item( action = "launch_rtmp" , title = title + '' + server + '' , extra = show, url = params.get("url") ,  thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                        break

                    elif url.startswith("plugin") == True:
                        if url.find("plugin.video.f4mTester") >= 0:
                            if cat != "":
                                if busqueda == 'search.txt':
                                    plugintools.add_item( action = "play" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR orange] [F4M][/COLOR][I][COLOR lightblue] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = art + "icon.png" , fanart = art + 'fanart.jpg' , show = show, folder = False , isPlayable = True )
                                    data = file.readline()
                                    i = i + 1
                                    continue
                                else:                                    
                                    plugintools.add_item( action = "play" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR orange] [F4M][/COLOR]', plot = plot , url = url , thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                    data = file.readline()
                                    i = i + 1
                                    continue
                            else:
                                if busqueda == 'search.txt':
                                    plugintools.add_item( action = "play" , title = '[COLOR white]' + title + '[COLOR orange] [F4M][/COLOR][I][COLOR lightblue] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = art + "icon.png" , fanart = art + 'fanart.jpg' , show = show, folder = False , isPlayable = True )
                                    data = file.readline()
                                    i = i + 1
                                    continue
                                else:                                    
                                    plugintools.add_item( action = "play" , title = '[COLOR white]' + title + '[COLOR orange] [F4M][/COLOR]', plot = plot , url = url , thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                    data = file.readline()
                                    i = i + 1
                                    continue
                        
                        elif url.find("plugin.video.youtube") >= 0:
                            plugintools.log("URL= "+url)
                            plugintools.add_item( action = "play" , title = title + ' [COLOR white] [[COLOR red]You[COLOR white]tube Video][/COLOR][/COLOR]' , extra = show, url = url ,  thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                            i = i + 1
                            continue
                        
                        elif url.find("plugin.video.p2p-streams") >= 0:
                            if url.find("mode=1") >= 0:
                                title = parser_title(title)
                                url = url.strip()
                                plugintools.add_item(action="play" , title = title + ' [COLOR lightblue][Acestream][/COLOR]' , extra = show, url = url, thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True)
                                i = i + 1
                                continue
                            elif url.find("mode=2") >= 0:
                                title = parser_title(title)
                                url = url.strip()
                                plugintools.add_item(action="play" , title = title_fixed + ' [COLOR lightblue][Sopcast][/COLOR]' , extra = show, url = url, thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True)
                                i = i + 1
                                continue

                    elif url.startswith("sop") == True:
                        # plugin://plugin.video.p2p-streams/?url=sop://124.232.150.188:3912/11265&mode=2&name=Titulo+canal+Sopcast
                        title = parser_title(title)
                        url = 'plugin://plugin.video.p2p-streams/?url=' + url + '&mode=2&name='
                        url = url.strip()
                        plugintools.add_item(action="play" , title = title + ' [COLOR lightgreen][Sopcast][/COLOR]' , extra = show, url = url, thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True)
                        data = file.readline()
                        data = data.strip()
                        i = i + 1                        
                        continue

                    elif url.startswith("ace") == True:
                        title = parser_title(title)
                        url = url.replace("ace:", "")
                        url = 'plugin://plugin.video.p2p-streams/?url=' + url + '&mode=1&name='
                        url = url.strip()
                        plugintools.add_item(action="play" , title = title + ' [COLOR lightblue][Acestream][/COLOR]' , extra = show, url = url, thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True)
                        data = file.readline()
                        data = data.strip()
                        i = i + 1
                        continue

                    elif url.startswith("magnet") >= 0:
                        url = urllib.quote_plus(data)
                        title = parser_title(title)
                        url = launch_torrent(url)
                        plugintools.add_item(action="play" , title = title + ' [COLOR orangered][Torrent][/COLOR]' , extra = show, url = url, thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True)
                        break
                    
                    else:
                        plugintools.add_item(action="play" , title = title , extra = show, url = url , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True)
                        plugintools.log("URL = "+url)
                        break

                elif data == "" :
                    break
                else:
                    data = file.readline()
                    data = data.strip()
                    i = i + 1
                    print i

        if (data == 'type=playlist') == True:
            # Control si no se definió fanart en cada entrada de la lista => Se usa fanart global de la lista
            if fanart == "":
                fanart = background
            data = file.readline()
            i = i + 1
            print i
            while data <> "" :
                if data.startswith("name") == True :
                    data = data.replace("name=", "")
                    title = data.strip()
                    if title == '>>>' :
                        title = title.replace(">>>", "[I][COLOR lightyellow]Siguiente[/I][/COLOR]")
                        data = file.readline()
                        data = data.strip()
                        i = i + 1

                    elif title == '<<<' :
                        title = title.replace("<<<", "[I][COLOR lightyellow]Anterior[/I][/COLOR]")
                        data = file.readline()
                        data = data.strip()
                        i = i + 1

                    elif title.find("Sorted by user-assigned order") >= 0:
                        title = "[I][COLOR lightyellow]Ordenar listas por...[/I][/COLOR]"
                        data = file.readline()
                        data = data.strip()
                        i = i + 1

                    elif title.find("Sorted A-Z") >= 0:
                        title = "[I][COLOR lightyellow][COLOR lightyellow]De la A a la Z[/I][/COLOR]"
                        data = file.readline()
                        data = data.strip()
                        i = i + 1

                    elif title.find("Sorted Z-A") >= 0:
                        title = "[I][COLOR lightyellow]De la Z a la A[/I][/COLOR]"
                        data = file.readline()
                        data = data.strip()
                        i = i + 1

                    elif title.find("Sorted by date added, newest first") >= 0:
                        title = "Ordenado por: Las + recientes primero..."
                        data = file.readline()
                        data = data.strip()
                        i = i + 1

                    elif title.find("Sorted by date added, oldest first") >= 0:
                        title = "Ordenado por: Las + antiguas primero..."
                        data = file.readline()
                        data = data.strip()
                        i = i + 1

                    elif title.find("by user-assigned order") >= 0:
                        title = "[COLOR lightyellow]Ordenar listas por...[/COLOR]"
                        data = file.readline()
                        data = data.strip()
                        i = i + 1

                    elif title.find("by date added, newest first") >= 0 :
                        title = "Las + recientes primero..."
                        data = file.readline()
                        data = data.strip()
                        i = i + 1
                    elif title.find("by date added, oldest first") >= 0 :
                        title = "Las + antiguas primero..."
                        data = file.readline()
                        data = data.strip()
                        i = i + 1

                elif data.startswith("thumb") == True:
                    data = data.replace("thumb=", "")
                    data = data.strip()
                    thumbnail = data
                    data = file.readline()
                    data = data.strip()
                    i = i + 1
                    print i
                    continue

                elif data.startswith("URL") == True:
                    data = data.replace("URL=", "")
                    data = data.strip()
                    url = data
                    parse_url(url)
                    if url.startswith("m3u") == True:
                        url = url.replace("m3u:", "")
                        plugintools.add_item(action="getfile_http" , title = title , extra = show, url = url , thumbnail = thumbnail , fanart = fanart , folder = True , isPlayable = False)
                    elif url.startswith("plx") == True:
                        url = url.replace("plx:", "")
                        plugintools.add_item(action="plx_items" , title = title , extra = show, url = url , thumbnail = thumbnail , fanart = fanart , folder = True , isPlayable = False)

                elif data == "" :
                    break

                else:
                    data = file.readline()
                    data = data.strip()
                    i = i + 1
                    print i
                    continue


    file.close()


    # Purga de listas erróneas creadas al abrir listas PLX (por los playlists de ordenación que crea Navixtreme)

    if os.path.isfile(playlists + 'Siguiente.plx'):
        os.remove(playlists + 'Siguiente.plx')
        print "Correcto!"
    else:
        pass

    if os.path.isfile(playlists + 'Ordenar listas por....plx'):
        os.remove(playlists + 'Ordenar listas por....plx')
        print "Ordenar listas por....plx eliminado!"
        print "Correcto!"
    else:
        print "No es posible!"
        pass

    if os.path.isfile(playlists + 'A-Z.plx'):
        os.remove(playlists + 'A-Z.plx')
        print "A-Z.plx eliminado!"
    else:
        print "No es posible!"
        pass

    if os.path.isfile(playlists + 'De la A a la Z.plx'):
        os.remove(playlists + 'De la A a la Z.plx')
        print "De la A a la Z.plx eliminado!"
    else:
        print "No es posible!"
        pass

    if os.path.isfile(playlists + 'Z-A.plx'):
        os.remove(playlists + 'Z-A.plx')
        print "Z-A.plx eliminado!"
    else:
        print "No es posible!"
        pass

    if os.path.isfile(playlists + 'De la Z a la A.plx'):
        os.remove(playlists + 'De la Z a la A.plx')
        print "De la Z a la A.plx eliminado!"
    else:
        print "No es posible!"
        pass

    if os.path.isfile(playlists + 'Las + antiguas primero....plx'):
        os.remove(playlists + 'Las + antiguas primero....plx')
        print "Las más antiguas primero....plx eliminado!"
    else:
        print "No es posible!"
        pass

    if os.path.isfile(playlists + 'by date added, oldest first.plx'):
        os.remove(playlists + 'by date added, oldest first.plx')
        print "by date added, oldest first.plx eliminado!"
    else:
        print "No es posible!"
        pass

    if os.path.isfile(playlists + 'Las + recientes primero....plx'):
        os.remove(playlists + 'Las + recientes primero....plx')
    else:
        print "No es posible!"
        pass

    if os.path.isfile(playlists + 'by date added, newest first.plx'):
        os.remove(playlists + 'by date added, newest first.plx')
        print "by date added, newest first.plx eliminado!"
    else:
        print "No es posible!"
        pass

    if os.path.isfile(playlists + 'Sorted by user-assigned order.plx'):
        os.remove(playlists + 'Sorted by user-assigned order.plx')
        print "Sorted by user-assigned order.plx eliminado!"
    else:
        print "No es posible!"
        pass

    if os.path.isfile(playlists + 'Ordenado por.plx'):
        os.remove(playlists + 'Ordenado por.plx')
        print "Correcto!"
    else:
        print "No es posible!"
        pass

    if os.path.isfile(playlists + 'Ordenado por'):
        os.remove(playlists + 'Ordenado por')
        print "Correcto!"
    else:
        print "No es posible!"
        pass





def encode_string(txt):
    plugintools.log('[%s %s].encode_string %s' % (addonName, addonVersion, txt))

    txt = txt.replace("&#231;", "ç")
    txt = txt.replace('&#233;', 'é')
    txt = txt.replace('&#225;', 'á')
    txt = txt.replace('&#233;', 'é')
    txt = txt.replace('&#225;', 'á')
    txt = txt.replace('&#241;', 'ñ')
    txt = txt.replace('&#250;', 'ú')
    txt = txt.replace('&#237;', 'í')
    txt = txt.replace('&#243;', 'ó')
    txt = txt.replace('&#39;', "'")
    txt = txt.replace("&nbsp;", "")
    txt = txt.replace("&nbsp;", "")
    txt = txt.replace('&#39;', "'")
    return txt



def splive_items(params):
    plugintools.log('[%s %s].splive_items %s' % (addonName, addonVersion, repr(params)))
    data = plugintools.read( params.get("url") )

    channel = plugintools.find_multiple_matches(data,'<channel>(.*?)</channel>')

    for entry in channel:
        # plugintools.log("channel= "+channel)
        title = plugintools.find_single_match(entry,'<name>(.*?)</name>')
        category = plugintools.find_single_match(entry,'<category>(.*?)</category>')
        thumbnail = plugintools.find_single_match(entry,'<link_logo>(.*?)</link_logo>')
        rtmp = plugintools.find_single_match(entry,'<rtmp>([^<]+)</rtmp>')
        isIliveTo = plugintools.find_single_match(entry,'<isIliveTo>([^<]+)</isIliveTo>')
        rtmp = rtmp.strip()
        pageurl = plugintools.find_single_match(entry,'<url_html>([^<]+)</url_html>')
        link_logo = plugintools.find_single_match(entry,'<link_logo>([^<]+)</link_logo>')

        if pageurl == "SinProgramacion":
            pageurl = ""

        playpath = plugintools.find_single_match(entry, '<playpath>([^<]+)</playpath>')
        playpath = playpath.replace("Referer: ", "")
        token = plugintools.find_single_match(entry, '<token>([^<]+)</token>')

        iliveto = 'rtmp://188.122.91.73/edge'

        if isIliveTo == "0":
            if token == "0":
                url = rtmp
                url = url.replace("&amp;", "&")
                parse_url(url)
                plugintools.add_item( action = "play" , title = title , url = url , thumbnail = thumbnail , fanart = fanart , plot = title , folder = False , isPlayable = True )
                plugintools.log("url= "+url)
            else:
                url = rtmp + " pageUrl=" + pageurl + " " + 'token=' + token + playpath + " live=1"
                parse_url(url)
                plugintools.add_item( action = "play" , title = title , url = url , thumbnail = thumbnail , fanart = fanart , plot = title , folder = False , isPlayable = True )
                plugintools.log("url= "+url)

        if isIliveTo == "1":
            if token == "1":
                url = iliveto + " pageUrl=" + pageurl + " " + 'token=' + token + playpath + " live=1"
                url = url.replace("&amp;", "&")
                parse_url(url)
                plugintools.add_item( action = "play" , title = title , url = url , thumbnail = thumbnail , fanart = fanart , plot = title , folder = False , isPlayable = True )
                plugintools.log("url= "+url)

            else:
                url = iliveto + ' swfUrl=' + rtmp +  " playpath=" + playpath + " pageUrl=" + pageurl
                url = url.replace("&amp;", "&")
                parse_url(url)
                plugintools.add_item( action = "play" , title = title , url = url , thumbnail = thumbnail , fanart = fanart , plot = title , folder = False , isPlayable = True )
                plugintools.log("url= "+url)



def get_fecha():

    from datetime import datetime

    ahora = datetime.now()
    anno_actual = ahora.year
    mes_actual = ahora.month
    dia_actual = ahora.day
    fecha = str(dia_actual) + "/" + str(mes_actual) + "/" + str(anno_actual)
    plugintools.log("fecha de hoy= "+fecha)
    return fecha




def p2p_items(params):
    plugintools.log('[%s %s].p2p_items %s' % (addonName, addonVersion, repr(params)))

    # Vamos a localizar el título
    title = params.get("plot")
    if title == "":
        title = params.get("title")

    data = plugintools.read("http://pastebin.com/raw.php?i=ydUjKXnN")
    subcanal = plugintools.find_single_match(data,'<name>' + title + '(.*?)</subchannel>')
    thumbnail = plugintools.find_single_match(subcanal, '<thumbnail>(.*?)</thumbnail>')
    fanart = plugintools.find_single_match(subcanal, '<fanart>(.*?)</fanart>')
    plugintools.log("thumbnail= "+thumbnail)


    # Controlamos el caso en que no haya thumbnail en el menú de TvWin
    if thumbnail == "":
        thumbnail = art + 'p2p.png'
    elif thumbnail == 'name_rtmp.png':
        thumbnail = art + 'p2p.png'

    if fanart == "":
        fanart = art + 'p2p.png'

    # Comprobamos si la lista ha sido descargada o no
    plot = params.get("plot")

    if plot == "":
        title = params.get("title")
        title = parser_title(title)
        filename = title + '.p2p'
        getfile_url(params)
    else:
        print "Lista ya descargada (plot no vacío)"
        filename = params.get("plot")
        params["ext"] = 'p2p'
        params["plot"]=filename
        filename = filename + '.p2p'
        plugintools.log("Lectura del archivo P2P")

    plugintools.add_item(action="" , title='[COLOR lightyellow][I][B]' + title + '[/B][/I][/COLOR]' , thumbnail=thumbnail , fanart=fanart , folder=False, isPlayable=False)

    # Abrimos el archivo P2P y calculamos número de líneas
    file = open(playlists + filename, "r")
    file.seek(0)
    data = file.readline()
    num_items = len(file.readlines())
    print num_items
    file.seek(0)
    data = file.readline()
    if data.startswith("default") == True:
        data = data.replace("default=", "")
        data = data.split(",")
        thumbnail = data[0]
        fanart = data[1]
        plugintools.log("fanart= "+fanart)

    # Leemos entradas
    i = 0
    file.seek(0)
    data = file.readline()
    data = data.strip()
    while i <= num_items:
        if data == "":
            data = file.readline()
            data = data.strip()
            # plugintools.log("linea vacia= "+data)
            i = i + 1
            #print i
            continue

        elif data.startswith("default") == True:
            data = file.readline()
            data = data.strip()
            i = i + 1
            #print i
            continue

        elif data.startswith("#") == True:
            title = data.replace("#", "")
            plugintools.log("title comentario= "+title)
            plugintools.add_item(action="play" , title = title , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True)
            data = file.readline()
            data = data.strip()
            i = i + 1
            continue

        else:
            title = data
            title = title.strip()
            plugintools.log("title= "+title)
            data = file.readline()
            data = data.strip()
            i = i + 1
            #print i
            plugintools.log("linea URL= "+data)
            if data.startswith("sop") == True:
                print "empieza el sopcast..."
                # plugin://plugin.video.p2p-streams/?url=sop://124.232.150.188:3912/11265&mode=2&name=Titulo+canal+Sopcast
                title_fixed = parser_title(title)
                title = title.replace(" " , "+")
                url = 'plugin://plugin.video.p2p-streams/?url=' + data + '&mode=2&name=' + title_fixed
                url = url.strip()
                plugintools.add_item(action="play" , title = title_fixed + ' [COLOR lightgreen][Sopcast][/COLOR]' , url = url, thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True)
                data = file.readline()
                data = data.strip()
                i = i + 1
                #print i
                continue

            elif data.startswith("magnet") == True:
                url = urllib.quote_plus(data)
                title_fixed = parser_title(title)
                url = launch_torrent(url)
                plugintools.add_item(action="play" , title = title_fixed + ' [COLOR orangered][Torrent][/COLOR]' , url = url, thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True)
                data = file.readline()
                data = data.strip()
                i = i + 1
                continue

            else:
                print "empieza el acestream..."
                # plugin://plugin.video.p2p-streams/?url=a55f96dd386b7722380802b6afffc97ff98903ac&mode=1&name=Sky+Sports+title
                title = parser_title(title)
                print title
                url = 'plugin://plugin.video.p2p-streams/?url=' + data + '&mode=1&name='
                plugintools.add_item(action="play" , title = title + ' [COLOR lightblue][Acestream][/COLOR]' , url = url, thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True)
                data = file.readline()
                data = data.strip()
                i = i + 1
                #print i




def contextMenu(params):
    plugintools.log('[%s %s].contextMenu %s' % (addonName, addonVersion, repr(params)))

    dialog = xbmcgui.Dialog()
    plot = params.get("plot")
    canales = plot.split("/")
    len_canales = len(canales)
    print len_canales
    plugintools.log("canales= "+repr(canales))

    if len_canales == 1:
        tv_a = canales[0]
        tv_a = parse_channel(tv_a)
        search_channel(params)
        selector = ""
    else:
        if len_canales == 2:
            print "len_2"
            tv_a = canales[0]
            tv_a = parse_channel(tv_a)
            tv_b = canales[1]
            tv_b = parse_channel(tv_b)
            selector = dialog.select('TvWin', [tv_a, tv_b])

        elif len_canales == 3:
            tv_a = canales[0]
            tv_a = parse_channel(tv_a)
            tv_b = canales[1]
            tv_b = parse_channel(tv_b)
            tv_c = canales[2]
            tv_c = parse_channel(tv_c)
            selector = dialog.select('TvWin', [tv_a, tv_b, tv_c])

        elif len_canales == 4:
            tv_a = canales[0]
            tv_a = parse_channel(tv_a)
            tv_b = canales[1]
            tv_b = parse_channel(tv_b)
            tv_c = canales[2]
            tv_c = parse_channel(tv_c)
            tv_d = canales[3]
            tv_d = parse_channel(tv_d)
            selector = dialog.select('TvWin', [tv_a, tv_b, tv_c, tv_d])

        elif len_canales == 5:
            tv_a = canales[0]
            tv_a = parse_channel(tv_a)
            tv_b = canales[1]
            tv_b = parse_channel(tv_b)
            tv_c = canales[2]
            tv_c = parse_channel(tv_c)
            tv_d = canales[3]
            tv_d = parse_channel(tv_d)
            tv_e = canales[4]
            tv_e = parse_channel(tv_e)
            selector = dialog.select('TvWin', [tv_a, tv_b, tv_c, tv_d, tv_e])

        elif len_canales == 6:
            tv_a = canales[0]
            tv_a = parse_channel(tv_a)
            tv_b = canales[1]
            tv_b = parse_channel(tv_b)
            tv_c = canales[2]
            tv_c = parse_channel(tv_c)
            tv_d = canales[3]
            tv_d = parse_channel(tv_d)
            tv_e = canales[4]
            tv_e = parse_channel(tv_e)
            tv_f = canales[5]
            tv_f = parse_channel(tv_f)
            selector = dialog.select('TvWin', [tv_a , tv_b, tv_c, tv_d, tv_e, tv_f])

        elif len_canales == 7:
            tv_a = canales[0]
            tv_a = parse_channel(tv_a)
            tv_b = canales[1]
            tv_b = parse_channel(tv_b)
            tv_c = canales[2]
            tv_c = parse_channel(tv_c)
            tv_d = canales[3]
            tv_d = parse_channel(tv_d)
            tv_e = canales[4]
            tv_e = parse_channel(tv_e)
            tv_f = canales[5]
            tv_f = parse_channel(tv_f)
            tv_g = canales[6]
            tv_g = parse_channel(tv_g)
            selector = dialog.select('TvWin', [tv_a , tv_b, tv_c, tv_d, tv_e, tv_f, tv_g])

    if selector == 0:
        print selector
        if tv_a.startswith("Gol") == True:
            tv_a = "Gol"
        params["plot"] = tv_a
        plugintools.log("tv= "+tv_a)
        search_channel(params)
    elif selector == 1:
        print selector
        if tv_b.startswith("Gol") == True:
            tv_b = "Gol"
        params["plot"] = tv_b
        plugintools.log("tv= "+tv_b)
        search_channel(params)
    elif selector == 2:
        print selector
        if tv_c.startswith("Gol") == True:
            tv_c = "Gol"
        params["plot"] = tv_c
        plugintools.log("tv= "+tv_c)
        search_channel(params)
    elif selector == 3:
        print selector
        if tv_d.startswith("Gol") == True:
            tv_d = "Gol"
        params["plot"] = tv_d
        plugintools.log("tv= "+tv_d)
        search_channel(params)
    elif selector == 4:
        print selector
        if tv_e.startswith("Gol") == True:
            tv_e = "Gol"
        params["plot"] = tv_e
        plugintools.log("tv= "+tv_e)
        search_channel(params)
    elif selector == 5:
        print selector
        if tv_f.startswith("Gol") == True:
            tv_f = "Gol"
        params["plot"] = tv_f
        plugintools.log("tv= "+tv_f)
        search_channel(params)
    elif selector == 6:
        print selector
        if tv_g.startswith("Gol") == True:
            tv_g = "Gol"
        params["plot"] = tv_g
        plugintools.log("tv= "+tv_g)
        search_channel(params)
    else:
        pass






def parse_channel(txt):
    plugintools.log('[%s %s].parse_channelñana %s' % (addonName, addonVersion, txt))

    txt = txt.rstrip()
    txt = txt.lstrip()
    return txt







def parser_title(title):
    plugintools.log('[%s %s].parser_title %s' % (addonName, addonVersion, title))

    cyd = title

    cyd = cyd.replace("[COLOR lightyellow]", "")
    cyd = cyd.replace("[COLOR green]", "")
    cyd = cyd.replace("[COLOR red]", "")
    cyd = cyd.replace("[COLOR blue]", "")
    cyd = cyd.replace("[COLOR royalblue]", "")
    cyd = cyd.replace("[COLOR white]", "")
    cyd = cyd.replace("[COLOR pink]", "")
    cyd = cyd.replace("[COLOR cyan]", "")
    cyd = cyd.replace("[COLOR steelblue]", "")
    cyd = cyd.replace("[COLOR forestgreen]", "")
    cyd = cyd.replace("[COLOR olive]", "")
    cyd = cyd.replace("[COLOR khaki]", "")
    cyd = cyd.replace("[COLOR lightsalmon]", "")
    cyd = cyd.replace("[COLOR orange]", "")
    cyd = cyd.replace("[COLOR lightgreen]", "")
    cyd = cyd.replace("[COLOR lightblue]", "")
    cyd = cyd.replace("[COLOR lightpink]", "")
    cyd = cyd.replace("[COLOR skyblue]", "")
    cyd = cyd.replace("[COLOR darkorange]", "")
    cyd = cyd.replace("[COLOR greenyellow]", "")
    cyd = cyd.replace("[COLOR yellow]", "")
    cyd = cyd.replace("[COLOR yellowgreen]", "")
    cyd = cyd.replace("[COLOR orangered]", "")
    cyd = cyd.replace("[COLOR grey]", "")
    cyd = cyd.replace("[COLOR gold]", "")
    cyd = cyd.replace("[COLOR=FF00FF00]", "")

    cyd = cyd.replace("&quot;", '"')

    cyd = cyd.replace("[/COLOR]", "")
    cyd = cyd.replace("[B]", "")
    cyd = cyd.replace("[/B]", "")
    cyd = cyd.replace("[I]", "")
    cyd = cyd.replace("[/I]", "")
    cyd = cyd.replace("[Auto]", "")
    cyd = cyd.replace("[Parser]", "")
    cyd = cyd.replace("[TinyURL]", "")
    cyd = cyd.replace("[Auto]", "")

    # Control para evitar filenames con corchetes
    cyd = cyd.replace(" [Lista M3U]", "")
    cyd = cyd.replace(" [Lista PLX]", "")
    cyd = cyd.replace(" [Multilink]", "")
    cyd = cyd.replace(" [Multiparser]", "")
    cyd = cyd.replace(" [COLOR orange][Lista [B]PLX[/B]][/COLOR]", "")
    cyd = cyd.replace(" [COLOR orange][Lista [B]M3U[/B]][/COLOR]", "")
    cyd = cyd.replace(" [COLOR lightyellow][B][Dailymotion[/B] playlist][/COLOR]", "")
    cyd = cyd.replace(" [COLOR lightyellow][B][Dailymotion[/B] video][/COLOR]", "")
    cyd = cyd.replace(' [COLOR gold][CBZ][/COLOR]', "")
    cyd = cyd.replace(' [COLOR gold][CBR][/COLOR]', "")
    cyd = cyd.replace(' [COLOR gold][Mediafire][/COLOR]', "")
    cyd = cyd.replace(' [CBZ]', "")
    cyd = cyd.replace(' [CBR]', "")
    cyd = cyd.replace(' [Mediafire]', "")

    # Control para evitar errores al crear archivos
    cyd = cyd.replace("[", "")
    cyd = cyd.replace("]", "")
    #cyd = cyd.replace(".", "")
    
    title = cyd
    title = title.strip()
    if title.endswith(" .plx") == True:
        title = title.replace(" .plx", ".plx")

    plugintools.log("title_parsed= "+title)
    return title








def youtube_playlists(params):
    plugintools.log('[%s %s].youtube_playlists %s' % (addonName, addonVersion, repr(params)))

    data = plugintools.read( params.get("url") )

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
def youtube_videos(params):
    plugintools.log('[%s %s].youtube_videos %s' % (addonName, addonVersion, repr(params)))

    # Fetch video list from YouTube feed
    data = plugintools.read( params.get("url") )
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



def server_rtmp(params):
    plugintools.log('[%s %s].server_rtmp %s' % (addonName, addonVersion, repr(params)))

    url = params.get("url")
    plugintools.log("URL= "+url)

    if url.find("iguide.to") >= 0:
        params["server"] = 'iguide'
        if url.find("timeout") < 0:
            if url.endswith("conn=S:OK") == True:  # Control para aquellos servidores que requieran al final de la URL la expresión: conn=S:OK
                url = url.replace("conn=S:OK", "").strip()
                url = url + ' timeout=15 conn=S:OK'
                params["url"]=url
            else:
                url = url + ' timeout=15'
                params["url"]=url
        return params

    elif url.find("freetvcast.pw") >= 0:
        params["server"] = 'freetvcast'
        return params

    elif url.find("9stream") >= 0:
        params["server"] = '9stream'
        if url.find("timeout") < 0:
            if url.endswith("conn=S:OK") == True:  # Control para aquellos servidores que requieran al final de la URL la expresión: conn=S:OK
                url = url.replace("conn=S:OK", "").strip()
                url = url + ' timeout=15 conn=S:OK'
                params["url"]=url
            else:
                url = url + ' timeout=15'
                params["url"]=url
        return params

    elif url.find("freebroadcast") >= 0:
        params["server"] = 'freebroadcast'
        if url.find("timeout") < 0:
            url = url + ' timeout=15'
            params["url"]=url
        return params

    elif url.find("goodgame.ru") >= 0:
        params["server"] = 'goodgame.ru'
        if url.find("timeout") < 0:
            if url.endswith("conn=S:OK") == True:  # Control para aquellos servidores que requieran al final de la URL la expresión: conn=S:OK
                url = url.replace("conn=S:OK", "").strip()
                url = url + ' timeout=15 conn=S:OK'
                params["url"]=url
            else:
                url = url + ' timeout=15'
                params["url"]=url
        return params

    elif url.find("hdcast") >= 0:
        params["server"] = 'hdcast'
        if url.find("timeout") < 0:
            if url.endswith("conn=S:OK") == True:  # Control para aquellos servidores que requieran al final de la URL la expresión: conn=S:OK
                url = url.replace("conn=S:OK", "").strip()
                url = url + ' timeout=15 conn=S:OK'
                params["url"]=url
            else:
                url = url + ' timeout=15'
                params["url"]=url
        return params

    elif url.find("sharecast") >= 0:
        params["server"] = 'sharecast'
        if url.find("timeout") < 0:
            if url.endswith("conn=S:OK") == True:  # Control para aquellos servidores que requieran al final de la URL la expresión: conn=S:OK
                url = url.replace("conn=S:OK", "").strip()
                url = url + ' timeout=15 conn=S:OK'
                params["url"]=url
            else:
                url = url + ' timeout=15'
                params["url"]=url
        return params

    elif url.find("cast247") >= 0:
        params["server"] = 'cast247'
        if url.find("timeout") < 0:
            if url.endswith("conn=S:OK") == True:  # Control para aquellos servidores que requieran al final de la URL la expresión: conn=S:OK
                url = url.replace("conn=S:OK", "").strip()
                url = url + ' timeout=15 conn=S:OK'
                params["url"]=url
            else:
                url = url + ' timeout=15'
                params["url"]=url
        return params

    elif url.find("castalba") >= 0:
        params["server"] = 'castalba'
        if url.find("timeout") < 0:
            if url.endswith("conn=S:OK") == True:  # Control para aquellos servidores que requieran al final de la URL la expresión: conn=S:OK
                url = url.replace("conn=S:OK", "").strip()
                url = url + ' timeout=15 conn=S:OK'
                params["url"]=url
            else:
                url = url + ' timeout=15'
                params["url"]=url
        return params

    elif url.find("direct2watch") >= 0:
        params["server"] = 'direct2watch'
        if url.find("timeout") < 0:
            if url.endswith("conn=S:OK") == True:  # Control para aquellos servidores que requieran al final de la URL la expresión: conn=S:OK
                url = url.replace("conn=S:OK", "").strip()
                url = url + ' timeout=15 conn=S:OK'
                params["url"]=url
            else:
                url = url + ' timeout=15'
                params["url"]=url
        return params

    elif url.find("businessapp1") >= 0:
        params["server"] = 'businessapp'
        if url.find("timeout") < 0:
            if url.endswith("conn=S:OK") == True:  # Control para aquellos servidores que requieran al final de la URL la expresión: conn=S:OK
                url = url.replace("conn=S:OK", "").strip()
                url = url + ' timeout=15 conn=S:OK'
                params["url"]=url
            else:
                url = url + ' timeout=15'
                params["url"]=url
        return params    

    elif url.find("vaughnlive") >= 0:
        params["server"] = 'vaughnlive'
        if url.find("timeout") < 0:
            if url.endswith("conn=S:OK") == True:  # Control para aquellos servidores que requieran al final de la URL la expresión: conn=S:OK
                url = url.replace("conn=S:OK", "").strip()
                url = url + ' timeout=15 conn=S:OK'
                params["url"]=url
            else:
                url = url + ' timeout=15'
                params["url"]=url
        return params

    elif url.find("sawlive") >= 0:
        params["server"] = 'sawlive'
        if url.find("timeout") < 0:
            if url.endswith("conn=S:OK") == True:  # Control para aquellos servidores que requieran al final de la URL la expresión: conn=S:OK
                url = url.replace("conn=S:OK", "").strip()
                url = url + ' timeout=15 conn=S:OK'
                params["url"]=url
            else:
                url = url + ' timeout=15'
                params["url"]=url
        return params

    elif url.find("streamingfreetv") >= 0:
        params["server"] = 'streamingfreetv'
        if url.find("timeout") < 0:
            if url.endswith("conn=S:OK") == True:  # Control para aquellos servidores que requieran al final de la URL la expresión: conn=S:OK
                url = url.replace("conn=S:OK", "").strip()
                url = url + ' timeout=15 conn=S:OK'
                params["url"]=url
            else:
                url = url + ' timeout=15'
                params["url"]=url        
        return params

    elif url.find("totalplay") >= 0:
        params["server"] = 'totalplay'
        if url.find("timeout") < 0:
            if url.endswith("conn=S:OK") == True:  # Control para aquellos servidores que requieran al final de la URL la expresión: conn=S:OK
                url = url.replace("conn=S:OK", "").strip()
                url = url + ' timeout=15 conn=S:OK'
                params["url"]=url
            else:
                url = url + ' timeout=15'
                params["url"]=url
        return params

    elif url.find("shidurlive") >= 0:
        params["server"] = 'shidurlive'
        return params

    elif url.find("everyon") >= 0:
        params["server"] = 'everyon'
        if url.find("timeout") < 0:
            if url.endswith("conn=S:OK") == True:  # Control para aquellos servidores que requieran al final de la URL la expresión: conn=S:OK
                url = url.replace("conn=S:OK", "").strip()
                url = url + ' timeout=15 conn=S:OK'
                params["url"]=url
            else:
                url = url + ' timeout=15'
                params["url"]=url
        return params

    elif url.find("iviplanet") >= 0:
        params["server"] = 'iviplanet'
        if url.find("timeout") < 0:
            if url.endswith("conn=S:OK") == True:  # Control para aquellos servidores que requieran al final de la URL la expresión: conn=S:OK
                url = url.replace("conn=S:OK", "").strip()
                url = url + ' timeout=15 conn=S:OK'
                params["url"]=url
            else:
                url = url + ' timeout=15'
                params["url"]=url
        return params

    elif url.find("cxnlive") >= 0:
        params["server"] = 'cxnlive'
        if url.find("timeout") < 0:
            if url.endswith("conn=S:OK") == True:  # Control para aquellos servidores que requieran al final de la URL la expresión: conn=S:OK
                url = url.replace("conn=S:OK", "").strip()
                url = url + ' timeout=15 conn=S:OK'
                params["url"]=url
            else:
                url = url + ' timeout=15'
                params["url"]=url
        return params

    elif url.find("ucaster") >= 0:
        params["server"] = 'ucaster'
        if url.find("timeout") < 0:
            if url.endswith("conn=S:OK") == True:  # Control para aquellos servidores que requieran al final de la URL la expresión: conn=S:OK
                url = url.replace("conn=S:OK", "").strip()
                url = url + ' timeout=15 conn=S:OK'
                params["url"]=url
            else:
                url = url + ' timeout=15'
                params["url"]=url
        return params

    elif url.find("mediapro") >= 0:
        params["server"] = 'mediapro'
        if url.find("timeout") < 0:
            url = url + ' timeout=15'
            params["url"]=url
        return params

    elif url.find("veemi") >= 0:
        params["server"] = 'veemi'
        if url.find("timeout") < 0:
            if url.endswith("conn=S:OK") == True:  # Control para aquellos servidores que requieran al final de la URL la expresión: conn=S:OK
                url = url.replace("conn=S:OK", "").strip()
                url = url + ' timeout=15 conn=S:OK'
                params["url"]=url
            else:
                url = url + ' timeout=15'
                params["url"]=url
        return params

    elif url.find("yukons.net") >= 0:
        params["server"] = 'yukons.net'
        if url.find("timeout") < 0:
            if url.endswith("conn=S:OK") == True:  # Control para aquellos servidores que requieran al final de la URL la expresión: conn=S:OK
                url = url.replace("conn=S:OK", "").strip()
                url = url + ' timeout=15 conn=S:OK'
                params["url"]=url
            else:
                url = url + ' timeout=15'
                params["url"]=url
        return params

    elif url.find("janjua") >= 0:
        params["server"] = 'janjua'
        if url.find("timeout") < 0:
            if url.endswith("conn=S:OK") == True:  # Control para aquellos servidores que requieran al final de la URL la expresión: conn=S:OK
                url = url.replace("conn=S:OK", "").strip()
                url = url + ' timeout=15 conn=S:OK'
                params["url"]=url
            else:
                url = url + ' timeout=15'
                params["url"]=url
        return params

    elif url.find("mips") >= 0:
        params["server"] = 'mips'
        if url.find("timeout") < 0:
            if url.endswith("conn=S:OK") == True:  # Control para aquellos servidores que requieran al final de la URL la expresión: conn=S:OK
                url = url.replace("conn=S:OK", "").strip()
                url = url + ' timeout=15 conn=S:OK'
                params["url"]=url
            else:
                url = url + ' timeout=15'
                params["url"]=url
        return params

    elif url.find("zecast") >= 0:
        params["server"] = 'zecast'
        if url.find("timeout") < 0:
            if url.endswith("conn=S:OK") == True:  # Control para aquellos servidores que requieran al final de la URL la expresión: conn=S:OK
                url = url.replace("conn=S:OK", "").strip()
                url = url + ' timeout=15 conn=S:OK'
                params["url"]=url
            else:
                url = url + ' timeout=15'
                params["url"]=url
        return params

    elif url.find("vertvdirecto") >= 0:
        params["server"] = 'vertvdirecto'
        if url.find("timeout") < 0:
            if url.endswith("conn=S:OK") == True:  # Control para aquellos servidores que requieran al final de la URL la expresión: conn=S:OK
                url = url.replace("conn=S:OK", "").strip()
                url = url + ' timeout=15 conn=S:OK'
                params["url"]=url
            else:
                url = url + ' timeout=15'
                params["url"]=url
        return params

    elif url.find("filotv") >= 0:
        params["server"] = 'filotv'
        if url.find("timeout") < 0:
            if url.endswith("conn=S:OK") == True:  # Control para aquellos servidores que requieran al final de la URL la expresión: conn=S:OK
                url = url.replace("conn=S:OK", "").strip()
                url = url + ' timeout=15 conn=S:OK'
                params["url"]=url
            else:
                url = url + ' timeout=15'
                params["url"]=url
        return params

    elif url.find("dinozap") >= 0:
        params["server"] = 'dinozap'
        if url.find("timeout") < 0:
            if url.endswith("conn=S:OK") == True:  # Control para aquellos servidores que requieran al final de la URL la expresión: conn=S:OK
                url = url.replace("conn=S:OK", "").strip()
                url = url + ' timeout=15 conn=S:OK'
                params["url"]=url
            else:
                url = url + ' timeout=15'
                params["url"]=url
        return params

    elif url.find("ezcast") >= 0:
        params["server"] = 'ezcast'
        if url.find("timeout") < 0:
            if url.endswith("conn=S:OK") == True:  # Control para aquellos servidores que requieran al final de la URL la expresión: conn=S:OK
                url = url.replace("conn=S:OK", "").strip()
                url = url + ' timeout=15 conn=S:OK'
                params["url"]=url
            else:
                url = url + ' timeout=15'
                params["url"]=url
        return params

    elif url.find("flashstreaming") >= 0:
        params["server"] = 'flashstreaming'
        if url.find("timeout") < 0:
            url = url + ' timeout=15'
            params["url"]=url
        return params

    elif url.find("shidurlive") >= 0:
        params["server"] = 'shidurlive'
        if url.find("timeout") < 0:
            if url.endswith("conn=S:OK") == True:  # Control para aquellos servidores que requieran al final de la URL la expresión: conn=S:OK
                url = url.replace("conn=S:OK", "").strip()
                url = url + ' timeout=15 conn=S:OK'
                params["url"]=url
            else:
                url = url + ' timeout=15'
                params["url"]=url
        return params

    elif url.find("multistream") >= 0:
        params["server"] = 'multistream'
        if url.find("timeout") < 0:
            if url.endswith("conn=S:OK") == True:  # Control para aquellos servidores que requieran al final de la URL la expresión: conn=S:OK
                url = url.replace("conn=S:OK", "").strip()
                url = url + ' timeout=15 conn=S:OK'
                params["url"]=url
            else:
                url = url + ' timeout=15'
                params["url"]=url
        return params

    elif url.find("playfooty") >= 0:
        params["server"] = 'playfooty'
        if url.find("timeout") < 0:
            if url.endswith("conn=S:OK") == True:  # Control para aquellos servidores que requieran al final de la URL la expresión: conn=S:OK
                url = url.replace("conn=S:OK", "").strip()
                url = url + ' timeout=15 conn=S:OK'
                params["url"]=url
            else:
                url = url + ' timeout=15'
                params["url"]=url
        return params

    elif url.find("flashtv") >= 0:
        params["server"] = 'flashtv'
        if url.find("timeout") < 0:
            if url.endswith("conn=S:OK") == True:  # Control para aquellos servidores que requieran al final de la URL la expresión: conn=S:OK
                url = url.replace("conn=S:OK", "").strip()
                url = url + ' timeout=15 conn=S:OK'
                params["url"]=url
            else:
                url = url + ' timeout=15'
                params["url"]=url
        return params

    elif url.find("04stream") >= 0:
        params["server"] = '04stream'
        if url.find("timeout") < 0:
            if url.endswith("conn=S:OK") == True:  # Control para aquellos servidores que requieran al final de la URL la expresión: conn=S:OK
                url = url.replace("conn=S:OK", "").strip()
                url = url + ' timeout=15 conn=S:OK'
                params["url"]=url
            else:
                url = url + ' timeout=15'
                params["url"]=url
        return params

    elif url.find("vercosas") >= 0:
        params["server"] = 'vercosasgratis'
        if url.find("timeout") < 0:
            if url.endswith("conn=S:OK") == True:  # Control para aquellos servidores que requieran al final de la URL la expresión: conn=S:OK
                url = url.replace("conn=S:OK", "").strip()
                url = url + ' timeout=15 conn=S:OK'
                params["url"]=url
            else:
                url = url + ' timeout=15'
                params["url"]=url
        return params

    elif url.find("") >= 0:
        params["server"] = ''
        if url.find("timeout") < 0:
            if url.endswith("conn=S:OK") == True:  # Control para aquellos servidores que requieran al final de la URL la expresión: conn=S:OK
                url = url.replace("conn=S:OK", "").strip()
                url = url + ' timeout=15 conn=S:OK'
                params["url"]=url
            else:
                url = url + ' timeout=15'
                params["url"]=url
        return params

    elif url.find("playfooty") >= 0:
        params["server"] = 'playfooty'
        if url.find("timeout") < 0:
            if url.endswith("conn=S:OK") == True:  # Control para aquellos servidores que requieran al final de la URL la expresión: conn=S:OK
                url = url.replace("conn=S:OK", "").strip()
                url = url + ' timeout=15 conn=S:OK'
                params["url"]=url
            else:
                url = url + ' timeout=15'
                params["url"]=url
        return params

    elif url.find("pvtserverz") >= 0:
        params["server"] = 'pvtserverz'
        if url.find("timeout") < 0:
            if url.endswith("conn=S:OK") == True:  # Control para aquellos servidores que requieran al final de la URL la expresión: conn=S:OK
                url = url.replace("conn=S:OK", "").strip()
                url = url + ' timeout=15 conn=S:OK'
                params["url"]=url
            else:
                url = url + ' timeout=15'
                params["url"]=url
        return params

    else:
        params["server"] = ''
        if url.find("timeout") < 0:
            if url.endswith("conn=S:OK") == True:  # Control para aquellos servidores que requieran al final de la URL la expresión: conn=S:OK
                url = url.replace("conn=S:OK", "").strip()
                url = url + ' timeout=15 conn=S:OK'
                params["url"]=url
            else:
                url = url + ' timeout=15'
                params["url"]=url
        return params

    if url.startswith("rtsp") >= 0:
        params["server"] = ''
        params["url"]=url
        return params



def launch_rtmp(params):
    plugintools.log('[%s %s].launch_rtmp %s' % (addonName, addonVersion, repr(params)))

    url = params.get("url")
    title = params.get("title")
    title = title.replace("[/COLOR]", "")
    title = title.strip()
    plugintools.log("Vamos a buscar en el título: "+title)

    if title.endswith("[9stream]") == True:
        print '9stream'
        params["server"] = '9stream'
        ninestreams(params)

    elif title.endswith("[iguide]") == True:
        plugintools.log("es un iguide!")
        params["server"] = 'iguide'
        # DEBUG: Keyboard: scancode: 0x01, sym: 0x001b, unicode: 0x001b, modifier: 0x0
        #pDialog = xbmcgui.DialogProgress()
        #msg = pDialog.create('TvWin', 'Intentando reproducir RTMP...')
        plugintools.play_resolved_url(url)
        #xbmc.sleep(15000)
        #plugintools.stop_resolved_url(url)

    elif title.endswith("[streamingfreetv]") == True:
        print 'streamingfreetv'
        params["server"] = 'streamingfreetv'
        streamingfreetv(params)

    elif title.endswith("[vercosasgratis]") == True:
        print 'vercosasgratis'
        params["server"] = 'vercosasgratis'
        vercosas(params)

    elif title.endswith("[freebroadcast]") == True:
        print 'freebroadcast'
        params["server"] = 'freebroadcast'
        freebroadcast(params)

    elif title.endswith("[ucaster]") == True:
        params["server"] = 'ucaster'
        plugintools.play_resolved_url(url)

    elif title.endswith("[direct2watch]") == True:
        params["server"] = 'direct2watch'
        directwatch(params)

    elif title.endswith("[shidurlive]") == True:
        params["server"] = 'shidurlive'
        shidurlive(params)

    elif title.endswith("[cast247]") == True:
        params["server"] = 'cast247'
        castdos(params)

    elif url.find("hdcast") >= 0:
        params["server"] = 'hdcast'
        plugintools.play_resolved_url(url)

    elif url.find("janjua") >= 0:
        params["server"] = 'janjua'
        plugintools.play_resolved_url(url)

    elif url.find("mips") >= 0:
        params["server"] = 'mips'
        plugintools.play_resolved_url(url)

    elif url.find("zecast") >= 0:
        params["server"] = 'zecast'
        plugintools.play_resolved_url(url)

    elif url.find("filotv") >= 0:
        params["server"] = 'filotv'
        print "filotv"
        plugintools.play_resolved_url(url)

    elif url.find("ezcast") >= 0:
        params["server"] = 'ezcast'
        plugintools.play_resolved_url(url)

    elif url.find("flashstreaming") >= 0:
        params["server"] = 'flashstreaming'
        plugintools.play_resolved_url(url)

    elif url.find("shidurlive") >= 0:
        params["server"] = 'shidurlive'
        plugintools.play_resolved_url(url)

    elif url.find("multistream") >= 0:
        params["server"] = 'multistream'
        print "multistream"
        plugintools.play_resolved_url(url)

    elif url.find("playfooty") >= 0:
        params["server"] = 'playfooty'
        plugintools.play_resolved_url(url)

    elif url.find("flashtv") >= 0:
        params["server"] = 'flashtv'
        print "flashtv"
        plugintools.play_resolved_url(url)

    elif url.find("freetvcast") >= 0:
        params["server"] = 'freetvcast'
        print "freetvcast"
        freetvcast(params)

    elif url.find("04stream") >= 0:
        params["server"] = '04stream'
        plugintools.play_resolved_url(url)

    elif url.find("sharecast") >= 0:
        params["server"] = 'sharecast'
        plugintools.play_resolved_url(url)

    elif url.find("vaughnlive") >= 0:
        params["server"] = 'vaughnlive'
        resolve_vaughnlive(params)

    elif url.find("sawlive") >= 0:
        params["server"] = 'sawlive'
        sawlive(params)

    elif url.find("goodcast") >= 0:
        params["server"] = 'goodcast'
        plugintools.play_resolved_url(url)

    elif url.find("dcast.tv") >= 0:
        params["server"] = 'dcast.tv'
        plugintools.play_resolved_url(url)

    elif url.find("castalba") >= 0:
        params["server"] = 'castalba'
        castalba(params)

    elif url.find("businessapp") >= 0:
        params["server"] = 'businessapp'
        businessapp(params)        

    elif url.find("tutelehd.com") >= 0:
        params["server"] = 'tutelehd.com'
        plugintools.play_resolved_url(url)

    elif url.find("flexstream") >= 0:
        params["server"] = 'flexstream'
        plugintools.play_resolved_url(url)

    elif url.find("xxcast") >= 0:
        params["server"] = 'xxcast'
        plugintools.play_resolved_url(url)

    elif url.find("vipi.tv") >= 0:
        params["server"] = 'vipi.tv'
        plugintools.play_resolved_url(url)

    elif url.find("watchjsc") >= 0:
        params["server"] = 'watchjsc'
        plugintools.play_resolved_url(url)

    elif url.find("zenex.tv") >= 0:
        params["server"] = 'zenex.tv'
        plugintools.play_resolved_url(url)

    elif url.find("castto") >= 0:
        params["server"] = 'castto'
        plugintools.play_resolved_url(url)

    elif url.find("tvzune") >= 0:
        params["server"] = 'tvzune'
        plugintools.play_resolved_url(url)

    elif url.find("flashcast") >= 0:
        params["server"] = 'flashcast'
        plugintools.play_resolved_url(url)

    elif url.find("ilive.to") >= 0:
        params["server"] = 'ilive.to'
        print "iliveto"
        plugintools.play_resolved_url(url)

    elif url.find("Direct2Watch") >= 0:
        params["server"] = 'Direct2Watch'
        print "direct2watch"
        plugintools.play_resolved_url(url)

    else:
        print "No ha encontrado launcher"
        params["server"] = 'undefined'
        print "ninguno"
        plugintools.play_resolved_url(url)



def peliseries(params):
    plugintools.log('[%s %s].peliseries %s' % (addonName, addonVersion, repr(params)))

    # Abrimos archivo remoto
    url = params.get("url")
    filepelis = urllib2.urlopen(url)

    # Creamos archivo local para pegar las entradas
    plot = params.get("plot")
    plot = parser_title(plot)
    if plot == "":
        title = params.get("title")
        title = parser_title(title)
        filename = title + ".m3u"
        fh = open(playlists + filename, "wb")
    else:
        filename = params.get("plot") + ".m3u"
        fh = open(playlists + filename, "wb")

    plugintools.log("filename= "+filename)
    url = params.get("url")
    plugintools.log("url= "+url)


    #open the file for writing
    fw = open(playlists + filename, "wb")

    #open the file for writing
    fh = open(playlists + 'filepelis.m3u', "wb")
    fh.write(filepelis.read())

    fh.close()

    fw = open(playlists + filename, "wb")
    fr = open(playlists + 'filepelis.m3u', "r")
    fr.seek(0)
    num_items = len(fr.readlines())
    print num_items
    fw.seek(0)
    fr.seek(0)
    data = fr.readline()
    fanart = params.get("extra")
    thumbnail = params.get("thumbnail")
    fw.write('#EXTM3U:"background"='+fanart+',"thumbnail"='+thumbnail)
    fw.write("#EXTINF:-1,[COLOR lightyellow][I]playlists / " + filename + '[/I][/COLOR]' + '\n\n')
    i = 0

    while i <= num_items:

        if data == "":
            data = fr.readline()
            data = data.strip()
            plugintools.log("data= " +data)
            i = i + 1
            print i
            continue

        elif data.find("http") >= 0 :
            data = data.split("http")
            chapter = data[0]
            chapter = chapter.strip()
            url = "http" + data[1]
            url = url.strip()
            plugintools.log("url= "+url)
            fw.write("\n#EXTINF:-1," + chapter + '\n')
            fw.write(url + '\n\n')
            data = fr.readline()
            plugintools.log("data= " +data)
            i = i + 1
            print i
            continue

        else:
            data = fr.readline()
            data = data.strip()
            plugintools.log("data= "+data)
            i = i + 1
            print i
            continue

    fw.close()
    fr.close()
    params["ext"]='m3u'
    filename = filename.replace(".m3u", "")
    params["plot"]=filename
    params["title"]=filename

    # Capturamos de nuevo thumbnail y fanart

    os.remove(playlists + 'filepelis.m3u')
    simpletv_items(params)






# Conexión con el servicio longURL.org para obtener URL original


def longurl(params):
    plugintools.log("[TvWin-0.3.0].longURL "+repr(params))

    url = params.get("url")
    url_getlink = 'http://api.longurl.org/v2/expand?url=' +url

    plugintools.log("url_fixed= "+url_getlink)

    try:
        request_headers=[]
        request_headers.append(["User-Agent","Application-Name/3.7"])
        body,response_headers = plugintools.read_body_and_headers(url_getlink, headers=request_headers)
        plugintools.log("data= "+body)

        # <long-url><![CDATA[http://85.25.43.51:8080/DE_skycomedy?u=euorocard:p=besplatna]]></long-url>
        # xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('TvWin', "Redireccionando enlace...", 3 , art+'icon.png'))
        longurl = plugintools.find_single_match(body, '<long-url>(.*?)</long-url>')
        longurl = longurl.replace("<![CDATA[", "")
        longurl = longurl.replace("]]>", "")
        plugintools.log("longURL= "+longurl)
        if longurl.startswith("http"):
            plugintools.play_resolved_url(longurl)

    except:
        play(params)






def encode_url(url):
    url_fixed= urlencode(url)
    print url_fixed



def m3u_items(title):
    plugintools.log('[%s %s].m3u_items %s' % (addonName, addonVersion, title))    

    thumbnail = art + 'icon.png'
    fanart = art + 'fanart.jpg'
    only_title = title

    if title.find("tvg-logo") >= 0:
        thumbnail = re.compile('tvg-logo="(.*?)"').findall(title)
        num_items = len(thumbnail)
        print 'num_items',num_items
        if num_items == 0:
            thumbnail = 'icon.png'
        else:
            thumbnail = thumbnail[0]
        
        only_title = only_title.replace('tvg-logo="', "")
        only_title = only_title.replace(thumbnail, "")

    if title.find("tvg-wall") >= 0:
        fanart = re.compile('tvg-wall="(.*?)"').findall(title)
        fanart = fanart[0]
        only_title = only_title.replace('tvg-wall="', "")
        only_title = only_title.replace(fanart, "")
        
    try:
        if title.find("imdb") >= 0:
            imdb = re.compile('imdb="(.*?)"').findall(title)
            imdb = imdb[0]
            only_title = only_title.replace('imdb="', "")
            only_title = only_title.replace(imdb, "")
        else:
            imdb = ""
    except:
        imdb = ""

    try:
        if title.find("dir") >= 0:
            dir = re.compile('dir="(.*?)"').findall(title)
            dir = dir[0]
            only_title = only_title.replace('dir="', "")
            only_title = only_title.replace(dir, "")
        else:
            dir = ""
    except:
        dir = ""

    try:
        if title.find("wri") >= 0:
            writers = re.compile('wri="(.*?)"').findall(title)
            writers = writers[0]
            only_title = only_title.replace('wri="', "")
            only_title = only_title.replace(writers, "")
        else:
            writers = ""
    except:
        writers = ""

    try:
        if title.find("votes") >= 0:
            num_votes = re.compile('votes="(.*?)"').findall(title)
            num_votes = num_votes[0]
            only_title = only_title.replace('votes="', "")
            only_title = only_title.replace(num_votes, "")
        else:
            num_votes = ""
    except:
        num_votes = ""

    try:
        if title.find("plot") >= 0:
            plot = re.compile('plot="(.*?)"').findall(title)
            plot = plot[0]
            only_title = only_title.replace('plot="', "")
            only_title = only_title.replace(plot, "")
        else:
            plot = ""
    except:
        plot = ""

    try:
        if title.find("genre") >= 0:
            genre = re.compile('genre="(.*?)"').findall(title)
            genre = genre[0]
            only_title = only_title.replace('genre="', "")
            only_title = only_title.replace(genre, "")
            print 'genre',genre
        else:
            genre = ""
    except:
        genre = ""

    try:
        if title.find("time") >= 0:
            duration = re.compile('time="(.*?)"').findall(title)
            duration = duration[0]
            only_title = only_title.replace('time="', "")
            only_title = only_title.replace(duration, "")
            print 'duration',duration
        else:
            duration = ""
    except:
        duration = ""

    try:
        if title.find("year") >= 0:
            year = re.compile('year="(.*?)"').findall(title)
            year = year[0]
            only_title = only_title.replace('year="', "")
            only_title = only_title.replace(year, "")
            print 'year',year
        else:
            year = ""
    except:
        year = ""

    if title.find("group-title") >= 0:
        cat = re.compile('group-title="(.*?)"').findall(title)
        if len(cat) == 0:
            cat = ""
        else:
            cat = cat[0]
        plugintools.log("m3u_categoria= "+cat)
        only_title = only_title.replace('group-title=', "")
        only_title = only_title.replace(cat, "")
    else:
        cat = ""

    if title.find("tvg-id") >= 0:
        title = title.replace('”', '"')
        title = title.replace('“', '"')
        tvgid = re.compile('tvg-id="(.*?)"').findall(title)
        print 'tvgid',tvgid
        tvgid = tvgid[0]
        plugintools.log("m3u_categoria= "+tvgid)
        only_title = only_title.replace('tvg-id=', "")
        only_title = only_title.replace(tvgid, "")
    else:
        tvgid = ""

    if title.find("tvg-name") >= 0:
        tvgname = re.compile('tvg-name="(.*?)').findall(title)
        tvgname = tvgname[0]
        plugintools.log("m3u_categoria= "+tvgname)
        only_title = only_title.replace('tvg-name=', "")
        only_title = only_title.replace(tvgname, "")
    else:
        tvgname = ""

    only_title = only_title.replace('"', "").strip()

    return thumbnail, fanart, cat, only_title, tvgid, tvgname, imdb, duration, year, dir, writers, genre, num_votes, plot




def xml_skin():
    plugintools.log('[%s %s].xml_skin ' % (addonName, addonVersion))

    mastermenu = plugintools.get_setting("mastermenu")
    xmlmaster = plugintools.get_setting("xmlmaster")
    SelectXMLmenu = plugintools.get_setting("SelectXMLmenu")

    # values="default|HD|SD|MEDIA|"
    if xmlmaster == 'true':
        if SelectXMLmenu == '0':
            mastermenu = 'http://pastebin.com/raw.php?i=maCUftFJ'
            plugintools.log("[TvWin.xml_skin: "+SelectXMLmenu)
            # Control para ver la intro de wintv
            ver_intro = plugintools.get_setting("ver_intro")
            if ver_intro == "true":
                xbmc.Player(xbmc.PLAYER_CORE_AUTO).play(art + 'intro.mp4')
                
        elif SelectXMLmenu == '1': # ALTA 
            mastermenu = 'http://pastebin.com/raw.php?i=umhZzM9Y'
            plugintools.log("[TvWin.xml_skin: "+SelectXMLmenu)
            # Control para ver la intro de BAJO
            ver_intro = plugintools.get_setting("ver_intro")
            if ver_intro == "true":
                xbmc.Player(xbmc.PLAYER_CORE_AUTO).play(art + 'intro.mp4')              
            
        elif SelectXMLmenu == '2': # MEDIA 
            mastermenu = 'http://pastebin.com/raw.php?i=nLHRcK6c'
            plugintools.log("[TvWin.xml_skin: "+SelectXMLmenu)
            # Control para ver la intro de media
            ver_intro = plugintools.get_setting("ver_intro")
            if ver_intro == "true":
                xbmc.Player(xbmc.PLAYER_CORE_AUTO).play(art + 'intro.mp4')  
        elif SelectXMLmenu == '3':# BAJA
            mastermenu = 'http://pastebin.com/raw.php?i=9fQ8aGbM'
            plugintools.log("[TvWin.xml_skin: "+SelectXMLmenu)
            # Control para ver la intro de media
            ver_intro = plugintools.get_setting("ver_intro")
            if ver_intro == "true":
                xbmc.Player(xbmc.PLAYER_CORE_AUTO).play(art + 'intro.mp4')                
        elif SelectXMLmenu == '4':  # Pastebin
            id_pastebin = plugintools.get_setting("id_pastebin")
            if id_pastebin == "":
                plugintools.log("[TvWin.xml_skin: No definido")                
                mastermenu = 'http://pastebin.com/raw.php?i=EWZ7FnPG'
            else:                
                mastermenu = 'http://pastebin.com/raw.php?i=' +id_pastebin
                plugintools.log("[TvWin.xml_skin: "+mastermenu)
        elif SelectXMLmenu == '5':   
            mastermenu = ''
            if mastermenu == "":
                plugintools.log("[TvWin.xml_skin: No definido")
                mastermenu = 'http://pastebin.com/raw.php?i=umhZzM9Y'                
                # Control para ver la intro de TvWin
                ver_intro = plugintools.get_setting("ver_intro")
                if ver_intro == "true":
                    xbmc.Player(xbmc.PLAYER_CORE_AUTO).play(art + 'intro.mp4')                
        elif SelectXMLmenu == '6':  
            mastermenu = ''
            if mastermenu == "":
                plugintools.log("[TvWin.xml_skin: No definido")
                mastermenu = ''                    
                # Control para ver la intro de TvWin
                ver_intro = plugintools.get_setting("ver_intro")
                if ver_intro == "true":
                    xbmc.Player(xbmc.PLAYER_CORE_AUTO).play(art + 'intro.mp4')              
             
        
    else:
        # xmlmaster = False (no activado), menú por defecto     
        mastermenu = 'http://pastebin.com/raw.php?i=maCUftFJ'

        # Control para ver la intro de TvWin
        ver_intro = plugintools.get_setting("ver_intro")
        if ver_intro == "true":
            xbmc.Player(xbmc.PLAYER_CORE_AUTO).play(art + 'intro.mp4')
        

    return mastermenu







def add_playlist(params):
    plugintools.log('[%s %s].add_playlist %s' % (addonName, addonVersion, repr(params)))
    url_pl1 = plugintools.get_setting("url_pl1")
    url_pl2 = plugintools.get_setting("url_pl2")
    url_pl3 = plugintools.get_setting("url_pl3")

    # Sintaxis de la lista online. Acciones por defecto (M3U)
    action_pl1 = "getfile_http"
    action_pl2 = "getfile_http"
    action_pl3 = "getfile_http"

    tipo_pl1 = plugintools.get_setting('tipo_pl1')
    tipo_pl2 = plugintools.get_setting('tipo_pl2')
    tipo_pl3 = plugintools.get_setting('tipo_pl3')

    if tipo_pl1 == '0':
        action_pl1 = 'getfile_http'

    if tipo_pl1 == '1':
        action_pl1 = 'plx_items'

    if tipo_pl2 == '0':
        action_pl2 = 'getfile_http'

    if tipo_pl2 == '1':
        action_pl2 = 'plx_items'

    if tipo_pl3 == '0':
        action_pl3 = 'getfile_http'

    if tipo_pl3 == '1':
        action_pl3 = 'plx_items'

    title_pl1 = plugintools.get_setting("title_pl1")
    title_pl2 = plugintools.get_setting("title_pl2")
    title_pl3 = plugintools.get_setting("title_pl3")

    plugintools.add_item(action="", title='[COLOR lightyellow]Listas online:[/COLOR]', url="", folder=False, isPlayable=False)

    if url_pl1 != "":
        if title_pl1 == "":
            title_pl1 = "[COLOR lightyellow]Lista online 1[/COLOR]"
        plugintools.add_item(action=action_pl1, title='  '+title_pl1, url=url_pl1, folder=True, isPlayable=False)

    if url_pl2 != "":
        if title_pl2 == "":
            title_pl2 = "[COLOR lightyellow]Lista online 2[/COLOR]"
        plugintools.add_item(action=action_pl2, title='  '+title_pl2, url=url_pl2, folder=True, isPlayable=False)

    if url_pl3 != "":
        if title_pl3 == "":
            title_pl3 == "[COLOR lightyellow]Lista online 3[/COLOR]"
        plugintools.add_item(action=action_pl3, title='  '+title_pl3, url=url_pl3, folder=True, isPlayable=False)





# Esta función añade coletilla de tipo de enlace a los multilink
def multiparse_title(title, url):

    if url.startswith("serie") == True:
        if url.find("seriesflv") >= 0:
            title = title + ' [COLOR lightyellow][I][Series[B]FLV[/B]][/I][/COLOR]'
        if url.find("seriesyonkis") >= 0:
            title = title + ' [COLOR lightyellow][I][Series[B]Yonkis[/B]][/I][/COLOR]'
        if url.find("seriesadicto") >= 0:
            title = title + ' [COLOR lightyellow][I][Series[B]Adicto[/B]][/I][/COLOR]'
        if url.find("seriesblanco") >= 0:
            title = title + ' [COLOR lightyellow][I][Series[B]Blanco[/B]][/I][/COLOR]'            

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

        elif url.find(".cbz") >= 0:
            title = title + ' [COLOR lightyellow][I][CBZ][/I][/COLOR]'

        elif url.find(".cbr") >= 0:
            title = title + ' [COLOR lightyellow][I][CBR][/I][/COLOR]'            

        elif url.find(".pdf") >= 0:
            title = title + ' [COLOR lightyellow][I][PDF][/I][/COLOR]'              


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
        elif url.find("businessapp") >= 0:
            title = title + ' [COLOR lightyellow][I][businessapp][/I][/COLOR]'            
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
	title = title + ' [COLOR lightyellow][I][Unknown][/I][/COLOR]'

    plugintools.log("title_fixed= "+title)
    plugintools.log("url= "+url)
    return title




    


   


    



    


def show_cbx(params):
    plugintools.log('[%s %s].show_CBX %s' % (addonName, addonVersion, repr(params)))
    xbmc.executebuiltin("Container.SetViewMode(500)")
    url = params.get("url")
    dst_folder = params.get("extra")
    page = params.get("page")
    plugintools.log("url= "+url)
    page_to_start = dst_folder + '\\'+str(page)    
    xbmc.executebuiltin( "ShowPicture("+url+")" )    
    

def show_image(params):
    plugintools.log('[%s %s].show_image %s' % (addonName, addonVersion, repr(params)))
    url=params.get("url")
    url = url.replace("img:", "")

    plugintools.log("Iniciando descarga desde..."+url)
    h=urllib2.HTTPHandler(debuglevel=0)  # Iniciamos descarga...
    request = urllib2.Request(url)
    opener = urllib2.build_opener(h)
    urllib2.install_opener(opener)
    filename = url.split("/")
    max_len = len(filename)
    max_len = int(max_len) - 1
    filename = filename[max_len]
    fh = open(tmp + filename, "wb")  #open the file for writing
    connected = opener.open(request)
    meta = connected.info()
    filesize = meta.getheaders("Content-Length")[0]
    size_local = fh.tell()
    print 'filesize',filesize
    print 'size_local',size_local
    while int(size_local) < int(filesize):
        blocksize = 100*1024
        bloqueleido = connected.read(blocksize)
        fh.write(bloqueleido)  # read from request while writing to file
        size_local = fh.tell()
        print 'size_local',size_local
    imagen = tmp + filename
    xbmc.executebuiltin( "ShowPicture("+imagen+")" )  



run()



