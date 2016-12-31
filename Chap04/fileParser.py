#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 30 16:11:11 2016

@author: megan

based on code from here:

https://github.com/bonzanini/Book-SocialMediaMiningPython/tree/master/Chap04
Chap04/facebook_get_page_posts.py & facebook_top_posts.py
"""

import json
import unicodecsv

outfile = 'out.csv'
who = 'PUT FACEBOOK NAME HERE'
urlstem = 'https://www.facebook.com/' + who + '/posts/'
fname = 'posts_' + who + ".jsonl"

# open file
all_posts = []
with open(fname) as f:
    for line in f:
        post = json.loads(line)
        n_likes = post['likes']['summary']['total_count']
        n_comments = post['comments']['summary']['total_count']
        try:
            n_shares = post['shares']['count']
        except KeyError:
            n_shares = 0
        post['all_interactions'] = n_likes + n_shares + n_comments
        all_posts.append(post)
most_liked_all = sorted(all_posts,
                        key=lambda x: x['all_interactions'],
                        reverse=True)
most_liked = most_liked_all[0]

# create a CSV file
outputFile = open(outfile, 'wb')
outputWriter = unicodecsv.writer(outputFile)
# write header row
outputWriter.writerow(['id',
                       'url',
                       'created',
                       'likes',
                       'shares',
                       'interactions',
                       'message'])
for post in most_liked_all:
    postid = post['id']
    hyphenToEnd = postid.find('_')
    url = urlstem + postid[hyphenToEnd+1:]

    created = post['created_time']
    n_likes = post['likes']['summary']['total_count']
    try:
        n_shares = post['shares']['count']
    except KeyError:
        n_shares = 0
    n_interactions = post['all_interactions']
    n_comments = post['comments']['summary']['total_count']

    try:
        message = post['message']
    except:
        message = ''
    outputWriter.writerow([postid,
                           url,
                           created,
                           n_likes,
                           n_shares,
                           n_interactions,
                           message])
outputFile.close()
