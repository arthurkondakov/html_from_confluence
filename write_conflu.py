#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import requests

def get_page_ancestors(auth, headers, endpoint, pageid):

    # Get basic page information plus the ancestors property

    url = '{endpoint}/{pageid}?expand=ancestors'.format(endpoint = endpoint, pageid = pageid)

    r = requests.get(url, headers=headers, auth=auth)

    r.raise_for_status()

    return r.json()['ancestors']


def get_page_info(auth, headers, endpoint, pageid):

    # Get basic page information plus the ancestors property

    url = '{endpoint}/{pageid}'.format(endpoint = endpoint, pageid = pageid)

    r = requests.get(url, headers=headers, auth=auth)

    # r.raise_for_status()

    return r.json()


def write_data(auth, headers, endpoint, pageid, html, title = None):

    info = get_page_info(auth, headers, endpoint, pageid)

    ver = int(info['version']['number']) + 1

    ancestors = get_page_ancestors(auth, headers, endpoint, pageid)

    anc = ancestors[-1]
    del anc['_links']
    del anc['_expandable']
    del anc['extensions']

    if title is not None:
        info['title'] = title

    data = {
        'id' : str(pageid),
        'type' : 'page',
        'title' : info['title'],
        'version' : {'number' : ver},
        'ancestors' : [anc],
        'body'  : {
            'storage' :
            {
                'representation' : 'storage',
                'value' : str(html),
            }
        }
    }

    data = json.dumps(data)

    url = '{endpoint}/{pageid}'.format(endpoint = endpoint, pageid = pageid)

    r = requests.put(
        url,
        data = data,
        auth = auth,
        headers = headers
    )

    r.raise_for_status()

    print("Wrote '%s' version %d" % (info['title'], ver))

def write_data(auth, headers, endpoint, pageid, html, title = None):

    info = get_page_info(auth, headers, endpoint, pageid)

    ver = int(info['version']['number']) + 1

    ancestors = get_page_ancestors(auth, headers, endpoint, pageid)

    anc = ancestors[-1]
    del anc['_links']
    del anc['_expandable']
    del anc['extensions']

    if title is not None:
        info['title'] = title

    data = {
        'id' : str(pageid),
        'type' : 'page',
        'title' : info['title'],
        'version' : {'number' : ver},
        'ancestors' : [anc],
        'body'  : {
            'storage' :
            {
                'representation' : 'storage',
                'value' : str(html),
            }
        }
    }

    data = json.dumps(data)

    url = '{endpoint}/{pageid}'.format(endpoint = endpoint, pageid = pageid)

    r = requests.put(
        url,
        data = data,
        auth = auth,
        headers = headers
    )

    r.raise_for_status()

    print("Wrote '%s' version %d" % (info['title'], ver))