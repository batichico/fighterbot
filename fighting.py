# -*# -*- coding: utf-8 -*-

import telebot # Librería de la API del bot.
import os
import json
import requests
from telebot import types # Tipos para la API del bot.
from datetime import datetime, date, time, timedelta
import calendar
from threading import Thread
from random import randrange
from os import listdir
from os.path import isfile, join
import time # Librería para hacer que el programa que controla el bot no se acabe.
from pathlib import Path

from files_functions import *

from war import *

import subprocess

import logging

# Here @BotFather gived TOKEN).
TOKEN = '1216059921:AAHH8iBugocg_bZUZYBQQ11vJjsWOMQ1qbU' 
# Creation of bot object
bot = telebot.TeleBot(TOKEN)
#############################################


# Listener
def listener(messages): 
	# Here we define the listener of the messages.
        for m in messages: 
            if m.content_type == 'text': # Filter by content type text
                cid = m.chat.id # Save chat id
                logging.debug(f'[{cid}]: {m.text}')
                print ("[" + str(cid) + "]: " + m.text) # Y haremos que imprima algo parecido a esto -> [52033876]: /start

bot.set_update_listener(listener) # Así, le decimos al bot que utilice como función escuchadora nuestra función 'listener' declarada arriba.


# Handle '/start' and '/help'
@bot.message_handler(commands=['ayuda', 'start'])
def command_start(m): 
        cid = m.chat.id
        bot.send_message( cid, 'Gracias por iniciarme')


@bot.message_handler(commands=['mywars'])
def command_mywars(m):
	# This command is to show what channels have registered the user
    cid = m.chat.id
    id_user = m.from_user.id
    dict_channels = get_channels_from_user(id_user)
    lst_channels = []
    if dict_channels:
        for c in dict_channels:
            info_chanell = dict_channels[c]
            id_channel = info_chanell['id_channel']
            channel_title = info_chanell['channel_title']
            lst_channels.append(types.InlineKeyboardButton(channel_title, callback_data=f"c*{str(id_channel)}"))

        channelsKeyboard = types.InlineKeyboardMarkup()
        channelsKeyboard.add(*lst_channels)
        bot.send_message(cid, "Estos son tus canales:", reply_markup=channelsKeyboard, disable_web_page_preview=True)
    else:
        bot.send_message(cid, "No tienes registrado ningún canal, utilice /createwar")

@bot.callback_query_handler(func=lambda call: call.data.startswith('c*'))
def callback_channel_menu(call):
    # This callback show the channels that have the user.
    cid = call.message.chat.id
    mid = call.message.message_id
    id_user = call.from_user.id 
    channel_id = call.data.split('*')[1]
    pack_keyboard = types.InlineKeyboardMarkup()
    dict_channels = get_channels_from_user(id_user)
    lst_packs = dict_channels[channel_id]['packs']
    lst_packs_buttons = []
    if len(lst_packs) >= 1: 
        packs = dict_channels[channel_id]['packs']
        channel_name = dict_channels[channel_id]['channel_title']
        if len(packs) >= 1 :
            for pack in packs:
            	pack_name = packs[pack]['pack_name']
            	id_pack = packs[pack]['id']
            	lst_packs_buttons.append(types.InlineKeyboardButton(pack_name, callback_data=f"p*{id_pack}"))

            pack_keyboard = types.InlineKeyboardMarkup()
            pack_keyboard.add(*lst_packs_buttons)
            pack_keyboard.add(types.InlineKeyboardButton("NUEVO PACK", callback_data=f"addp*{str(channel_id)}"),
                types.InlineKeyboardButton("VOLVER 🔙", callback_data="mywars")
                )

        bot.edit_message_text(f"Estos son los packs que tienes en el canal {channel_name}", cid, mid, reply_markup=pack_keyboard, disable_web_page_preview=True)

    else:
        packKeyboard.add(types.InlineKeyboardButton('Ver packs', callback_data=f"vr*{str(channel_id)}"),
            types.InlineKeyboardButton('Añadir Pack', callback_data=f"ad*{str(channel_id)}"))
        bot.edit_message_text("Elige una opción", cid, mid, reply_markup=packKeyboard, disable_web_page_preview=True)

