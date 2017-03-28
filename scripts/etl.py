#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import stdin, stdout, stderr
import os, time, traceback
import json
import re
from urllib.parse import urlparse, parse_qs, unquote

import geoip2.database
loc_reader = geoip2.database.Reader('/opt/GeoLite2-City.mmdb')

#last_tm = 1465457924
last_tm = 1465344000
now = int(time.time())
t_offset = now - last_tm

class Event(dict):
    def __init__(self, data):
        super(Event, self).__init__(data)

    def path2resource(self):

        if not 'path' in self:
            self['resource_type'] = 'UNKNOWN'
            self['resource_item'] = 'UNKNOWN'
            self['resource'] = 'UNKNOWN'
            self['path'] = 'UNKNOWN'
            self['is_continue'] = False
            return

        url_result  = urlparse(self['path'])
        path_arr    = url_result.path.replace('/v1/','').split('/')
        self['resource'] = path_arr[0].upper()


        url_params  = parse_qs(url_result.query)

        self['is_continue'] = True if 'next' in url_params else False


        if 'q' in url_params:
            #print "======"
            #print url_params
            #print unquote(url_params['q'][0].encode('ISO-8859-1'))
            #print ""
            #print self['path']
            #print unquote(self['path'])
            #print unquote(self['path']).encode('utf-8')
            #print "======"
            #print ""

            self['resource_type'] = 'SEARCH'
            #self['resource_item'] = unquote(url_params['q'][0].encode('ISO-8859-1')).decode('utf-8')
            self['resource_item'] = unquote(url_params['q'][0])
        elif len(path_arr) == 1:
            self['resource_type'] = 'LIST'
            self['resource_item'] = ''
        elif len(path_arr) == 2:
            self['resource_type'] = 'ITEM'
            self['resource_item'] = path_arr[1]
        elif len(path_arr) == 3:
            self['resource_type'] = 'ITEM_LIST'
            self['resource_item'] = path_arr[1]

    def ip2latlng(self):
        ip = self['remote']
        resp = loc_reader.city(ip)

        try:
            float(resp.location.longitude)
        except:
            return

        self['geoip'] = {}
        self['geoip']['continent_code'] = resp.continent.code
        self['geoip']['coordinates'] = [resp.location.longitude, resp.location.latitude]
        self['geoip']['country'] = resp.country.name
        self['geoip']['city'] = resp.city.name
        self['geoip']['continent'] = resp.continent.name

    def agent2device(self):

        if not 'agent' in self:
            self['device'] = 'UNKNOWN'
            self['agent'] = 'UNKNOWN'
            return

        if self['agent'] == 'okhttp/3.3.1':
            self['device'] = 'ANDROID'
        elif re.search('iosapp',self['agent'], re.IGNORECASE):
            self['device'] = 'IOS'
        else:
            self['device'] = 'UNKNOWN'


    def shiftTime2Now(self):
        self['time'] = str( int(self['time']) + t_offset )


while True:
    try:
        raw = stdin.readline().strip()
        data = json.loads(raw)

        event = Event(data)
        event.path2resource()
        event.ip2latlng()
        event.agent2device()
        event.shiftTime2Now()

        stdout.write(json.dumps(event))
        stdout.flush()
    except Exception as e:
        stderr.write( "\n[ERROR] <%s>\n"%(e.args[0]) )
        #stderr.write( "[ERROR_DATA] <%s>\n\n"%(str(data)) )
        traceback.print_exc()
        stderr.flush()
        pass
