from telegram import Update, ForceReply
from telegram.ext import Updater, InlineQueryHandler, CommandHandler
from telegram.ext.dispatcher import run_async
import requests
import re

        
        
#### start command
def start(update, context):
    '''Send a message when the command /start is issued.'''
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\! \
        run /help for more information',
        reply_markup=ForceReply(selective=True),
    )

#### help command
def help_command(update, context):
    '''Send a message when the command /help is issued.'''
    update.message.reply_text('Help! \n \
    Include a descriptions of commands')

#### Random dog command
def get_url_dog():
    '''Request url information for random dog generator'''
    contents = requests.get('https://random.dog/woof.json').json()   
    url = contents['url']
    return url    
    
def get_image_url_dog():
    '''Iterates until find an image (there are also gifts and videos in the webpage'''
    allowed_extension = ['jpg','jpeg','png']
    file_extension = ''
    while file_extension not in allowed_extension:
        url = get_url_dog()
        file_extension = re.search("([^.]*)$",url).group(1).lower()
    return url

def dog(update, context):
    '''Send a random dog.'''
    url = get_image_url_dog()
    chat_id = update.message.chat_id
    context.bot.send_photo(chat_id=chat_id, photo=url)
    
#### Random cat command
def get_url_cat():
    '''Request url information for random cat generator'''
    contents = requests.get('http://aws.random.cat/meow').json()  
    url = contents['file']
    return url    
    
def get_image_url_cat():
    '''Iterates until find an image (there are also gifts and videos in the webpage'''
    allowed_extension = ['jpg','jpeg','png']
    file_extension = ''
    while file_extension not in allowed_extension:
        url = get_url_cat()
        file_extension = re.search("([^.]*)$",url).group(1).lower()
    return url

def cat(update, context):
    '''Send a random dog.'''
    url = get_image_url_cat()
    chat_id = update.message.chat_id
    context.bot.send_photo(chat_id=chat_id, photo=url)


#### Aare general information command    
def get_aare_info(value):
    '''Request general Aare information. This is Aare temperature and flow, air temperature.'''
    verbose = False  # for debug
    url = f'http://aareguru.existenz.ch/v2018/current?city=bern&app=my.app.ch&version=1.0.42&values={value}'
    contents = requests.get(url).json()
    if verbose:   
        print('content in Aare coomand') 
        print(contents)
    return contents
      
def general_info(update, context):
    '''Send general Aare information. This is Aare temperature and flow, air temperature.'''
    chat_id = update.message.chat_id
    temperature = get_aare_info('aare.temperature')
    flow = get_aare_info('aare.flow')
    air_temp = get_aare_info('weather.current.tt')
    update.message.reply_text(
        f'Aare general information: \n \
        Aare temperature: {temperature} °C \n \
        Aare flow: {flow} m3/s \n \
        Air temperature: {air_temp} °C'
        )
        

#### Main  
def main():
    ## load token
    with open("token.txt", "r") as f:
         token = f.read()[0:46] # not sure why it works..
    ## update and interact
    updater = Updater(token, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start',start))
    dp.add_handler(CommandHandler('help',help_command))
    dp.add_handler(CommandHandler('dog',dog))
    dp.add_handler(CommandHandler('cat',cat))
    dp.add_handler(CommandHandler('aare',general_info))
    updater.start_polling()
    updater.idle()
    
if __name__ == '__main__':
    main()
