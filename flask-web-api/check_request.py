import requests

res = requests.post('https://unfake.herokuapp.com/detect' ,
 params = {"q":'Beijing is the capital of China'})

import json
print(res)
print(res.json())