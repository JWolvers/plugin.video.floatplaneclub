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

from xbmcswift2 import Plugin
import resources.lib.scraper as scraper

plugin = Plugin()


@plugin.route('/')
def show_page1():
    videos, has_next_page = scraper.get_videos()
    items = [{
        'label': video['title'],
        'info': {
            'originaltitle': video['title']
        },
        'path': plugin.url_for(
            endpoint='watch_video',
            video_id=video['url']
        ),
        'is_playable': True,
    } for video in videos]
    if has_next_page:
        next_page = str(2)
        items.append({
            'label': '>> Page %s >>' % (
                next_page
            ),
            'path': plugin.url_for(
                endpoint='show_page',
                page=next_page
            ),
        })
    return plugin.finish(items)


@plugin.route('/<page>/')
def show_page(page):
    videos, has_next_page = scraper.get_videos(page)
    items = [{
        'label': video['title'],
        'info': {
            'originaltitle': video['title']
        },
        'path': plugin.url_for(
            endpoint='watch_video',
            video_id=video['url']
        ),
        'is_playable': True,
    } for video in videos]
    if has_next_page:
        next_page = str(int(page) + 1)
        items.append({
            'label': '>> page %s >>' % (
                next_page
            ),
            'path': plugin.url_for(
                endpoint='show_page',
                page=next_page
            ),
        })
    if int(page) > 1:
        prev_page = str(int(page) - 1)
        items.insert(0, {
            'label': '<< page %s <<' % (
                prev_page
            ),
            'path': plugin.url_for(
                endpoint='show_page',
                page=prev_page
            ),
        })
    return plugin.finish(items)


@plugin.route('/watch/<video_id>/')
def watch_video(video_id):
    video_url = scraper.get_video_url(video_id)
    return plugin.set_resolved_url(video_url)


if __name__ == '__main__':
    plugin.run()
