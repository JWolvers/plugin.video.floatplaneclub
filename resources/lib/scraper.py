#!/usr/bin/python
'''
plugin.video.floatplaneclub
Copyright (C) 2017  MrWolvetech

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import sys

from bs4 import BeautifulSoup
import requests, re
import xbmc, xbmcgui, xbmcaddon

loginURL = "https://linustechtips.com/main/login/"
videoBaseURL = "https://linustechtips.com/main/forum/91-the-floatplane-club/"
videoThumbURL = "https://cms.linustechtips.com/get/thumbnails/by_guid/{}"
videoPlayerURL = "https://linustechtips.com/main/applications/floatplane/interface/video_url.php?video_guid={}&video_quality={}&download=1"

settings = xbmcaddon.Addon(id='plugin.video.floatplaneclub')
user = settings.getSetting("username")
password = settings.getSetting("password")
quality = settings.getSetting("quality")
s = requests.Session()


def do_login():
    r = s.get(loginURL)
    soup = BeautifulSoup(r.text, "html.parser")
    csrfKey = soup.find("input", {"name":"csrfKey"})['value']
    
    headers = {"content-type" : "application/x-www-form-urlencoded"}
    data = {"login__standard_submitted": '1',
			"csrfKey": csrfKey,
			"auth": user,
			"password": password,
			"remember_me": '0',
			"remember_me_checkbox": '1',
			"signin_anonymous": '0'}
    r = s.post(loginURL, data=data, headers=headers)
    return


def get_videos(page=1):
    do_login()
    r = s.get(videoBaseURL + str(page))
    soup = BeautifulSoup(r.text, "html.parser")
    pages = str(soup.find(text=re.compile('.*Page [0-9]* of [0-9]*')).replace(u'\xa0', u''))
    has_next_page = page < int(pages.split()[-1]) 
    
    forum = soup.find("ol", {"class":"cForumTopicTable"})
    linkContainers = forum.findAll("div", {"class":"ipsDataItem_main"})
    for linkContainer in linkContainers:
        if len(linkContainer.findAll("span", {"title":"Pinned"})) > 0:
            linkContainers.remove(linkContainer)
    links = [linkContainer.find("a") for linkContainer in linkContainers]
    videos = [{"title":link['title'], "url":link['href']} for link in links]
    return videos, has_next_page

    
def get_video_url(url):
    do_login()
    r = s.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    player = soup.find("iframe", {"src" : re.compile("https://cms\.linustechtips\.com/get/player/.*")})
    vidID = player['src'].rsplit('/', 1)[-1]
    r = s.get(videoPlayerURL.format(vidID, quality))
    return r.text
    
def get_thumbnail(url):
    do_login()
    r = s.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    player = soup.find("iframe", {"src" : re.compile("https://cms\.linustechtips\.com/get/player/.*")})
    vidID = player['src'].rsplit('/', 1)[-1]
    r = s.get(videoThumbURL.format(vidID))
    return r.text
