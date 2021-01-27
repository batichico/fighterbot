# -*# -*- coding: utf-8 -*-
import os
import json


def add_new_user (id_user, u_first_name):
  # Here we add new user info to users.json
  file_path = "app/config/users.json"
  directory = os.path.dirname(file_path)
  new_user = {str(id_user): {'id_user': id_user, 'first_name': u_first_name, 'channels': {}}}

  if not os.path.exists(directory):
    os.makedirs(directory)
  if os.path.isfile(file_path):
    with open(file_path, "r") as jsonFile:
      data = json.load(jsonFile)
    if str(id_user) not in data:
      data[id_user] =  {'id_user': id_user, 'first_name': u_first_name}
    with open(file_path, "w") as outfile:
      json.dump(data, outfile, indent=4)
  else:
    with open(file_path, "w", encoding='utf-8') as outfile:
      json.dump(new_user, outfile, indent=4, ensure_ascii=False)


def add_channel_to_user(id_user, u_first_name, id_channel, channel_title):
  # Here we add channel to user
  file_path = "app/config/users.json"
  directory = os.path.dirname(file_path)

  if not os.path.exists(directory):
    os.makedirs(directory)
  
  if os.path.isfile(file_path):
    with open(file_path, "r") as jsonFile:
      data = json.load(jsonFile)
    if str(id_user) not in data:
      data[id_user] =  {'id_user': id_user, 'first_name': u_first_name, 'channels': {str(id_channel) : {'id': '0', 'id_father': None, 'id_channel': id_channel, 'channel_title': channel_title, 'packs':{}}}}
    else:
      print(data)
      print(data[str(id_user)])
      if len(data[str(id_user)]['channels']) == 0 or str(id_channel) not in data[str(id_user)]['channels']:
        data[str(id_user)]['channels'][id_channel] = {'id': '0', 'id_father': None, 'id_channel': id_channel, 'channel_title': channel_title, 'packs':{}} 

    with open(file_path, "w", encoding='utf-8') as outfile:
      json.dump(data, outfile, indent=4, ensure_ascii=False)
  else:
    with open(file_path, "w", encoding='utf-8') as outfile:
      json.dump(new_user, outfile, indent=4, ensure_ascii=False)


def add_new_to_pack(id_user, channel_id):
  file_path = "app/config/users.json"
  directory = os.path.dirname(file_path)
  if os.path.isfile(file_path):
  	with open(file_path, "r") as jsonFile:
  		data = json.load(jsonFile)
  		lst_packs = data[id_user]['channels'][channel_id]['packs']

  		if len(lst_packs) >= 1:
  			print("longitud de packs >= 1")
  		else:
  			data[id_user]['channels'][channel_id]['packs'] = {'new_pack': {}}
  			print("data finised")
  			print(data)

  			with open(file_path, "w", encoding='utf-8') as outfile:
  				json.dump(data, outfile, indent=4, ensure_ascii=False)
  else:
  	print("not file")


def create_war_pack(id_user, pack_name):
  cwd = os.getcwd()
  users_path = "app/config/users.json"
  directory = os.path.dirname(users_path)
  pack_characters_json = f"{cwd}/app/packs/{pack_name}/jsons/characters.json"
  print("entramos en create_war_pack")
  id_alive_characters = []

  # Creation of alives characters list:
  with open(pack_characters_json, "r+") as jsonFile:
    data = json.load(jsonFile)
    id_alive_characters = list(data.keys())
   

  # Adding info to user json
  if os.path.isfile(users_path):
    with open(users_path, "r") as jsonFile:
      data = json.load(jsonFile)
    print(data)
    lst_channels = data[id_user]['channels']
    if len(lst_channels) >= 1:
    	for channel in lst_channels:
    	 	new_id_pack = None
    	 	new_id_father = None
    	 	if len(data[id_user]['channels'][channel]['packs']) >= 1:
                 lst_packs = data[id_user]['channels'][channel]['packs']
                 if 'new_pack' not in lst_packs:
                     pass
                 else:
                     for pack in lst_packs:
                         if pack != 'new_pack':
                             new_id_pack = data[id_user]['channels'][channel]['packs']['id']
                             new_id_father = data[id_user]['channels'][channel]['packs']['id_father']
                         else:
                             if new_id_pack and new_id_father:
                                 id_number = int(new_id_pack.split('-')[1]) + 1
                                 id_father = new_id_father
                                 id_pack = new_id_father + str(id_number)
                             else:
                                 id_father = data[id_user]['channels'][channel]['id']
                                 id_pack = id_father + '-0'
                                 data[id_user]['channels'][channel]['packs'] = {
                                 id_pack : {
                                      "id": id_pack,
                                      "id_father": id_father,
                                      "pack_name": pack_name,
                                      "pack_path": f"app/{id_user}/{pack_name}",
                                      "characters_json": f"app/{id_user}/{pack_name}_characters_json",
                                      "started": False,
                                      "rounds": 0,
                                      "lst_alives": id_alive_characters,
                                      "lst_deaths": [],
                                      "time_per_fight": 100,
                                      "winner": ""
                                      }
	                            }
    with open(users_path, "w", encoding='utf-8') as outfile:
      json.dump(data, outfile, indent=4, ensure_ascii=False)


