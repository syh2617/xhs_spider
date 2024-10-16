import json
import time
import re
from apis.pc_apis import XHS_Apis
import pymysql
from confluent_kafka import Producer, KafkaError, Consumer
from account_Pool import account_Pool
from multiprocessing import Lock, Pool

#笔记
TOPIC_request = ''
TOPIC_response = ''
Bootstrap_servers = '120.27.240.219:27011'
Group_id='spider'

def save_in_note_detail(data):
    conn = pymysql.connect(host="localhost", database="MYSQL", user='root',
                           password='shudong123', charset='utf8mb4')

    cursor = conn.cursor()
    # 达人个人信息表
    insert_sql = ("INSERT INTO note_details_1 VALUES (%s, %s, %s, %s, %s, "
                  "%s,%s, %s, %s, %s,"
                  "%s,%s, %s, %s, %s,  "
                  "%s,%s, %s, %s)")

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

def one_profile_info(note_id, num, cookies_str, cookies_nickname, one_request):
    xhs_apis = XHS_Apis()

    success = False
    while success == False:
        url = f"https://www.xiaohongshu.com/explore/{note_id}"
        success, msg, note_info = xhs_apis.get_note_info(url, cookies_str)
        # print("笔记信息", success, msg, json.dumps(note_info, ensure_ascii=False, separators=(',', ':')))
        #print(note_info)
        #return
        time.sleep(1)
        if success == True:
            note_detail = note_process(note_id, note_info)

            print(f"{num}  {num % 5}  {cookies_nickname}  ")
            print(note_detail)
            save_in_note_detail(note_detail)
            user_message_setting(one_request, note_detail)
        else:
            print(msg, f"查询失败 {note_id} {cookies_nickname}")
            time.sleep(5)

def note_process(note_id, note_json):
    # note_json = json.loads(note_json)

    note_json = note_json.get("note")
    note_json = note_json.get("noteDetailMap")
    note_json = note_json.get(f"{note_id}")
    note_detail = note_json.get("note")

    # note_detail = note_json["data"]["items"][0]

    # 文章id
    note_id = note_id
    # note_detail = note_detail.get('note_card')
    # 笔记的类型
    note_type = note_detail.get("type")
    # 笔记对应达人的头像
    user_avatar = note_detail["user"].get("avatar")
    # 达人id
    user_id = note_detail["user"].get("userId")
    # 笔记对应达人的昵称
    user_nickname = note_detail["user"].get("nickname")

    import time
    # 笔记的采集时间
    collection_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

    # 笔记的发布时间
    create_time = note_detail.get("time")
    # 最后更新时间
    last_update_time = note_detail.get("lastUpdateTime")
    # 标题
    title = note_detail.get("title")
    # 内容
    desc = note_detail.get("desc")

    note_interact_info = note_detail.get("interactInfo")
    # 笔记的点赞数
    liked_count = note_interact_info.get("likedCount")
    # 笔记的收藏数
    collected_count = note_interact_info.get("collectedCount")
    # 笔记的评论数
    comment_count = note_interact_info.get("commentCount")
    # 笔记的转发数
    share_count = note_interact_info.get("shareCount")

    note_tag_list = note_detail.get("tagList")
    # 笔记的话题列表
    tag_list = []
    if len(note_tag_list) != 0:
        for tag in note_tag_list:
            a = tag.get("name")
            tag_list.append(a)

    note_image_list = note_detail.get("imageList")
    # 笔记的所有图片列表
    image_list = []
    if len(note_image_list) != 0:
        for image in note_image_list:
            image = image.get("urlDefault")
            image_list.append(image)
    # 封面图片的url
    first_image = image_list[0]
    # 原文链接
    note_url = f'https://www.xiaohongshu.com/explore/{note_id}'
    # IP地址
    ipLocation = note_detail.get("ipLocation")
    # 视频链接
    try:
        note_video = note_detail.get("video")
        note_video=str(note_video)
        pattern="'masterUrl': '(.*?)',"
        result=re.findall(pattern, note_video)
        note_video=result[0]
        #note_video = note_video.get("media")
        #note_video = note_video.get("video")
        #note_video = note_video.get("stream")
        #note_video = note_video.get("h264")
        #if note_video != None:
        #note_video = note_video[0]
        #note_video = note_video.get("masterUrl")

    except Exception as e:
        print("video scrape fail ", e)
        note_video = "video scrape fail"

    answer = [collection_time, note_id,note_type, desc,
              user_id, user_avatar, user_nickname,
              comment_count, share_count, liked_count, collected_count,
              tag_list, create_time, title, note_video,
              note_url, image_list, last_update_time, ipLocation]
    for i in range(len(answer)):
        answer[i] = str(answer[i])
    return answer

