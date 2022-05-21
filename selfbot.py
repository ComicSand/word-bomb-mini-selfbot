import discord
import re
import io
import time
import random
import pyperclip
import asyncio

dictionary = open("master.txt").read().splitlines()

def solve(prompt, characterRes):
    start = time.time()

    prompt = re.compile(prompt)
    solutions = []

    for word in dictionary:
        if prompt.search(word):
            if characterRes:
                if int(characterRes) == len(word):
                    solutions.append(word)
            else:
                solutions.append(word)

    return sorted(solutions), time.time() - start



def convertFromEmoji(emoji):
    if not "White" in emoji and not "Gold" in emoji:
        return False

    if "Blank" in emoji:
        return "."

    return emoji[2].lower()

def getEmojis(message):
    custom_emojis = re.findall(r'<:\w*:\d*>', message)
    return custom_emojis

def getRestriction(message):
    if not "characters" in message:
        return False

    lines = message.splitlines()

    for line in lines:
        if "characters" in line:
            return re.findall(r'\b\d+\b', line)[0]


# print(convertFromEmoji("<:BlankWhite:971179538350477342>"))

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author.id != 482315309580025886:
            return

        if not "Type a word containing" in message.content:
            return

        prompt = r""

        for emoji in getEmojis(message.content):
            realEmoji = convertFromEmoji(emoji)
            if realEmoji:
                prompt += realEmoji

        characterRestriction = getRestriction(message.content)

        print("{} | character restriction: {}".format(prompt, characterRestriction if characterRestriction else "none"))

        solver = solve(prompt, characterRestriction)
        
        solutions = solver[0]
        timeTaken = solver[1]

        await message.channel.send(max(solutions, key = len))

        print("found all solutions in {} ({} and {} more)".format(timeTaken, solutions[0], len(solutions) - 1))

client = MyClient()
client.run('OTExNDczMTEwNjM5ODYxNzkw.GSII9K.CmJKH0Ll-F9wIPGGzZ30EBC-7kEUoUUIKqs-Ok')