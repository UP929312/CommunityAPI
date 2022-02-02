import discord  # type: ignore
from discord.ext import commands    # type: ignore

from typing import Optional

MENU_CONTROLLERS = [244543752889303041, 481795555333242881]  # People who can control other people's menus

###################################################################################
# Static Preset Menus, gets all the data prior and flicks between the preset pages
###################################################################################
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
        if view.ctx.author.id == interaction.user.id or interaction.user.id in MENU_CONTROLLERS:
            view.page = self.view.emoji_list.index(str(self.emoji))

            for child in self.view.children:
                child.disabled = False
            self.disabled = True
            
            await self.view.update_embed(interaction)
        else:
            await interaction.response.send_message("This isn't your command!\nYou can run this command yourself to change the pages!", ephemeral=True)


class StaticPresetMenuView(discord.ui.View):
    def __init__(self, ctx, list_of_embeds: list[discord.Embed], emoji_list: list[str], alternate_colours: bool, is_response: bool):
        super().__init__()
        self.ctx = ctx
        self.page: int = 0
        self.list_of_embeds = list_of_embeds
        self.emoji_list = emoji_list
        self.is_response = is_response

        for i, emoji in enumerate(emoji_list):
            self.add_item(StaticPresetMenuButton(emoji=emoji, index=i, disabled=(i==0), alternate_colours=alternate_colours))

    async def update_embed(self, interaction: discord.Interaction):
        await interaction.response.edit_message(view=self, embed=self.list_of_embeds[self.page])

    async def on_timeout(self):
        if not isinstance(self.message, discord.Message):
            return
        try:
            for button in self.children:
                button.disabled = True
            await self.message.edit(view=self)
        except discord.NotFound:
            pass

async def generate_static_preset_menu(ctx, list_of_embeds: list[discord.Embed], emoji_list: list[str], alternate_colours: bool = False, is_response: bool = False):
    view = StaticPresetMenuView(ctx=ctx, list_of_embeds=list_of_embeds, emoji_list=emoji_list, alternate_colours=alternate_colours, is_response=is_response)
    if is_response:
        view.message = await ctx.respond(embed=list_of_embeds[0], view=view)
    else:
        view.message = await ctx.send(embed=list_of_embeds[0], view=view)

# This edits the original message, only used in .maxer
async def generate_static_preset_changing_menu(ctx, list_of_embeds: list[discord.Embed], emoji_list: list[str], message_object: discord.Message):
    view = StaticPresetMenuView(ctx=ctx, list_of_embeds=list_of_embeds, emoji_list=emoji_list, alternate_colours=False, is_response=False)
    await message_object.edit(embed=list_of_embeds[0], view=view)
    view.message = message_object

###############################################################################
# Static Scrolling Menus, flicks through a list of pre-made embeds,
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
        disable = emoji in START_DISABLED or last == 1
        super().__init__(style=discord.ButtonStyle.blurple, emoji=emoji, disabled=disable)
        self.middle: int = middle
        self.last: int = last

    async def callback(self, interaction: discord.Interaction):
        view: StaticScrollingMenuView = self.view
        if view.ctx.author.id == interaction.user.id or interaction.user.id in MENU_CONTROLLERS:
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

            await self.view.update_embed(interaction)
        else:
            await interaction.response.send_message("This isn't your command!\nYou can run this command yourself to change the pages!", ephemeral=True)
        

class StaticScrollingMenuView(discord.ui.View):
    def __init__(self, ctx, list_of_embeds: list[discord.Embed], is_response: bool):
        super().__init__()
        self.ctx = ctx
        self.list_of_embeds = list_of_embeds
        self.page = 1
        self.is_response = is_response

        middle: int = int(len(list_of_embeds)/2)
        last: int = len(list_of_embeds)
        for emoji in SCROLLING_EMOJIS.keys():
            self.add_item(ScrollingMenuButton(emoji=emoji, middle=middle, last=last))

    async def update_embed(self, interaction: discord.Interaction):
        embed = self.list_of_embeds[self.page-1]
        await interaction.response.edit_message(view=self, embed=embed)

    async def on_timeout(self):
        if not isinstance(self.message, discord.Message):
            return
        try:
            for button in self.children:
                button.disabled = True
            await self.message.edit(view=self)
        except discord.NotFound:
            pass


