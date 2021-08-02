from player_commands.bazaar import bazaar_cog
from player_commands.sky import sky_cog
from player_commands.wiki import wiki_cog
from player_commands.dungeons import dungeons_cog
from player_commands.kills import kills_cog
from player_commands.lowest_bin import lowest_bin_cog
from player_commands.skills import skills_cog
from player_commands.slayer import slayer_cog
from player_commands.invite import invite_cog
from player_commands.auction_house import auction_house_cog
from player_commands.missing import missing_cog
from player_commands.weights import weights_cog
from player_commands.graph import graph_cog
from player_commands.leaderboard import leaderboard_cog
from player_commands.price_check import price_check_cog
from player_commands.minions import minions_cog

from player_commands.set_prefix import set_prefix_cog
from player_commands.link_account import link_account_cog
from player_commands.help_command import help_cog

assistant_commands = [set_prefix_cog, link_account_cog, help_cog]

regular_commands = [sky_cog, wiki_cog, bazaar_cog,
                    dungeons_cog, kills_cog, lowest_bin_cog,
                    skills_cog, slayer_cog, invite_cog,
                    auction_house_cog, missing_cog, weights_cog,
                    graph_cog, leaderboard_cog, price_check_cog,
                    minions_cog]

player_commands = regular_commands+assistant_commands
