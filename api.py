import requests
import urllib
import hashlib
import time
import re

# 服务地址
host = "https://api.map.baidu.com"

# 接口地址
riding_uri = "/direction/v2/riding"
suggestion_uri = "/place/v2/suggestion"
detail_uri = "/place/v2/detail"

ak = "TXESXXydj0MSAzwCQwE9DDBWDLGgzEht"
sk = "Oimq26d1d7w7ntLral4CxBM2yBhaiZiZ"

def generate_sn(url, sk):
    encodedStr = urllib.request.quote(url, safe="/:=&?#+!$,;'@()*[]")
    rawStr = encodedStr + sk
    sn = hashlib.md5(urllib.parse.quote_plus(rawStr).encode("utf8")).hexdigest()
    return sn

def make_request(uri, params):
    queryArr = [f"{key}={params[key]}" for key in params]
    queryStr = uri + "?" + "&".join(queryArr)
    sn = generate_sn(queryStr, sk)
    queryStr += "&sn=" + sn
    url = host + queryStr
    response = requests.get(url)
    return response.json() if response else None

def get_suggestions(query, region):
    suggest_params = {
        "query": query,
        "region": region,
        "city_limit": "true",
        "output": "json",
        "ak": ak,
    }
    return make_request(suggestion_uri, suggest_params)

def get_detail(uid):
    detail_params = {
        "uid": uid,
        "output": "json",
        "scope": "2",
        "ak": ak,
    }
    return make_request(detail_uri, detail_params)

def print_suggestions(suggestions):
    if suggestions and 'result' in suggestions:
        results = suggestions['result'][:5]
        for idx, result in enumerate(results):
            print(f"{idx}. {result['name']}")

def get_user_choice(input_prompt, query, region):
    suggestions = get_suggestions(query, region)
    print_suggestions(suggestions)
    choice = int(input(input_prompt))
    selected_place = suggestions['result'][choice]
    detail = get_detail(selected_place['uid'])
    location = detail['result']['location']
    lat_lng = f"{location['lat']},{location['lng']}"
    return selected_place['uid'], lat_lng
    
def get_choice(query, region):
    suggestions = get_suggestions(query, region)
    # print_suggestions(suggestions)
    choice = 0
    selected_place = suggestions['result'][choice]
    detail = get_detail(selected_place['uid'])
    location = detail['result']['location']
    lat_lng = f"{location['lat']},{location['lng']}"
    return selected_place['uid'], lat_lng

def get_directions(origin_lat_lng, destination_lat_lng, origin_uid, destination_uid, turn_type_set):
    timestamp = str(int(time.time()))
    direction_params = {
        "origin": origin_lat_lng,
        "destination": destination_lat_lng,
        "origin_uid": origin_uid,
        "destination_uid": destination_uid,
        "ak": ak,
        "timestamp": timestamp,
    }
    response = make_request(riding_uri, direction_params)
    if response and response['status'] == 0:
        steps = response['result']['routes'][0]['steps']
        for step in steps:
            turn_type = step.get('turn_type','None')
            turn_type_set.add(turn_type)
    return response

def time_convert(seconds):
    seconds = int(seconds)
    hours = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    str = f"{hours} 小时, {minutes} 分钟, {seconds} 秒"
    return str

def remove_tags(sentence):
    clean_sentence = re.sub(r'<.*?>', '', sentence)
    return clean_sentence

def detect_turn_type(sentence):
    if re.search(r'(直行|向前)', sentence):
        return 0
    elif re.search(r'左.*?转', sentence):
        return 1
    elif re.search(r'右.*?转', sentence):
        return 2
    elif re.search(r'(掉头|往回)', sentence):
        return 3
    else :
        return -1

def get_steps():
    origin_input = "深圳大学"
    origin_uid, origin_lat_lng = get_choice(origin_input, origin_input[:2])

    destination_input = "深圳宝安国际机场"
    destination_uid, destination_lat_lng = get_choice(destination_input, destination_input[:2])

    turn_type_set = set()
    direction_response = get_directions(origin_lat_lng, destination_lat_lng, origin_uid, destination_uid, turn_type_set)
    
    if direction_response:
        if direction_response['status'] == 0:
            route = direction_response['result']['routes'][0]
            print(f"预计用时：{time_convert(route['duration'])}")
            steps = route['steps']
            
            for idx, step in enumerate(steps):
                instruction = remove_tags(step['instructions'])
                content = instruction[instruction.rfind(',') + 1 :]
                print(f"Step {idx + 1}\t:{re.sub(r'骑行.*?', '', content)}\t{step['turn_type']}\t{detect_turn_type(step['turn_type'])}")
                #print(f"Step {idx + 1}\t:{content}\t{step['turn_type']}\t{detect_turn_type(step['turn_type'])}")
        else:
            print("方向请求失败:", direction_response['message'])

def main():
    turn_type_set = set()
    origin_input = input("请输入起点：")
    origin_uid, origin_lat_lng = get_user_choice("请选择起点（输入序号）：", origin_input, origin_input[:2])

    destination_input = input("请输入终点：")
    destination_uid, destination_lat_lng = get_user_choice("请选择终点（输入序号）：", destination_input, destination_input[:2])

    direction_response = get_directions(origin_lat_lng, destination_lat_lng, origin_uid, destination_uid, turn_type_set)

    if direction_response:
        if direction_response['status'] == 0:
            route = direction_response['result']['routes'][0]
            print(f"从{origin_input}到{destination_input}预计用时：{time_convert(route['duration'])}")
            steps = route['steps']
            for idx, step in enumerate(steps):
                print(f"Step {idx + 1}: {remove_tags(step['instructions'])} 后 {step['turn_type']}, action: {detect_turn_type(step['turn_type'])}")
        else:
            print("方向请求失败:", direction_response['message'])

if __name__ == "__main__":
    # import pdb; pdb.set_trace()
    main()
    #get_steps()