async def generate_static_scrolling_menu(ctx, list_of_embeds: list[discord.Embed], is_response: bool = False):
    view = StaticScrollingMenuView(ctx=ctx, list_of_embeds=list_of_embeds, is_response=is_response)
    if is_response:
        view.message = await ctx.respond(embed=list_of_embeds[0], view=view)
    else:
        view.message = await ctx.send(embed=list_of_embeds[0], view=view)

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
    def __init__(self, ctx, data: list, page_generator, is_response: bool):
        super().__init__()
        self.ctx = ctx
        self.data = data
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
        if not isinstance(self.message, discord.Message):
            return
        try:
            for button in self.children:
                button.disabled = True
            await self.message.edit(view=self)
        except discord.NotFound:
            pass


async def generate_dynamic_scrolling_menu(ctx, data, page_generator, is_response: bool = False):
    starting_embed = await page_generator(ctx=ctx, data=data, page=1)
    view = DynamicScrollingMenuView(ctx=ctx, data=data, page_generator=page_generator, is_response=is_response)
    if is_response:
        view.message = await ctx.respond(embed=starting_embed, view=view)
    else:
        view.message = await ctx.send(embed=starting_embed, view=view)

###############################################################################
# Option Picker, will allow the user to input a number between 1 and x.
# Give it context and the number of options.
###############################################################################
"""
Instructions on how to use Option Picker:
# Call the function `generate_option_picker` with context, and the number of options
# call it with await. It will return the number picked (e.g. 1 to x) and the view
"""

class NumberPickerButton(discord.ui.Button):
    def __init__(self, number: int):
        super().__init__(style=discord.ButtonStyle.blurple, label=str(number), row=(number-1)//5)

    async def callback(self, interaction: discord.Interaction):
        if self.view.ctx.author.id == interaction.user.id or interaction.user.id in MENU_CONTROLLERS:
            await self.view.picked_option(int(self.label))
        else:
            await interaction.response.send_message("This isn't your command!\nYou can run this command yourself to explore this menu!", ephemeral=True)
        

class NumberPickerView(discord.ui.View):
    def __init__(self, ctx, number_of_options: int):
        super().__init__()
        self.ctx = ctx
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
        if not isinstance(self.message, discord.Message):
            return
        try:
            for button in self.children:
                button.disabled = True
            await self.message.edit(view=self)
        except discord.NotFound:
            pass

async def generate_number_picker(ctx, embed: discord.Embed, number_of_options: int):    
    view = NumberPickerView(ctx=ctx, number_of_options=number_of_options)
    view.message = await ctx.send(embed=embed, view=view)

    await view.wait()
    return view.value, view

###############################################################################
# Option Picker, will allow the user to input a number between 1 and x.
# Give it context and the number of options.
###############################################################################
"""
Instructions on how to use Option Picker:
# Call the function `generate_option_picker` with context, and the number of options
# call it with await. It will return the number picked (e.g. 1 to x) and the view
"""

class OptionPickerButton(discord.ui.Button):
    def __init__(self, option: str, index: int):
        super().__init__(style=discord.ButtonStyle.blurple, emoji=option)

    async def callback(self, interaction: discord.Interaction):
        if self.view.ctx.author.id == interaction.user.id or interaction.user.id in MENU_CONTROLLERS:
            await self.view.picked_option(self.emoji)
        else:
            await interaction.response.send_message("This isn't your command!\nYou can run this command yourself to explore this menu!", ephemeral=True)
        

class OptionPickerView(discord.ui.View):
    def __init__(self, ctx, options: list[str]):
        super().__init__()
        self.ctx = ctx
        self.value: Optional[str] = None

        for i, label in enumerate(options):
            self.add_item(OptionPickerButton(option=label, index=i))

    async def picked_option(self, option):
        self.value: str = option
        for button in self.children:
            button.disabled = True
        await self.message.edit(view=self)
        self.stop()

    async def on_timeout(self):
        if not isinstance(self.message, discord.Message):
            return
        try:
            for button in self.children:
                button.disabled = True
            await self.message.edit(view=self)
        except discord.NotFound:
            pass

async def generate_option_picker(ctx, embed: discord.Embed, options: list[str], is_response: bool = False, message_object: discord.Message=None):
    view = OptionPickerView(ctx=ctx, options=options)
    if message_object and is_response:
        print("This doesn't work yet!")
        print("Editing!")
        print(dir(ctx.interaction))
        #print(ctx.interaction.original_message)
        #print(repr(ctx.interaction.original_message))
        #original_message = await ctx.interaction.original_message()
        #view.message = await original_message.edit(embed=embed, view=view)
    elif message_object:
        view.message = await ctx.edit(embed=embed, view=view)
    elif is_response:
        view.message = await ctx.respond(embed=embed, view=view)
    else:
        view.message = await ctx.send(embed=embed, view=view)

    await view.wait()
    return view.value, view
