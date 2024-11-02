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
import datetime as dt

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
    
    # Get the date
    date_str = email.utils.parsedate_to_datetime(msg['date']).strftime('%Y-%m-%d')
    print(f'{i}: {date_str}')
    
    # Store
    bodies.append((body, date_str))

bodies.pop(128)  # Accidentally booked a 2-meal box!

#%% Parse email

def year_swap(d, year):
    return dt.datetime(year, d.month, d.day)

body_cleaned = {}

for el in bodies:
    body = el[0]
    send_date = el[1]
    b = body.decode("utf-8")
    b = b.replace('\xad', '')
    b = b.replace('\u00ad', '')
    b = b.replace('\N{SOFT HYPHEN}', '')
    b = b.replace('\u200c', '')
    # bodys = bodys.replace('\n\n', '\n')
    # bodys = re.sub('\n\s+\n', '\n', bodys)
    # bodys = re.sub(r'\s{5,}', '    ', bodys)
    # body_cleaned.append(b)
    
    # Get the delivery date
    b_oneline = b.replace('\n', ' ')
    b_oneline = b_oneline.replace('  ', ' ')
    date_str_rgx = r"(delivered|arriving) on ([\w]+ \d{1,2}(rd|st|nd|th)?([\s]?[\d]{4})?[\s]?[\w]+)"
    date_surround = re.search(date_str_rgx, b_oneline).group(2)
    parsed_date = dparser.parse(date_surround, fuzzy=True)
    # delivery_date = year_swap(parsed_date, int(send_date[:4]))
    # print(send_date, delivery_date.strftime('%Y-%m-%d'))
    delivery_date = None
    for year in range(2019, 2024+1):
        delivery_option = year_swap(parsed_date, year)
        diff = (dparser.parse(send_date) - delivery_option).days
        if abs(diff) < 50:
            delivery_date = delivery_option
    # print(send_date, delivery_date.strftime('%Y-%m-%d'))
    body_cleaned[delivery_date.strftime('%Y-%m-%d')] = b

#%% Get relevant lines

# lines = bodys.split('\n')
# dupes = [k for k,v in Counter(lines).items() if v>1]
# dupes = [i for i in dupes if not re.search(r'^(\s+)?$', i)]

counter = 0

titles = {}

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

for d, b in body_cleaned.items():
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
        print(d, title_clean)
        counter += 1
    titles[d] = title_clean

print(f'{counter} weeks with issues')

#%% Make weights using date

# Unweighted list
mega_list = [t for t_list in titles.values() for t in t_list]

# Weighted by frequency
recipes = dict((k, {'count': mega_list.count(k)}) for k in set(mega_list))

# Get most recent date
min_date = min(titles.keys())
for r in recipes.keys():
    date_list = [d for d in titles.keys() if r in titles[d]]
    max_date = max(date_list)
    recipes[r]['dates'] = date_list
    recipes[r]['max'] = max_date
    recipes[r]['distance'] = (dparser.parse(max_date) - dparser.parse(min_date)).days

#%% Get random meal

recipe_weights = {k: v['distance'] for k, v in recipes.items()}

random.choices(list(recipe_weights.keys()),
               weights=list(recipe_weights.values()),
               k=10)
