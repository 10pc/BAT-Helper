import discord
import os
import requests

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

class mapList():
  def __init__(self, db = []):
    self.db = db
    
  def newMap(self, map):
    self.db.append(map)

class map():
  def __init__(self, name, mapId, parentSetId, sr, bpm, totalLength, hitLength, ar, cs, od, combo):
    self.name = name
    self.mapId = mapId
    self.parentSetId = parentSetId
    self.sr = sr
    self.bpm = bpm
    self.totalLength = totalLength
    self.hitLength = hitLength
    self.ar = ar
    self.cs = cs
    self.od = od
    self.combo = combo

ls = mapList()

def sec(seconds):
  m = seconds // 60
  s = seconds % 60
  return f'{m}:{s}'

@client.event
async def on_ready():
  print('{0.user} says hi'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  if message.content.startswith('https://osu.ppy.sh/'):
    url = message.content.split("/")
    id = url[-1]
    r = requests.get(f"https://api.chimu.moe/v1/map/{id}")
    r = r.json()
      
    mapName = r["OsuFile"]
    totalL = sec(r["TotalLength"])
    hitL = sec(r["HitLength"])

    ls.newMap(map(mapName, id, r["ParentSetId"], r["DifficultyRating"], r["BPM"], totalL, hitL, r["AR"], r["CS"], r["OD"], r["MaxCombo"]))

    success = discord.Embed(description = "BN's have been notified, please wait.", color = 0x00ff40)
    success.set_author(name = "Request sent!")
    await message.channel.send(embed=success)
    
    embed = discord.Embed(title = mapName[:len(mapName) - 4], url=message.content, description=f'**Star:** {r["DifficultyRating"]} **BPM:** {r["BPM"]} **Length:** {r["TotalLength"]} ({r["HitLength"]})\n**[Preview](https://osu-preview.jmir.ml/preview#{id})**', color = 0x0c0aa4)
    embed.set_author(name = "New request!")
    embed.add_field(name="", value=f'**AR:** {r["AR"]} **CS:** {r["CS"]} **OD:** {r["OD"]}\n**Max Combo:** {r["MaxCombo"]}x', inline=True)
    embed.set_image(url=f'https://assets.ppy.sh/beatmaps/{r["ParentSetId"]}/covers/cover.jpg')
      
    c = client.get_channel(1059771218271678524)
    await c.send(embed = embed)

client.run(os.environ["TOKEN"])