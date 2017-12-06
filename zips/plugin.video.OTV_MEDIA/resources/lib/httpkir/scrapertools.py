﻿# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# streamondemand 5
# Copyright 2015 tvalacarta@gmail.com
# http://www.mimediacenter.info/foro/viewforum.php?f=36
#
# Distributed under the terms of GNU General Public License v3 (GPLv3)
# http://www.gnu.org/licenses/gpl-3.0.html
# ------------------------------------------------------------
# This file is part of streamondemand 5.
#
# streamondemand 5 is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# streamondemand 5 is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with streamondemand 5.  If not, see <http://www.gnu.org/licenses/>.
# --------------------------------------------------------------------------------
# Scraper tools for reading and processing web elements
# --------------------------------------------------------------------------------

import re
import socket
import time

import logger
import httptools


def cache_page(url,post=None,headers=None,modo_cache=None, timeout=None):
    return cachePage(url,post,headers,modo_cache,timeout=timeout)


def cachePage(url,post=None,headers=None,modoCache=None, timeout=None):
    data = downloadpage(url,post=post,headers=headers, timeout=timeout)
    return data


def downloadpage(url,post=None,headers=None, follow_redirects=True, timeout=None, header_to_get=None):
    response = httptools.downloadpage(url, post=post, headers=headers, follow_redirects = follow_redirects, timeout=timeout)
    
    if header_to_get:
      return response.headers.get(header_to_get)
    else:
      return response.data


def downloadpageWithResult(url,post=None,headers=None,follow_redirects=True, timeout=None, header_to_get=None):
    response = httptools.downloadpage(url, post=post, headers=headers, follow_redirects = follow_redirects, timeout=timeout)
    
    if header_to_get:
      return response.headers.get(header_to_get)
    else:
      return response.data, response.code


def downloadpageWithoutCookies(url):
    response = httptools.downloadpage(url, cookies=False)
    return response.data


def downloadpageGzip(url):
    response = httptools.downloadpage(url, add_referer=True)
    return response.data


def getLocationHeaderFromResponse(url):
    response = httptools.downloadpage(url, only_headers=True, follow_redirects=False)
    return response.headers.get("location")


def get_header_from_response(url, header_to_get="", post=None, headers=None, follow_redirects=False):
    header_to_get = header_to_get.lower()
    response = httptools.downloadpage(url, post=post, headers=headers, only_headers=True,
                                      follow_redirects=follow_redirects)
    return response.headers.get(header_to_get)


def get_headers_from_response(url, post=None, headers=None, follow_redirects=False):
    response = httptools.downloadpage(url, post=post, headers=headers, only_headers=True,
                                      follow_redirects=follow_redirects)
    return response.headers.items()
    

def read_body_and_headers(url, post=None, headers=None, follow_redirects=False, timeout=None):
    response = httptools.downloadpage(url, post=post, headers=headers, follow_redirects=follow_redirects, timeout=timeout)
    return response.data, response.headers


def anti_cloudflare(url, headers=None, post=None):
    #anti_cloudfare ya integrado en httptools por defecto
    response = httptools.downloadpage(url, post=post, headers=headers)
    return response.data




def printMatches(matches):
    i = 0
    for match in matches:
        logger.info("%d %s" % (i, match))
        i = i + 1

def get_match(data,patron,index=0):
    matches = re.findall( patron , data , flags=re.DOTALL )
    return matches[index]

def find_single_match(data,patron,index=0):
    try:
        matches = re.findall( patron , data , flags=re.DOTALL )
        return matches[index]
    except:
        return ""

# Parse string and extracts multiple matches using regular expressions
def find_multiple_matches(text,pattern):
    return re.findall(pattern,text,re.DOTALL)

def entityunescape(cadena):
    return unescape(cadena)

def unescape(text):
    """Removes HTML or XML character references
       and entities from a text string.
       keep &amp;, &gt;, &lt; in the source code.
    from Fredrik Lundh
    http://effbot.org/zone/re-sub.htm#unescape-html
    """
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16)).encode("utf-8")
                else:
                    return unichr(int(text[2:-1])).encode("utf-8")

            except ValueError:
                logger.error("error de valor")
                pass
        else:
            # named entity
            try:
                '''
                if text[1:-1] == "amp":
                    text = "&amp;amp;"
                elif text[1:-1] == "gt":
                    text = "&amp;gt;"
                elif text[1:-1] == "lt":
                    text = "&amp;lt;"
                else:
                    print text[1:-1]
                    text = unichr(htmlentitydefs.name2codepoint[text[1:-1]]).encode("utf-8")
                '''
                import htmlentitydefs
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]]).encode("utf-8")
            except KeyError:
                logger.error("keyerror")
                pass
            except:
                pass
        return text # leave as is
    return re.sub("&#?\w+;", fixup, text)

    # Convierte los codigos html "&ntilde;" y lo reemplaza por "ñ" caracter unicode utf-8
