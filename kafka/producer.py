from confluent_kafka import Producer, KafkaError
import pymysql
import json
import re



TOPIC='crawler-talent-test-topic'
Bootstrap_servers='120.27.240.219:27011'


"""
    从MySQL导出数据为元素为元组的列表
    #:param data: json数据
    从MySQL导出数据为元素为元组的列表
"""


def sql_to_user_list():
    conn = pymysql.connect(host="localhost", database="MYSQL", user='root',
                           password='shudong123', charset='utf8mb4')

    cursor = conn.cursor()

    get_user_id_sql = ("SELECT * FROM user_details_1;")
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


"""
    把元素为元组的列表转化为json格式的数据
    :param sql_data: json数据
    把元素为元组的列表转化为json格式的数据
    json格式：
    data={
        "525fdebbb4c4d605de63885a":{
            "collection_time":"2024-08-22-17_53_04",
            ......
        },
        ......
    }
"""
def user_list_to_json(sql_data: list):
    json_data = {}

    for one_sql in sql_data:

        collection_time = one_sql[0]
        user_id = one_sql[1]
        nickname = one_sql[2]
        red_id = one_sql[3]
        desc = one_sql[4]
        gender = one_sql[5]
        ip_location = one_sql[6]
        image_url = one_sql[7]
        follows = one_sql[8]
        fans = one_sql[9]
        interaction = one_sql[10]
        xingzuo = one_sql[11]
        age = one_sql[12]
        location = one_sql[13]
        profession = one_sql[14]
        user_url = one_sql[15]

        '''patt = '\'(.*?)\', \'(.*?)\''
        res = re.findall(pattern=patt, string=image_url)
        res = list(res[0])
        image_url=res[0]'''

        gender = int(gender)
        follows=int(follows)
        fans=int(fans)
        interaction=int(interaction)
        if '岁' in age:
            age=age[:-1]
            age=int(age)

        ti=collection_time
        collection_time=ti[:10]+' '+ti[11:13]+':'+ti[14:16]+':'+ti[17:19]

        if nickname=='':nickname=None
        if red_id=='':red_id=None
        if desc=='':desc=None
        if gender=='':gender=None
        if ip_location=='':ip_location=None
        if image_url=='':image_url=None
        if follows=='':follows=None
        if fans=='':fans=None
        if interaction=='':interaction=None
        if xingzuo=='':xingzuo=None
        if age=='':age=None
        if location=='':location=None
        if profession=='':profession=None
        if profession=='':profession=None

        one_data = {
            "requestMessage": {
                "talent_id": user_id,
                "time_stamp": "2024-08-28 20:03:20",
                "user_id": "34cbd013-c925-4ee2-87f9-beb3f367d5cb"
            },
            "responseMessage":{
                "collection_time": collection_time,
                "nickname": nickname,
                "red_id": red_id,
                "desc": desc,
                "gender": gender,
                "ip_location": ip_location,
                "image_url": image_url,
                "follows": follows,
                "fans": fans,
                "interaction": interaction,
                "xingzuo": xingzuo,
                "age": age,
                "location": location,
                "profession": profession,
                "user_url": user_url
            },
        }

        json_data[user_id] = one_data

    print("数据转化成功! ")
    return json_data
"""
    Kafka生产者，获取json格式的数据，传入Kafka
    :param json_data: json数据
    Kafka生产者，获取json格式的数据，传入Kafka
"""
def kafka_producer(json_data: dict):
    # 配置Kafka生产者
    p = Producer({'bootstrap.servers': Bootstrap_servers})

    # 定义要发送的消息
    def delivery_report(err, msg):
        if err is not None:
            print('Message delivery failed: {}'.format(err))
        else:
            print('Message delivered to {} [{}] at offset {}'.format(msg.topic(), msg.partition(), msg.offset()))

    # 发送消息到Kafka
    for one_data in json_data:
        print(one_data)
        print(json_data[one_data])

        one_json_data = json.dumps(json_data[one_data], ensure_ascii=False)

        # 创建一个新的ProducerRecord对象
        try:
            # 发送消息并获取结果
            record = p.produce(TOPIC, key=str(one_data),
                               value=one_json_data.encode('utf-8'), on_delivery=delivery_report)
            p.poll(0)
        except BufferError as e:
            print('Local producer queue is full: {}'.format(e))

    # 关闭生产者连接
    p.flush()

def start_producer():
    sql_data = sql_to_user_list()

    sql_data = sql_data[:3]

    json_data = user_list_to_json(sql_data)

    kafka_producer(json_data)

if __name__ == '__main__':
    start_producer()



    """
    ('2024-08-22-17_53_04', '525fdebbb4c4d605de63885a', 'Raytian', '100492283', '装修黑白简约风～ 家居｜好物｜日常分享～ 📮731683090@qq.com', '0', '浙江',
             "['https://sns-avatar-qc.xhscdn.com/avatar/5e3af809e1590f000106b118.jpg?imageView2/2/w/540/format/webp', 'https://sns-avatar-qc.xhscdn.com/avatar/5e3af809e1590f000106b118.jpg?imageView2/2/w/360/format/webp']",
             '354', '6377', '18924', '', '', '上海市', '',
             'https://www.xiaohongshu.com/user/profile/525fdebbb4c4d605de63885a')

    """
