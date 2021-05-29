import os
path = r'D:\gitdown\brainout-content\packages\base\smart\Weapons\r8'

upgrade_dict = {}
upgrade_path = ''
obtain_method = ''
bullet = ''
amount = 0
name = ''
gl_flag = 0


default_dict = {
    'accuracy': [0],
    'damage': [0],
    'recoil': [0],
    'reloadTime': [0],
    'clipSize': [0],
    'allowedBullets': [''],
    'fire-rate': [0],
    'aimDistance': [0],
    'silenced': [False],
    'shootModes': [''],
    'wear': [0],
    'speed-coef': [1],
    'weight': [0]
}

for entry in os.listdir(path):
    new_path = os.path.join(path, entry)
    if os.path.isdir(new_path):
        if entry == 'Upgrades':
            upgrade_path = new_path
    elif os.path.isfile(os.path.join(path, entry)):
        if entry == 'Store Item.txt':
            with open(new_path) as f:
                lines = f.readlines()
                amount_flag = 0
                upgrade_flag = 0
                hide_tree_flag = 0
                for i, itr_str in enumerate(lines):
                    temp_str = itr_str.strip()
                    if temp_str.startswith('upgrades'):
                        upgrade_flag = 1
                    elif upgrade_flag:
                        if temp_str.startswith('}'):
                            upgrade_flag = 0
                        else:
                            upgrade_dict[temp_str[:temp_str.index('=')].rstrip()] = temp_str[temp_str.index('=')+1:].lstrip().split(',')
                    elif temp_str.startswith('amount'):
                        amount_flag = i
                        amount = temp_str[temp_str.index('=')+1:]
                    elif temp_str.startswith('id'):
                        if amount_flag == i - 1 and amount_flag != 0:
                            bullet = temp_str[temp_str.index('=')+1:]
                        elif name == '':
                            name = temp_str[temp_str.index('=')+1:].strip()
                    elif temp_str.startswith('items') and amount_flag:
                        hide_tree_flag = i
                    elif hide_tree_flag:
                        if itr_str.startswith('}'):
                            obtain_method = ''.join(a.strip() for a in lines[hide_tree_flag+1:i])
                            hide_tree_flag = 0
        elif entry == 'Weapon.txt':
            with open(new_path) as f:
                lines = f.readlines()
                for i, itr_str in enumerate(lines):
                    temp_str = itr_str.strip()
                    if temp_str.startswith('wear'):
                        default_dict[temp_str[:temp_str.index('=')].rstrip()][0] = float(temp_str[temp_str.index('=')+1:].lstrip())
                    elif temp_str.startswith('weight'):
                        default_dict[temp_str[:temp_str.index('=')].rstrip()][0] = float(temp_str[temp_str.index('=')+1:].lstrip())
                    elif temp_str.startswith(tuple(default_dict.keys())):
                        if temp_str.startswith('allowedBullets') or temp_str.startswith('shootModes'):
                            default_dict[temp_str[:temp_str.index('=')].rstrip()][0] = temp_str[temp_str.index('=')+1:].lstrip().split(',')
                        elif temp_str.startswith('silenced'):
                            default_dict[temp_str[:temp_str.index('=')].rstrip()][0] = temp_str[temp_str.index('=')+1:].lstrip()
                        else:
                            default_dict[temp_str[:temp_str.index('=')].rstrip()][0] = float(temp_str[temp_str.index('=')+1:])

connect = {'accuracy': 'Accuracy.txt',
          'recoil': 'Recoil.txt', 
          'reload-time' : 'Reload Time.txt',
          'shoot-time': 'Shoot Time.txt',
          'wear-resistance': 'Wear Resistance.txt'}

details_arr = [connect[i] for i in set(connect)&set(upgrade_dict)]

details_dict = {
    'accuracy': 0,
    'recoil': 0,
    'reloadTime': 0,
    'fire-rate': 0,
    'wear': 0
}

upgrade_flag = 0
for value in upgrade_dict.values():
    if len(value) > 1:
        upgrade_flag = 1
        break

upgrade_final_str = '{{Улучшения11|'
upgrade_names = ['No modifications']
dumb_upgrade_flag = 0
dumb_temp_str = ''

