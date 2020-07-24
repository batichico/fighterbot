import os
from os import walk
import json
import random

from PIL import Image,ImageOps
import sys
import requests
import time
from threading import Thread

dict_characters = {}

dict_characters_winners = {}
dict_characters_lossers = {}


# ##### Lógica de fights ##########################

def start_war(id_user, id_channel, id_pack):
  file_path = "app/config/users.json"
  directory = os.path.dirname(file_path)
  message_error= ""
  if os.path.isfile(file_path):
    with open(file_path, "r") as jsonFile:
      data = json.load(jsonFile)
      if id_pack in data[id_user]["channels"][id_channel]["packs"]:
        pack_info = data[id_user]["channels"][id_channel]["packs"][id_pack]
        if len(pack_info['lst_deaths']) == 0 and pack_info['started'] is False:
          print("len 0")
          pack_name = pack_info['pack_name']
          # configurate_new_war(id_user, id_channel, pack_name)
          continue_war(id_user, id_channel, id_pack, pack_name)
        elif len(pack_info['lst_deaths']) > 0 and pack_info["winner"] == "":
          # continue_war
          pass
        elif len(pack_info['lst_deaths']) > 0 and pack_info["winner"] != "":
          # reset_war
          pass
        characters_json = pack_info['characters_json']


'''def configurate_new_war(id_user, id_channel, pack_name):
  users_path = "app/config/users.json"
  directory = os.path.dirname(users_path)
  pack_path = f"/home/fighting_bot/app/packs/{pack_name}/jsons/characters.json"  
  characters_info = None
  lst_alives_characters = None

  with open(pack_path, "r") as jsonFile:
    characters_info = json.load(jsonFile)
    lst_alives_characters = list(characters_info.keys())

  with open(users_path, "r", encoding='utf-8') as jsonFile:
    data = json.load(jsonFile)
    data[str(id_user)]['lst_alives'] = lst_alives_characters

    with open(users_path, "w", encoding='utf-8') as jsonFile:
      json.dump(data, outfile, indent=4, ensure_ascii=False)'''

def continue_war(id_user, id_channel, id_pack, pack_name):
  users_path = "app/config/users.json"
  directory = os.path.dirname(users_path)
  pack_path = f"/home/fighting_bot/app/packs/{pack_name}/jsons/characters.json"
  user_pack_info = None
  characters_info = None

  # prueba
  fighter1_id = None
  fighter2_id  = None
  id_winner = None
  id_losser = None
  fighter1_info = {}
  fighter2_info = {}
  winner_info = {}
  losser_info = {}
  rey = False
  guerra_on = True
  exists_type= True
  frase_rey = ""
  id_died_characters = []
  lst_alives_characters = None
  # prueba
  fight_lst = []

  with open(pack_path, "r") as jsonFile:
    characters_info = json.load(jsonFile)

  with open(users_path, "r") as jsonFile:
    data = json.load(jsonFile)
    user_pack_info = data[id_user]['channels'][id_channel]['packs'][id_pack]
    lst_alives_characters = data[id_user]['channels'][id_channel]['packs'][id_pack]['lst_alives']

  if len(lst_alives_characters) == 0:
    guerra_on = False  
    return "Guerra finalizada", guerra_on 
  elif len(lst_alives_characters) > 2:
    f1 = random.randrange(0, len(lst_alives_characters)-1)
    fighter1_id = lst_alives_characters[f1]
    fight_lst.append(fighter1_id)
    fight_close = False
    while fight_close == False:
      f2 = random.randrange(0, len(lst_alives_characters)-1)
      fighter2_id = lst_alives_characters[f2]
      if fighter2_id not in fight_lst:
        fight_lst.append(fighter2_id)
        fight_close = True
  else:
    fight_lst = lst_alives_characters
    fighter1_id = lst_alives_characters[0]
    fighter2_id = lst_alives_characters[1]

  fight_winner = random.randrange(0, len(fight_lst))
  id_winner = fight_lst[fight_winner]
  if fight_winner == 0:
    id_losser = fight_lst[1]
  else:
    id_losser = fight_lst[0]

  user_pack_info['lst_alives'].remove(id_losser)
  user_pack_info['lst_deaths'].append(id_losser)

  with open(users_path, "r") as jsonFile:
    data = json.load(jsonFile)
    data[id_user]['channels'][id_channel]['packs'][id_pack] = user_pack_info

  with open(users_path, "w") as outfile:
  	json.dump(data, outfile, indent=4)

  # id_alive_characters.remove(id_losser)
  # id_died_characters.append(id_losser)



  fighter1_info = characters_info[fighter1_id]
  fighter2_info = characters_info[fighter2_id]
  winner_info = characters_info[id_winner]
  losser_info = characters_info[id_losser]
  pic_url1 = fighter1_info['image_path']
  pic_url2 = fighter2_info['image_path']

  images_fight_dict = f"/home/fighting_bot/app/packs/{pack_name}/images_fight"

  '''with open(f'{images_fight_dict}/pic1.jpg', 'wb') as handle:
            response = requests.get(pic_url1, stream=True)
            if not response.ok:
                print (response)
            for block in response.iter_content(1024):
                if not block:
                    break
                handle.write(block)
      
        with open(f'{images_fight_dict}/pic2.jpg', 'wb') as handle:
            response = requests.get(pic_url2, stream=True)
            if not response.ok:
                print (response)
            for block in response.iter_content(1024):
                if not block:
                    break
                handle.write(block)'''

  images = list(map(Image.open, [f'{images_fight_dict}/pic1.jpg', f'{images_fight_dict}/pic2.jpg']))
  widths, heights = zip(*(i.size for i in images))

  total_width = sum(widths)
  max_height = max(heights)

  # puro copy

  new_im = Image.new('RGB', (total_width, max_height))

  x_offset = 0
  for im in images:
    new_im.paste(im, (x_offset,0))
    x_offset += im.size[0]

  new_im.save(f'{images_fight_dict}/fight.jpg')
  
  if id_losser == fighter1_id:
    image_loser = Image.open(f'{images_fight_dict}/pic1.jpg')
    data = image_loser.getdata()
    
    new_image = ImageOps.grayscale(image_loser)
    new_image.save(f'{images_fight_dict}/pic1.jpg')
    
  else:
    image_loser = Image.open(f'{images_fight_dict}/pic2.jpg')
    data = image_loser.getdata()
    
    new_image = ImageOps.grayscale(image_loser)
    new_image.save(f'{images_fight_dict}/pic2.jpg')
  
  images = list(map(Image.open, [f'{images_fight_dict}/pic1.jpg', f'{images_fight_dict}/pic2.jpg']))
  widths, heights = zip(*(i.size for i in images))

  total_width = sum(widths)
  max_height = max(heights)

  new_im = Image.new('RGB', (total_width, max_height))

  x_offset = 0
  for im in images:
    new_im.paste(im, (x_offset,0))
    x_offset += im.size[0]

  new_im.save(f'{images_fight_dict}/result.jpg')
  if len(id_alive_characters) == 1:
    print(id_alive_characters)
    rey  = True
    frase_rey = "We have a winner!!" + winner_info['Name'] + " is the new Pirate King!!"
    pic_url_king = winner_info['Imagen']
    with open('king.jpg', 'wb') as handle:
      response = requests.get(pic_url_king, stream=True)
      if not response.ok:
          print (response)
      for block in response.iter_content(1024):
          if not block:
              break
          handle.write(block)

  anuncio_lucha = "The fight start between *" + fighter1_info['Name'] + "* and *" + fighter2_info['Name'] + "* \n\nLa pelea será una dura pelea de 30 minutos, veremos quien será el ganador :)"
  anuncio_resultado = "*" + winner_info['Name']  + "* kills *" + losser_info['Name'] + "*\n\nThe winner is: *" + winner_info['Name'] + "* \n\nAlives: *" + str(len(id_alive_characters))  + "*\nDeaths: *" + str(len(id_died_characters)) +"*"

  return anuncio_lucha, anuncio_resultado, rey, frase_rey




