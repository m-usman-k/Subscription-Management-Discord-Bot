# Discord Trial Bot

This is a Discord bot that provides trial content to users. The bot checks user eligibility and sends trial content if the user is eligible.

## Features

- Check user eligibility for trial content
- Send trial content to eligible users via direct message
- Store user data in a CSV file

## Requirements

- Python 3.8+
- `discord.py` library
- `requests` library
- `beautifulsoup4` library
- `python-dotenv` library

## Setup

1. Clone the repository:

    ```sh
    git clone https://github.com/m-usman-k/Subscription-Management-Discord-Bot.git
    cd Subscription-Management-Discord-Bot
    ```

2. Install the required packages:

    ```sh
    pip install -r requirements.txt
    ```

3. Create a `.env` file in the root directory and add your Discord bot token:

    ```env
    BOT_TOKEN=your-discord-bot-token
    ```

4. Run the bot:

    ```sh
    python main.py
    ```

## Usage

- Invite the bot to your Discord server.
- Use the `!trial` command to check eligibility and receive trial content.

## Commands

- `!trial`: Check eligibility and receive trial content.

## File Structure

- `main.py`: Main bot script.
- `requirements.txt`: List of required Python packages.
- `user_data.csv`: CSV file to store user data.

## License

This project is licensed under the MIT License.

## Acknowledgements

- [discord.py](https://github.com/Rapptz/discord.py)
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)
- [requests](https://docs.python-requests.org/en/latest/)

Feel free to contribute to this project by submitting issues or pull requests.
