from asyncio import TimeoutError
from discord.ext import commands
from helpers import *
import discord

intents = discord.Intents().default()
intents.members = True
intents.reactions = True
bot = commands.Bot(command_prefix = "$", case_insensitive = True, intents = intents)

with open("token.txt", "r") as f:
    token = f.read().strip()

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await bot.change_presence(activity = discord.Game(name = "With Admin Authority"))

@bot.event
async def on_member_join(member):
    await member.add_roles(bot.guilds[0].get_role([r.id for r in bot.guilds[0].roles if r.name == "Recruit"][0]), reason = "Server Default.")

@bot.command(name = "echo")
async def echo(ctx, *, message = None):
    message = message or "Say something, Sheep."
    await ctx.message.delete()
    await ctx.send(message)

@bot.command(name = "plan")
async def plan(ctx):
    await ctx.send("https://tenor.com/view/already-in-motion-mordecai-regular-show-gif-15820780")

@bot.command(name = "game", aliases = ["tictactoe", "tic-tac-toe"])
async def game(ctx, board = [float("nan")]*9, player = "One"):
    if all(sq!=sq for sq in board):
        game_msg = await ctx.send(board_to_string(board))
        ctx = await bot.get_context(game_msg)

    if all(sq==sq for sq in board):
        await ctx.send("The game ends in a draw.")
        return

    if win:=has_won(board):
        await ctx.message.edit(content = board_to_string(board, win))
        winner = "Two" if player == "One" else "One"
        await ctx.send(f"Player {winner} wins!")
        return

    try:
        reaction, user = await bot.wait_for("reaction_add", timeout = 60.0, check = lambda r, _: r.message.id == ctx.message.id)
        index = int(reaction.emoji[0]) - 1
        if board[index]!=board[index]:
            board[index] = 0 if player == "One" else 1
        else:
            await ctx.send(f"{user.mention} forfeits because they had to cheat at tic-tac-toe.")
            return
    except TimeoutError:
        await ctx.send(f"Player {player} forfeits due to time.")
        return
    except Exception:
        await ctx.send(f"{user.mention} forfeits because they are a dipass.")
        return
    finally:
        await ctx.message.clear_reactions()

    await ctx.message.edit(content = board_to_string(board))
    await game(ctx, board, "Two" if player == "One" else "One")

bot.run(token)
