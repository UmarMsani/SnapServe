# SnapServe: Food Delivery and Recipe App

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Technologies](#technologies)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- 
## Introduction
SnapServe is a food delivery and recipe app designed to provide users with a seamless experience of discovering new recipes and ordering food from their favorite restaurants.

## Features
- User Authentication: Register, log in, and manage your account.
- Recipe Discovery: Explore a wide variety of recipes with detailed instructions and ingredients.
- Restaurant Ordering: Order food from your favorite local restaurants with ease.
- User Profile: Customize your profile and keep track of your favorite recipes and orders.

## Getting Started

### Prerequisites
- [Python](https://www.python.org/) installed
- [SQLite](https://www.sqlite.org/index.html) database

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/UmarMsani/snapserve.git
   
# Navigate to the project directory:
cd snapserve

# Install dependencies:
pip install -r requirements.txt

# Set up the database:
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

# Usage
Run the application:
flask run
Open your web browser and go to http://localhost:5000/

# Technologies

Flask (Python web framework)
SQLAlchemy (Database ORM)
HTML, CSS, JavaScript (Frontend)
SQLite (Database)

# Project Structure

app.py: Main application file.
templates/: HTML templates for rendering pages.
static/: Static files such as images and stylesheets.
models.py: Database models and schema definitions.
migrations/: Database migration files.

# Contributing

Contributions are welcome! Please follow the contribution guidelines when making changes.
