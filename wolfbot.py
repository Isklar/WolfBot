#!/usr/bin/python

import sys
import string
import random
import wolframalpha
import discord
import asyncio
import credentials
import re

# Regex for IP address
ipv4_regex = re.compile(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b')
ipv6_regex = re.compile(r'(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))')

# Wolfram Alpha credentials and client session
app_id = credentials.app_id
waclient = wolframalpha.Client(app_id)

# Discord client session
client = discord.Client()
client.login(credentials.username, credentials.password)

# Globals for message removal
messageHistory = set()
computemessageHistory = set()
previousQuery = ""

# Fun strings for invalid queries
invalidQueryStrings = ["Nobody knows.", "It's a mystery.", "I have no idea.", "No clue, sorry!", "I'm afraid I can't let you do that.", "Maybe another time.", "Ask someone else.", "That is anybody's guess.", "Beats me.", "I haven't the faintest idea."]

# Prints a single result pod
async def printPod(channel, text, title):
    text = text.replace("Wolfram|Alpha", "Wolfbot")
    text = text.replace("Wolfram", "Wolf")
    text = re.sub(ipv4_regex, "IP Redacted", text)
    text = re.sub(ipv6_regex, "IP Redacted", text)
    newmessage = await client.send_message(channel, "__**" + title + ":**__\n" + "`" + text + "`")
    messageHistory.add(newmessage)

# Prints a single image pod
async def printImgPod(channel, img, title):
#    img = img.encode('ascii', 'ignore')
    newmessage = await client.send_message(channel, "__**" + title + ":**__\n" + img)
    messageHistory.add(newmessage)

# Connection confirmation
@client.event
async def on_ready():
    print('Connected!')
    print('Username: ' + client.user.name)
    print('ID: ' + client.user.id)
    print("------------------")

@client.event
async def on_message(message):
    # Check if message isnt the bot and query/command exists
    if message.author.id != client.user.id:
        if message.content.startswith('!wolf'):
            if len(message.content) > 5:

                # Strip !wolf
                query = message.content[6:]
                
                # Purge messages
                # Deletes all messages sent by the bot and delete !wolf calls if the bot has perms
                if query == 'purge':
                    print(message.author.name + " | Command: Purge")
                    if message.author.id == credentials.owner_id:
                        await client.send_message(message.channel, "Purging messages.")

                        async for historicMessage in client.logs_from(message.channel):
                                if historicMessage.author == client.user:
                                    await client.delete_message(historicMessage)
                                if historicMessage.content.startswith('!wolf'):
                                    try:
                                       await client.delete_message(historicMessage)
                                    except:
                                       print('Error: Cannot delete messages!')
                
                # Clean messages
                elif query == 'clean':
                    print(message.author.name + " | Command: Clean")
                    messageHistory.add(await client.send_message(message.channel, "Cleaning messages."))
                    for wolfbotMessage in messageHistory:
                        await client.delete_message(wolfbotMessage)   
                    messageHistory.clear()

                    for computeMessage in computemessageHistory:
                        await client.edit_message(computeMessage, computeMessage.content + "Cleared output. :ok_hand:")
                    computemessageHistory.clear()

                # Kill the bot
                elif query == 'kill':
                    print(message.author.name + " | Command: Kill")
                    if message.author.id == credentials.owner_id:
                        await client.send_message(message.channel, "Shutting down, bye! :wave:")
                        sys.exit()
                    else:
                        await client.send_message(message.channel, "You have no power here. :clap::+1:")


                # Help
                elif query == 'help':
                    await client.send_message(message.channel, ":wolf: Usage: !wolf <query|command> | !wolf+ <query|command>  :wolf:  Commands: clean | kill")

                
                # Run wolfram alpha query
                else:
                    queryComputeMessage = await client.send_message(message.channel, ":wolf: Computing '" + query + "' :computer: :thought_balloon: ...")
                    computemessageHistory.add(queryComputeMessage)
                    
                    print(message.author.name + " | Query: " + query)
                    
                    if message.content.startswith('!wolf+'):
                         # Expanded query
                         if len(query) > 1:
                             res = waclient.query(query)
                             if len(res.pods) > 0:
                                 for pod in res.pods:
                                      if pod.text:
                                         await printPod(message.channel, pod.text, pod.title)
                                      elif pod.img:
                                         await printImgPod(message.channel, pod.img, pod.title)

                                 await client.edit_message(queryComputeMessage, queryComputeMessage.content + "Finished! " + message.author.mention + " :checkered_flag:")
                             else:
                                 await client.send_message(message.channel, random.choice(invalidQueryStrings))
                         else:
                             if len(res.pods) > 0:
                                 res = waclient.query(previousQuery)
                                 for pod in res.pods:
                                      if pod.text:
                                         await printPod(message.channel, pod.text, pod.title)
                                      elif pod.img:
                                         await printImgPod(message.channel, pod.img, pod.title)

                                 await client.edit_message(queryComputeMessage, queryComputeMessage.content + "Finished! " + message.author.mention + " :checkered_flag:")
                    else:
                         # Short answer query
                         res = waclient.query(query)
                         if len(res.pods) > 0:
                             resultPresent = 0
                             podLimit = 0

                             # WA returns a "result" pod for simple maths queries but for more complex ones it returns randomly titled ones
                             for pod in res.pods:
                                if pod.title == 'Result':
                                    resultPresent = 1

                             for pod in res.pods:
                                if pod.text:
                                     if resultPresent == 1:
                                         if pod.title == 'Result':
                                              await printPod(message.channel, pod.text, pod.title)
                                     # If no result pod is present, prints input interpretation and 1 other pod (normally contains useful answer)
                                     else:
                                         if podLimit < 2:
                                              await printPod(message.channel, pod.text, pod.title)
                                              podLimit += 1
                         else:
                             await client.send_message(message.channel, random.choice(invalidQueryStrings))
                             
                         if len(res.pods)-2 > 0:
                            await client.edit_message(queryComputeMessage, queryComputeMessage.content + "Finished! " + message.author.mention + " :checkered_flag: (" + str(len(res.pods)-2) + " more result pods available, rerun query with !wolf+)")
                         else:
                            await client.edit_message(queryComputeMessage, queryComputeMessage.content + "Finished! " + message.author.mention + " :checkered_flag:")
                    previousQuery = query
            
            else:
                await client.send_message(message.channel, ":wolf: Usage: !wolf <query|command> | !wolf+ <query|command>  :wolf:  Commands: clean | kill")
                await client.send_message(message.channel, ":wolf: Github: https://github.com/Isklar/WolfBot")
        
client.run(credentials.username, credentials.password)


 
 
 
 




