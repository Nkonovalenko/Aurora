'''     This file is to experiment with the Finnhub.io API      '''
import requests

# Specify which secret to read
SECRET_TYPE = 'sandbox_secret.txt'

# Read in secret API key
secret_file = open(SECRET_TYPE, 'r')
SECRET_API_KEY = secret_file.read()
secret_file.close()