def decodeHtmlentities(string):
    string = entitiesfix(string)
    entity_re = re.compile("&(#?)(\d{1,5}|\w{1,8});")

    def substitute_entity(match):
        from htmlentitydefs import name2codepoint as n2cp
        ent = match.group(2)
        if match.group(1) == "#":
            return unichr(int(ent)).encode('utf-8')
        else:
            cp = n2cp.get(ent)

            if cp:
                return unichr(cp).encode('utf-8')
            else:
                return match.group()

    return entity_re.subn(substitute_entity, string)[0]

def entitiesfix(string):
    # Las entidades comienzan siempre con el símbolo & , y terminan con un punto y coma ( ; ).
    string = string.replace("&aacute","&aacute;")
    string = string.replace("&eacute","&eacute;")
    string = string.replace("&iacute","&iacute;")
    string = string.replace("&oacute","&oacute;")
    string = string.replace("&uacute","&uacute;")
    string = string.replace("&Aacute","&Aacute;")
    string = string.replace("&Eacute","&Eacute;")
    string = string.replace("&Iacute","&Iacute;")
    string = string.replace("&Oacute","&Oacute;")
    string = string.replace("&Uacute","&Uacute;")
    string = string.replace("&uuml"  ,"&uuml;")
    string = string.replace("&Uuml"  ,"&Uuml;")
    string = string.replace("&ntilde","&ntilde;")
    string = string.replace("&#191"  ,"&#191;")
    string = string.replace("&#161"  ,"&#161;")
    string = string.replace(";;"     ,";")
    return string


def htmlclean(cadena):
    cadena = re.compile("<!--.*?-->",re.DOTALL).sub("",cadena)

    cadena = cadena.replace("<center>","")
    cadena = cadena.replace("</center>","")
    cadena = cadena.replace("<cite>","")
    cadena = cadena.replace("</cite>","")
    cadena = cadena.replace("<em>","")
    cadena = cadena.replace("</em>","")
    cadena = cadena.replace("<u>","")
    cadena = cadena.replace("</u>","")
    cadena = cadena.replace("<li>","")
    cadena = cadena.replace("</li>","")
    cadena = cadena.replace("<turl>","")
    cadena = cadena.replace("</tbody>","")
    cadena = cadena.replace("<tr>","")
    cadena = cadena.replace("</tr>","")
    cadena = cadena.replace("<![CDATA[","")
    cadena = cadena.replace("<Br />"," ")
    cadena = cadena.replace("<BR />"," ")
    cadena = cadena.replace("<Br>"," ")
    cadena = re.compile("<br[^>]*>",re.DOTALL).sub(" ",cadena)

    cadena = re.compile("<script.*?</script>",re.DOTALL).sub("",cadena)

    cadena = re.compile("<option[^>]*>",re.DOTALL).sub("",cadena)
    cadena = cadena.replace("</option>","")

    cadena = re.compile("<button[^>]*>",re.DOTALL).sub("",cadena)
    cadena = cadena.replace("</button>","")

    cadena = re.compile("<i[^>]*>",re.DOTALL).sub("",cadena)
    cadena = cadena.replace("</iframe>","")
    cadena = cadena.replace("</i>","")

    cadena = re.compile("<table[^>]*>",re.DOTALL).sub("",cadena)
    cadena = cadena.replace("</table>","")

    cadena = re.compile("<td[^>]*>",re.DOTALL).sub("",cadena)
    cadena = cadena.replace("</td>","")

    cadena = re.compile("<div[^>]*>",re.DOTALL).sub("",cadena)
    cadena = cadena.replace("</div>","")

    cadena = re.compile("<dd[^>]*>",re.DOTALL).sub("",cadena)
    cadena = cadena.replace("</dd>","")

    cadena = re.compile("<b[^>]*>",re.DOTALL).sub("",cadena)
    cadena = cadena.replace("</b>","")

    cadena = re.compile("<font[^>]*>",re.DOTALL).sub("",cadena)
    cadena = cadena.replace("</font>","")

    cadena = re.compile("<strong[^>]*>",re.DOTALL).sub("",cadena)
    cadena = cadena.replace("</strong>","")

    cadena = re.compile("<small[^>]*>",re.DOTALL).sub("",cadena)
    cadena = cadena.replace("</small>","")

    cadena = re.compile("<span[^>]*>",re.DOTALL).sub("",cadena)
    cadena = cadena.replace("</span>","")

    cadena = re.compile("<a[^>]*>",re.DOTALL).sub("",cadena)
    cadena = cadena.replace("</a>","")

    cadena = re.compile("<p[^>]*>",re.DOTALL).sub("",cadena)
    cadena = cadena.replace("</p>","")

    cadena = re.compile("<ul[^>]*>",re.DOTALL).sub("",cadena)
    cadena = cadena.replace("</ul>","")

    cadena = re.compile("<h1[^>]*>",re.DOTALL).sub("",cadena)
    cadena = cadena.replace("</h1>","")

    cadena = re.compile("<h2[^>]*>",re.DOTALL).sub("",cadena)
    cadena = cadena.replace("</h2>","")

    cadena = re.compile("<h3[^>]*>",re.DOTALL).sub("",cadena)
    cadena = cadena.replace("</h3>","")

    cadena = re.compile("<h4[^>]*>",re.DOTALL).sub("",cadena)
    cadena = cadena.replace("</h4>","")

    cadena = re.compile("<!--[^-]+-->",re.DOTALL).sub("",cadena)

    cadena = re.compile("<img[^>]*>",re.DOTALL).sub("",cadena)

    cadena = re.compile("<object[^>]*>",re.DOTALL).sub("",cadena)
    cadena = cadena.replace("</object>","")
    cadena = re.compile("<param[^>]*>",re.DOTALL).sub("",cadena)
    cadena = cadena.replace("</param>","")
    cadena = re.compile("<embed[^>]*>",re.DOTALL).sub("",cadena)
    cadena = cadena.replace("</embed>","")

    cadena = re.compile("<title[^>]*>",re.DOTALL).sub("",cadena)
    cadena = cadena.replace("</title>","")

    cadena = re.compile("<link[^>]*>",re.DOTALL).sub("",cadena)

    cadena = cadena.replace("\t","")
    cadena = entityunescape(cadena)
    return cadena


