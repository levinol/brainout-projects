import json

with open("brain-out-content-bundle.json", "r", encoding="utf-8") as f:
    localizejson = json.load(f)


localize_skin_ids = {}
for language in localizejson.keys():
    for key, value in localizejson[language].items():
        if key.startswith('ITEM_PLAYER_SKIN_'):
            if value:
                localize_skin_ids.setdefault(key, []).append(value.casefold())

with open('localize_skin_ids.json', 'w', encoding="utf-8") as f:
    json.dump(localize_skin_ids, f, indent=4, ensure_ascii=False)