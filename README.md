# Vulnerable APP

his repository contains a demonstration of common security vulnerabilities in web applications, such as SQL Injection, Cross-Site Scripting (XSS), Command Injection, Harcoded Credentials, and Broken Authorization. The application uses Flask as the web framework and PostgreSQL as the database.

## Features

- Demonstrates various web application security vulnerabilities
- Includes examples of how to fix vulnerabilities

## Prerequisites

- Python 3.6+
- PostgreSQL
- Docker (optional, for running PostgreSQL in a container)

## Setup

### Database

Run PostgreSQL using Docker or install it directly on your machine

`docker run --name postgres-db -e POSTGRES_PASSWORD=password123 -d -p 5432:5432 postgres`

Login into PostgreSQL and create database

`psql -U postgres -h localhost`

`postgres=# create database vulner;`

### Virtual Env

Create virtual env for the project

`python3 -m venv virtualenv`

Active the virtual env

`source virtualenv/bin/activate`

Install python libs

`pip3 install -r requirements.txt`

### Run the app

`python3 app.py`

Now visit the app http://127.0.0.1:8000