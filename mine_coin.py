import hashlib
import requests
import sys
import json
import os
import time
from dotenv import load_dotenv
from utils import base_url,balance_url
load_dotenv()
token = os.getenv('API_KEY')
auth = {'Authorization': f'Token {token}'}

def check_status():
    status_response = requests.post(f"{base_url}/status", headers=auth)
    status = status_response.json()
    # print('status', status)
    return status

# status = check_status()
# print(status)

def check_balance():
    response = requests.get(balance_url, headers=auth)
    balance = response.json()
    return balance

# balance = check_balance()
# print(balance)


def proof_of_work(block):
    """
    Simple Proof of Work Algorithm
    Stringify the block and look for a proof.
    Loop through possibilities, checking each one against `valid_proof`
    in an effort to find a number that is a valid proof
    :return: A valid proof for the provided block
    """
    block_string = json.dumps(block, sort_keys=True)
    proof = 0
    while valid_proof(block_string, proof) is False:
        proof += 1
    return proof
def valid_proof(block_string, proof):
    """
    Validates the Proof:  Does hash(block_string, proof) contain 6
    leading zeroes?  Return true if the proof is valid
    :param block_string: <string> The stringified block to use to
    check in combination with `proof`
    :param proof: <int?> The value that when combined with the
    stringified previous block results in a hash that has the
    correct number of leading zeroes.
    :return: True if the resulting hash is a valid proof, False otherwise
    """
    guess = f"{block_string}{proof}".encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    return guess_hash[:difficulty] == '0'*difficulty
    # return guess_hash[:3] == "000"
if __name__ == '__main__':
    # What is the server address? IE `python3 miner.py https://server.com/api/`
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "https://lambda-treasure-hunt.herokuapp.com/api/bc"
    # Load ID
    # f = open("my_id.txt", "r")
    # id = f.read()
    # print("ID is", id)
    # f.close()
    # # Load Balance
    # f = open("my_balance.txt", "r")
    # balance = f.read()
    # print("Balance is", balance)
    # f.close()
    # Run forever until interrupted
    coins = 0
    while True:
        # auth = {'Authorization': f'Token {token}'}
        r = requests.get(url=node + "/last_proof/", headers=auth)
        # Handle non-json response
        try:
            data = r.json()
            print('data', data)
            difficulty = data['difficulty']
            time.sleep(data['cooldown'])
        except ValueError:
            print("Error:  Non-json response")
            print("Response returned:")
            print(r)
            break
        # TODO: Get the block from `data` and use it to look for a new proof
        new_proof = proof_of_work(data['proof'])
        # When found, POST it to the server {"proof": new_proof, "id": id}
        post_data = {"proof": new_proof}
        r = requests.post(url=node + "/mine/", headers=auth, json=post_data)
        data = r.json()
        print('data from post', data)
        print('cooldown', data['cooldown'])
        time.sleep(data['cooldown'])
        # TODO: If the server responds with a 'message' 'New Block Forged'
        # add 1 to the number of coins mined and print it.  Otherwise,
        # print the message from the server.
        try:
            if data['proof']:
                coins += 1
                print(coins)
            else:
                print('failed')
        except:
            print('no proof exits on the data response', data)
            sys.exit(1)