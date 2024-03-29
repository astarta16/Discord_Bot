import discord
from discord.ext import commands
import responses
import random

async def send_message(message, user_message, is_private):
    try:
        response = responses.get_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)

    except Exception as e:
        print(e)

def run_discord_bot():
    TOKEN = ''
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True  # Enable member-related events
    bot = commands.Bot(command_prefix='!', intents=intents)

    @bot.event
    async def on_ready():
        print(f'{bot.user} is now running!')

    @bot.event
    async def on_message(message):
        if message.author == bot.user:
            return

        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        print(f'{username} said: "{user_message}" ({channel})')

        if user_message.startswith('?'):
            user_message = user_message[1:]
            await send_message(message, user_message, is_private=True)
        elif user_message.lower() == 'motivation':
            await send_motivation(message)
        else:
            await send_message(message, user_message, is_private=False)

        await bot.process_commands(message)  # Process bot commands

    @bot.command()
    @commands.has_permissions(kick_members=True)
    async def kick(ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f'Kicked {member.name}')

    @bot.command()
    @commands.has_permissions(ban_members=True)
    async def ban(ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f'Banned {member.name}')

    @bot.command()
    @commands.has_permissions(manage_messages=True)
    async def delete(ctx, amount: int):
        await ctx.channel.purge(limit=amount + 1)

    @bot.command()
    async def invite(ctx):
        invite_link = "https://discord.gg/HGJYPty5" 
        await ctx.send(f"Here is the invite link to join our server: {invite_link}")

    async def send_motivation(message):
        motivation_pictures = [
            'https://img.freepik.com/free-vector/motivational-poster-with-inspirational-quote_1284-45846.jpg?w=2000',
            'https://images.unsplash.com/photo-1528716321680-815a8cdb8cbe?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8bW90aXZhdGlvbnxlbnwwfHwwfHx8MA%3D%3D&w=1000&q=80',
            'data:image/jpeg;base64,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',
            'https://media.istockphoto.com/id/1255203350/photo/teamwork-friendship-hiking-help-each-other-trust-assistance-silhouette-in-mountains-sunrise.jpg?s=612x612&w=0&k=20&c=XU9MhkkMdyM59gAMDSUwltr-LhVyjWHLvTxQCPwVbF8%3D&fbclid=IwAR3QWzuq9Vvc2M4b6p6L4mE5Jgpi5clVN6I7To-AWGNzR0ms90ibn-d-6sc'
        ]
        random_motivation_picture = random.choice(motivation_pictures)
        await message.channel.send(random_motivation_picture)

    bot.run(TOKEN)

if __name__ == '__main__':
    run_discord_bot()
