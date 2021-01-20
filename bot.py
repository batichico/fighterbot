from config import *
import importdir

importdir.do('plugins', globals())

#################################################
#                    POLLING                    #
#################################################


try:
    bot.send_message(239822769, "Bot encendido")
    print("Bot encendido")
except:
    print("No tienes iniciado el bot con tu usuario")

bot.polling()