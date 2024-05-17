import os
import discord
from discord.ext import commands
import asyncio
import websockets
import json

DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
OLLAMA_BOT_URL = 'ws://localhost:8765'  # URL of the Ollama bot server

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)  # Use '!' as the prefix

@bot.command(name='chat')
async def chat_command(ctx, *, message: str):
    print(f"Chat command invoked by: {ctx.author} ({ctx.author.id}) in {ctx.channel}")
    await ctx.send("Thinking...")  # Send an initial message to indicate processing
    print(f"Received message: {message}")

    try:
        print(f"Connecting to Ollama bot at {OLLAMA_BOT_URL}...")
        async with websockets.connect(OLLAMA_BOT_URL) as websocket:
            await websocket.send(json.dumps({'message': message}))
            print("Sent message to Ollama bot, waiting for response...")
            response = await websocket.recv()
            print(f"Received response from Ollama bot: {response}")
            data = json.loads(response)
            if 'response' in data:
                await ctx.send(data['response'])
                print(f"Sent Ollama response to Discord: {data['response']}")
            else:
                error_msg = data.get('error', 'Unknown error')
                await ctx.send(f"Ollama bot error: {error_msg}")
                print(f"Ollama bot returned an error: {error_msg}")
    except Exception as e:
        print(f"Error communicating with Ollama bot: {e}")
        await ctx.send("An error occurred while processing your request.")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("Bot is ready!")

bot.run(DISCORD_BOT_TOKEN)