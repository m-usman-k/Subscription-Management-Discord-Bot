import time
import discord, os
import csv, requests, bs4
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

# CSV file handling functions
CSV_FILE = 'user_data.csv'

def get_file_text_as_file():
    URL = "https://gitfront.io/r/Spiken/uHyZnJRDYaFy/kuken/blob/globalslib.lua"
    response = requests.get(URL)
    soup = bs4.BeautifulSoup(response.text, 'html.parser').find(name="div", class_="content")
    content = soup.get_text()

    # Write the content to a file
    file_path = "trial_content.lua"
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)
    return file_path

def read_csv():
    if not os.path.exists(CSV_FILE):
        return []
    with open(CSV_FILE, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        return list(reader)

def write_csv(data):
    with open(CSV_FILE, mode='w', newline='') as file:
        fieldnames = ['userid', 'username', 'timestamp']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def update_user_data(userid, username):
    data = read_csv()
    user_found = False
    for row in data:
        if row['userid'] == str(userid):
            user_found = True
            last_trial = row['timestamp']
            if int(time.time()) > int(last_trial):
                row['timestamp'] = int(time.time())+180*24*60*60
                write_csv(data)
                return False
            else:
                return last_trial
    if not user_found:
        this_timestamp = int(time.time())+180*24*60*60
        data.append({'userid': str(userid), 'username': username, 'timestamp': this_timestamp})
        write_csv(data)
        return False

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command()
async def trial(ctx):
    embed = discord.Embed(title='Trial Content', description='Click the button to receive trial content.', color=0x00ff00)
    view = CustomView()
    await ctx.send(embed=embed, view=view)

class CustomView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='Check Eligibility', style=discord.ButtonStyle.primary)
    async def on_button_click(self, interaction: discord.Interaction, button: discord.ui.Button):
        user = interaction.user
        is_timestamp = update_user_data(user.id, user.name)
        if not is_timestamp:
            try:
                file_path = get_file_text_as_file()
                await user.send("Here is your trial content:", file=discord.File(file_path))
                await interaction.response.send_message('You have been given a trial! Check your DMs.', ephemeral=True)
            except discord.Forbidden:
                await interaction.response.send_message('Please enable your DMs to receive the trial.', ephemeral=True)
            finally:
                # Clean up the file after sending
                if os.path.exists(file_path):
                    os.remove(file_path)
        else:
            await interaction.response.send_message(f'Not Eligible! Request Again In <t:{is_timestamp}:R>', ephemeral=True)

bot.run(BOT_TOKEN)
