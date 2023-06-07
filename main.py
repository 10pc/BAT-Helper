import discord
import os
import requests
#commit
client = discord.Client()

@client.event
async def on_ready():
  print('{0.user} says hi'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  if message.content.startswith('https://osu.ppy.sh/'):
    if (message.channel.id == 1115863989612728381):
      url = message.content.split("/")
      id = url[-1]
      r = requests.get(f"https://api.chimu.moe/v1/map/{id}")
      r = r.json()
      mapName = r["OsuFile"]
      
      embed=discord.Embed(description=f'**Star:** {r["DifficultyRating"]} **BPM:** {r["BPM"]} **Length:** {r["TotalLength"]} ({r["HitLength"]})\n**[Preview](https://osu-preview.jmir.ml/preview#{id})**')
      embed.set_author(name=mapName[:len(mapName) - 4], url=message.content)
      embed.add_field(name="", value=f'**AR:** {r["AR"]} ● **CS:** {r["CS"]} ● **OD:** {r["OD"]}\n**Max Combo:** {r["MaxCombo"]}x', inline=True)
      embed.set_image(url=f'https://assets.ppy.sh/beatmaps/{r["ParentSetId"]}/covers/cover.jpg')
      await message.channel.send(embed=embed)

try:
  client.run(os.environ["TOKEN"])
except discord.HTTPException as e:
  if e.status == 429:
    print("skill issue")
  else:
    raise e