# Onii-Chan  
Onii-Chan (translated from Japanese as "older brother" or "big brother") is a Discord Bot that I have made to provide some basic features for a server. I've reworked and published this project as an example of how one could make use of the discord.py library. Inspired by George Orwell's *1984*, the bot serves as an entity that can "look after" Discord servers that I used to manage.

---

## Built with  
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![discord.py](https://img.shields.io/badge/discord.py-7289DA?style=for-the-badge&logo=discord&logoColor=white)](https://discordpy.readthedocs.io/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)  

---

## Development  
The bot code will be updated from time to time to showcase different use cases with Python and Discord. Updates may include new features, enhancements to existing ones, and optimizations for better performance.

---

## Features  
- [x] Moderation  
- [x] Logging  
- [x] Auto-Restart (through Docker)  
- [x] Server Monitoring  
- [ ] API Status Updates  
- [ ] Webhooks
---

## Run Locally  
These steps below assume you have created a bot application in the Discord developer portal. If you haven't done so, first do that [here](https://discord.com/developers/applications). There should be sufficient instructions online for generating a token and adding your bot to a server.

### Run Locally - With Docker  

1. **Clone the repository**  
   Clone this Git repository into a directory with sufficient storage:  
   ```sh
   git clone https://github.com/NV-9/Onii-Chan.git
   ```
2. **Ensure Docker is installed and running**  
    Install Docker Desktop or another Docker runtime and ensure it is running.
3. **Navigate to the project folder**
    ```sh
    cd Onii-Chan
    ```
4. **Set up a .env file**  
    Create a `.env` file in the project directory and populate it with the following variables:
    ```sh
    BOT_TOKEN=<Your-Discord-Bot-Token>
    ```
5. **Run the bot**
    Use Docker Compose to build and run the bot:
    ```sh
    docker compose up -d
    ```  
### Run Locally - Manual Setup
1. **Clone the repository**  
    Clone this Git repository into a directory with sufficient storage:  
    ```sh
    git clone https://github.com/NV-9/Onii-Chan.git
    ```
2. **Navigate to the project folder**
    ```sh
    cd Onii-Chan
    ```
3. **Install Python and dependencies**  
    Ensure Python 3.8 or newer is installed. Set up a virtual environment:
    ```sh
    python -m venv env
    source env/bin/activate  # For macOS/Linux
    env\Scripts\activate     # For Windows
    pip install --upgrade pip
    pip install -r requirements.txt
    ```
4. **Set up a .env file**  
    Create a `.env` file in the project directory and populate it with the following variables:
    ```sh
    BOT_TOKEN=<Your-Discord-Bot-Token>
    ```
5. **Run the bot**
    Use the following command to start the bot:
    ```sh
    python run.py
    ```   
---

## License
This project is licensed under the MIT License.

You are free to use, modify, and distribute this code for any purpose, whether personal or commercial.

See the [LICENSE](./LICENSE) file for more details.

---