for entry in os.listdir(upgrade_path):
    new_path = os.path.join(upgrade_path, entry)
    if entry in details_arr:
        with open(new_path) as f:
            lines = f.readlines()
            for i, itr_str in enumerate(lines):
                temp_str = itr_str.strip()
                if temp_str.startswith('upgrades'):
                    if '[' not in temp_str:
                        count = int(itr_str.split('-')[-1])
                    else:
                        dumb_upgrade_flag = 1
                elif dumb_upgrade_flag == 1:
                    if ']' in temp_str:
                        dumb_upgrade_flag = 0
                        count =int(dumb_temp_str.split('-')[-1])
                    else:
                        dumb_temp_str = temp_str
            if entry == 'Accuracy.txt':
                details_dict['accuracy'] = count*2
                if count == 5:
                    upgrade_final_str += 'точность = 1|'
                else:
                    upgrade_final_str += 'точность2 = 1|'
            elif entry == 'Recoil.txt':
                details_dict['recoil'] = count*(-2)
                if count == 5:
                    upgrade_final_str += 'отдача = 1|'
                else:
                    upgrade_final_str += 'отдача2 = 1|'
            elif entry == 'Reload Time.txt':
                details_dict['reloadTime'] = count*(-0.05)
                if count == 5:
                    upgrade_final_str += 'перезарядка = 1|'
                else:
                    upgrade_final_str += 'перезарядка2 = 1|'
            elif entry == 'Shoot Time.txt':
                details_dict['fire-rate'] = count*(10)
                if count == 5:
                    upgrade_final_str += 'скорость_стрельбы = 1|'
                else:
                    upgrade_final_str += 'скорость_стрельбы2 = 1|'
            elif entry == 'Wear Resistance.txt':
                details_dict['wear'] = count*(50)
                if count == 5:
                    upgrade_final_str += 'износостойкость = 1|'
                else:
                    upgrade_final_str += 'износостойкость2 = 1|'
    else:
        if entry.lower().startswith('gl') or entry.lower().endswith('gl.txt'):
            gl_flag = 1
        else:
            temp_dict = {
                'accuracy': 0,
                'damage': 0,
                'recoil': 0,
                'reloadTime': 0,
                'clipSize': 0,
                'allowedBullets': '',
                'fire-rate': 0,
                'aimDistance': 0,
                'silenced': None,
                'shootModes': '',
                'wear': 0,
                'speed-coef': 0,
                'weight' : 0
            }
            upgrade_names.append(entry[:-4])
            with open(new_path) as f:
                lines = f.readlines()
                properties_flag = 0
                for i, itr_str in enumerate(lines):
                    temp_str = itr_str.strip()
                    if temp_str.startswith('properties'):
                        properties_flag = 1
                    elif properties_flag:
                        if temp_str.startswith('}'):
                            properties_flag = 0
                        else:
                            ind = temp_str.index('=')
                            left_str = temp_str[:ind].rstrip()
                            right_str = temp_str[ind+1:].replace('"','')
                            right_str = right_str.strip()
                            if left_str == 'aim-distance':
                                temp_dict['aimDistance'] = right_str
                            elif left_str == 'silent':
                                temp_dict['silenced'] = right_str
                            elif left_str == 'clip-size':
                                temp_dict['clipSize'] = right_str
                            elif left_str == 'shoot-modes':
                                temp_dict['shootModes'] = right_str
                            elif left_str == 'wear-resistance':
                                temp_dict['wear'] = right_str
                            elif left_str == 'reload-time':
                                temp_dict['reloadTime'] = right_str
                            elif left_str == 'bullet':
                                temp_dict['allowedBullets'] = right_str
                            else:
                                temp_dict[left_str] = right_str

            for key, value in temp_dict.items():
                if temp_dict[key]:
                    if key in ['allowedBullets', 'shootModes']:
                        if value[0] == '=':
                            default_dict[key].append(value[1:].split(','))
                        else: 
                            default_dict[key].append(value.split(','))
                    elif key == 'silenced':
                        default_dict[key].append(True)
                    else:                    
                        if value[0] == '=':
                            default_dict[key].append(float(value[1:]))
                        else:
                            default_dict[key].append(default_dict[key][0] + float(value))
                else:
                    if key == 'silenced':
                        default_dict[key].append(default_dict[key][0])
                    else:
                        default_dict[key].append(default_dict[key][0])    

