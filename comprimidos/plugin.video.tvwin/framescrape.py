# -*- coding: utf-8 -*-
#--------------------------------------------------------
#  creado por quequeQ para PalcoTV
# (http://forum.rojadirecta.es/member.php?1370946-quequeQ)
# (http://xbmcspain.com/foro/miembro/quequino/)
# Version 0.0.1 (26.10.2014)
#--------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
#--------------------------------------------------------
#
#Solo funcionan los 9streams,se tienen que añadir mas ...
#

import os,sys,urlparse,urllib,urllib2,re,shutil,zipfile,cookielib

import xbmc,xbmcgui,xbmcaddon,xbmcplugin

import plugintools,ioncube,nstream
from plugintools import *
from nstream import *
from ioncube import *


art = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.cipqtv/art', ''))
playlists = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.cipqtv/playlists', ''))
tmp = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.cipqtv/tmp', ''))
tools = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.cipqtv/resources/tools', ''))
icon = art + 'icon.png'
fanart = 'fanart.jpg'

def frame_parserl(params):
	url = params.get("url")
	print "START="+params.get("url")
	if params.get("title")=="[COLOR=red]Pon[COLOR=yellow]Tu[COLOR=red]Canal[/COLOR][/COLOR][/COLOR]" :
	 pattern1 = 'popUp\(\'([^\']+).*src="([^"]+)'
	 pattern2 = "http://canalesgratis.me/canales/"#http://canalesgratis.me/canales/ant3op2.php
	 pattern3 = ".php"
	else :#PonLaTele
	 pattern1 = 'popUp\(\'([^\']+).*src="([^"]+)'
	 pattern2 = "http://verdirectotv.com/canales/"
	 pattern3 = ".html"
	request_headers=[]
	request_headers.append(["User-Agent","Mozilla/4.0 (compatible; MSIE 5.01; Windows NT 5.0)"])
	body,response_headers = plugintools.read_body_and_headers(url, headers=request_headers)
	data=body
	ref = url
	matches = find_multiple_matches_multi(data,pattern1)
	i=0
	for scrapedurl, scrapedthumbnail in matches:
		thumb = scrapedthumbnail
		url = urlparse.urljoin( params.get("url") , scrapedurl.strip() )
		import string
		#title = url.replace(pattern2,"").replace(pattern3,"").replace("-"," ").upper()
		title = url.replace(pattern2,"").replace(pattern3,"").replace("-"," ");title = string.capwords(title)
		if i%2==0:
		 #title = "[COLOR=red]"+string.capwords(title)+"[/COLOR]"
		 p1 = title[0]
		 p2 = "[COLOR=red]"+title[0]+"[/COLOR]"
		 title = title.replace(p1,p2);
		else:
		 #title = "[COLOR=yellow]"+string.capwords(title)+"[/COLOR]"
		 p1 = title[0]
		 p2 = "[COLOR=yellow]"+title[0]+"[/COLOR]"
		 title = title.replace(p1,p2);
		i+=1
		msg = "Resolviendo enlace ... "
		uri = url+'@'+title+'@'+ref
		#plugintools.log("\nURI= "+uri)
		plugintools.add_item( action="frame_parser2" , title=title , url=uri ,thumbnail=thumb ,fanart=thumb , isPlayable=True, folder=False )
		
def frame_parser2(params):
	#regex='<iframe.*?src="([^\'"]*).*?<\/iframe>|"window\.open\(\'([^\']+)'#en futuras versiones
	regex='<iframe.*?src="([^\'"]*).*?<\/iframe>'
	url,title,thumbnail = params.get("url"),params.get("title"),params.get("thumbnail")
	url=url.split('@');title=url[1];ref=url[2];url=url[0];
	body='';bodyi=[];urli=[];bodyy='';enctrdiy=[];enctrdi=[];j=1;
	urli+=([url]);bodyi+=([body]);
	urli=list(set(urli));bodyi=list(set(bodyi));
	for i in range(-1,j):
	 m=0
	 ref=url;url=urli[i]
	 print "\n***URL:"+str(i);print url;
	 curl_frame(url,ref,body,bodyi,bodyy,urli);
	 bodyy=' '.join([str(i) for i in bodyi]);
	 enctrd=find_multiple_matches_multi(bodyy,regex);
	 enctrd=list(set(enctrd))
	 urli=([b for b in set(enctrd)]);j=len(urli)
	 if j>0:
	  i=-1;m+=1
	p=('m3u8','freelivetv','freetvcast','goo\.gl','vercosasgratis','byetv','9stream','castalba','direct2watch','kbps','flashstreaming','cast247','ilive','freebroadcast','flexstream','mips','veemi','yocast','yukons','ilive','iguide','ucaster','ezcast','plusligaonline','tvonlinegratis');z=len(p);
	for i in range(0, z):
	 regex='<script.*?('+str(p[i])+').*?<\/script>'
	 caster=[];
	 enctrd=plugintools.find_single_match(bodyy,regex);
	 #!!!Quita el "if" de abajo para ver todo los "enctrd" encontrados de cada "p" caster !!!
	 if len(enctrd)>0:
	  caster=''.join(map(str,enctrd));
	  import re
	  #regex2 = re.compile('<script.*?(?=>)>(.*?)(?=<).*?src=\'?"?(.*?'+caster+'[^\'",;]+)', re.VERBOSE)
	  regex2 = re.compile('(<script.*?(?=>)>(.*?)(?=<))?.*?src=\'?"?(.*?'+caster+'[^\'",;]+)', re.VERBOSE)
	  res = re.findall(regex2,bodyy)
	  print 'res',res
	  res=filter(None,res);
	  res=list(set(res));
	  script=''.join(map(str,res));
	  print 'res',res
	  nstream(url,ref,caster,res,script)
		
def curl_frame(url,ref,body,bodyi,bodyy,urli):
	request_headers=[];
	request_headers.append(["User-Agent","Mozilla/4.0 (compatible; MSIE 5.01; Windows NT 5.0)"])
	request_headers.append(["Referer",ref])
	body,response_headers=plugintools.read_body_and_headers(url, headers=request_headers);
	print "HEADERS:\n";print response_headers
	urli+=([url]);bodyi+=([body]);#print bodyi;print urli;
	urli=list(set(urli));#bodyi=filter(len,list(set(bodyi)));

def find_multiple_matches_multi(text,pattern):
    matches = re.findall(pattern,text, re.MULTILINE)
    return matches

