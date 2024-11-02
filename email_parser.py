# -*- coding: utf-8 -*-
"""
Created on Sat Nov  2 14:43:33 2024

@author: setat
"""

import email
from os import listdir
from os.path import isfile, join
import re
from collections import Counter

#%% Get list off emails

folder = 'RawData\\mails'

onlyfiles = [f for f in listdir(folder) if isfile(join(folder, f))]

#%% Grab the email bodys

bodies = []

for f in onlyfiles:
    fp = f'RawData\\mails\\{f}'
    
    with open(fp, 'r') as f:
        msg = email.message_from_file(f)
    
    body = ""
    
    if msg.is_multipart():
        for part in msg.walk():
            ctype = part.get_content_type()
            cdispo = str(part.get('Content-Disposition'))
    
            # skip any text/plain (txt) attachments
            if ctype == 'text/plain' and 'attachment' not in cdispo:
                body = part.get_payload(decode=True)  # decode
                break
    # not multipart - i.e. plain text, no attachments, keeping fingers crossed
    else:
        body = msg.get_payload(decode=True)
    bodies.append(body)

#%% Parse email

body_cleaned = []

for body in bodies:
    b = body.decode("utf-8")
    b = b.replace('\xad', '')
    b = b.replace('\u00ad', '')
    b = b.replace('\N{SOFT HYPHEN}', '')
    b = b.replace('\u200c', '')
    # bodys = bodys.replace('\n\n', '\n')
    # bodys = re.sub('\n\s+\n', '\n', bodys)
    # bodys = re.sub(r'\s{5,}', '    ', bodys)
    body_cleaned.append(b)

#%% Get relevant lines

# lines = bodys.split('\n')
# dupes = [k for k,v in Counter(lines).items() if v>1]
# dupes = [i for i in dupes if not re.search(r'^(\s+)?$', i)]

# Meat-Free --> Meat Free
# Remove ’'- 
# lower case 'with'
# BBQ

for i, b in enumerate(body_cleaned):
    lines = b.split('\n')
    title = [s for s in lines if s.istitle()]
    title = list(set(title))
    drop_strings = ['Google Play', 'Total: ', 'App Store', '©', 'Inc.',
                    'Box Price', 'Hi Sami', 'Your Gousto Team']
    # https://www.geeksforgeeks.org/python-filter-a-list-based-on-the-given-list-of-strings/
    title_clean = [b for b in title if all(a not in b for a in drop_strings)]
    if len(title_clean) != 4:
        print(i, title_clean)