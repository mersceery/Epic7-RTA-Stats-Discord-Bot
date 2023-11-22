import discord
import trialRequest
from discord.ext import commands

# Define the intents your bot will use
intents = discord.Intents.default()

# Add the specific intents your bot needs
intents.message_content = True

# Create a bot instance with the specified intents
bot = commands.Bot(command_prefix="!", intents=intents)


# Event handler for when the bot is ready
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")


@bot.event
async def on_message(message):
    if message.content.startswith("!"):
        try:
            username = f"E7 RTA Stats for user: **{message.content[1:]}**"

            # Call the trialRequest.rta_stats function and catch any exceptions
            try:
                response2 = trialRequest.rta_stats(message.content[1:])
            except Exception as e:
                # Handle the exception and send an error message
                await message.channel.send(f"An error occurred: {str(e)}")
                return  # Return to exit the function

            formatted_response = f"\n**Most Common Picks:**\n{next(response2)}"
            result_battle_response = next(response2)
            formatted_response_mvp = f"\n**Most MVP Picks within {result_battle_response} Matches:**\n{next(response2)}"
            formatted_response_preban = f"\n**Most Pre-ban Char within {result_battle_response} Matches:**\n{next(response2)}"
            total_first_pick_matches = next(response2)
            formatted_response_first_pick = f"\n**Most First Pick Char within {total_first_pick_matches} Matches:**\n{next(response2)}"

            # Send the response
            combined_response = f"{username}\n{formatted_response}\n{formatted_response_mvp}\n{formatted_response_preban}\n{formatted_response_first_pick}"

            # Send the combined response
            await message.channel.send(combined_response)
        except Exception as e:
            # Handle any other exceptions that may occur
            await message.channel.send(f"An error occurred: {str(e)}")


# Run the bot with your token
bot.run("SECRET")
