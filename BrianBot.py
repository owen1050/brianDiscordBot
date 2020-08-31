import discord, threading, requests, time

client = discord.Client()
lastTimeBrianWasAssigned = time.time()
timeToWaitBetweenBrians = 5
messageMustContain = ["brian", "please"]
lastUser = None
firstTime = True
leaderboard = {}
channelText = "asking-for-brian"

f = open("leaderboard.txt", "r")
leadText = f.read()
f.close()

while leadText.find("\n") >0:
    eolI = leadText.find("\n")
    line = leadText[0:eolI]

    colI = line.find(":")
    name = line[:colI]
    time = line[colI+1:]

    leaderboard[name] = float(time)
    print(name, time)
    leadText = leadText[eolI + 1:]


@client.event
async def on_ready():   
    print('Logged in as')
    print(client.user.name)


async def removeAllBrians(brianRole):
    lastMem = None
    for member in brianRole.members:
        lastMem = member
        await member.remove_roles(brianRole)
    return lastMem

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

def leaderboardToText():
    global leaderboard
    retStr = ""
    for mem in leaderboard:
        totalTime = round(leaderboard[mem]/3600, 2)
        retStr = retStr + mem + " " * (40-len(mem))+ str(totalTime) + " hours\n"

    return retStr

def updateLeaderboardTxt():
    global leaderboard
    outStr = ""
    for member in leaderboard:
        outStr = outStr + str(member) + ":" + str(leaderboard[member]) + "\n"
    f = open("leaderboard.txt", "w")
    f.write(outStr)
    f.close()


@client.event        
async def on_message(message):
    global timeToWaitBetweenBrians, lastTimeBrianWasAssigned, lastUser, leaderboard, firstTime, channelText
    channel = message.channel
    user = message.author
    guild = message.guild
    print("message")
    brianRole = discord.utils.get(guild.roles, id = int(750022258432671935))
    
    if str(channel) == channelText and str(message.content).find("leaderboard") >= 0:
        await channel.send(leaderboardToText())

    if str(channel) == channelText and containsAllKeywords(message.content):
        if time.time() - lastTimeBrianWasAssigned > timeToWaitBetweenBrians:
            lastMem = await removeAllBrians(brianRole)
            await addUserToBrian(user, brianRole)
            
            await channel.send("The new Brian is " + str(user.nick))
            print("assigned new brian to:" + str(user.nick))

            if firstTime:
                firstTime = False
            else:
                if lastMem in leaderboard:
                    leaderboard[lastMem] = leaderboard[lastMem] + (time.time() - lastTimeBrianWasAssigned)
                else:
                    leaderboard[lastMem] = (time.time() - lastTimeBrianWasAssigned)

            updateLeaderboardTxt()
            lastUser = user
            lastTimeBrianWasAssigned = time.time()
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
