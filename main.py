import discord
import json
import re


startup = True
client = discord.Client()

stand_names = None
stylized_stand_names = []

with open('standnames.txt', 'r') as read_file:
    stand_names = read_file.readlines()
    stand_names = [i[:-1] for i in stand_names]

for i in stand_names:
    stylized_stand_name = "「"
    for j in i:
        stylized_stand_name += j + " "
    stylized_stand_name = stylized_stand_name[:-1]
    stylized_stand_name += "」"
    stylized_stand_names.append(stylized_stand_name)

with open('config.json', 'r') as read_file:
    config = json.load(read_file)


# add each command as a static method to this class
class Commands:
    @staticmethod
    async def test(params, message):
        await message.channel.send("Hello")
    
    @staticmethod
    async def general(message):
        
        global client

        content = message.content

        for stand_name, stylized_stand_name in zip(stand_names, stylized_stand_names):
            content = re.sub(stand_name, stylized_stand_name, content, flags=re.IGNORECASE)
        
        print(dir(message))

        if content != message.content:
            await message.channel.send(content)


@client.event
async def on_ready():
    global startup
    if startup:
        print('Logged in as')
        print(client.user.name)
        print(client.user.id)
        print('------')

@client.event
async def on_message(message):
    if (message.content.startswith(config['trigger'])):
        content = message.content.replace(config['trigger'], '', 1).split(' ')
        command = content[0]
        params = []
        if len(content) > 1:
            params = content[1:]
        try:
            await getattr(Commands, command)(params, message)
        except AttributeError:
            await message.channel.send("'" + command + "' is not a command" +
                                       ", use 'help' to get a list of commands")
    else:
        await Commands.general(message)

if __name__ == "__main__":
    client.run(config['token'])
