#should be ran once from bash in heroku 
from db import database
database().createTable()