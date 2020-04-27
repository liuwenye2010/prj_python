import configparser

try:
    config=configparser.ConfigParser()
    config.read('./example.conf')
    example_setting = config.get("settings", "project").strip()
    print(example_setting)
except:
    example_setting = ''
    print("error")
    pass

import configparser
config = configparser.ConfigParser()
config['DEFAULT'] = {'ServerAliveInterval': '45', \
                    'Compression': 'yes',\
                     'CompressionLevel': '9'}
config['bitbucket.org'] = {}
config['bitbucket.org']['User'] = 'hg'
config['topsecret.server.com'] = {}
topsecret = config['topsecret.server.com']
topsecret['Port'] = '50022'     # mutates the parser
topsecret['ForwardX11'] = 'no'  # same here
config['DEFAULT']['ForwardX11'] = 'yes'
with open('example.ini', 'w') as configfile:
    config.write(configfile)



#read from config file 
config = configparser.ConfigParser()
config.sections()
config.read('example.ini')
config.sections()
config['bitbucket.org']['User']
config['DEFAULT']['Compression']
topsecret = config['topsecret.server.com']
topsecret['ForwardX11']
topsecret['Port']
for key in config['bitbucket.org']: print(key)


