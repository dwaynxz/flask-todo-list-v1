# Flask Todo List - Version 1

This is the first version of my Todo List web application built with Flask.  
It uses Python dictionaries to store tasks instead of a database — a simple approach for learning and prototyping.

## Overview
Flask Todo List (Version 1) is a simple web application built with Flask that allows you to create and manage multiple todo lists. This version stores data in Python dictionaries rather than a database, making it lightweight and easy to understand for beginners learning Flask.

This application does not require any external database setup, making it ideal for quick prototyping or as a learning project. Tasks and lists exist only in memory, so data is cleared when the app restarts.

A modern user interface is provided using Bootstrap, with some design assistance and suggestions from Chatgpt to enhance the layout. You can customize or replace it with your own design.

For a more advanced version with persistent storage and SQLAlchemy database integration, see Flask Todo List v2(in development).



---
## Features
- Create multiple todo lists
- Add, mark done/undone, and remove tasks
- Save and edit existing todo lists
- Flash messages for user feedback
- Clean Bootstrap-based UI

---

## Getting Started

### Prerequisites

- Python 3.x  
- Flask  
- python-dotenv  

### Installation

1. Clone this repository:

```bash
  git clone https://github.com/dwaynxz/flask-todo-list-v1.git
  cd flask-todo-list-v1
````

2. Install dependencies:
``` bash
    pip install -r requirements.txt
```
3. Create a .env file and add your secret key:
```bash
  SECRET_KEY=your_secret_key
```
4. Run the app:
```bash
  flask run
```
### Future Version
I’m currently working on **[Flask Todo List v2](https://github.com/dwaynxz/flask-todo-list-v2.git)**, that will use SQL alchemy for persistent storage.

