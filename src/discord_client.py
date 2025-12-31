import discord
from discord.ext import commands
import logging
from .config import DISCORD_TOKEN, COMMAND_PREFIX
from .llm_engine import LLMEngine

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GenerativeBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix=COMMAND_PREFIX, intents=intents)
        
        self.llm = LLMEngine()

    async def on_ready(self):
        logger.info(f'Logged in as {self.user} (ID: {self.user.id})')
        logger.info('------')
        
        # Load the model in the background or here
        logger.info("Loading LLM Engine...")
        self.llm.load_model()
        logger.info("LLM Engine Ready.")

    async def on_message(self, message):
        # Ignore own messages
        if message.author.id == self.user.id:
            return

        # Process commands if any
        await self.process_commands(message)

        # Chat functionality (if not a command)
        # Check if mentioned or in a specific channel
        if self.user.mentioned_in(message) or isinstance(message.channel, discord.DMChannel):
            async with message.channel.typing():
                response = self.llm.generate_response(message.content, message.author.name)
                await message.reply(response)

def run_bot():
    if not DISCORD_TOKEN:
        logger.error("Error: DISCORD_TOKEN not found in environment variables.")
        return
    
    bot = GenerativeBot()
    bot.run(DISCORD_TOKEN)
