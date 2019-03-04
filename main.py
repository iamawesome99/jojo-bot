import discord
import json


startup = True
client = discord.Client()

with open('config.json', 'r') as read_file:
    config = json.load(read_file)


# add each command as a static method to this class
class Commands:
    @staticmethod
    async def test(params, message):
        await message.channel.send("Hello")
    
    @staticmethod
    async def general(message):
        pass


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
        Commands.general(message)

if __name__ == "__main__":
    client.run(config['token'])