def slugify(title):

    #print title

    # Sustituye acentos y eñes
    title = title.replace("Á","a")
    title = title.replace("É","e")
    title = title.replace("Í","i")
    title = title.replace("Ó","o")
    title = title.replace("Ú","u")
    title = title.replace("á","a")
    title = title.replace("é","e")
    title = title.replace("í","i")
    title = title.replace("ó","o")
    title = title.replace("ú","u")
    title = title.replace("À","a")
    title = title.replace("È","e")
    title = title.replace("Ì","i")
    title = title.replace("Ò","o")
    title = title.replace("Ù","u")
    title = title.replace("à","a")
    title = title.replace("è","e")
    title = title.replace("ì","i")
    title = title.replace("ò","o")
    title = title.replace("ù","u")
    title = title.replace("ç","c")
    title = title.replace("Ç","C")
    title = title.replace("Ñ","n")
    title = title.replace("ñ","n")
    title = title.replace("/","-")
    title = title.replace("&amp;","&")

    # Pasa a minúsculas
    title = title.lower().strip()

    # Elimina caracteres no válidos
    validchars = "abcdefghijklmnopqrstuvwxyz1234567890- "
    title = ''.join(c for c in title if c in validchars)

    # Sustituye espacios en blanco duplicados y saltos de línea
    title = re.compile("\s+",re.DOTALL).sub(" ",title)

    # Sustituye espacios en blanco por guiones
    title = re.compile("\s",re.DOTALL).sub("-",title.strip())

    # Sustituye espacios en blanco duplicados y saltos de línea
    title = re.compile("\-+",re.DOTALL).sub("-",title)

    # Arregla casos especiales
    if title.startswith("-"):
        title = title [1:]

    if title=="":
        title = "-"+str(time.time())

    return title

def remove_htmltags(string):
    return re.sub('<[^<]+?>', '', string)

def remove_show_from_title(title,show):
    #print slugify(title)+" == "+slugify(show)
    # Quita el nombre del programa del título
    if slugify(title).startswith(slugify(show)):

        # Convierte a unicode primero, o el encoding se pierde
        title = unicode(title,"utf-8","replace")
        show = unicode(show,"utf-8","replace")
        title = title[ len(show) : ].strip()

        if title.startswith("-"):
            title = title[ 1: ].strip()

        if title=="":
            title = str( time.time() )

        # Vuelve a utf-8
        title = title.encode("utf-8","ignore")
        show = show.encode("utf-8","ignore")

    return title