@bot.callback_query_handler(func=lambda call: call.data.startswith('p*'))
def callback_channel(call):
    cid = call.message.chat.id
    mid = call.message.message_id
    id_user = call.from_user.id 
    id_pack = call.data.split('*')[1]
    id_channel = get_info_from_pack(id_user, id_pack)['id_channel']
    pack_name = get_info_from_pack(id_user, id_pack)['pack_name']
    channel_name = get_info_from_pack(id_user, id_pack)['channel_name']

    pack_keyboard = types.InlineKeyboardMarkup()
    pack_keyboard.add(types.InlineKeyboardButton("INICIAR GUERRA ▶️", callback_data=f"initwar*{id_pack}"))
    pack_keyboard.add(types.InlineKeyboardButton("ACTUALIZAR PACK 🔄", callback_data=f"upp*{id_pack}"),
        types.InlineKeyboardButton("ELIMINAR PACK ❌", callback_data=f"delpo*{id_pack}"))
    pack_keyboard.add(types.InlineKeyboardButton("CONFIGURAR ⚙️", callback_data=f"cnfp*{id_pack}"),
        types.InlineKeyboardButton("VOLVER 🔙", callback_data=f"c*{id_channel}"))
    bot.edit_message_text(f"Elige una opción que hacer sobre el pack {pack_name} del canal {channel_name}", cid, mid, reply_markup=pack_keyboard, disable_web_page_preview=True)


@bot.callback_query_handler(func=lambda call: call.data.startswith('initwar'))
def callback_init_war(call):
    cid = call.message.chat.id
    mid = call.message.message_id
    id_user = call.from_user.id
    id_pack = call.data.split('*')[1]
    id_channel = get_info_from_pack(id_user, id_pack)['id_channel']
    pack_name = get_info_from_pack(id_user, id_pack)['pack_name']
    channel_name = get_info_from_pack(id_user, id_pack)['channel_name']

    war_thread(cid, mid, id_user, id_pack, id_channel, pack_name, channel_name)


@bot.callback_query_handler(func=lambda call: call.data.startswith('delpo'))
def callback_delpack(call):
    cid = call.message.chat.id
    mid = call.message.message_id
    id_user = call.from_user.id
    id_pack = call.data.split('*')[1]
    id_channel = get_info_from_pack(id_user, id_pack)['id_channel']
    pack_name = get_info_from_pack(id_user, id_pack)['pack_name']
    channel_name = get_info_from_pack(id_user, id_pack)['channel_name']

    if call.data.startswith('delp'):
        del_keyboard = types.InlineKeyboardMarkup()
        del_keyboard.add(types.InlineKeyboardButton("SI", callback_data=f"delps*{id_pack}"),
        types.InlineKeyboardButton("NO", callback_data=f"delpn*{id_pack}")
        )
        bot.edit_message_text(f"Estas segur@ de que quieres ELIMINAR el pack {pack_name} del canal {channel_name}?", cid, mid, reply_markup=del_keyboard, disable_web_page_preview=True)

@bot.callback_query_handler(func=lambda call: call.data.startswith('delpn'))
def callback_delpackn(call):
    cid = call.message.chat.id
    mid = call.message.message_id
    id_user = call.from_user.id
    id_pack = call.data.split('*')[1]
    id_channel = get_info_from_pack(id_user, id_pack)['id_channel']
    pack_name = get_info_from_pack(id_user, id_pack)['pack_name']
    channel_name = get_info_from_pack(id_user, id_pack)['channel_name']

    if call.data.startswith('delpn'):
        delpn_keyboard = types.InlineKeyboardMarkup()
        delpn_keyboard.add(types.InlineKeyboardButton("VOLVER 🔙", callback_data=f"p*{id_pack}"))
        bot.edit_message_text(f"El pack {pack_name} del canal {channel_name} no ha sido eliminado", cid, mid, reply_markup=delpn_keyboard, disable_web_page_preview=True)


