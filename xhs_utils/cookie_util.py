# 从文件中读取cookie字符串列表
def get_all_cookies_str(path="./cookies"):
    with open(path, "r", encoding="utf-8") as f:
        cookies_str = f.read()
    cookies_str_list = cookies_str.split("\n")
    if cookies_str_list[-1] == "":
        cookies_str_list = cookies_str_list[:-1]
    return cookies_str_list

# 将ck_str转换为ck_dict
def trans_cookies(cookies_str):
    return {i.split('=')[0]: '='.join(i.split('=')[1:]) for i in cookies_str.split('; ')}

# 获取所有cookie字典格式的，用列表存储
def get_all_cookies_list(path="./cookies"):
    cookies_str_list = get_all_cookies_str(path)
    cookies_list = []
    for cookies_str in cookies_str_list:
        cookies_list.append(trans_cookies(cookies_str))
    return cookies_list

# 深拷贝cookie_1
def deepcopy_cookies(cookies_1):
    cookies_2 = dict()
    for key in cookies_1.keys():
        cookies_2[key] = cookies_1[key]
    return cookies_2

