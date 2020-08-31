import discord, threading, requests, time

client = discord.Client()
lastTimeBrianWasAssigned = time.time()
timeToWaitBetweenBrians = 20 * 60
messageMustContain = ["brian", "please"]


@client.event
async def on_ready():   
    print('Logged in as')
    print(client.user.name)


async def removeAllBrians(brianRole):
    for member in brianRole.members:
        await member.remove_roles(brianRole)

async def addUserToBrian(user, brianRole):
    await user.add_roles(brianRole)

def containsAllKeywords(message):
    global messageMustContain

    contAll = True
    for word in messageMustContain:
        if message.find(word) >= 0:
            pass
        else:
            contAll = False

    return contAll

@client.event        
async def on_message(message):
    global timeToWaitBetweenBrians, lastTimeBrianWasAssigned
    channel = message.channel
    user = message.author
    guild = message.guild

    brianRole = discord.utils.get(guild.roles, id = int(267495672041832448))
        
    if str(channel) == "asking-for-brian" and containsAllKeywords(message.content):
        if time.time() - lastTimeBrianWasAssigned > timeToWaitBetweenBrians:
            await removeAllBrians(brianRole)
            await addUserToBrian(user, brianRole)
            lastTimeBrianWasAssigned = time.time()
            await channel.send("The new Brian is " + str(user.nick))
            print("assigned new brian to:" + str(user.nick))
            #say who lost it and who gained it
        else:
            pass
            print("didnt wait long enough")
            secondsToWait = round(timeToWaitBetweenBrians - (time.time() - lastTimeBrianWasAssigned), 2)
            if secondsToWait > 60:
                await channel.send("You must wait another " + str(round(secondsToWait/60, 2)) + " minutes")
            else:
                await channel.send("You must wait another " + str(secondsToWait) + " seconds")
            #say how much more time must be waited

client.run('NzQ5ODIzMzE1MjA3NTIwMzM3.X0xlYQ.FhPaHuRPb25sO5JbKR6gJHLI_f')