def get_channels_from_user(id_user):
  file_path = "app/config/users.json"
  if not os.path.exists(file_path):
    return None
  if os.path.isfile(file_path):
    with open(file_path, "r") as jsonFile:
      data = json.load(jsonFile)
    if str(id_user) in data:
      user_channels = data[str(id_user)]['channels']
      return user_channels


def add_character_json(count, characteres_json_path, photo, images_path):
  directory = os.path.dirname(characteres_json_path)
  character_name = photo.split('.')[0]
  new_character = {
    count: {
      'name': character_name, 
      'image_path': f"{images_path}/{photo}",
      'kills': 0, 
      'death': False,
      'rampage': False
    }
  }
  if not os.path.exists(directory):
    os.makedirs(directory)
  if os.path.isfile(characteres_json_path):
    with open(characteres_json_path, "r") as jsonFile:
      data = json.load(jsonFile)
    data[count] =  {
      'name': character_name,
      'image_path': f"{images_path}/{photo}",
      'kills': 0, 
      'death': False,
      'rampage': False
    }
    with open(characteres_json_path, "w", encoding='utf-8') as outfile:
      json.dump(data, outfile, indent=4, ensure_ascii=False)
  else:
    print("else")
    with open(characteres_json_path, "w", encoding='utf-8') as outfile:
      json.dump(new_character, outfile, indent=4, ensure_ascii=False)

'''
def get_pack_id(id_user, channel_id, pack_title):
	file_path = "app/config/users.json"
	directory = os.path.dirname(file_path)
	if not os.path.exists(file_path):
		return None
	if os.path.isfile(file_path):
		with open(file_path, "r") as jsonFile:
			data = json.load(jsonFile)
		if str(id_user) in data:
			id_pack = data[str(id_user)]['channels'][str(channel_id)]['packs'][pack_title]['id']
			return id_pack
'''


def get_info_from_pack(id_user, id_channel, id_pack):
	file_path = "app/config/users.json"
	directory = os.path.dirname(file_path)
	info = None
	channel_name = None
	pack_name = None

	if not os.path.exists(file_path):
		return None
	if os.path.isfile(file_path):
		with open(file_path, "r") as jsonFile:
			data = json.load(jsonFile)
		if str(id_user) in data:
		    # print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
		    # print('-------------------------------')
		    # print(f' id_channel {id_channel}')
		    # print('-------------------------------')
		    # print(data[str(id_user)]['channels'])
		    # print(f' id_channel {data[str(id_user)]["channels"][id_channel]}')
		    # print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
		    # pack_info = data[str(id_user)]['channels'][id_channel]['packs'][id_pack]
		    channel_name = data[str(id_user)]['channels'][id_channel]['channel_title']
		    pack_name = data[str(id_user)]['channels'][id_channel]["packs"][id_pack]["pack_name"]
		    info = {
               'id_channel': id_channel,
               'channel_name': channel_name,
               'pack_name': pack_name
            }
		    return info
			# channels = data[str(id_user)]['channels']
			# for channel in channels:
				# packs = channels[channel]['packs']
				# for pack in packs:
					# pack_info = data[str(id_user)]['channels'][channel]['packs'][pack]
					# if pack_info['id'] == id_pack:
						# id_channel = channel
						# channel_name = data[str(id_user)]['channels'][channel]['channel_title']
						# pack_name = pack_info['pack_name']
						# info = {
							# 'id_channel': id_channel,
							# 'channel_name': channel_name,
							# 'pack_name': pack_name
						# }
						# return info
