from utils import *
import requests
import json
import random
import time
import pickle

adv_url = 'https://lambda-treasure-hunt.herokuapp.com/api/adv/'
take_url = 'https://lambda-treasure-hunt.herokuapp.com/api/adv/take/'
sell_url = 'https://lambda-treasure-hunt.herokuapp.com/api/adv/sell/'
ep_status = 'status/'
ep_init = 'init/'
ep_move = 'move/'

param = {'Authorization': 'Token e91091807dc50e6bf25669440c1b4fc3ebaf2aaa'}

# init_response = requests.get(adv_url+ep_init, headers=param)
# init_res = init_response.text
# ir = json.loads(init_res)
# #cur_exits = ir['exits']
# cur_room = ir['room_id']
# cur_cd = ir['cooldown']
# time.sleep(cur_cd)


status_response = requests.post(adv_url+ep_status, headers=param)
stat_res = status_response.text
sr = json.loads(stat_res)
cur_encumb = sr['encumbrance']
cur_cd = sr['cooldown']
gold = sr['gold']
time.sleep(cur_cd)

print('gold', gold)
print('cur_encumb', cur_encumb)