'''
def war(chat_id, fight_type):
	fight_lst = []
  fighter1_id = 0
	fighter2_id  = 0
	id_died_characters = []
	id_alive_characters = []
	id_winner = 0
	id_losser = 0
	fighter1_info = {}
	fighter2_info = {}
	winner_info = {}
	losser_info = {}
	rey = False
	guerra_on = True
	exists_type= True
	frase_rey = ""
	fighter1_stats = {
		"Id":0,
		"Name":"",
		"Imagen": "",
		"Kills": [],
		"PowerLevel":0,
		"LastFight":"",
		"Dieds":0,
		"Alive":True
	}
	fighter2_stats = {
		"Id":0,
		"Name":"",
		"Imagen": "",
		"Kills": [],
		"PowerLevel":0,
		"LastFight":"",
		"Dieds":0,
		"Alive":True
	}

	file_path_alive = f"app/{str(chat_id)}/{fight_type}_alive.json"
	directory_alive = os.path.dirname(file_path_alive)

	file_path_died = f"app/{str(chat_id)}/{fight_type}_died.json"
	directory_died  = os.path.dirname(file_path_died)

	file_path_fight_type = f"app/{fight_type}.json"
	directory_fight_type = os.path.dirname(file_path_fight_type)

	if not os.path.exists(directory_alive):
		os.makedirs(directory_alive)
	else:
		if os.path.isfile(file_path_alive):
		  with open(file_path_alive, "r+") as jsonFile:
		    data = json.load(jsonFile)
		    print(data)
		    if len(data)== 0:
		      if not os.path.exists(directory_fight_type):
		        exists_type = False
		        return "ERROR No está registrada este tipo de guerra", False
		      else:
		        with open(file_path_fight_type, "r+") as jsonFile:
		          data = json.load(jsonFile)
		          id_alive_characters = list(data.keys())
		        with open(file_path_alive, "w", encoding='utf-8') as outfile:
		          json.dump(id_alive_characters, outfile, indent=4, ensure_ascii=False)
		    elif len(data) > 1 :
		      id_alive_characters = data
		else:
		  with open(file_path_fight_type, "r+") as jsonFile:
		    data = json.load(jsonFile)
		    id_alive_characters = list(data.keys())
		  with open(file_path_alive, "w", encoding='utf-8') as outfile:
		    json.dump(id_alive_characters, outfile, indent=4, ensure_ascii=False)

  if not os.path.exists(directory_died):
    os.makedirs(directory_died)
  else:
    if os.path.isfile(file_path_died):
      with open(file_path_died, "r+") as jsonFile:
        data = json.load(jsonFile)
        if len(data)== 0:
          pass
        else:
          id_died_characters = data
    else:
      with open(file_path_died, "w", encoding='utf-8') as outfile:
        json.dump(id_died_characters, outfile, indent=4, ensure_ascii=False)
        
  if len(id_alive_characters) == 0:
    guerra_on = False  
    return "Guerra finalizada", guerra_on 
  elif len(id_alive_characters) > 2:
    f1 = random.randrange(0, len(id_alive_characters)-1)
    fighter1_id = id_alive_characters[f1]
    fight_lst.append(fighter1_id)
    fight_close = False
    while fight_close == False:
      f2 = random.randrange(0, len(id_alive_characters)-1)
      fighter2_id = id_alive_characters[f2]
      if fighter2_id not in fight_lst:
        fight_lst.append(fighter2_id)
        fight_close = True
  else:
    fight_lst = id_alive_characters
    fighter1_id = id_alive_characters[0]
    fighter2_id = id_alive_characters[1]


  fight_winner = random.randrange(0, len(fight_lst))
  id_winner = fight_lst[fight_winner]
  if fight_winner == 0:
    id_losser = fight_lst[1]
  else:
    id_losser = fight_lst[0]

  id_alive_characters.remove(id_losser)
  id_died_characters.append(id_losser)

  with open(file_path_alive, "w") as outfile:
    json.dump(id_alive_characters, outfile, indent=4)

  with open(file_path_died, "w") as outfile:
    json.dump(id_died_characters, outfile, indent=4)

  with open(file_path_anime, "r+") as jsonFile:
    data = json.load(jsonFile)
    fighter1_info = data[fighter1_id]
    fighter2_info = data[fighter2_id]
    winner_info = data[id_winner]
    losser_info = data[id_losser]
  
  pic_url1 = fighter1_info['Imagen']
  pic_url2 = fighter2_info['Imagen']
  with open('pic1.jpg', 'wb') as handle:
      response = requests.get(pic_url1, stream=True)
      if not response.ok:
          print (response)
      for block in response.iter_content(1024):
          if not block:
              break
          handle.write(block)
          
  with open('pic2.jpg', 'wb') as handle:
      response = requests.get(pic_url2, stream=True)
      if not response.ok:
          print (response)
      for block in response.iter_content(1024):
          if not block:
              break
          handle.write(block)
          
  images = list(map(Image.open, ['pic1.jpg', 'pic2.jpg']))
  widths, heights = zip(*(i.size for i in images))

  total_width = sum(widths)
  max_height = max(heights)

  new_im = Image.new('RGB', (total_width, max_height))

  x_offset = 0
  for im in images:
    new_im.paste(im, (x_offset,0))
    x_offset += im.size[0]

  new_im.save('fight.jpg')
  
  if id_losser == fighter1_id:
    image_loser = Image.open('pic1.jpg')
    data = image_loser.getdata()
    
    new_image = ImageOps.grayscale(image_loser)
    new_image.save("pic1.jpg")
    
  else:
    image_loser = Image.open('pic2.jpg')
    data = image_loser.getdata()
    
    new_image = ImageOps.grayscale(image_loser)
    new_image.save("pic2.jpg")
  
  images = list(map(Image.open, ['pic1.jpg', 'pic2.jpg']))
  widths, heights = zip(*(i.size for i in images))

  total_width = sum(widths)
  max_height = max(heights)

  new_im = Image.new('RGB', (total_width, max_height))

  x_offset = 0
  for im in images:
    new_im.paste(im, (x_offset,0))
    x_offset += im.size[0]

  new_im.save('result.jpg')
  if len(id_alive_characters) == 1:
    print(id_alive_characters)
    rey  = True
    frase_rey = "We have a winner!!" + winner_info['Name'] + " is the new Pirate King!!"
    pic_url_king = winner_info['Imagen']
    with open('king.jpg', 'wb') as handle:
      response = requests.get(pic_url_king, stream=True)
      if not response.ok:
          print (response)
      for block in response.iter_content(1024):
          if not block:
              break
          handle.write(block)
    
    
    
  anuncio_lucha = "The fight start between *" + fighter1_info['Name'] + "* and *" + fighter2_info['Name'] + "* \n\nLa pelea será una dura pelea de 30 minutos, veremos quien será el ganador :)"
  anuncio_resultado = "*" + winner_info['Name']  + "* kills *" + losser_info['Name'] + "*\n\nThe winner is: *" + winner_info['Name'] + "* \n\nAlives: *" + str(len(id_alive_characters))  + "*\nDeaths: *" + str(len(id_died_characters)) +"*"

  return anuncio_lucha, anuncio_resultado, rey, frase_rey
'''

