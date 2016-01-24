#!/usr/bin/python

import sys
import wolframalpha
import discord
import string
import credentials
import random

# Wolfram Alpha credentials and client session
app_id = credentials.app_id
waclient = wolframalpha.Client(app_id)

# Discord client session
client = discord.Client()
client.login(credentials.username, credentials.password)

# Globals for message removal
messageHistory = set()
computemessageHistory = set()

# Fun strings for invalid queries
invalidQueryStrings = ["Nobody knows.", "It's a mystery.", "I have no idea.", "No clue, sorry!", "Im afraid I can't let you do that", "Maybe another time.", "Ask someone else.", "That is anybody's guess.", "Beats me.", "I havent the faintest idea"]

# Prints a single result pod
def printPod(channel, text, title):
    text.replace("Wolfram|Alpha", "Wolfbot")
    newmessage = client.send_message(channel, "__**" + title + ":**__\n" + "`" + text + "`")
    messageHistory.add(newmessage)


# Connection confirmation
@client.event
def on_ready():
    print('Connected!')
    print('Username: ' + client.user.name)
    print('ID: ' + client.user.id)
    print("------------------")

@client.event
def on_message(message):
    # Check if message isnt the bot and query/command exists
    if message.author.id != client.user.id:
        if message.content.startswith('!wolf'):
            if len(message.content) > 5:
                
                # Strip !wolf
                query = message.content[6:]
                
                # Clean messages
                if query == 'clean':
                    print("Command: Clean")
                    messageHistory.add(client.send_message(message.channel, "Cleaning messages."))
                    for wolfbotMessage in messageHistory:
                        client.delete_message(wolfbotMessage)   
                    messageHistory.clear()

                    for computeMessage in computemessageHistory:
                        client.edit_message(computeMessage, computeMessage.content + "Cleared output. :ok_hand:")
                    computemessageHistory.clear()

                # Kill the bot
                elif query == 'kill':
                    print("Command: Kill")
                    if message.author.id == credentials.owner_id:
                        client.send_message(message.channel, "Shutting down, bye! :wave:")
                        sys.exit()
                    else:
                        client.send_message(message.channel, "You have no power here. :clap::+1:")


                # Help
                elif query == 'help':
                    client.send_message(message.channel, ":wolf: Usage: !wolf <query|command> | !wolf+ <query|command>  :wolf:  Commands: clean | kill")

                
                # Run wolfram alpha query
                else:
                    computemessageHistory.add(client.send_message(message.channel, ":wolf: Computing '" + query + "' :computer: :thought_balloon: ..."))
                    res = waclient.query(query)
                    print("Query: " + query)
                    
                    if message.content.startswith('!wolf+'):
                         # Expanded query
                         if len(res.pods) > 0:
                             texts = ""
                             for pod in res.pods:
                                if pod.text:
                                     printPod(message.channel, pod.text, pod.title)

                             for computemessage in computemessageHistory:
                                 client.edit_message(computemessage, computemessage.content + "Finished! :checkered_flag:")                     
                         else:
                             client.send_message(message.channel, random.choice(invalidQueryStrings))
                    else:
                         # Short answer query
                         if len(res.pods) > 0:
                             texts = ""
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
                                              printPod(message.channel, pod.text, pod.title)
                                     # If no result pod is present, prints input interpretation and 1 other pod (normally contains useful answer)
                                     else:
                                         if podLimit < 2:
                                              printPod(message.channel, pod.text, pod.title)
                                              podLimit += 1

                             for computemessage in computemessageHistory:
                                 if len(res.pods)-2 != 0:
                                    client.edit_message(computemessage, computemessage.content + "Finished! :checkered_flag: (" + str(len(res.pods)-2) + " more result pods availiable, rerun query with !wolf+)")
                                 else:
                                    client.edit_message(computemessage, computemessage.content + "Finished! :checkered_flag:")
                         else:
                             client.send_message(message.channel, random.choice(invalidQueryStrings))

            else:
                client.send_message(message.channel, ":wolf: Usage: !wolf <query|command> | !wolf+ <query|command>  :wolf:  Commands: clean | kill")
                client.send_message(message.channel, ":wolf: Github: https://github.com/Isklar/WolfBot")
        
client.run()


 
 
 
 




