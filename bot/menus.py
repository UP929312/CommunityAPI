import discord  # type: ignore
from discord.ext import commands    # type: ignore

from typing import Optional  # For typing

###############################################################################
# Dynamic Preset Menus, processed the data on each button press
###############################################################################
"""
Instructions on how to use Preset Menus:
Call the generate_menu function with `await`, giving the context object (ctx),
any data, the username, or None, starting page, probably "main" or 1, the emoji map
(a dict mapping page names to emojis), and a function to take the data and display it as an embed.
"""

class DynamicPresetMenuButton(discord.ui.Button['DynamicPresetMenuView']):
    def __init__(self, emoji: str, index: int, disabled: bool):
        super().__init__(style=discord.ButtonStyle.blurple, emoji=emoji, row=index//5, disabled=disabled)

    async def callback(self, interaction: discord.Interaction):
        view: DynamicPresetMenuView = self.view
        if view.ctx.author.id == interaction.user.id or interaction.user.id == 244543752889303041:
            view.page = self.view.emoji_map_reversed[f"<:{self.emoji.name}:{self.emoji.id}>"]

            for child in self.view.children:
                child.disabled = False
            self.disabled = True
            
            await self.view.update_embed(interaction)
        else:
            await interaction.response.send_message("This isn't your command!\nYou can run this command yourself to change the pages!", ephemeral=True)
        
class DynamicPresetMenuView(discord.ui.View):
    def __init__(self, ctx, data, username: str, emoji_map: dict, page_generator):
        super().__init__()
        self.ctx: commands.Context = ctx
        self.page: str = "main"
        self.data = data
        self.username: str = username
        self.emoji_map: dict = emoji_map
        self.emoji_map_reversed: dict = dict((v,k) for k,v in emoji_map.items())
        self.page_generator = page_generator

        for i, page in enumerate(emoji_map.keys()):
            self.add_item(DynamicPresetMenuButton(emoji=emoji_map[page], index=i, disabled=(i==0) ))

    async def update_embed(self, interaction: discord.Interaction):
        embed = self.page_generator(self.context, self.data, self.username, self.page)
        await interaction.response.edit_message(view=self, embed=embed)

    async def on_timeout(self):
        try:
            for button in self.children:
                button.disabled = True
            await self.message.edit(view=self)
        except discord.errors.NotFound:
            pass

async def generate_dynamic_preset_menu(ctx: commands.Context, data, username: str, starting_page: str, emoji_map: dict, page_generator):
    main_embed = page_generator(ctx=ctx, data=data, username=username, page=starting_page)
    view = DynamicPresetMenuView(ctx=ctx, data=data, username=username, emoji_map=emoji_map, page_generator=page_generator)
    view.message = await ctx.send("\u200b", embed=main_embed, view=view)


###############################################################################
# Static Preset Menus, gets all the data prior and flicks between the preset pages
###############################################################################
"""
Instructions on how to use Static Preset Menus:
Call the generate_static_preset_menu function with `await`, giving the context object (ctx),
the list of all the premade embeds, as well as a list of emojis mapping index to the page
"""

class StaticPresetMenuButton(discord.ui.Button['StaticPresetMenuView']):
    def __init__(self, emoji: str, index: int, disabled: bool, alternate_colours: bool):
        
        style: discord.ButtonStyle = discord.ButtonStyle.grey if index%2==0 and alternate_colours else discord.ButtonStyle.blurple
        super().__init__(style=style, emoji=emoji, row=index//5, disabled=disabled)

    async def callback(self, interaction: discord.Interaction):
        view: StaticPresetMenuView = self.view
        if view.ctx.author.id == interaction.user.id or interaction.user.id == 244543752889303041:
            view.page = self.view.emoji_list.index(str(self.emoji))

            for child in self.view.children:
                child.disabled = False
            self.disabled = True
            
            await self.view.update_embed(interaction)
        else:
            await interaction.response.send_message("This isn't your command!\nYou can run this command yourself to change the pages!", ephemeral=True)


class StaticPresetMenuView(discord.ui.View):
    def __init__(self, ctx, list_of_embeds, emoji_list: list, alternate_colours: bool, is_response: bool):
        super().__init__()
        self.ctx: commands.Context = ctx
        self.page: int = 0
        self.list_of_embeds: list[discord.Embed] = list_of_embeds
        self.emoji_list: list[str] = emoji_list
        self.is_response = is_response

        for i, emoji in enumerate(emoji_list):
            self.add_item(StaticPresetMenuButton(emoji=emoji, index=i, disabled=(i==0), alternate_colours=alternate_colours))

    async def update_embed(self, interaction: discord.Interaction):
        await interaction.response.edit_message(view=self, embed=self.list_of_embeds[self.page])

    async def on_timeout(self):
        if self.is_response:
            return
        try:
            for button in self.children:
                button.disabled = True
            await self.message.edit(view=self)
        except discord.errors.NotFound:
            pass

async def generate_static_preset_menu(ctx: commands.Context, list_of_embeds: list[discord.Embed], emoji_list: list[str], message_object: discord.Message=None, alternate_colours: bool = False, is_response: bool = False):
    view = StaticPresetMenuView(ctx=ctx, list_of_embeds=list_of_embeds, emoji_list=emoji_list, alternate_colours=alternate_colours, is_response=is_response)
    assert (not is_response or not message_object)
    if is_response:
        view.message = await ctx.respond("\u200b", embed=list_of_embeds[0], view=view)#, ephemeral=True)
        return
    if message_object:
        await message_object.edit(embed=list_of_embeds[0], view=view)
        view.message = message_object
        return
    view.message = await ctx.send("\u200b", embed=list_of_embeds[0], view=view)

###############################################################################
# Static Scrolling Menus, flicks through a list of preset list of embeds,
# Comes with First, Left, Middle, Right and Last buttons
###############################################################################
"""
Instructions on how to use static scrolling menus:
Call the function `generate_static_scrolling_menu` with context and a list of embeds
you want to cycle through.
It must be called with await
"""
SCROLLING_EMOJIS = {
    "<:rewind:876491533451427951>": lambda page, middle, last: 1,
    "<:left_arrow:876505406980116541>": lambda page, middle, last: page-1,
    "<:middle:876491600296050740>": lambda page, middle, last: middle,
    "<:right_arrow:876505406501949472>": lambda page, middle, last: page+1,
    "<:fast_forward:876491622311952394>": lambda page, middle, last: last,
}
START_DISABLED = list(SCROLLING_EMOJIS.keys())[:2]  # The first page can't go back or to the start

class ScrollingMenuButton(discord.ui.Button):
    def __init__(self, emoji: str, middle: int, last: int):
        super().__init__(style=discord.ButtonStyle.blurple, emoji=emoji, disabled=emoji in START_DISABLED)
        self.middle: int = middle
        self.last: int = last

    async def callback(self, interaction: discord.Interaction):
        view: StaticScrollingMenuView = self.view
        if view.ctx.author.id == interaction.user.id or interaction.user.id == 244543752889303041:
            view.page = SCROLLING_EMOJIS[f"{self.emoji}"](view.page, self.middle, self.last)

            # Enable all buttons
            for button in self.view.children:
                button.disabled = False

            if view.page <= 1:
                # If we're on page 1, disable going left (previous pages)
                for button in self.view.children[:2]:
                    button.disabled = True
            elif view.page >= self.last:
                # If we're on the last page, disable going forward (next pages)
                for button in self.view.children[-2:]:
                    button.disabled = True

            if self.last <= 1:
                # If there's only 1 item, don't let them change page.
                for button in self.view.children[-2:]:
                    button.disabled = True    
            
            await self.view.update_embed(interaction)
        else:
            await interaction.response.send_message("This isn't your command!\nYou can run this command yourself to change the pages!", ephemeral=True)
        

class StaticScrollingMenuView(discord.ui.View):
    def __init__(self, ctx: commands.Context, list_of_embeds: list[discord.Embed]):
        super().__init__()
        self.ctx: commands.Context = ctx
        self.list_of_embeds: list[discord.Embed] = list_of_embeds
        self.page: int = 1

        middle: int = int(len(list_of_embeds)/2)
        last: int = len(list_of_embeds)
        for emoji in SCROLLING_EMOJIS.keys():
            self.add_item(ScrollingMenuButton(emoji=emoji, middle=middle, last=last))

    async def update_embed(self, interaction: discord.Interaction):
        embed = self.list_of_embeds[self.page-1]
        await interaction.response.edit_message(view=self, embed=embed)

    async def on_timeout(self):
        try:
            for button in self.children:
                button.disabled = True
            await self.message.edit(view=self)
        except discord.errors.NotFound:
            pass


async def generate_static_scrolling_menu(ctx, list_of_embeds: list[discord.Embed]):
    view = StaticScrollingMenuView(ctx=ctx, list_of_embeds=list_of_embeds)
    view.message = await ctx.send("\u200b", embed=list_of_embeds[0], view=view)

###############################################################################
# Dynamic Scrolling Menus, flicks through a list of preset list of data,
# But does also do processing on each one
# Comes with First, Left, Middle, Right and Last buttons
###############################################################################
"""
Instructions on how to use dynamic scrolling menus:
Call the function `generate_dynamic_scrolling_menu` with context, the data (groups of 10),
and the function that formats each page, call it with await
"""

class DynamicScrollingMenuView(discord.ui.View):
    def __init__(self, ctx: commands.Context, data, page_generator, is_response: bool):
        super().__init__()
        self.ctx: commands.Context = ctx
        self.data: list = data
        self.page: int = 1
        self.page_generator = page_generator
        self.is_response = is_response

        middle = int((len(data)/2)/10)  # We give it 100 items, but 10 per page
        last = int(len(data)/10)
        for emoji in SCROLLING_EMOJIS.keys():
            self.add_item(ScrollingMenuButton(emoji=emoji, middle=middle, last=last))

    async def update_embed(self, interaction: discord.Interaction):
        embed = await self.page_generator(self.ctx, self.data, self.page)
        await interaction.response.edit_message(view=self, embed=embed)

    async def on_timeout(self):
        if self.is_response:
            return
        try:
            for button in self.children:
                button.disabled = True
            await self.message.edit(view=self)
        except discord.errors.NotFound:
            pass


async def generate_dynamic_scrolling_menu(ctx: commands.Context, data, page_generator, is_response: bool = False):
    starting_embed = await page_generator(ctx=ctx, data=data, page=1)
    view = DynamicScrollingMenuView(ctx=ctx, data=data, page_generator=page_generator, is_response=is_response)
    if is_response:
        await ctx.respond("\u200b", embed=starting_embed, view=view)
    else:
        view.message = await ctx.send("\u200b", embed=starting_embed, view=view)

###############################################################################
# Option Picker, will allow the user to input a number between 1 and x.
# Give it context and the number of options.
###############################################################################
"""
Instructions on how to use Option Picker:
# Call the function `generate_option_picker` with context, and the number of options
# call it with await. It will return the number picked (e.g. 1 to x) and the view
"""

class OptionPickerButton(discord.ui.Button['OptionPickerView']):
    def __init__(self, number: int):
        super().__init__(style=discord.ButtonStyle.blurple, label=str(number), row=(number-1)//5)

    async def callback(self, interaction: discord.Interaction):
        if self.view.ctx.author.id == interaction.user.id or interaction.user.id == 244543752889303041:
            await self.view.picked_option(int(self.label))
        else:
            await interaction.response.send_message("This isn't your command!\nYou can run this command yourself to explore this menu!", ephemeral=True)
        

class OptionPickerView(discord.ui.View):
    def __init__(self, ctx: commands.Context, number_of_options: int):
        super().__init__()
        self.ctx: commands.Context = ctx
        self.value: Optional[int] = None

        for label in range(1, number_of_options+1):
            self.add_item(OptionPickerButton(number=label))

    async def picked_option(self, number):
        self.value: int = number
        for button in self.children:
            button.disabled = True
        await self.message.edit(view=self)
        self.stop()

    async def on_timeout(self):
        try:
            for button in self.children:
                button.disabled = True
            await self.message.edit(view=self)
        except discord.errors.NotFound:
            pass

async def generate_option_picker(ctx: commands.Context, embed: discord.Embed, number_of_options: int):    
    view = OptionPickerView(ctx=ctx, number_of_options=number_of_options)
    view.message = await ctx.send("\u200b", embed=embed, view=view)

    await view.wait()
    return view.value, view

###############################################################################
# 
###############################################################################
