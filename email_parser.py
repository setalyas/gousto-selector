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
from bs4 import BeautifulSoup
import csv
import json

#%% Get list off emails

folder = 'RawData\\mails'

onlyfiles = [f for f in listdir(folder) if isfile(join(folder, f))]

#%% Grab the email bodys

bodies = []

for i, f in enumerate(onlyfiles):
    fp = f'RawData\\mails\\{f}'
    
    with open(fp, 'r') as f:
        msg = email.message_from_file(f)
    
    body_html = ""
    body_txt = ""

    # if not msg.is_multipart():
    #     print("Not multipart")
    
    if msg.is_multipart():
        for part in msg.walk():
            ctype = part.get_content_type()
            cdispo = str(part.get('Content-Disposition'))
            # print(ctype)
            # print(cdispo)
    
            # skip any text/plain (txt) attachments
            if ctype == 'text/plain' and 'attachment' not in cdispo:
                body_txt = part.get_payload(decode=True)  # decode
                # break
            if ctype == 'text/html' and 'attachment' not in cdispo:
                body_html = part.get_payload(decode=True)  # decode

    # not multipart - i.e. plain text, no attachments, keeping fingers crossed
    # else:
    #     body = msg.get_payload(decode=True)
    
    # Get the date
    date_str = email.utils.parsedate_to_datetime(msg['date']).strftime('%Y-%m-%d')
    print(f'{i}: {date_str}')
    
    # Store
    bodies.append((date_str, body_txt, body_html))

bodies.pop(128)  # Accidentally booked a 2-meal box!

# with open('AmendedData\\email.html', "w", encoding="utf-8") as fp:
#     email_html = body.decode('utf-8')
#     fp.write(email_html)
    # soup = BeautifulSoup(email_html, 'html.parser')
    # soup.find('img', alt='Marmite Teriyaki Tofu With Edamame Rice')

#%% Parse email

def year_swap(d, year):
    return dt.datetime(year, d.month, d.day)

body_cleaned = {}

for el in bodies:
    send_date = el[0]
    body_txt = el[1]
    body_html = el[2]
    # Decode the plain-text version, clean up
    b = body_txt.decode("utf-8")
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
    date_str = delivery_date.strftime('%Y-%m-%d')
    
    # Decode the HTML version (don't clean yet)
    h = body_html.decode("utf-8")
    with open(f'AmendedData\\{date_str}.html', "w", encoding="utf-8") as fp:
        fp.write(h)
    
    body_cleaned[date_str] = {'text': b, 'html': h}


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

for d, dct in body_cleaned.items():
    # Need to clean them up to be able to detect the titles *only* (to avoid false positives)
    txt = dct['text']
    lines = txt.split('\n')
    selected_lines = {}
    for i, line in enumerate(lines):
        # Remove trip hazards
        clean_line = line
        for k, v in replacers.items():
            clean_line = clean_line.replace(k, v)
        if clean_line.istitle():
            selected_lines[i] = {'original': line, 'clean': clean_line}
    # Remove tricks - https://www.geeksforgeeks.org/python-filter-a-list-based-on-the-given-list-of-strings/
    drop_strings = ['Google Play', 'Total: ', 'App Store', '©', 'Inc.',
                    'Box Price', 'Hi Sami', 'Your Gousto Team']
    selected_lines = {k: v for k,v in selected_lines.items() if all(a not in v['clean'] for a in drop_strings)}
    # print(selected_lines)
    # This should now be only the title lines - but duplicated still
    # Take only the titles, dedupe with mapping from unclean to clean
    name_lines = {}
    for l in selected_lines.values():
        name_lines[l['original']] = l['clean']
    if len(name_lines) != 4 and len(name_lines) != 5:
        print(d, name_lines.values())
        counter += 1
    titles[d] = name_lines

print(f'{counter} weeks with issues')

#%% Get the images

imgs = {}

for d, dct in body_cleaned.items():
    rich = dct['html']
    soup = BeautifulSoup(rich, 'html.parser')
    name_map = titles[d]
    for original, clean in name_map.items():
        recip_img = soup.find('img', alt=original)
        imgs[original] = recip_img['src']

# Save the list
with open('AmendedData\\image_locations.csv','w', newline='') as f:
    w = csv.writer(f)
    w.writerows(imgs.items())

#%% Make weights using date

# Unweighted list
mega_list = [t for t_dict in titles.values() for t in t_dict.keys()]

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

recipe_list = random.choices(list(recipe_weights.keys()),
                             weights=list(recipe_weights.values()),
                             k=3)

# print(recipe_list)
print('\n'.join([f'- {a}' for a in recipe_list]))

#%% Export data

with open('AmendedData\\recipe_weights.json', 'w', encoding='utf-8') as f:
    json.dump(recipe_weights, f, ensure_ascii=False, indent=4)
