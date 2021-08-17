import discord

class PresetMenuButton(discord.ui.Button['MenuView']):
    def __init__(self, emoji: str, index: int, disabled: bool):
        super().__init__(style=discord.ButtonStyle.blurple, emoji=emoji, row=index//5, disabled=disabled)

    async def callback(self, interaction: discord.Interaction):
        view: PresetMenuView = self.view
        if view.context.author.id == interaction.user.id or interaction.user.id == 244543752889303041:
            view.page: str = self.view.emoji_map_reversed[f"<:{self.emoji.name}:{self.emoji.id}>"]

            for child in self.view.children:
                child.disabled: bool = False
            self.disabled: bool = True
            
            await self.view.update_embed(interaction)
        else:
            await interaction.response.send_message("This isn't your command!\nYou can run this command yourself to change the pages!", ephemeral=True)
        

class PresetMenuView(discord.ui.View):
    def __init__(self, context, data, username: str, emoji_map: dict, page_generator):
        super().__init__()
        self.context = context
        self.page: str = "main"
        self.data = data
        self.username: str = username
        self.emoji_map: dict = emoji_map
        self.emoji_map_reversed: dict = dict((v,k) for k,v in emoji_map.items())
        self.page_generator = page_generator

        for i, page in enumerate(emoji_map.keys()):
            self.add_item(PresetMenuButton(emoji=emoji_map[page], index=i, disabled=(i==0) ))

    async def update_embed(self, interaction: discord.Interaction):
        embed = self.page_generator(self.context, self.data, self.username, self.page)
        await interaction.response.edit_message(view=self, embed=embed)

    async def on_timeout(self):
        try:
            for button in self.children:
                button.disabled: bool = True
            await self.message.edit(view=self)
        except discord.errors.NotFound:
            pass

async def generate_preset_menu(ctx, data, username, starting_page, emoji_map, page_generator):
    
    main_embed = page_generator(ctx=ctx, data=data, username=username, page=starting_page)
    view = PresetMenuView(context=ctx, data=data, username=username, emoji_map=emoji_map, page_generator=page_generator)
    view.message = await ctx.send(embed=main_embed, view=view)


"""
Instructions on how to use Preset Menus, V2:
Call the generate_menu function with `await`, giving the context object (ctx),
any data, the username, or None, starting page, probably "main" or 1, the emoji map
(a dict mapping page names to emojis), and a function to take the data and display it as an embed.
"""

SCROLLING_EMOJIS = {
    "\U000023ea": lambda page, list_of_embeds: 1,
    "\U00002b05": lambda page, list_of_embeds: page-1,
    "\U000023fa": lambda page, list_of_embeds: int(len(list_of_embeds)/2),
    "\U000027a1": lambda page, list_of_embeds: page+1,
    "\U000023e9": lambda page, list_of_embeds: len(list_of_embeds),
}

SCROLLING_EMOJIS = {
    "<:rewind:876491533451427951>": lambda page, middle, last: 1,
    "<:left_arrow:876505406980116541>": lambda page, middle, last: page-1,
    "<:middle:876491600296050740>": lambda page, middle, last: middle,
    "<:right_arrow:876505406501949472>": lambda page, middle, last: page+1,
    "<:fast_forward:876491622311952394>": lambda page, middle, last: last,
}
  
START_DISABLED = list(SCROLLING_EMOJIS.keys())[:2]

class ScrollingMenuButton(discord.ui.Button['MenuView']):
    def __init__(self, emoji: str, middle: int, last: int):
        super().__init__(style=discord.ButtonStyle.blurple, emoji=emoji, disabled=emoji in START_DISABLED)
        self.middle = middle
        self.last = last

    async def callback(self, interaction: discord.Interaction):
        view: ScrollingMenuView = self.view
        if view.ctx.author.id == interaction.user.id or interaction.user.id == 244543752889303041:
            view.page: int = SCROLLING_EMOJIS[f"{self.emoji}"](view.page, self.middle, self.last)

            # Enable all buttons
            for button in self.view.children:
                button.disabled: bool = False

            if view.page <= 1:
                # If we're on page 1, disable going left (previous pages)
                for button in self.view.children[:2]:
                    button.disabled: bool = True
            elif view.page >= self.last:
                # If we're on the last page, disable going forward (next pages)
                for button in self.view.children[-2:]:
                    button.disabled: bool = True
            
            await self.view.update_embed(interaction)
        else:
            await interaction.response.send_message("This isn't your command!\nYou can run this command yourself to change the pages!", ephemeral=True)
        

class ScrollingMenuView(discord.ui.View):
    def __init__(self, ctx, list_of_embeds):
        super().__init__()
        self.ctx = ctx
        self.list_of_embeds: list = list_of_embeds
        self.page: int = 1

        middle = int(len(list_of_embeds)/2)
        last = len(list_of_embeds)
        for emoji in SCROLLING_EMOJIS.keys():
            self.add_item(ScrollingMenuButton(emoji=emoji, middle=middle, last=last))

    async def update_embed(self, interaction: discord.Interaction):
        embed: discord.Embed = self.list_of_embeds[self.page-1]
        await interaction.response.edit_message(view=self, embed=embed)

    async def on_timeout(self):
        try:
            for button in self.children:
                button.disabled: bool = True
            await self.message.edit(view=self)
        except discord.errors.NotFound:
            pass


async def generate_scrolling_menu(ctx, list_of_embeds):
    
    view = ScrollingMenuView(ctx=ctx, list_of_embeds=list_of_embeds)
    view.message = await ctx.send(embed=list_of_embeds[0], view=view)

"""
Instructions on how to use scrolling menus:
Call the function `generate_scrolling_menu` with context and a list of embeds
you want to cycle through.
It must be called with await
"""

class DynamicScrollingMenuView(discord.ui.View):
    def __init__(self, ctx, data, page_generator):
        super().__init__()
        self.ctx = ctx
        self.data: list = data
        self.page: int = 1
        self.page_generator = page_generator

        middle = int((len(data)/2)/10)  # We give it 100 items, but 10 per page
        last = int(len(data)/10)
        for emoji in SCROLLING_EMOJIS.keys():
            self.add_item(ScrollingMenuButton(emoji=emoji, middle=middle, last=last))

    async def update_embed(self, interaction: discord.Interaction):
        embed: discord.Embed = await self.page_generator(self.ctx, self.data, self.page)
        await interaction.response.edit_message(view=self, embed=embed)

    async def on_timeout(self):
        try:
            for button in self.children:
                button.disabled: bool = True
            await self.message.edit(view=self)
        except discord.errors.NotFound:
            pass


async def generate_dynamic_scrolling_menu(ctx, data, page_generator):
    starting_embed: discord.Embed = await page_generator(ctx=ctx, data=data, page=1)
    view: discord.ui.View = DynamicScrollingMenuView(ctx=ctx, data=data, page_generator=page_generator)
    view.message: discord.Message = await ctx.send(embed=starting_embed, view=view)

"""
Instructions on how to use dynamic scrolling menus:
Call the function `generate_dynamic_scrolling_menu` with context, the data (groups of 10),
and the function that formats each page, call it with await
"""
