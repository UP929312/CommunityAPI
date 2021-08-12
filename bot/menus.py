import discord

class MenuButton(discord.ui.Button['MenuView']):
    def __init__(self, emoji: str, disabled: bool):
        super().__init__(style=discord.ButtonStyle.blurple, emoji=emoji, row=0, disabled=disabled)

    async def callback(self, interaction: discord.Interaction):
        view: MenuView = self.view
        if view.context.author.id == interaction.user.id or interaction.user.id == 244543752889303041:
            view.page: str = self.view.emoji_map_reversed[f"<:{self.emoji.name}:{self.emoji.id}>"]

            for child in self.view.children:
                child.disabled: bool = False
            self.disabled: bool = True
            
            await self.view.update_embed(interaction)
        else:
            await interaction.response.send_message("This isn't your command!\nYou can run this command yourself to change the pages!", ephemeral=True)
        

class MenuView(discord.ui.View):
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
            self.add_item(MenuButton(emoji=emoji_map[page], disabled=(i==0) ))

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

"""
Instructions on how to use:
First, create the initial function, this will most likely use the same
function, `page_generator`, you pass to the MenuView.
You probably want to do something like this:

main_embed = generate_page(ctx, response, username, "main")

Where generate_page is the page_generator function passed in.

Then, you want to initialise the MenuView, where you need to pass
a dictionary that maps pages to their emoji, e.g.
    "test": "<my_emoji:1234567890>",

You also want to pass in the page_generator, which is a function that takes
the context, data, username and a page.
        
view = MenuView(context=ctx, data=response, username=username, emoji_map=PAGE_TO_EMOJI, page_generator=generate_page)

Finally, update the view's message so we can disable the buttons when it
times out, like so:

view.message = await ctx.send(embed=main_embed, view=view)
"""
