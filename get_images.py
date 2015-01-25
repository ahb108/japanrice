# -*- coding: utf-8 -*-

# This file is part of PyBOSSA.
#
# PyBOSSA is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PyBOSSA is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with PyBOSSA.  If not, see <http://www.gnu.org/licenses/>.

import urllib
import urllib2
import re
import json
import string
import requests
try:
    import config
except:
    print "You need to create a config.py file (see config.py.template)"

def get_flickr_set_photos(set_id):
    """Get public photos from a Flickr set_id and return a list."""
    url = 'https://api.flickr.com/services/rest/'
    page = 1
    payload = dict(
        method='flickr.photosets.getPhotos',
        api_key=config.flickr_api_key,
        photoset_id=set_id,
        extras='original_format',
        format='json',
        page=page,
        nojsoncallback=1)

    # Get the first batch of photos in the the photoset
    res = requests.get(url, params=payload)
    # Convert it to JSON
    data = json.loads(res.text)
    # Initiate the list of photos to return
    photos = []
    # If there are no errors, then proceed
    if res.status_code == 200 and 'photoset' in data.keys():
        # Get the owner name to create the photo link page
        owner_name = data['photoset']['ownername']
        # Get the total number of photos in this set
        n_photos = int(data['photoset']['total'])
        # Use a while loop for looping through all the available photos
        # in the set. By default Flickr returns 500 pictures per page
        while 'photoset' in data.keys():
            for photo in data['photoset']['photo']:
                direct_link = "https://farm%s.staticflickr.com/%s/%s_%s" % (
                    photo['farm'], photo['server'],
                    photo['id'], photo['secret'])
                original_link = "https://farm%s.staticflickr.com/%s/%s_%s" % (
                    photo['farm'], photo['server'],
                    photo['id'], photo['originalsecret'])
                link = 'https://www.flickr.com/photos/%s/%s' % (
                    owner_name, photo['id'])
                tmp = dict(url_m=direct_link + "_m.jpg",
                           url_o=original_link + "_o.jpg",
                           link=link + "/sizes/l/")
                photos.append(tmp)
            payload['page'] += 1
            res = requests.get(url, params=payload)
            data = json.loads(res.text)
        if len(photos) == n_photos:
            return photos
        else:
            print "Something went wrong! Different number of photos %s != %s" % (len(photos), n_photos)
            return []
    else:
        print "Something went wrong"
        print "ERROR: [%s]: %s" % (res.status_code, res.text)
