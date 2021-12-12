skin_name = input()

import json
with open("localize_skin_ids.json", "r", encoding="utf-8") as f:
    localize_skin_ids = json.load(f)

founded_skin_id = None
for skin_id, utf_names in localize_skin_ids.items():
    if skin_name.casefold() in utf_names:
        print(skin_id)
        founded_skin_id = skin_id
        break

with open("localize_ids.json", "r", encoding="utf-8") as f:
    localize_ids = json.load(f)

import random
print(localize_ids[founded_skin_id])
filename = 'actor-' + localize_ids[founded_skin_id][0] + '.png' if len(localize_ids[founded_skin_id]) == 1 else 'actor-' + random.choice(localize_ids[founded_skin_id]) + '.png'

print(filename)
workdir = r'C:\Users\levmi\Desktop\uniforms_2k'

from PIL import Image  
import os                                                                              
img = Image.open(os.path.join(workdir, filename))
img.show() 