#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#    Twitter UnFav
#    Copyright 2015     Torsten Grote <t at grobox.de>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys, os
from optparse import OptionParser
import ConfigParser
import twitter
import time, datetime

config_files = [
    'config.ini',                                                   # executing folder
    os.path.dirname(os.path.realpath(__file__)) + '/config.ini',    # real folder of script
    os.path.dirname(__file__) + '/config.ini'                       # folder of (symlinked) script
]

# Parse Command Line Options
usage = "usage: %prog option"
parser = OptionParser(usage=usage, version="%prog 0.1")
parser.add_option("-t", "--time",   dest="time",   action="store", type="int", default=7, help="Delete favorites older than this time in days.")
parser.add_option("-c", "--config", dest="config", action="store",      help="Use specified config file instead of default.")
parser.add_option("", "--debug",    dest="debug",  action="store_true", help="Print debugging output.")
(opt, args) = parser.parse_args()

if(opt.config != None):
    if(os.access(opt.config, os.R_OK)):
        # use supplied argument for config file first
        config_files.insert(0, opt.config)
    else:
        print "Error: Could not find config file '%s'." % opt.config
        sys.exit(1)

config = ConfigParser.SafeConfigParser()
used_config = config.read(config_files)

if(not config.has_section('Twitter')):
    print "Error: Could not find a valid config file."
    sys.exit(1)

# Set-up Twitter API
api = twitter.Api(
    consumer_key        = config.get('Twitter', 'consumer_key'),
    consumer_secret     = config.get('Twitter', 'consumer_secret'),
    access_token_key    = config.get('Twitter', 'access_token_key'),
    access_token_secret = config.get('Twitter', 'access_token_secret')
)


def main():
    if(opt.debug):
        print "Used configuration file(s): %s" % used_config
        print
        print "Will unfav all tweets older than %d days." % opt.time
        print

    # get maximum number of favorited tweets
    favs = api.GetFavorites(count=200, include_entities=False)

    for fav in favs:
        if opt.debug:
            print fav.id
            print fav.text
            print fav.created_at

        # parse date of tweet
        fav_date = datetime.datetime.fromtimestamp(time.mktime(time.strptime(fav.created_at, "%a %b %d %H:%M:%S +0000 %Y")))
        
        if opt.debug:
            print (datetime.datetime.today() - fav_date).days
            print
        
        # check if tweet is older than X days
        if((datetime.datetime.today() - fav_date).days > opt.time):
            # check all, because we don't trust Twitter to return list sorted
            if opt.debug:
                print "Unfav %i\n" % fav.id

            # unfav tweet
            api.DestroyFavorite(id=fav.id)


if __name__ == '__main__':
    main()
