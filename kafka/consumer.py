from confluent_kafka import Consumer, KafkaError
import pymysql

TOPIC='crawler-talent-test-topic'
Bootstrap_servers='120.27.240.219:27011'
Group_id='spider'

def msg_to_sql(data):
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
    # print(type(results))
    #results = list(results)
    #print("数据条数： ", len(results))


def kafka_consumer():
    # 配置Kafka消费者
    c = Consumer({'bootstrap.servers': Bootstrap_servers,
                  'group.id': Group_id,
                  'auto.offset.reset': 'earliest'})

    # 订阅主题
    c.subscribe([TOPIC])

    try:
        while True:
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
            msg_to_sql(data)


    except KeyboardInterrupt:
        pass
    finally:
        # 关闭消费者连接
        c.close()

if __name__ == '__main__':
    kafka_consumer()