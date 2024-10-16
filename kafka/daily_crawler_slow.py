import time
import json
from apis.pc_apis import XHS_Apis
import pymysql
from confluent_kafka import Producer, KafkaError, Consumer
from account_Pool import account_Pool
from multiprocessing import Lock, Pool

#宇超 存量 达人 每日更新
TOPIC_request = 'spider-offline-xhs-talent-request-topic'
TOPIC_response = 'spider-realtime-xhs-talent-response-topic'
Bootstrap_servers = '120.27.240.219:27011'
Group_id='spider'

'''
def insert_to_sql(data):
    conn = pymysql.connect(host="localhost", database="MYSQL", user='root',
                           password='shudong123', charset='utf8mb4')

    cursor = conn.cursor()
    # 达人个人信息表
    insert_sql = ("INSERT INTO user_request VALUES (%s, %s, %s)")

    try:
        cursor.execute("USE shudong;")
        cursor.execute(insert_sql, data)
        conn.commit()
        print("数据插入成功！")
    except pymysql.Error as e:
        print(f"数据插入失败：{e}")
    finally:
        cursor.close()
        conn.close()
'''
'''
def read_user_request():
    conn = pymysql.connect(host="localhost", database="shudong", user='root',
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
'''
def save_in_user_detail(data):
    conn = pymysql.connect(host="localhost", database="MYSQL", user='root',
                           password='shudong123', charset='utf8mb4')

    cursor = conn.cursor()
    # 达人个人信息表
    insert_sql = ("INSERT INTO user_details_2 VALUES (%s, %s, %s, %s, %s, "
                  "%s,%s, %s, %s, %s,"
                  "%s,%s, %s, %s, %s,  %s)")

    try:
        cursor.execute("USE shudong;")
        cursor.execute(insert_sql, data)
        conn.commit()
        print("数据插入成功！")
    except pymysql.Error as e:
        print(f"数据插入失败：{e}")
    finally:
        cursor.close()
        conn.close()

def handle_profile_info(user_id, user_json):
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
    image_url = basic_info.get('imageb')

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
                    age = age[:-1]
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

def one_profile_info(user_id, num, cookies_str, cookies_nickname, one_request):
    xhs_apis = XHS_Apis()

    success = False
    chong_num=0
    while success == False:
        success, msg, user = xhs_apis.get_user_info(user_id, cookies_str)
        time.sleep(1.2)
        if success == True:
            user_detail = handle_profile_info(user_id, user)

            print(f"{num}  {num % 5}  {cookies_nickname}  ")
            print(user_detail)
            save_in_user_detail(user_detail)
            user_message_setting(one_request, user_detail)
        else:
            print(msg, f"查询失败 {user_id} {cookies_nickname}")
            time.sleep(5)
            chong_num += 1
            if chong_num == 5:
                success = True

def user_message_setting(one_request, user_detail):
    for i in range(len(user_detail)):
        if user_detail[i] == '':
            user_detail[i] = None

    #性别、关注、粉丝、获赞、年龄  int格式
    for i in [5,8,9,10,12]:
        if user_detail[i] != None:
            user_detail[i] = int(user_detail[i])

    one_data = {
        'requestMessage': {
            'talent_id': one_request[0],
            'time_stamp': one_request[1],
            'user_id': one_request[2]
            # 这里的user_id特指Kafka——id
            # talent_id  是达人id
        },
        'responseMessage': {
            'collection_time': user_detail[0],
            'nickname': user_detail[2],
            'red_id': user_detail[3],
            'desc': user_detail[4],
            'gender': user_detail[5],
            'ip_location': user_detail[6],
            'image_url': user_detail[7],
            'follows': user_detail[8],
            'fans': user_detail[9],
            'interaction': user_detail[10],
            'xingzuo': user_detail[11],
            'age': user_detail[12],
            'location': user_detail[13],
            'profession': user_detail[14],
            'user_url': user_detail[15]
        }
    }
    print(one_data)
    kafka_producer(one_data)
    pass

def kafka_producer(json_data: dict):
    # 配置Kafka生产者
    p = Producer({'bootstrap.servers': Bootstrap_servers})

    # 定义要发送的消息
    def delivery_report(err, msg):
        if err is not None:
            print('Message delivery failed: {}'.format(err))
        else:
            print('Message delivered to {} [{}] at offset {}'.format(msg.topic(), msg.partition(), msg.offset()))

    # 发送一条消息到Kafka
    #for one_data in json_data:
        #print("1",one_data)
        #print(json_data[one_data])

    data_key=json_data["requestMessage"]["talent_id"]
    json_data = json.dumps(json_data, ensure_ascii=False)
    # 创建一个新的ProducerRecord对象
    try:
        # 发送消息并获取结果
        record = p.produce(TOPIC_response, key=str(data_key),
                           value=json_data.encode('utf-8'), on_delivery=delivery_report)
        p.poll(0)
    except BufferError as e:
        print('Local producer queue is full: {}'.format(e))

    # 关闭生产者连接
    p.flush()

'''def daily_user_crawler():
    user_request = read_user_request()
    pool = Pool(processes=5)
    num = 1
    for one_request in user_request:
        print(one_request)
        num = num + 1
        cookie = account_Pool[num % 5]
        cookies_nickname = cookie['nickname']
        cookies_str = cookie.get('cookies_str')
        user_id = one_request[0]
        pool.apply_async(one_profile_info, (user_id, num, cookies_str, cookies_nickname, one_request))

    print("Started processes")
    pool.close()
    pool.join()
    print("Subprocesses done.")'''

def kafka_consumer():
    # 配置Kafka消费者
    c = Consumer({'bootstrap.servers': Bootstrap_servers,
                  'group.id': Group_id,
                  'auto.offset.reset': 'earliest'})

    # 订阅主题
    c.subscribe([TOPIC_request])


    pool = Pool(processes=1)
    num = 1
    try:
        while True:
            num = num + 1
            msg = c.poll(1.0)

            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition event
                    continue
                else:
                    print(msg.error())
                    break

            # 处理接收到的消息
            print('Received message: {}'.format(msg.value().decode('utf-8')))
            data=msg.value().decode('utf-8')
            data=eval(data)
            data=[ data["talent_id"] , data["time_stamp"] , data["user_id"] ]
            #insert_to_sql(data)

            cookie = account_Pool[num % 5]
            #宇超暂用cookie： 'nickname': '艾吉奥', 'way': 'qq', 'id': '42191199019', 'browser': '油猴'
            cookie = account_Pool[2]
            cookies_nickname = cookie['nickname']
            cookies_str = cookie.get('cookies_str')

            user_id = data[0]
            pool.apply_async(one_profile_info, (user_id, num, cookies_str, cookies_nickname, data))

    except KeyboardInterrupt:
        pass
    finally:
        # 关闭消费者连接
        print("Started processes")
        pool.close()
        pool.join()
        print("Subprocesses done.")
        c.close()





if __name__ == '__main__':
    #daily_user_crawler()
    kafka_consumer()
    pass
    '''cookie = account_Pool[6]
    print(cookie)'''
