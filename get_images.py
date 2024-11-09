# -*- coding: utf-8 -*-
"""
Created on Sat Nov  9 12:09:10 2024

@author: setat
"""

import pandas as pd
import requests
import re
import time
import json
import random

#%% Get data

imgs = pd.read_csv('AmendedData\\image_locations.csv', header=None,
                   encoding='utf-8')
imgs.columns = ['name', 'url']
print(imgs.head())

#%% Extract image locations

imgs['filename'] = None

for i in imgs.index:
    url = imgs.loc[i, 'url']
    # Get filename
    file_rgx = re.search(r'/([\w\._-]+[.](jpg|gif|png))$', url)
    filename = file_rgx.group(1)
    imgs.loc[i, 'filename'] = filename

print(f"Unique image URLs: {len(imgs['filename'].unique())}")
# N.B. there are more rows in imgs than there are images, because some are shared

#%% Use duplicate images to de-dupe names

# Get all the duplicate rows
dupes = imgs[imgs['filename'].duplicated(keep=False)].sort_values('filename')

# Want to uniquely grab one => get the lengths of each row, keep longest
dupes['length'] = dupes['name'].str.len()

# Loop through, make a dict to replace names
remove_dupes = {}
for fn in imgs.loc[imgs['filename'].duplicated(), 'filename'].unique():
    # Get the subset for a given filename
    slc = dupes.loc[dupes['filename'] == fn, ['name', 'length']].copy()
    max_len = slc['length'].max()
    not_longest = []
    longest = []
    for i in slc.index:
        row_len = slc.loc[i, 'length']
        row_name = slc.loc[i, 'name']
        if (row_len==max_len) and len(longest)==0:
            longest.append(row_name)
        else:
            not_longest.append(row_name)
    assert len(longest) == 1
    for i in not_longest:
        remove_dupes[i] = longest[0]

#%% Grab images from URLs

pause_counter = 0
total_counter = 0
for i, row in imgs.iterrows():
    # Make new file path
    fp = f'AmendedData\\imgs\\{row["filename"]}'
    # Grab file, save locally
    with open(fp, 'wb') as f:
        response = requests.get(row["url"])
        f.write(response.content)
    pause_counter += 1
    total_counter += 1
    if pause_counter == 5:
        pause_counter = 0
        time.sleep(1)
        print(f'{total_counter} complete...')

#%% Use dupes to dedupe core files: recipe_weights

with open('AmendedData\\recipe_weights.json', 'r', encoding='utf-8') as f:
    recipe_weights = json.load(f)

recipe_weights_cleaned = {}
for t_orig, w_orig in recipe_weights.items():
    if t_orig not in remove_dupes.keys():
        recipe_weights_cleaned.setdefault(t_orig, 0)
        recipe_weights_cleaned[t_orig] += w_orig
    else:
        recipe_weights_cleaned.setdefault(remove_dupes[t_orig], 0)
        recipe_weights_cleaned[remove_dupes[t_orig]] += w_orig

# They should total the same
assert sum(recipe_weights.values()) == sum(recipe_weights_cleaned.values())

#%% Use dupes to dedupe core files: imgs

imgs_clean = imgs.copy()
imgs_clean['drop'] = imgs_clean['name'].isin(remove_dupes.keys())
imgs_clean = imgs_clean[~imgs_clean['drop']].copy()  # drop any rows with title in cleaner file
imgs_clean.drop('drop', inplace=True, axis=1)

#%% Check there's nothing in one but not the other

weights_names = set(recipe_weights_cleaned.keys())
imgs_names = set(imgs_clean['name'].values)
assert weights_names == imgs_names
# assert len(weights_names.symmetric_difference(imgs_names)) == 0
# assert len(imgs_names.symmetric_difference(weights_names)) == 0

#%% Overwrite with cleaned files

imgs_clean.to_csv('AmendedData\\image_locations.csv', encoding='utf-8',
                  header=False, index=False)

with open('AmendedData\\recipe_weights.json', 'w', encoding='utf-8') as f:
    json.dump(recipe_weights_cleaned, f, ensure_ascii=False, indent=4)

#%% Check image look-up works

img_lookup = {t:f for t, f in imgs_clean[['name', 'filename']].values}

sample = 10
keys = random.sample(list(recipe_weights_cleaned), sample)
values = [recipe_weights_cleaned[k] for k in keys]
recipe_sample = dict(zip(keys, values))
for t, w in recipe_sample.items():
    i = img_lookup[t]
    print(f'Title: {t}\nWeight: {w}\nImg: {i}\n')

#%% Make merged dict

recipe_lookup = {}

for t, w in recipe_weights.items():
    i = img_lookup[t]
    recipe_lookup[t] = {'weight': w, 'img': i}

with open('AmendedData\\recipe_lookup.json', 'w', encoding='utf-8') as f:
    json.dump(recipe_lookup, f, ensure_ascii=False, indent=4)