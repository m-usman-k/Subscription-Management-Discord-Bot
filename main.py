import discord, os
import csv, requests, bs4
from datetime import datetime, timedelta
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
            last_trial = datetime.strptime(row['timestamp'], '%Y-%m-%d %H:%M:%S')
            if datetime.now() - last_trial > timedelta(days=180):
                row['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                write_csv(data)
                return True
            else:
                return False
    if not user_found:
        data.append({'userid': str(userid), 'username': username, 'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')})
        write_csv(data)
        return True

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
        if update_user_data(user.id, user.name):
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
            await interaction.response.send_message('You are not eligible for a trial at this time.', ephemeral=True)

bot.run(BOT_TOKEN)