def user_message_setting(one_request, note_detail):
    for i in range(len(note_detail)):
        if note_detail[i] == '':
            note_detail[i] = None

    # 四个数  int格式
    for i in [7, 8, 9,10]:
        if note_detail[i] != None:
            note_detail[i] = int(note_detail[i])

    one_data = {
        'requestMessage': {
            'note_id': one_request[0],
            'time_stamp': one_request[1],
            'user_id': one_request[2]
            # 这里的user_id特指Kafka——id
            # talent_id  是达人id
        },
        'responseMessage': {
            'collection_time': note_detail[0],
            "type": note_detail[2],  # 笔记类型  normal或者video
            #"desc": note_detail[3],  # 笔记内容
            "user_id": note_detail[4],  # 达人id
            "avatar": note_detail[5],  # 达人头像
            "nickname": note_detail[6],  # 达人昵称
            "commentCount": note_detail[7],  # 评论数
            "shareCount": note_detail[8],  # 分享数
            "likedCount": note_detail[9],  # 点赞数
            "collectedCount": note_detail[10],  # 收藏数
            "topicList": note_detail[11],  # 话题列表
            "publish_time": note_detail[12],  # 创建时间
            "title": note_detail[13],  # 笔记题目
            "content": note_detail[3],  # 笔记内容
            "video": note_detail[14],  # 视频链接，如果笔记类型为视频，imageList将只有一个封面
            "url": note_detail[15],  # 原文链接
            "imageList": note_detail[16],  # 图片列表
            "lastUpdateTime": note_detail[17],  # 最后更新时间
            "ipLocation": note_detail[18]  # IP地址
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
            #笔记 暂用cookie： 'nickname': '艾吉奥', 'way': 'qq', 'browser': '油猴',
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
    kafka_consumer()
    pass
    # daily_user_crawler()
    '''one_request = {
        "talent_id": "66cdc573000000001f016e7e",  # 笔记id
        "time_stamp": "2024-08-28 20:03:20",  # 时间戳
        "user_id": "34cbd013-c925-4ee2-87f9-beb3f367d5cb"
    }
    cookies_str = "abRequestId=c4a33db7-fd7a-5397-a902-b7eca7e5a73c; xsecappid=xhs-pc-web; a1=1914fb8edadn0dvsxjkha7xqn6kgca4fougopqglb50000320659; webId=62aa5e1f2f9e8b19f694ef079d8c7e90; gid=yjy4iDYijKl4yjy4iDYdf7Ak0fI8fhMCVTx0k1DWCAIKTl28kS04iU888qJ8K2j82q0dyy40; web_session=040069b7d4a8997d718702c4f0344ba697e04a; webBuild=4.33.2; acw_tc=1b4690e71b6650a2277f9328751bcf18190c5ee38a8c3223df67217847e4b416; websectiga=2845367ec3848418062e761c09db7caf0e8b79d132ccdd1a4f8e64a11d0cac0d; sec_poison_id=3237673f-909d-406e-934b-7fd676f25b7f; unread={%22ub%22:%2266d7d581000000001f01c519%22%2C%22ue%22:%2266d85af3000000000c0189d2%22%2C%22uc%22:5}"
    one_profile_info('66cdc573000000001f016e7e', 1,
                     cookies_str, 1, one_request)
'''
    # note_json = json.loads(note_json, strict=False)
    # print(note_json)
    #pass
