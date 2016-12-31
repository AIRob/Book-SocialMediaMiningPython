#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 30 16:11:11 2016

@author: megan

based on code from Marco Bonzanini:

https://github.com/bonzanini/Book-SocialMediaMiningPython/tree/master/Chap04
Chap04/facebook_get_page_posts.py & facebook_top_posts.py
"""

import json
from argparse import ArgumentParser
import facebook
import requests

token = 'PUT TOKEN HERE'

who = 'ALAMANCEOURS'
urlstem = 'https://www.facebook.com/' + who + '/posts/'
fname = 'posts_' + who + ".jsonl"


def get_parser():
    parser = ArgumentParser()
    parser.add_argument('--page')
    parser.add_argument('--n', default=1000, type=int)
    return parser


parser = get_parser()
args = parser.parse_args()

graph = facebook.GraphAPI(token)
all_fields = [
    'id',
    'message',
    'created_time',
    'shares',
    'likes.summary(true)',
    'comments.summary(true)'
]
all_fields = ','.join(all_fields)
posts = graph.get_connections(who, 'posts', fields=all_fields)

# save FB stuff into a JSON file
downloaded = 0
while True:  # keep paginating
    if downloaded >= args.n:
        break
    try:
        with open(fname, 'a') as f:
            for post in posts['data']:
                downloaded += 1
                f.write(json.dumps(post)+"\n")
            # get next page
            posts = requests.get(posts['paging']['next']).json()
    except KeyError:
        # no more pages, break the loop
        break