maxed_dict = {}

for key, value in default_dict.items():
    if key == 'silenced':
        if True in value or 'true' in value:
            maxed_dict[key] = 1
        else:
            maxed_dict[key] = 0
    elif key in ['shootModes','allowedBullets']:
        if min(value) == max(value):
            maxed_dict[key] = 0
        else:
            maxed_dict[key] = 1
    elif key in 'damage':
        m = max(value)
        if m != value[0]:
            maxed_dict[key] = m
        else:
            mi = min(value)
            if mi == m:
                maxed_dict[key] = 0
            else:
                maxed_dict[key] = mi
    elif key in ['recoil', 'reloadTime', 'weight']:
        m = min(value)
        if key in ['recoil', 'reloadTime']:
            m += float(details_dict[key])
        if m != value[0]:
            maxed_dict[key] = m
        else:
            if max(value) == m:
                maxed_dict[key] = 0
            else:
                maxed_dict[key] = m
    elif key in ['accuracy', 'clipSize', 'aimDistance', 'fire-rate', 'speed-coef', 'wear']:
        m = max(value)
        if key in ['accuracy','fire-rate', 'wear']:
            m += float(details_dict[key])
        if m != value[0]:
            maxed_dict[key] = m
        else:
            if min(value) == m:
                maxed_dict[key] = 0
            else:
                maxed_dict[key] = m

bullet_arr = ['bullet-5.45x39', 'bullet-5.56x45', 'bullet-9mm-39', 'bullet-9mmx19', 'bullet-9mmx18', 'bullet-45acp', 'bullet-5.7x28', 'bullet-12.7x55', 'bullet-7.62x51', 'bullet-7.62x39',
 'bullet-338-Lapua', 'bullet-357-magnum', 'bullet-12-76', 'bullet-12-slug', 'bullet-9.3x74R', 'rpg7-bullet', 'grenade-bullet', 'm72law-bullet', 'arrow-bullet']

