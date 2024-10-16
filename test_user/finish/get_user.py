import csv
import json
import pymysql
import time
from apis.pc_apis import XHS_Apis
from test_user.db_user import save_in_user_details
from account_Pool import account_Pool

from multiprocessing import Lock, Pool


class Get_user_info_db():
    def __init__(self):
        self.base_url = "https://edith.xiaohongshu.com"

    def handle_profile_info(self, user_id, user_json):
        # print(user_json)
        user_json = user_json.get('data')
        # 采集时间
        collection_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        # 达人长id，网址里面
        user_id = user_id

        basic_info = user_json.get('basic_info')
        # 昵称
        nickname = basic_info.get('nickname')
        # 达人短id，小红书账号
        red_id = basic_info.get('red_id')
        # 简介
        desc = basic_info.get('desc')
        # 性别
        gender = basic_info.get('gender')
        # IP地址
        ip_location = basic_info.get('ip_location')
        # 头像链接
        image_url = [basic_info.get('imageb'), basic_info.get('images')]

        interactions = user_json.get('interactions')
        follows = ''
        fans = ''
        interaction = ''
        for item in interactions:
            # 关注数
            if item['type'] == 'follows':
                follows = item['count']
            # 粉丝数
            if item['type'] == 'fans':
                fans = item['count']
            # 获赞与收藏数
            if item['type'] == 'interaction':
                interaction = item['count']

        # 达人标签，重点注意
        tags = user_json.get("tags")
        xingzuo = ''
        age = ''
        location = ''
        profession = ''
        for tag in tags:
            if tag.get('tagType') == 'info':
                if tag.get('name') is not None:
                    # 星座
                    if '座' in tag.get('name'):
                        xingzuo = tag.get('name')
                    # 年龄
                    elif '岁' in tag.get('name'):
                        age = tag.get('name')
            # 位置
            elif tag.get('tagType') == 'location':
                location = tag.get('name')
            # 职业
            elif tag.get('tagType') == 'profession':
                if profession == '':
                    profession = tag.get('name')
                elif profession != '':
                    profession = tag.get('name') + '、' + profession

        user_head = ['采集时间', '达人长id', '达人昵称', '达人小红书账号', '简介', '达人性别 1-女，0-男',
                     'ip地址', '达人头像链接',
                     '关注数', '粉丝数', '获赞与收藏数',
                     '星座', '年龄', '位置', '职业', '主页链接']
        user_url = "https://www.xiaohongshu.com/user/profile/" + str(user_id)
        user_detail = [collection_time, user_id, nickname, red_id, desc, gender,
                       ip_location, image_url,
                       follows, fans, interaction,
                       xingzuo, age, location, profession, user_url]
        # print(user_detail)
        for i in range(len(user_detail)):
            user_detail[i] = str(user_detail[i])
        return user_detail


def one_profile_info(user_id, num, cookies_str, cookies_nickname):
    xhs_apis = XHS_Apis()
    get_user_info_db = Get_user_info_db()

    success = False
    while success == False:
        success, msg, user = xhs_apis.get_user_info(user_id, cookies_str)
        time.sleep(1)
        if success == True:
            user_details = get_user_info_db.handle_profile_info(user_id, user)

            print(f"{num}  {num % 5}  {cookies_nickname}  ")
            print(user_details)
            save_in_user_details(user_details)
        else:
            print(msg, f"查询失败 {user_id} {cookies_nickname}")
            time.sleep(5)


def read_csv_list():
    filename_list = ['userid-part01.csv', 'userid-part02.csv', 'userid-part03.csv', 'userid-part04.csv',
                     'userid-part05.csv']
    user_id_list = []
    for filename in filename_list:
        ans = []
        with open(filename, mode='r', newline='', encoding='gbk') as file:
            csv_reader = csv.reader(file)

            for row in csv_reader:
                ans.append(row[0])

        # 去掉表头
        ans = ans[1:]
        user_id_list = user_id_list + ans

    return user_id_list

'''
def task_all_user_details():
    lock = Lock()

    # user_id_list = read_csv_list()
    user_id_list = compare_user_id()
    print(len(user_id_list))

    num = 1
    pool = Pool(processes=5)
    for user_id in user_id_list:
        num = num + 1
        # if num<396326:continue
        # if num==60:break
        cookie = account_Pool[num % 5]

        cookies_nickname = cookie['nickname']
        cookies_str = cookie.get('cookies_str')
        pool.apply_async(one_profile_info, (user_id, num, cookies_str, cookies_nickname))

    print("Started processes")
    pool.close()
    pool.join()
    print("Subprocesses done.")


def compare_user_id():
    conn = pymysql.connect(host="localhost", database="MYSQL", user='root',
                           password='shudong123', charset='utf8mb4')

    cursor = conn.cursor()

    get_user_id_sql = ("SELECT user_id FROM user_details_6;")
    results = []
    try:
        cursor.execute("USE shudong;")
        cursor.execute(get_user_id_sql)
        results = cursor.fetchall()
        # conn.commit()
        print("数据提取成功！")
    except pymysql.Error as e:
        print(f"数据提取失败：{e}")
    finally:
        cursor.close()
        conn.close()
    # print(len(results))
    results = list(results)
    for i in range(len(results)):
        results[i] = results[i][0]

    user_id_list = read_csv_list()
    user_id_list = list(set(user_id_list) - set(results))

    return user_id_list
    # user_id_list-results
    # print(len(user_id_list))

    # cursor.close()
    # conn.close()
'''

def read_user_request():
    conn = pymysql.connect(host="localhost",database="shudong", user='root',
                           password='shudong123', charset='utf8mb4')

    cursor = conn.cursor()

    get_user_id_sql = ("SELECT * FROM user_request;")
    results = []
    try:
        cursor.execute("USE shudong;")
        cursor.execute(get_user_id_sql)
        results = cursor.fetchall()
        # conn.commit()
        print("数据提取成功！")
    except pymysql.Error as e:
        print(f"数据提取失败：{e}")
    finally:
        cursor.close()
        conn.close()
    # print(type(results))
    results = list(results)
    print("数据条数： ", len(results))

    return results


def kafka_user_details():
    user_id_list = read_user_request()
    print(len(user_id_list))
    print(user_id_list)
    #return
    num = 1
    pool = Pool(processes=5)
    for user_id in user_id_list:
        num = num + 1
        cookie = account_Pool[num % 5]
        cookies_nickname = cookie['nickname']
        cookies_str = cookie.get('cookies_str')
        pool.apply_async(one_profile_info, (user_id, num, cookies_str, cookies_nickname))

    print("Started processes")
    pool.close()
    pool.join()
    print("Subprocesses done.")


'''def read_csv(self, filename: str):
    ans = []
    with open(filename, mode='r', newline='', encoding='gbk') as file:
        csv_reader = csv.reader(file)

        for row in csv_reader:
            ans.append(row[0])

    # 去掉表头
    ans = ans[1:]

    for i in range(len(ans)):
        if filename == 'note_link.csv':
            ans[i] = ans[i].split('explore/')[1]
        else:
            # filename=='user_link.csv'
            ans[i] = ans[i].split('profile/')[1]

    return ans'''


if __name__ == '__main__':
    kafka_user_details()

    # task_all_user_details()
    # compare_user_id()
    '''print("test")
    user_id_list = read_csv_list()
    print(len(user_id_list))
    num = 1

    for user_id in user_id_list:
        num = num + 1
        if user_id=="66b2e9c5000000001d022b37":
            print(num)'''
