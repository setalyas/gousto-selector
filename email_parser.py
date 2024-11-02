# -*- coding: utf-8 -*-
"""
Created on Sat Nov  2 14:43:33 2024

@author: setat
"""

import email
from os import listdir
from os.path import isfile, join
import re
import random
import dateutil.parser as dparser

#%% Get list off emails

folder = 'RawData\\mails'

onlyfiles = [f for f in listdir(folder) if isfile(join(folder, f))]

#%% Grab the email bodys

bodies = []

for i, f in enumerate(onlyfiles):
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
    date_str = email.utils.parsedate_to_datetime(msg['date']).strftime('%Y-%m-%d')
    print(f'{i}: {date_str}')

bodies.pop(128)  # Accidentally booked a 2-meal box!

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

counter = 0

titles = []

replacers = {'’': '',
             "'": '',
             " with": " With ",
             " x ": " X ",
             "BBQ": "Bbq",
             "DIY": "Diy",
             "TABASCO®": "Tabasco",
             " (DF)": "",
             "Squash-age": "Squashage",
             "Peri-nnaise": "Perinnaise",
             "Meat-free": "Meat-Free"}

for i, b in enumerate(body_cleaned):
    lines = b.split('\n')
    # Remove trip hazards
    for k, v in replacers.items():
        lines = [s.replace(k, v) for s in lines]
    title = [s for s in lines if s.istitle()]
    title = list(set(title))
    drop_strings = ['Google Play', 'Total: ', 'App Store', '©', 'Inc.',
                    'Box Price', 'Hi Sami', 'Your Gousto Team']
    # https://www.geeksforgeeks.org/python-filter-a-list-based-on-the-given-list-of-strings/
    title_clean = [b for b in title if all(a not in b for a in drop_strings)]
    if len(title_clean) != 4 and len(title_clean) != 5:
        print(i, title_clean)
        counter += 1
    titles.append(title_clean)

print(f'{counter} weeks with issues')

mega_list = [t for t_list in titles for t in t_list]

#%% Get random meal

random.choices(mega_list, k=10)
