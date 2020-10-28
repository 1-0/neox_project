### neox_project - simple REST API for posting posts

# Usage:

Object of this task is to create a simple REST API. You can use one framework from this list (Django Rest Framework, Flask or FastAPI) and all libraries which you are prefer to use with this frameworks.

## 1. Installation

- Install or/and check installed git and python3:
  - `git --version` for check or visit https://git-scm.com/ for installation instructions 
  - `python3 --version` for check or visit https://www.python.org for installation instructions
- `python3 -m pip venv neox_project`
- `cd neox_project`
- `source ./bin/activate` in nix OS or `.\Scripts\activate.bat` in Windows OS
- `python3 -m pip install -U pip`
- `git clone https://github.com/1-0/neox_project`
- `mv neox_project src` in nix OS or `move neox_project src` in Windows OS
- `cd src`
- `python -m pip install -r Requirements.txt`

## 2. Configuration

- `python manage.py createsuperuser`
- set params in bot config file `utils\bot\config.py`:

`
NUMBER_OF_USERS = 2
NUMBER_OF_CONNECTION_RETRY = 5
MAX_POSTS_PER_USER = 2
MAX_LIKES_PER_USER = 2
ADMIN_USERNAME = "a10"
ADMIN_EMAIL = "1_0@usa.com"
ADMIN_PASSWORD = "1111111111q"
ENTER_POINT = r'http://127.0.0.1:8000/api/'
BOT_LOG_FILE = r'bot_log.py'
`

## 3. Run

### Run Server

- `python manage.py runserver`

### Run Bot

- `cd utils`
- `python bot.py`

### Regular Run Bot

- instructions for Wind0ws like OS - https://www.isunshare.com/windows-10/4-ways-to-open-task-scheduler-on-windows-10.html
- instructions for *nix like OS - https://linuxconfig.org/how-to-schedule-tasks-using-at-command-on-linux


# Test task:

Object of this task is to create a simple REST API. You can use one framework from this list (Django Rest Framework, Flask or FastAPI) and all libraries which you are prefer to use with this frameworks.

## 1. Social Network

### Basic models:

- User
- Post (always made by a user)

### Basic Features:

- user signup
- user login
- post creation
- post like
- post unlike
- analytics about how many likes was made. Example url /api/analitics/?date_from=2020-02-02&date_to=2020-02-15 . API should return analytics aggregated by day.
- user activity an endpoint which will show when user was login last time and when he made a last request to the service.

### Requirements:

- Implement token authentication (JWT is prefered)
- Object of this bot demonstrate functionalities of the system according to defined rules.
- This bot should read rules from a config file (in any format chosen by the candidate), but should have following fields (all integers, candidate can rename as they see fit).

## 2. Automated bot

- number_of_users
- max_posts_per_user
- max_likes_per_user

### Bot should read the configuration and create this activity:
- signup users (number provided in config)
- each user creates random number of posts with any content (up to
max_posts_per_user)
- After creating the signup and posting activity, posts should be liked randomly, posts
can be liked multiple times

### Notes:
- Clean and usable REST API is important
- Bot this is just separate python script, not a django management command or etc.
- the project is not defined in detail, the candidate should use their best judgment for every non-specified requirements (including chosen tech, third party apps, etc), however every decision must be explained and backed by arguments in the interview
- Result should be sent by providing a Git url. This is a mandatory requirement.
