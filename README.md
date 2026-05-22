# Telegram Automation Toolkit
* A powerful, script-based automation suite for Telegram, designed to handle bulk channel management, data extraction, and automated interaction using the Telethon library.

# Features
* Account Management: Update bio, profile photos, usernames, and 2FA settings.
* Channel/Group Administration: Bulk joining, leaving, and information gathering.
* Content & Media Tools: Find and match images (via perceptual hashing) or videos in channels.
* Bulk forward posts, send messages, or comment on posts.
* Post analytics and statistics tracking.
* Data Collection: Scraping channel messages and exporting to Excel/SQLite.
* Automation: Advanced "bot" interactions and automated task queuing.

# Configuration
1. **Clone the repo**
    ```bash
    git clone https://github.com/Mister-None/tg
    ```
2. **Install Dependencies:**
    ```bash
    pip install Pillow moviepy colorama python-dotenv telethon pandas numpy ImageHash requests
    ```
3. **Create a `.env` file in the root directory with the following variables:**
    ```.env
    app_id=YOUR_APP_ID
    app_hash=YOUR_APP_HASH
    password=YOUR_2FA_PASSWORD
    sessions=path/to/sessions_folder
    tg_data=path/to/database.db
    max_channel=123456789
    secret_channel=123456789
    # ... add other required paths (CHATS_GROUPS, FORWARD_LOG, etc.)
    ```
4. **Setup the Database and xlsx file: Ensure you have `tg_data_template.db`, `bots_tg_template.xlsx`.**
    
5. **Make permanent variable by exporting `DOTENV_FILE_PATH` in `.bashrc`, etc.**
    ```.bashrc
    export DOTENV_FILE_PATH=path/to/.env
     ```
# Usage
**The script is designed to be run from the command line, accepting a function ID and a bot/index identifier(index defined by table row)**.
    ```bash
    python tbot.py <function_id> <bot_index>
    ```
**Execute the script without arguments to see the list of available functions:**
    ```bash
    python tbot.py
    ```
* Select a function ID from the list (0–26).
* Provide the required index or configuration parameters when prompted or via arguments.
** For multiplaying commands use second script `tg_massive.py`, for instance:**
    ```bash
    python tg_massive.py 1 2-100       
    ```
* The command above will open 99 tabs of your terminal and trigger commands `python tbot.py 1 2`, `python tbot.py 1 3`, `...`, `python tbot.py 1 100`
# Key Files Used
* tg_data: SQLite database storing channel/bot information.
* credentials: Excel sheet containing phone numbers, media paths, and task text.
* RECIPIENTS: Text file of bots and users for sending messages.
* CHATS_GROUPS / FORWARD_LOG: Text files for tracking target groups and forwarding history.


## This project is for educational purposes. Ensure you comply with Telegram's Terms of Service when using automation tools.
