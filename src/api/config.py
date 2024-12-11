from dotenv import dotenv_values
import os
PWD = os.path.dirname(os.path.realpath(__file__))[:-4]

PROCON_TOKEN = dotenv_values('.env')['PROCON_TOKEN']

# URL = "https://proconvn.duckdns.org"
URL = "https://procon.iuhkart.systems"
HEADERS = {"Authorization": PROCON_TOKEN}

if __name__ == '__main__':
    print(HEADERS)
    print(PWD)