def getRandom(str):
    return get_md5(str)

def unseo(cadena):
    if cadena.upper().startswith("VER GRATIS LA PELICULA "):
        cadena = cadena[23:]
    elif cadena.upper().startswith("VER GRATIS PELICULA "):
        cadena = cadena[20:]
    elif cadena.upper().startswith("VER ONLINE LA PELICULA "):
        cadena = cadena[23:]
    elif cadena.upper().startswith("VER GRATIS "):
        cadena = cadena[11:]
    elif cadena.upper().startswith("VER ONLINE "):
        cadena = cadena[11:]
    elif cadena.upper().startswith("DESCARGA DIRECTA "):
        cadena = cadena[17:]
    return cadena

#scrapertools.get_filename_from_url(media_url)[-4:]
def get_filename_from_url(url):

    import urlparse
    parsed_url = urlparse.urlparse(url)
    try:
        filename = parsed_url.path
    except:
        # Si falla es porque la implementación de parsed_url no reconoce los atributos como "path"
        if len(parsed_url)>=4:
            filename = parsed_url[2]
        else:
            filename = ""

    if "/" in filename:
        filename = filename.split("/")[-1]

    return filename

def get_domain_from_url(url):

    import urlparse
    parsed_url = urlparse.urlparse(url)
    try:
        filename = parsed_url.netloc
    except:
        # Si falla es porque la implementación de parsed_url no reconoce los atributos como "path"
        if len(parsed_url)>=4:
            filename = parsed_url[1]
        else:
            filename = ""

    return filename

def get_season_and_episode(title):
    """
    Retorna el numero de temporada y de episodio en formato "1x01" obtenido del titulo de un episodio
    Ejemplos de diferentes valores para title y su valor devuelto:
        "serie 101x1.strm", "s101e1.avi", "t101e1.avi"  -> '101x01'
        "Name TvShow 1x6.avi" -> '1x06'
        "Temp 3 episodio 2.avi" -> '3x02'
        "Alcantara season 13 episodie 12.avi" -> '13x12'
        "Temp1 capitulo 14" -> '1x14'
        "Temporada 1: El origen Episodio 9" -> '' (entre el numero de temporada y los episodios no puede haber otro texto)
        "Episodio 25: titulo episodio" -> '' (no existe el numero de temporada)
        "Serie X Temporada 1" -> '' (no existe el numero del episodio)
    @type title: str
    @param title: titulo del episodio de una serie
    @rtype: str
    @return: Numero de temporada y episodio en formato "1x01" o cadena vacia si no se han encontrado
    """
    filename = ""

    patrons = ["(\d+)x(\d+)", "(?:s|t)(\d+)e(\d+)",
               "(?:season|stag\w*)\s*(\d+)\s*(?:capitolo|epi\w*)\s*(\d+)"]

    for patron in patrons:
        try:
            matches = re.compile(patron, re.I).search(title)
            if matches:
                filename = matches.group(1) + "x" + matches.group(2).zfill(2)
                break
        except:
            pass

    logger.info("'" + title + "' -> '" + filename + "'")

    return filename

def get_sha1(cadena):
    try:
        import hashlib
        devuelve = hashlib.sha1(cadena).hexdigest()
    except:
        import sha
        import binascii
        devuelve = binascii.hexlify(sha.new(cadena).digest())

    return devuelve

def get_md5(cadena):
    try:
        import hashlib
        devuelve = hashlib.md5(cadena).hexdigest()
    except:
        import md5
        import binascii
        devuelve = binascii.hexlify(md5.new(cadena).digest())

    return devuelve

def internet(host="8.8.8.8", port=53, timeout=3):
    """
   Host: 8.8.8.8 (google-public-dns-a.google.com)
   OpenPort: 53/tcp
   Service: domain (DNS/TCP)
   """
    try:
        deftimeout = socket.getdefaulttimeout()
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        socket.setdefaulttimeout(deftimeout)
        return True
    except:
        pass
    return False


def wait_for_internet(wait=30, retry=5):
    import xbmc

    monitor = xbmc.Monitor()
    count = 0
    while True:
        if internet():
            return True
        count += 1
        if count >= retry or monitor.abortRequested():
            return False
        monitor.waitForAbort(wait)