print('''{{Оружие инфобокс
|Заголовок =\n''')
for i in range(len(upgrade_names)):
    if i == 0:
        print('|Без модификаций изображение = ', name + '_' + upgrade_names[i].lower().replace(' ', '_')+'.png\n')
        print('|Способ получения = ', obtain_method)

        temp_damage = int(default_dict['damage'][i])
        max_damage = int(maxed_dict['damage'])
        if max_damage == 0:
            print('|Урон = ', temp_damage)
        elif max_damage > temp_damage:
            print('|Урон = ', temp_damage, '- <abbr title="Максимально возможное улучшение">',max_damage,'</abbr>')
        elif max_damage < temp_damage:
            print('|Урон = ', '<abbr title="Максимально возможное улучшение">',max_damage,'</abbr> - ', temp_damage)
        else:
            print('|Урон = ','<abbr title="Максимально возможное улучшение">', temp_damage, '</abbr> ')
        
        temp_fire_rate = int(default_dict['fire-rate'][i])
        max_fire_rate = int(maxed_dict['fire-rate'])
        if max_fire_rate == 0:
            print('|Скорострельность = ', temp_fire_rate)
        elif max_fire_rate > temp_fire_rate:
            print('|Скорострельность = ', temp_fire_rate,'- <abbr title="Максимально возможное улучшение">', max_fire_rate,'</abbr>')
        else:
            print('|Скорострельность = ','<abbr title="Максимально возможное улучшение">', temp_fire_rate,'</abbr>')
        
        temp_accuracy = int(default_dict['accuracy'][i])
        max_accuracy = int(maxed_dict['accuracy'])
        if max_accuracy == 0:
            print('|Точность = ', temp_accuracy)
        elif max_accuracy > temp_accuracy:
            print('|Точность = ', temp_accuracy,'- <abbr title="Максимально возможное улучшение">', max_accuracy,'</abbr>')
        else:
            print('|Точность = ','<abbr title="Максимально возможное улучшение">', temp_accuracy,'</abbr>')


        temp_recoil = int(default_dict['recoil'][i])
        max_recoil = int(maxed_dict['recoil'])
        if max_recoil == 0:
            print('|Отдача = ', temp_recoil)
        elif max_recoil < temp_recoil:
            print('|Отдача = ', '<abbr title="Максимально возможное улучшение">',max_recoil,'</abbr> - ', temp_recoil)
        else:
            print('|Отдача = ','<abbr title="Максимально возможное улучшение">', temp_recoil,'</abbr>')
        

        temp_reloadTime = default_dict['reloadTime'][i]
        max_reloadTime = maxed_dict['reloadTime']
        if max_reloadTime == 0:
            print('|Скорость перезарядки = ', temp_reloadTime)
        elif max_reloadTime < temp_reloadTime:
            print('|Скорость перезарядки = ', '<abbr title="Максимально возможное улучшение">',max_reloadTime,'</abbr> - ', temp_reloadTime)
        else:
            print('|Скорость перезарядки = ','<abbr title="Максимально возможное улучшение">', temp_reloadTime,'</abbr>')


        temp_clipSize = int(default_dict['clipSize'][i])
        max_clipSize = int(maxed_dict['clipSize'])
        if max_clipSize == 0:
            print('|Обойма = ', temp_clipSize)
        elif max_clipSize > temp_clipSize:
            print('|Обойма = ', temp_clipSize,'- <abbr title="Максимально возможное улучшение">', max_clipSize,'</abbr>')
        else:
            print('|Обойма = ','<abbr title="Максимально возможное улучшение">', temp_clipSize,'</abbr>')

        temp_bullet = default_dict['allowedBullets'][i][0]
        print('|Боеприпас = ', bullet_arr.index(temp_bullet) + 1)


        temp_wear = int(default_dict['wear'][i])
        max_wear = int(maxed_dict['wear'])
        if max_wear == 0:
            print('|Износостойкость = ', temp_wear)
        elif max_wear > temp_wear:
            print('|Износостойкость = ', temp_wear,'- <abbr title="Максимально возможное улучшение">', max_wear,'</abbr>')
        else:
            print('|Износостойкость = ','<abbr title="Максимально возможное улучшение">', temp_wear,'</abbr>')

        temp_aimDistance = int(default_dict['aimDistance'][i])
        max_aimDistance = int(maxed_dict['aimDistance'])
        if max_aimDistance == 0:
            print('|Дальность прицеливания = ', temp_aimDistance)
        elif max_aimDistance > temp_aimDistance:
            print('|Дальность прицеливания = ', temp_aimDistance,'- <abbr title="Максимально возможное улучшение">', max_aimDistance,'</abbr>')
        else:
            print('|Дальность прицеливания = ','<abbr title="Максимально возможное улучшение">', temp_aimDistance,'</abbr>')

        if gl_flag == 1:
            print('|Наличие гранатомёта = Есть возможность установки')
        
        temp_silencer = default_dict['silenced'][i]
        max_silencer = maxed_dict['silenced']
        if True == temp_silencer or 'true' == temp_silencer:
            print('|Наличие глушителя = <b>Установлен</b>')
        elif max_silencer == 1:
            print('|Наличие глушителя = Есть возможность установки')
        
        temp_weight = int(default_dict['weight'][i])
        max_weight = int(maxed_dict['weight'])
        if max_weight == 0:
            print('|Вес = ', temp_weight)
        elif max_weight < temp_weight:
            print('|Вес = ', '<abbr title="Максимально возможное улучшение">',max_weight,'</abbr> - ', temp_weight)
        else:
            print('|Вес = ','<abbr title="Максимально возможное улучшение">', temp_weight,'</abbr>')
        
        temp_shootModes = default_dict['shootModes'][i]
        shootmod_arr = []
        for mod in temp_shootModes:
            if 'auto' in mod:
                shootmod_arr.append('Автоматич.')
            elif 'single' in mod:
                shootmod_arr.append('Одиноч.')
            elif 'burst' in mod:
                shootmod_arr.append('Отсечка по три патрона')
            elif 'burst2' in mod:
                shootmod_arr.append('Отсечка по два патрона')
        print('|Режим стрельбы = ', '<br /><br />'.join(shootmod_arr))
        
        print('|Стандартный боезапас = ', amount)
        print('')
    else:
        print(f'|Модификация {i} название = ', upgrade_names[i])
        print(f'|Модификация {i} изображение = ', name + '_' + upgrade_names[i].lower().replace(' ', '_')+'.png\n') 
        print(f'|Способ получения {i} = ', obtain_method)

        temp_damage = int(default_dict['damage'][i])
        max_damage = int(maxed_dict['damage'])
        if max_damage == 0:
            print(f'|Урон {i} = ', temp_damage)
        elif temp_damage != default_dict['damage'][0]:
            if temp_damage == max_damage:
                print(f'|Урон {i} = ','<b>',temp_damage,'</b>')
            elif max_damage > temp_damage:
                print(f'|Урон {i} = ','<b>',temp_damage,'</b>', '- <abbr title="Максимально возможное улучшение">',max_damage,'</abbr>')
            elif max_damage < temp_damage:
                print(f'|Урон {i} = ', '<abbr title="Максимально возможное улучшение">',max_damage,'</abbr> - ', '<b>',temp_damage,'</b>')
            else:
                print(f'|Урон {i} = ', temp_damage)
        elif max_damage > temp_damage:
            print(f'|Урон {i} = ', temp_damage, '- <abbr title="Максимально возможное улучшение">',max_damage,'</abbr>')
        elif max_damage < temp_damage:
            print(f'|Урон {i} = ', '<abbr title="Максимально возможное улучшение">',max_damage,'</abbr> - ', temp_damage)
        else:
            print(f'|Урон {i} = ','<abbr title="Максимально возможное улучшение">', temp_damage, '</abbr> ')
        
        temp_fire_rate = int(default_dict['fire-rate'][i])
        max_fire_rate = int(maxed_dict['fire-rate'])
        if max_fire_rate == 0:
            print(f'|Скорострельность {i} = ', temp_fire_rate)
        elif temp_fire_rate != default_dict['fire-rate'][0]:
            if max_fire_rate == temp_fire_rate:
                print(f'|Скорострельность {i} = ', '<b>', temp_fire_rate,'</b>')
            elif max_fire_rate > temp_fire_rate:
                print(f'|Скорострельность {i} = ','<b>',temp_fire_rate,'</b>', '- <abbr title="Максимально возможное улучшение">',max_fire_rate,'</abbr>')
            else:
                print(f'|Скорострельность {i} = ', temp_fire_rate)
        elif max_fire_rate > temp_fire_rate:
            print(f'|Скорострельность {i} = ', temp_fire_rate,'- <abbr title="Максимально возможное улучшение">', max_fire_rate,'</abbr>')
        else:
            print(f'|Скорострельность {i} = ','<abbr title="Максимально возможное улучшение">', temp_fire_rate,'</abbr>')
        
        temp_accuracy = int(default_dict['accuracy'][i])
        max_accuracy = int(maxed_dict['accuracy'])
        if max_accuracy == 0:
            print(f'|Точность {i} = ', temp_accuracy)
        elif temp_accuracy != default_dict['accuracy'][0]:
            if max_accuracy == temp_accuracy:
                print(f'|Точность {i} = ', '<b>', temp_accuracy,'</b>')
            elif max_accuracy > temp_accuracy:
                print(f'|Точность {i} = ','<b>',temp_accuracy,'</b>', '- <abbr title="Максимально возможное улучшение">',max_accuracy,'</abbr>')
            else:
                print(f'|Точность {i} = ', temp_accuracy)
        elif max_accuracy > temp_accuracy:
            print(f'|Точность {i} = ', temp_accuracy,'- <abbr title="Максимально возможное улучшение">', max_accuracy,'</abbr>')
        else:
            print(f'|Точность {i} = ','<abbr title="Максимально возможное улучшение">', temp_accuracy,'</abbr>')


        temp_recoil = int(default_dict['recoil'][i])
        max_recoil = int(maxed_dict['recoil'])
        if max_recoil == 0:
            print(f'|Отдача {i} = ', temp_recoil)
        elif temp_recoil != default_dict['recoil'][0]:
            if max_recoil == temp_recoil:
                print(f'|Отдача {i} = ', '<b>', temp_recoil,'</b>')
            elif max_recoil < temp_recoil:
                print(f'|Отдача {i} = ', '<abbr title="Максимально возможное улучшение">',max_recoil,'</abbr> - ', '<b>', temp_recoil,'</b>')
            else:
                print(f'|Отдача {i} = ', temp_recoil)
        elif max_recoil < temp_recoil:
            print(f'|Отдача {i} = ', '<abbr title="Максимально возможное улучшение">',max_recoil,'</abbr> - ', temp_recoil)
        else:
            print(f'|Отдача {i} = ','<abbr title="Максимально возможное улучшение">', temp_recoil,'</abbr>')
        

        temp_reloadTime = default_dict['reloadTime'][i]
        max_reloadTime = maxed_dict['reloadTime']
        if max_reloadTime == 0:
            print(f'|Скорость перезарядки {i} = ', temp_reloadTime)
        elif temp_reloadTime != default_dict['reloadTime'][0]:
            if max_reloadTime == temp_reloadTime:
                print(f'|Скорость перезарядки {i} = ', '<b>', temp_reloadTime,'</b>')
            elif max_reloadTime < temp_reloadTime:
                print(f'|Скорость перезарядки {i} = ', '<abbr title="Максимально возможное улучшение">',max_reloadTime,'</abbr> - ', '<b>', temp_reloadTime,'</b>')
            else:
                print(f'|Скорость перезарядки {i} = ', temp_reloadTime)
        elif max_reloadTime < temp_reloadTime:
            print(f'|Скорость перезарядки {i} = ', '<abbr title="Максимально возможное улучшение">',max_reloadTime,'</abbr> - ', temp_reloadTime)
        else:
            print(f'|Скорость перезарядки {i} = ','<abbr title="Максимально возможное улучшение">', temp_reloadTime,'</abbr>')
        

        temp_clipSize = int(default_dict['clipSize'][i])
        max_clipSize = int(maxed_dict['clipSize'])
        if max_clipSize == 0:
            print(f'|Обойма {i} = ', temp_clipSize)
        elif temp_clipSize != default_dict['clipSize'][0]:
            if max_clipSize == temp_clipSize:
                print(f'|Обойма {i} = ', '<b>', temp_clipSize,'</b>')
            elif max_clipSize > temp_clipSize:
                print(f'|Обойма {i} = ','<b>',temp_clipSize,'</b>', '- <abbr title="Максимально возможное улучшение">',max_clipSize,'</abbr>')
            else:
                print(f'|Обойма {i} = ', temp_clipSize)
        elif max_clipSize > temp_clipSize:
            print(f'|Обойма {i} = ', temp_clipSize,'- <abbr title="Максимально возможное улучшение">', max_clipSize,'</abbr>')
        else:
            print(f'|Обойма {i} = ','<abbr title="Максимально возможное улучшение">', temp_clipSize,'</abbr>')

        temp_bullet = default_dict['allowedBullets'][i][0]
        print(f'|Боеприпас {i} = ', bullet_arr.index(temp_bullet) + 1)


        temp_wear = int(default_dict['wear'][i])
        max_wear = int(maxed_dict['wear'])
        if max_wear == 0:
            print(f'|Износостойкость {i} = ', temp_wear)
        elif temp_clipSize != default_dict['wear'][0]:
            if max_wear == temp_wear:
                print(f'|Износостойкость {i} = ', '<b>', temp_wear,'</b>')
            elif max_wear > temp_wear:
                print(f'|Износостойкость {i} = ','<b>',temp_wear,'</b>', '- <abbr title="Максимально возможное улучшение">',max_wear,'</abbr>')
            else:
                print(f'|Износостойкость {i} = ', temp_wear)
        elif max_wear > temp_wear:
            print(f'|Износостойкость {i} = ', temp_wear,'- <abbr title="Максимально возможное улучшение">', max_wear,'</abbr>')
        else:
            print(f'|Износостойкость {i} = ','<abbr title="Максимально возможное улучшение">', temp_wear,'</abbr>')

        
        temp_aimDistance = int(default_dict['aimDistance'][i])
        max_aimDistance = int(maxed_dict['aimDistance'])
        if max_aimDistance == 0:
            print(f'|Дальность прицеливания {i} = ', temp_aimDistance)
        elif temp_clipSize != default_dict['aimDistance'][0]:
            if max_aimDistance == temp_aimDistance:
                print(f'|Дальность прицеливания {i} = ', '<b>', temp_aimDistance,'</b>')
            elif max_aimDistance > temp_aimDistance:
                print(f'|Дальность прицеливания {i} = ','<b>',temp_aimDistance,'</b>', '- <abbr title="Максимально возможное улучшение">',max_aimDistance,'</abbr>')
            else:
                print(f'|Дальность прицеливания {i} = ', temp_aimDistance)
        elif max_aimDistance > temp_aimDistance:
            print(f'|Дальность прицеливания {i} = ', temp_aimDistance,'- <abbr title="Максимально возможное улучшение">', max_aimDistance,'</abbr>')
        else:
            print(f'|Дальность прицеливания {i} = ','<abbr title="Максимально возможное улучшение">', temp_aimDistance,'</abbr>')

        if gl_flag == 1:
            print(f'|Наличие гранатомёта {i} = Есть возможность установки')
        
        temp_silencer = default_dict['silenced'][i]
        max_silencer = maxed_dict['silenced']
        if True == temp_silencer or 'true' == temp_silencer:
            print(f'|Наличие глушителя {i} = <b>Установлен</b>')
        elif max_silencer == 1:
            print(f'|Наличие глушителя {i} = Есть возможность установки')


        temp_weight = int(default_dict['weight'][i])
        max_weight = int(maxed_dict['weight'])
        if max_weight == 0:
            print(f'|Вес {i} = ', temp_weight)
        elif temp_weight != default_dict['weight'][0]:
            if max_weight == temp_weight:
                print(f'|Вес {i} = ', '<b>', temp_weight,'</b>')
            elif max_weight < temp_weight:
                print(f'|Вес {i} = ', '<abbr title="Максимально возможное улучшение">',max_weight,'</abbr> - ', '<b>', temp_weight,'</b>')
            else:
                print(f'|Вес {i} = ', temp_weight)
        elif max_weight < temp_weight:
            print(f'|Вес {i} = ', '<abbr title="Максимально возможное улучшение">',max_weight,'</abbr> - ', temp_weight)
        else:
            print(f'|Вес {i} = ','<abbr title="Максимально возможное улучшение">', temp_weight,'</abbr>')

        temp_shootModes = default_dict['shootModes'][i]
        shootmod_arr = []
        for mod in temp_shootModes:
            if 'auto' in mod:
                shootmod_arr.append('Автоматич.')
            elif 'single' in mod:
                shootmod_arr.append('Одиноч.')
            elif 'burst' in mod:
                shootmod_arr.append('Отсечка по три патрона')
            elif 'burst2' in mod:
                shootmod_arr.append('Отсечка по два патрона')
        print(f'|Режим стрельбы {i} = ', '<br /><br />'.join(shootmod_arr))

        print(f'|Стандартный боезапас {i} = ', amount)

        print('')
    
