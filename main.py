import discord
from discord.ext import commands
import os
import requests


class mapList:
  def __init__(self, db=[]):
    self.db = db

  def newMap(self, map):
    self.db.append(map)


class map:
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
  return f"{m}:{s:02}"


class Client(commands.Bot):
  async def on_ready(self):
    print(
      f"""
    {self.user} says hi! 
    ID: {self.user.id} 
    Latency: {self.latency * 1000:.0f}ms 
    Connected to {len(self.guilds)} guilds with {len(self.users)} users.
    """
    )

  async def on_message(self, message):
    if message.author != self.user and message.channel.id == '1115863989612728381' and message.content.startswith(
      "https://osu.ppy.sh/"
    ):
      url = message.content.split("/")
      id = url[-1]
      r = requests.get(f"https://api.chimu.moe/v1/map/{id}")
      r = r.json()
      mapName = r["OsuFile"]
      totalL = sec(r["TotalLength"])
      hitL = sec(r["HitLength"])

      ls.newMap(
        map(
          mapName,
          id,
          r["ParentSetId"],
          r["DifficultyRating"],
          r["BPM"],
          totalL,
          hitL,
          r["AR"],
          r["CS"],
          r["OD"],
          r["MaxCombo"],
        )
      )

      success = discord.Embed(
        description="BN's have been notified, please wait.", color=0x00FF40
      )
      success.set_author(name="Request sent!")
      await message.channel.send(embed=success)

      embed = discord.Embed(
        title=mapName[: len(mapName) - 4],
        url=message.content,
        description=f'**Star:** {r["DifficultyRating"]:.2f} **BPM:** {r["BPM"]} **Length:** {totalL} ({hitL})',
        color=0x0C0AA4,
      )
      embed.set_author(name="New request!")
      embed.add_field(
        name="",
        value=f'**AR:** {r["AR"]} **CS:** {r["CS"]} **OD:** {r["OD"]}\n**Max Combo:** {r["MaxCombo"]}x',
        inline=True,
      )
      embed.set_image(
        url=f'https://assets.ppy.sh/beatmaps/{r["ParentSetId"]}/covers/cover.jpg'
      )

      class ranking(discord.ui.View):
        def __init__(self):
          super().__init__(timeout=None)

          preview = discord.ui.Button(row=1, label='Preview', style=discord.ButtonStyle.gray, url=f'https://osu-preview.jmir.ml/preview#{id}')
          download = discord.ui.Button(row=1, label='Download', style=discord.ButtonStyle.gray, url=f'https://api.chimu.moe/v1{r["DownloadPath"]}')
          self.add_item(preview)
          self.add_item(download)
        
        @discord.ui.button(label="Rank", row=0, style=discord.ButtonStyle.success)
        async def rank(self, interaction: discord.Interaction, button: discord.ui.Button):
          await interaction.response.send_message(
            "no way u clicked the rank button", ephemeral=True
          )

        @discord.ui.button(label="Love", row=0, style=discord.ButtonStyle.danger)
        async def love(self, interaction: discord.Interaction, button: discord.ui.Button):
          await interaction.response.send_message(
            "no way u clicked the love button", ephemeral=True
          )

        @discord.ui.button(label="Unrank", row=0, style=discord.ButtonStyle.primary)
        async def unrank(self, interaction: discord.Interaction, button: discord.ui.Button):
          await interaction.response.send_message(
            "no way u clicked the unrank button", ephemeral=True
          )

        @discord.ui.button(label="Deny", row=0, style=discord.ButtonStyle.gray)
        async def deny(self, interaction: discord.Interaction, button: discord.ui.Button):
          await interaction.response.send_message(
            "no way u clicked the deny button", ephemeral=True
          )
          
      c = client.get_channel(1059771218271678524)
      await c.send(embed=embed, view=ranking())

    if message.author != self.user and message.content.startswith(
      "t"
    ):
      login = 'https://kap.kawata.pw/login'
      load = 'https://kap.kawata.pw/rank'

      payload = {
        'username': '10pc',
        'password': 'notmypassowrd'
      }

      s = requests.session() 
      response = s.post(login, data=payload) 
      await message.channel.send(response.text)

intents = discord.Intents.default()
intents.message_content = True
client = Client(command_prefix="!!", intents=intents)
client.run(os.getenv("TOKEN"))