@bot.callback_query_handler(func=lambda call: call.data.startswith('mywars'))
def callback_returns(call):
    cid = call.message.chat.id
    mid = call.message.message_id
    id_user = call.from_user.id 

    if call.data == 'mywars':
        dict_channels = get_channels_from_user(id_user)
        lst_channels = []
        if dict_channels:
            for c in dict_channels:
                info_chanell = dict_channels[c]
                id_channel = info_chanell['id_channel']
                channel_title = info_chanell['channel_title']
                lst_channels.append(types.InlineKeyboardButton(channel_title, callback_data=f"c*{str(id_channel)}"))

            channelsKeyboard = types.InlineKeyboardMarkup()
            channelsKeyboard.add(*lst_channels)
            bot.edit_message_text("Estos son tus canales:", cid, mid, reply_markup=channelsKeyboard, disable_web_page_preview=True)
        else:
            bot.edit_message_text("No tienes registrado ningún canal, utilice /createwar", cid, mid)




@bot.callback_query_handler(func=lambda call: call.data.startswith('vr*') or call.data.startswith('ad*'))
def callback_packs(call):
    cid = call.message.chat.id
    mid = call.message.message_id
    first_name = call.from_user.first_name
    id_user = call.from_user.id

    channel_id = call.data.split('*')[1]
    dict_channels = get_channels_from_user(id_user)
    bot.send_message(cid, str(dict_channels))
    packKeyboard = types.InlineKeyboardMarkup()

    if call.data.startswith('vr*'):
        packKeyboard.add(types.InlineKeyboardButton('VOLVER 🔙', callback_data=f"ad*{str(channel_id)}"))
        
    if call.data.startswith('ad*'):
        add_new_to_pack(str(id_user), channel_id)
        msg = bot.edit_message_text("A continuación crea una carpeta con las imagenes correspondientes para la guerra con sus respectivos nombres.\n\n1.- Guarda las imagenes que quieras con sus respectivos nombres. Ejemplo: Goku.jpg, Krillin.jpg,...\n\n2.- Guardadalos en una carpeta y comprímelos en un .rar.\n\n3.- Envíame el archivo .rar", cid, mid)
        bot.register_next_step_handler(msg, step_send_rar)


@bot.message_handler(commands=['createwar']) 
def command_createwar(m): 
    cid = m.chat.id
    id_user = m.from_user.id
    first_name = m.from_user.first_name

    if m.chat.type != "private":
        bot.send_message(cid, "hablame por privado")
    else:
        confirmKeyboard = types.InlineKeyboardMarkup()
        confirmKeyboard.add(types.InlineKeyboardButton('HECHO', callback_data='added_chat'))
        bot.send_message(cid, "Añademe a un canal o grupo como administrador", reply_markup=confirmKeyboard, disable_web_page_preview=True)


@bot.callback_query_handler(func=lambda call: call.data in ['added_chat'])
def callback_added_chat(call):
    cid = call.message.chat.id
    mid = call.message.message_id
    first_name = call.from_user.first_name
    id_user = call.from_user.id

    add_new_user (id_user, first_name)
    msg = bot.edit_message_text("Reenviame un texto del canal que me has añadido para comprobar que estoy dentro", cid, mid, parse_mode="Markdown")
    bot.register_next_step_handler(msg, step_validate_channell)

def step_validate_channell(m):
    cid = m.chat.id
    id_user = m.from_user.id
    first_name = m.from_user.first_name
    channell_validated = False
    id_channel = None
    channel_title = None

    if m.forward_from_chat !=  None:
        bot.send_message(cid, "enviado del canal")
        id_channel = m.forward_from_chat.id
        channel_title = m.forward_from_chat.title
        id_message = m.message_id
        try:
            bot.send_message(id_channel, 'Prueba ("ELIMINA ESTE MENSAJE")')
            channell_validated = True
            add_channel_to_user(id_user, first_name, id_channel, channel_title)
            bot.send_message(cid, f"Se me ha añadido correctamente a {channel_title}, a continuación puedes crear tu primer pack de guerra")
            
        except:
            bot.send_message(cid, f"No estoy en {channel_title}")

    if channell_validated:
        bot.send_message(cid, "Se guardó el canal correctamente")
        add_new_to_pack(str(id_user), str(id_channel))
        msg = bot.send_message(cid, "A continuación crea una carpeta con las imagenes correspondientes para la guerra con sus respectivos nombres.\n\n1.- Guarda las imagenes que quieras con sus respectivos nombres. Ejemplo: Goku.jpg, Krillin.jpg,...\n\n2.- Guardadalos en una carpeta y comprímelos en un .rar.\n\n3.- Envíame el archivo .rar")
        bot.register_next_step_handler(msg, step_send_rar)


