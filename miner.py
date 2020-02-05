import hashlib
import requests
import time
import sys
import json

param = {'Authorization': 'Token e79b12bf4f51c748e9edf3b395ad368c91c89ced'}
ep_init = 'init/'
adv_url = 'https://lambda-treasure-hunt.herokuapp.com/api/adv/'
status_url = 'https://lambda-treasure-hunt.herokuapp.com/api/adv/status/'
balance_url = 'https://lambda-treasure-hunt.herokuapp.com/api/bc/get_balance/'

init_response = requests.get(adv_url+ep_init, headers=param)
init_res = init_response.json()

cur_cd = init_res['cooldown']
print('current CD', cur_cd)
time.sleep(cur_cd)

status_response = requests.post(status_url, headers=param)
status_res = status_response.json()
print('status', status_res)

cur_cd = status_res['cooldown']
print('current CD', cur_cd)
time.sleep(cur_cd)

balance_response = requests.get(balance_url, headers=param)
balance_res = balance_response.json()
print('balance', balance_res)

cur_cd = balance_res['cooldown']
print('current CD', cur_cd)
time.sleep(cur_cd)


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

        r = requests.get(url=node + "/last_proof/", headers=param)
        # Handle non-json response
        try:
            data = r.json()

            difficulty = data['difficulty']
            cur_cd = data['cooldown']
            time.sleep(cur_cd)
        except ValueError:
            print("Error:  Non-json response")
            print("Response returned:")
            print(r)
            break

        # TODO: Get the block from `data` and use it to look for a new proof
        new_proof = proof_of_work(data['proof'])

        # When found, POST it to the server {"proof": new_proof, "id": id}
        post_data = {"proof": new_proof}

        r = requests.post(url=node + "/mine/", headers=param, json=post_data)
        data = r.json()
        print('HJERe', data)
        try:
            cur_cd = data['cooldown']
            time.sleep(cur_cd)
        except:
            pass

        # TODO: If the server responds with a 'message' 'New Block Forged'
        # add 1 to the number of coins mined and print it.  Otherwise,
        # print the message from the server.
        if data['proof']:
            coins += 1
            print(coins)
            print('valid proof', data['proof'])
        else:
            print('failed')
