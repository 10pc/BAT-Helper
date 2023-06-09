import discord
from discord.ext import commands
import os
import requests
from Panel import *
from typing import Tuple, Union

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
    if message.author != self.user and message.channel.id == 598986787632709652 and (message.content.startswith("https://osu.ppy.sh/b/") or message.content.startswith("https://osu.ppy.sh/beatmapsets/")):
      url = message.content.split("/")
      if message.content.startswith("https://osu.ppy.sh/beatmapsets/") and len(url) < 6:
        fail = discord.Embed(description="Nu uh, that's a mapset link.\nPlease provide a map link instead.", color=0x00FF40)
        fail.set_author(name="Oops")
        await message.channel.send(embed=fail)
      else:
        id = url[-1]
        r = requests.get(f"https://api.chimu.moe/v1/map/{id}")
        r = r.json()
        mapName = r["OsuFile"]
        totalL = sec(r["TotalLength"])
        hitL = sec(r["HitLength"])

        theBot = self.user
        
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
        await message.channel.send(embed=success, delete_after=5)

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
            download = discord.ui.Button(row=1, label='Download', style=discord.ButtonStyle.gray, url=f'https://api.chimu.moe/v1{r["DownloadPath"]}') # type: ignore
            self.add_item(preview)
            self.add_item(download)
        
          @discord.ui.button(label="Rank", row=0, style=discord.ButtonStyle.success)
          async def rank(self, interaction: discord.Interaction, button: discord.ui.Button):
              login_modal = Login()
              await interaction.response.send_modal(login_modal)
              await login_modal.wait()
              await interaction.followup.send("Logging in...", ephemeral=True)
              submitted_username = login_modal.username
              submitted_password = login_modal.password
              usersession = Panel()
              await interaction.followup.send(usersession.login(submitted_username, submitted_password), ephemeral=True) #type: ignore
              await interaction.followup.send(usersession.rank_map(id), ephemeral=True) #type: ignore
              await interaction.followup.send(usersession.logout(), ephemeral=True)
              await interaction.followup.send(f'`https://osu.ppy.sh/b/{id}`\nRanked by {submitted_username}')
              await message.add_reaction('✅')
              await rankingPage.delete()

          @discord.ui.button(label="Love", row=0, style=discord.ButtonStyle.danger)
          async def love(self, interaction: discord.Interaction, button: discord.ui.Button):
              login_modal = Login()
              await interaction.response.send_modal(login_modal)
              await login_modal.wait()
              await interaction.followup.send("Logging in...", ephemeral=True)
              submitted_username = login_modal.username
              submitted_password = login_modal.password
              usersession = Panel()
              await interaction.followup.send(usersession.login(submitted_username, submitted_password), ephemeral=True) #type: ignore
              await interaction.followup.send(usersession.love_map(id), ephemeral=True) #type: ignore
              await interaction.followup.send(usersession.logout(), ephemeral=True)
              await interaction.followup.send(f'`https://osu.ppy.sh/b/{id}`\nLoved by {submitted_username}')
              await message.add_reaction('❤️')
              await rankingPage.delete()

          @discord.ui.button(label="Unrank", row=0, style=discord.ButtonStyle.primary)
          async def unrank(self, interaction: discord.Interaction, button: discord.ui.Button):
              login_modal = Login()
              await interaction.response.send_modal(login_modal)
              await login_modal.wait()
              await interaction.followup.send("Logging in...", ephemeral=True)
              submitted_username = login_modal.username
              submitted_password = login_modal.password
              usersession = Panel()
              await interaction.followup.send(usersession.login(submitted_username, submitted_password), ephemeral=True) #type: ignore
              await interaction.followup.send(usersession.unrank_map(id), ephemeral=True) #type: ignore
              await interaction.followup.send(usersession.logout(), ephemeral=True)
              await interaction.followup.send(f'`https://osu.ppy.sh/b/{id}`\nUnranked by {submitted_username}')
              await message.add_reaction('❌')
              await rankingPage.delete()
              
          @discord.ui.button(label="Deny", row=0, style=discord.ButtonStyle.gray)
          async def deny(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.send_message(
              "Denied"
            )
            await message.add_reaction('🚫')
            await rankingPage.delete()
          
        c = client.get_channel(815264398947123210)
        rankingPage = await c.send(embed=embed, view=ranking()) # type: ignore

class Login(discord.ui.Modal, title="Panel Login"):
    def __init__(self):
        super().__init__()
        self.username = None
        self.password = None
        self.username_input = discord.ui.TextInput(label="Username", placeholder="Loki", required=True)
        self.password_input = discord.ui.TextInput(label="Password", placeholder="reallysecurepassword123", required=True)
        self.add_item(self.username_input)
        self.add_item(self.password_input)

    async def on_submit(self, interaction: discord.Interaction):
        self.username = self.username_input.value
        self.password = self.password_input.value
        await super().on_submit(interaction)
        self.stop()

intents = discord.Intents.all()
intents.message_content = True
client = Client(command_prefix="!!", intents=intents)
client.run(os.getenv("krx"))
  