def step_send_rar(m):
    cid = m.chat.id
    id_user = m.from_user.id
    first_name = m.from_user.first_name
    downloaded = False
    unpacked = False
    pack_path = None
    characteres_json = None
    alives_json = None
    deaths_json = None
    cwd = os.getcwd()
    bot.send_message(cid, f'cwd {str(cwd)}')
    if m.content_type == 'document':
        file_name = m.document.file_name
        file_title = file_name.split('.')[0]
        bot.send_message(cid, f"Se ha enviado un documento: {file_name}")
        file_info = bot.get_file(m.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        try:
            with open(file_name, 'wb') as new_file:
                new_file.write(downloaded_file)
            downloaded = True
        except:
            bot.send_message(cid, "Hubo un problema al descargar el rar")

        if downloaded:
            try:
            	subprocess.run(["unrar", "x", f"{cwd}/{file_name}"],stdout=subprocess.PIPE)
            	unpacked = True
            	bot.send_message(cid, "Se ha descomprimido correctamente")
            	file_path = f"app/packs/{file_title}"
            	os.makedirs(file_path)
            	subprocess.run(["sudo", "mv", f"{cwd}/{file_title}", f"{cwd}/app/packs/{file_title}"],stdout=subprocess.PIPE)
            	subprocess.run(["sudo", "mv", f"{cwd}/app/packs/{file_title}/{file_title}", f"{cwd}/app/packs/{file_title}/images"],stdout=subprocess.PIPE)
            	subprocess.run(["sudo", "rm", f"{cwd}/{file_name}"], stdout=subprocess.PIPE)
            except:
                bot.send_message(cid, "Error al descomprimir el archivo")

        if unpacked:
            characteres_json_path = f"{cwd}/app/packs/{file_title}/jsons/characters.json"
            images_path = f"{cwd}/app/packs/{file_title}/images"
            count = 0
            for photo in os.listdir(images_path):
                count += 1
                add_character_json(count, characteres_json_path, photo, images_path)

            create_war_pack(str(id_user), file_title)


@bot.message_handler(func=lambda message: True)
def echo_message(message):
    cid = message.chat.id
    if message.text.lower() == "mi id":
        id = message.from_user.id
        cid = message.chat.id
        idUser = str(id)
        bot.send_message( cid, idUser)

    if message.text.lower() == "holi":
        username = message.from_user.username
        id = message.from_user.id
        cid = message.chat.id

        if id == 239822769:
            bot.send_message( cid, 'Hola mi creador 😙')


'''@bot.message_handler(commands=['war']) # Indicamos que lo siguiente va a controlar el comando '/miramacho'
def war_command(m): # Definimos una función que resuleva lo que necesitemos.
    cid = m.chat.id 
    x=m.text
    id_user = m.from_user.id

    resultado = start_war(id_user, id_channel, id_pack)
    if len(resultado) == 2 and resultado[1] == False:
        bot.send_message(cid, resultado[0], parse_mode="Markdown")
    elif len(resultado) == 4 and resultado[2] == True:
        bot.send_photo( cid, open('fight.jpg', 'rb'),resultado[0], parse_mode="Markdown")
        time.sleep(2)
        bot.send_photo( cid, open('result.jpg', 'rb'), resultado[1], parse_mode="Markdown")
        time.sleep(5)
        bot.send_photo( cid, open('king.jpg', 'rb'), resultado[3], parse_mode="Markdown")
    else:
        bot.send_photo( cid, open('fight.jpg', 'rb'),resultado[0], parse_mode="Markdown")
        time.sleep(2)
        bot.send_photo( cid, open('result.jpg', 'rb'), resultado[1], parse_mode="Markdown")
    time.sleep(2)
    war_command(m)'''

'''
@bot.message_handler(commands=['war']) # Indicamos que lo siguiente va a controlar el comando '/miramacho'
def fight_func(m): # Definimos una función que resuleva lo que necesitemos.
    print(m)
    cid = m.chat.id 
    x=m.text
    idUsu = m.from_user.id
    if idUsu == 239822769:
      anime = "onepiece"
      resultado = fight(cid,anime)
      if len(resultado) == 2 and resultado[1] == False:
        bot.send_message(cid, resultado[0], parse_mode="Markdown")
      elif len(resultado) == 4 and resultado[2] == True:
        bot.send_photo( cid, open( 'fight.jpg', 'rb'),resultado[0], parse_mode="Markdown")
        time.sleep(2)
        bot.send_photo( cid, open( 'result.jpg', 'rb'), resultado[1], parse_mode="Markdown")
        time.sleep(5)
        bot.send_photo( cid, open( 'king.jpg', 'rb'), resultado[3], parse_mode="Markdown")
      else:
        bot.send_photo( cid, open( 'fight.jpg', 'rb'),resultado[0], parse_mode="Markdown")
        time.sleep(2)
        bot.send_photo( cid, open( 'result.jpg', 'rb'), resultado[1], parse_mode="Markdown")
    time.sleep(2)
    fight_func(m)
'''

'''def war_thread_func(): # Definimos una función que resuleva lo que necesitemos.
    cid = -1001215223535
    id_user = -1001215223535
    if id_user == -1001215223535:
      anime = "onepiece"
      resultado = start_war(id_user, cid, id_pack)
      if len(resultado) == 2 and resultado[1] == False:
        bot.send_message(cid, resultado[0], parse_mode="Markdown")
      elif len(resultado) == 4 and resultado[2] == True:
        bot.send_photo( cid, open( 'fight.jpg', 'rb'),resultado[0], parse_mode="Markdown")
        #time.sleep(1800)
        bot.send_photo( cid, open( 'result.jpg', 'rb'), resultado[1], parse_mode="Markdown")
        time.sleep(5)
        bot.send_photo( cid, open( 'king.jpg', 'rb'), resultado[3], parse_mode="Markdown")
      else:
        bot.send_photo( cid, open( 'fight.jpg', 'rb'),resultado[0], parse_mode="Markdown")
        time.sleep(1800)
        bot.send_photo( cid, open( 'result.jpg', 'rb'), resultado[1], parse_mode="Markdown")
    time.sleep(1800)
    fight_func(m)
'''

def war_command_function(cid, mid, id_user, id_pack, id_channel, pack_name, channel_name):
    resultado = start_war(str(id_user), id_channel, id_pack)
    if len(resultado) == 2 and resultado[1] == False:
        bot.send_message(id_channel, resultado[0], parse_mode="Markdown")
    elif len(resultado) == 4 and resultado[2] == True:
        bot.send_photo(id_channel, open('fight.jpg', 'rb'), resultado[0], parse_mode="Markdown")
        time.sleep(2)
        bot.send_photo(id_channel, open('result.jpg', 'rb'), resultado[1], parse_mode="Markdown")
        time.sleep(5)
        bot.send_photo(id_channel, open('king.jpg', 'rb'), resultado[3], parse_mode="Markdown")
    else:

        bot.send_photo(id_channel, open('fight.jpg', 'rb'), resultado[0], parse_mode="Markdown")
        time.sleep(2)
        bot.send_photo(id_channel, open('result.jpg', 'rb'), resultado[1], parse_mode="Markdown")
    time.sleep(2)
    war_thread(cid, mid, id_user, id_pack, id_channel, pack_name, channel_name)


def war_thread(cid, mid, id_user, id_pack, id_channel, pack_name, channel_name):
    Thread(target = war_command_function(cid, mid, id_user, id_pack, id_channel, pack_name, channel_name)).start()
    while True:
        time.sleep(2)
        Thread(target = war_command_function(cid, mid, id_user, id_pack, id_channel, pack_name, channel_name)).start()

      
bot.polling(none_stop=True) # Con esto, le decimos al bot que siga funcionando incluso si encuentra algún fallo.
