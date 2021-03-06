from dotenv import load_dotenv
from inch import OneInch
from oxapi import OxApi
from teradeus import Teradeus
import os
import requests
import sys
import time

path = os.path.dirname(os.path.abspath(__file__))

load_dotenv(dotenv_path = path + '/.env')

debug = os.getenv('TERADEUS_DEBUG') == 'true'

api = OxApi(os.getenv('OXAPI_URL'), debug)

if os.getenv('TERADEUS_API') == '1INCH':
    chain = os.getenv('INCH_CHAIN')

    api = OneInch(os.getenv('INCH_URL'), chain, debug)

teradeus = Teradeus(os.getenv('TERADEUS_RPC'), path, debug)

sellToken = 'USDC'

if os.getenv('TERADEUS_SELLTOKEN'):
    sellToken = os.getenv('TERADEUS_SELLTOKEN')

if len(sys.argv[1:]) == 3:
    sellToken = str(sys.argv[3])

teradeus.wallet(os.getenv('TERADEUS_ADDRESS'))
teradeus.key(os.getenv('TERADEUS_PRIVATE'))

teradeus.buy(sys.argv[1])
teradeus.sell(sellToken)
teradeus.amount(sys.argv[2])

try:
    result = teradeus.execute(api)

    print('[PASS]', 'Swap submitted!')
    print('[PASS]', 'Hash:', result['hash'])
except Exception as e:
    print('[FAIL]', e)

    sys.exit()

if os.getenv('TERADEUS_SUCCESS'):
    link = os.getenv('TERADEUS_SUCCESS')

    if debug:
        print('[INFO]', 'Sending data to', link + '...')

    requests.post(link, result)