workdir = r'D:\GitDown\brainout-content\packages\base\smart\Player Skins'

import os

localizeids = {}

for skin_folder in os.listdir(workdir):
    path2files = os.path.join(workdir, skin_folder)

    with open(os.path.join(path2files,'Skin.txt')) as f:
        for line in f.readlines():
            if line.startswith('data'):
                temp_data = line[line.find('=',) + 1:]
            elif line.startswith('name'):
                temp_name = line[line.find('=',) + 1:]
        localizeids.setdefault(temp_name.strip(), []).append(temp_data.strip())
        # localizeids[temp_name.strip()] = temp_data.strip()

import json
with open('localize_ids.json', 'w', encoding="utf-8") as f:
    json.dump(localizeids, f, indent=4, ensure_ascii=False)