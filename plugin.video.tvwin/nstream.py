# -*- coding: utf-8 -*-
#--------------------------------------------------------
#  creado por quequeQ para PalcoTV
# (http://forum.rojadirecta.es/member.php?1370946-quequeQ)
# (http://xbmcspain.com/foro/miembro/quequino/)
# Version 0.0.1 (26.10.2014)
#--------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)

import re,urllib,urllib2,sys
import plugintools,ioncube
def nstream(url,ref,caster,res,script):
 if caster == 'ucaster':
    ucaster(url,ref,res)
 elif caster == '9stream':
    nstr(url,ref,res)
 else:
    print "\nNSCRIPT = "+str(script);print "\nURL = "+url;print "\nREFERER = "+str(ref);print "\nCASTER = "+str(caster);
	
def nstr(url,ref,res):
 #print str(res);
 p1 = re.compile(ur'embed\/=?\'?"?([^\'"\&,;]+)')
 p2 = re.compile(ur'width=?\'?"?([^\'"\&,;]+)')
 p3 = re.compile(ur'height=?\'?"?([^\'"\&,;]+)')
 f1=re.findall(p1, str(res));f2=re.findall(p2, str(res));f3=re.findall(p3, str(res));#res=list(set(f));
 w=f2[0];h=f3[0];c=f1[0];
 #print f2;sys.exit()
 ref=url
 url='http://www.9stream.com/embedplayer.php?width='+w+'&height='+h+'&channel='+c+'&autoplay=true';body='';#
 
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
 
def ucaster(url,ref,res):
 p = re.compile(ur'(channel|width|height)=?\'?"?([^\'"\&,;]+)')
 f=re.findall(p, str(res));res=list(set(f));
 w=res[0][1];h=res[2][1];c=res[1][1];
 ref=url
 url='http://www.ucaster.eu/embedded/'+c+'/1/'+w+'/'+h;body=''
 curl_frame(url,ref,body)
		
def curl_frame(url,ref,body):
	request_headers=[];
	request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
	request_headers.append(["Referer",ref])
	body,response_headers=plugintools.read_body_and_headers(url, headers=request_headers);
	return body