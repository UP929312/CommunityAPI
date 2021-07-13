import discord
from discord.ext import commands

import requests

from utils import error, hf
from parse_profile import get_profile_data

with open('text_files/hypixel_api_key.txt') as file:
    API_KEY = file.read()

EMOJI_DICT = {
    "farming": "<:farming:832359758404386897>",
    "mining": "<:mining:832359758631272498>",
    "combat": "<:combat:832359758659977226>",
    "foraging": "<:foraging:832359758694187048>",
    "fishing": "<:fishing:832359758635597834>",
    "enchanting": "<:enchanting:832359758329020417>",
    "alchemy": "<:alchemy:832359758236876832>",
    "taming": "<:taming:832360479300648961>",
    "carpentry": "<:carpentry:832359758635597875>",
    "runecrafting": "<:runecrafting:832359758442004551>",

    "catacombs": "<:catacombs:864618274900410408>",
    "healer": "<:healer:864611797037350932>",
    "mage": "<:mage:864611797042331699>",
    "berserker": "<:berserker:864611797088075796>",
    "archer": "<:archer:864611797038530590>",
    "tank": "<:tank:864611797033156629>",
    
    "revenant": "<:zombie:832251786316349490>",
    "tarantula": "<:spider:832251785820504075>",
    "sven": "<:wolf:832251786059579473>",
    "enderman": "<:enderman:860902315347148801>",
}
PAGE_URLS = {"skills":   ["mining", "foraging", "enchanting", "farming", "combat", "fishing", "alchemy", "taming", "carpentry"],
             "dungeons": ["healer", "mage", "berserker", "archer", "tank"],
             "slayers":  ["revenant", "tarantula", "sven", "enderman"],}

PAGE_TO_EMOJI = {"main": "",
                 "slayers": "<:slayers:864588648111276072>",
                 "skills": "<:skills:864588638066311200>",
                 "dungeons": "<:dungeons:864588623394897930>",}

EMOJI_TO_PAGE = dict((v,k) for k,v in PAGE_TO_EMOJI.items())

class MenuButton(discord.ui.Button['MenuView']):
    def __init__(self, page: str):
        super().__init__(style=discord.ButtonStyle.blurple, emoji=PAGE_TO_EMOJI[page], row=0)
        self.page = page

    async def callback(self, interaction: discord.Interaction):
        view: MenuView = self.view
        if view.context.author.id == interaction.user.id or interaction.user.id == 244543752889303041:
            view.page = EMOJI_TO_PAGE[f"<:{self.emoji.name}:{self.emoji.id}>"]

            for child in self.view.children:
                child.disabled = False
            self.disabled = True
            
            await self.view.update_embed(interaction)
        else:
            await interaction.response.send_message("This isn't your command!\nYou can run this command yourself to change the pages!", ephemeral=True)
        

class MenuView(discord.ui.View):
    def __init__(self, context, data, username: str):
        super().__init__()
        self.context = context
        self.page = "main"
        self.data = data
        self.username = username

        for page in PAGE_URLS.keys():
            self.add_item(MenuButton(page))

    async def update_embed(self, interaction: discord.Interaction):
        embed = generate_page(self.context, self.data, self.username, self.page)
        await interaction.response.edit_message(content="", view=self, embed=embed)

    async def on_timeout(self):
        try:
            for button in self.children:
                button.disabled = True
            await self.message.edit(view=self)
        except discord.errors.NotFound:
            print("Message to disable buttons on was deleted (/weights)")

def generate_page(ctx, response, username, page):
    if page == "main":
        embed = discord.Embed(title=f"{page.title()} weights for {username}:", description=f"Click the buttons to start",
                          url=f"https://sky.shiiyu.moe/stats/{username}", colour=0x3498DB)
        embed.set_thumbnail(url=f"https://mc-heads.net/head/{username}")
        embed.set_footer(text=f"Command executed by {ctx.author.display_name} | Community Bot. By the community, for the community.")
        return embed

    data_start = response["data"][page]
    data = response["data"][page]
    total_weight = round(data["weight"]+data["weight_overflow"], 2)

    bank = PAGE_URLS[page]
    if page == "skills":
        description_start = f"Skill average: **{round(data['average_skills'], 2)}**"
    elif page == "slayers":
        description_start = f"Total coins spent: **{hf(data['total_coins_spent'])}**"
    elif page == "dungeons":
        description_start = f"Secrets found: **{data['secrets_found']}**"

    data = data.get("bosses", None) or data.get("classes", None) or data  # Remap data to be the sub list.

    embed = discord.Embed(title=f"{page.title()} weights for {username}:", description=f"Total {page[:-1]} weight: **{round(total_weight, 2)}**\n{description_start}",
                          url=f"https://sky.shiiyu.moe/stats/{username}", colour=0x3498DB)

    if page == "dungeons":
        catacombs_weight = round(data_start['types']['catacombs']['weight'], 2)
        catacombs_overflow = round(data_start['types']['catacombs']['weight_overflow'], 2)
        embed.add_field(name=f"{EMOJI_DICT['catacombs']} Cata ({round(data_start['types']['catacombs']['level'])})",
                        value=f"Regular: **{catacombs_weight}**\nOverflow: **{catacombs_overflow}**\nTotal: **{round(catacombs_weight+catacombs_overflow, 2)}**", inline=True)

    for category in bank:
        level = round(data[category]["level"])
        regular = round(data[category]["weight"], 2)
        overflow = round(data[category]["weight_overflow"], 2)
        embed.add_field(name=f"{EMOJI_DICT[category]} {category.title()} ({level})",
                        value=f"Regular: **{regular}**\nOverflow: **{overflow}**\nTotal: **{round(regular+overflow, 2)}**", inline=True)           

    if page == "dungeons":
        embed.add_field(name='\u200b', value='\u200b', inline=True)            
    
    embed.set_thumbnail(url=f"https://mc-heads.net/head/{username}")
    embed.set_footer(text=f"Command executed by {ctx.author.display_name} | Community Bot. By the community, for the community.")
    return embed
    

class weights_cog(commands.Cog):
    def __init__(self, bot):
        self.client = bot

    @commands.command(aliases=['weight', 'w', 'waits'])
    async def weights(self, ctx, username=None):

        player_data = await get_profile_data(ctx, username)
        if player_data is None:
            return
        username = player_data["username"]

        response = requests.get(f"https://hypixel-api.senither.com/v1/profiles/{player_data['uuid']}/weight?key={API_KEY}").json()
        if response["status"] != 200:
            return await error(ctx, "Error, the api couldn't fulfill this request.", "As this is an external API, CommunityBot cannot fix this for now. Please try again later.")

        main_embed = generate_page(ctx, response, username, "main")
        
        view = MenuView(context=ctx, data=response, username=username)
        view.message = await ctx.send(embed=main_embed, view=view)
