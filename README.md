# Cinema Management System
Web application that allows users to see cinema schedule and order tickets and staff to manage cinema - add new movies/showings and accept users' orders.

## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Database](#database)
* [Setup](#setup)
* [Staff user setup](#staff-user-setup)

## General info
Add more general information about project. What the purpose of the project is? Motivation?
On the main page there is a schedule of movies for current week.  
There is also possibility to search for movies in "movies" tab and showings in "showings" tab.  
In order to order a ticket, a client needs to have an account. There are 3 types of accounts:  
* client - basic account, allows to order tickets
* cashier - extension of basic account, allows to accept/reject orders in "profile" tab
* staff - extension of basic account, allows to manage the cinema and the cashiers in "staff panel" tab.

User can see his/her current tickets and orders history in "profile" tab.

## Technologies
* Python 3
* Django 3
* PostgreSQL
* Bootstrap 4

## Database
Diagram, create-script, example trigger and example function are in "database" directory.


## Setup
### Local development environment setup using **docker** and **docker-compose**.
1. Download repository and enter root directory (the one with manage.py)
2. Provide environment variables (e.g in .env file) e.g:
```
SECRET_KEY=some_secret_key
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
DEBUG=1
```
3. Export environment variables e.g with .env file:
```
export $(xargs < .env)
```
4. Run docker-compose:
```
docker-compose up --build -d
```
5. Perform migrations:
```
docker-compose exec web python3 manage.py migrate
```
6. That's it. Main page of the application should be in:
```
http://127.0.0.1:8000/
```
7. To stop the application, type 
```
docker-compose down
```
Once setup is done, in order to run application it's enough to export environment variables (from point 3) and run docker-compose:
```
docker-compose up -d
```

## Staff user setup
In order to create staff user, you need to create one in terminal:
```
docker-compose exec web python3 manage.py createsuperuser
```