if upgrade_flag == 1:
    print('}}')
else:
    i += 1
    print(f'|Модификация {i} название = All mods')
    print(f'|Модификация {i} изображение = ', name + '_' + 'all_mods.png\n') 
    print(f'|Способ получения {i} = ', obtain_method)
    if int(maxed_dict['damage']) != 0:
        print(f'|Урон {i} = ', int(maxed_dict['damage']))
    else:
        print(f'|Урон {i} = ', int(default_dict['damage'][0]))
    
    if int(maxed_dict['fire-rate']) != 0:
        if details_dict['fire-rate'] != 0:
            print(f'|Скорострельность {i} = ', int(maxed_dict['fire-rate'] - details_dict['fire-rate']),'- <abbr title="Максимально возможное улучшение">', int(maxed_dict['fire-rate']),'</abbr>')
        else:
            print(f'|Скорострельность {i} = ', int(maxed_dict['fire-rate']))
    else:
        print(f'|Скорострельность {i} = ', int(default_dict['fire-rate'][0]))


    if int(maxed_dict['accuracy']) != 0:   
        if details_dict['accuracy'] != 0:
            print(f'|Точность {i} = ', int(maxed_dict['accuracy'] - details_dict['accuracy']),'- <abbr title="Максимально возможное улучшение">', int(maxed_dict['accuracy']),'</abbr>')
        else:
            print(f'|Точность {i} = ', int(maxed_dict['accuracy']))
    else:
        print(f'|Точность {i} = ', int(default_dict['accuracy'][0]))
    
    if int(maxed_dict['recoil']) != 0:   
        if details_dict['recoil'] != 0:
            print(f'|Отдача {i} = ','<abbr title="Максимально возможное улучшение">', int(maxed_dict['recoil']),'</abbr> -', int(maxed_dict['recoil']) - details_dict['recoil'])
        else:
            print(f'|Отдача {i} = ', int(maxed_dict['recoil']))
    else:
        print(f'|Отдача {i} = ', int(default_dict['recoil'][0]))

    if maxed_dict['reloadTime'] != 0:
        if details_dict['reloadTime'] != 0:
            print(f'|Скорость перезарядки {i} = ','<abbr title="Максимально возможное улучшение">', maxed_dict['reloadTime'],'</abbr> -', maxed_dict['reloadTime'] - details_dict['reloadTime'])
        else:
            print(f'|Скорость перезарядки {i} = ', maxed_dict['reloadTime'])
    else:
        print(f'|Скорость перезарядки {i} = ', default_dict['reloadTime'][0])

    if maxed_dict['clipSize'] != 0:
        print(f'|Обойма {i} = ', int(maxed_dict['clipSize']))
    else:
        print(f'|Обойма {i} = ', int(default_dict['clipSize'][0]))

    temp_bullet = default_dict['allowedBullets'][0][0]
    print(f'|Боеприпас {i} = ', bullet_arr.index(temp_bullet) + 1)

    if int(maxed_dict['wear']) != 0:
        if details_dict['wear'] != 0:
            print(f'|Износостойкость {i} = ', int(maxed_dict['wear'] - details_dict['wear']),'- <abbr title="Максимально возможное улучшение">', int(details_dict['wear']),'</abbr>')
        else:
            print(f'|Износостойкость {i} = ', int(maxed_dict['wear']))
    else:
        print(f'|Износостойкость {i} = ', int(default_dict['wear'][0]))

    if maxed_dict['aimDistance'] != 0:
        print(f'|Дальность прицеливания {i} = ', int(maxed_dict['aimDistance']))
    else:
        print(f'|Дальность прицеливания {i} = ', int(default_dict['aimDistance'][0]))

    if gl_flag == 1:
            print(f'|Наличие гранатомёта {i} = Есть возможность установки')
        
    max_silencer = maxed_dict['silenced']
    if max_silencer == 1:
        print(f'|Наличие глушителя {i} = Установлен')

    if maxed_dict['weight'] != 0:
        print(f'|Вес {i} = ', int(maxed_dict['weight']))
    else:
        print(f'|Вес {i} = ', int(default_dict['weight'][0]))
        
    temp_shootModes = default_dict['shootModes'][0]
    shootmod_arr = []
    for mod in temp_shootModes:
        if 'auto' in mod:
            shootmod_arr.append('Автоматич.')
        elif 'single' in mod:
            shootmod_arr.append('Одиноч.')
        elif 'burst' in mod:
            shootmod_arr.append('Отсечка по три патрона')
        elif 'burst2' in mod:
            shootmod_arr.append('Отсечка по два патрона')
    print(f'|Режим стрельбы {i} = ', '<br /><br />'.join(shootmod_arr))
    print(f'|Стандартный боезапас {i} = ', amount)
    print('}}')

print(upgrade_final_str+'}}')
