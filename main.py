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
    def __init__(
        self,
        name,
        mapId,
        parentSetId,
        sr,
        bpm,
        totalLength,
        hitLength,
        ar,
        cs,
        od,
        combo,
    ):
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
    return f"{m}:{s}"


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
        if message.author != self.user and message.content.startswith(
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
                description=f'**Star:** {r["DifficultyRating"]} **BPM:** {r["BPM"]} **Length:** {r["TotalLength"]} ({r["HitLength"]})\n**[Preview](https://osu-preview.jmir.ml/preview#{id})**',
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
            channel = client.get_channel(1098781180414918718)
            await channel.send(embed=embed, view=ranking())


class ranking(discord.ui.View):
    @discord.ui.button(label="Rank", row=0, style=discord.ButtonStyle.success)
    async def rank(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(
            "no way u clicked the rank button", ephemeral=True
        )
        self.stop()  # stop interaction

    @discord.ui.button(label="Love", row=0, style=discord.ButtonStyle.danger)
    async def love(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(
            "no way u clicked the love button", ephemeral=True
        )
        self.stop()

    @discord.ui.button(label="Unrank", row=0, style=discord.ButtonStyle.gray)
    async def unrank(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(
            "no way u clicked the unrank button", ephemeral=True
        )
        self.stop()

    @discord.ui.button(label="Deny", row=0, style=discord.ButtonStyle.gray)
    async def deny(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(
            "no way u clicked the deny button", ephemeral=True
        )
        self.stop()

    @discord.ui.button(
        label="Download", row=1, style=discord.ButtonStyle.gray, emoji="💾"
    )
    async def download(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await interaction.response.send_message(
            "no way u clicked the download button", ephemeral=True
        )
        self.stop()

    # @discord.ui.button(
    #    label="Preview",
    #    row=1,
    #    style=discord.ButtonStyle.link,
    #    url=message.content,
    # )
    # async def preview(self, interaction: discord.Interaction):
    #    await interaction.response.send_message(
    #        "no way u clicked the preview button", ephemeral=True
    #    )
    #    self.stop()


intents = discord.Intents.default()
intents.message_content = True
client = Client(command_prefix="!!", intents=intents)
client.run(os.getenv("TOKEN"))
