from confluent_kafka import Producer
from clickhouse_driver import Client
import json

config = {
    'bootstrap.servers': '192.168.0.104:29092',  # адрес Kafka сервера
    'client.id': 'simple-producer'
}

producer = Producer(**config)

def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}")

def send_message(data):
    try:
        # Асинхронная отправка сообщения
        producer.produce('shkCreate', data.encode('utf-8'), callback=delivery_report)
        producer.poll(0)  # Поллинг для обработки обратных вызовов
    except BufferError:
        print(f"Local producer queue is full ({len(producer)} messages awaiting delivery): try again")

def main():
    with open("./secrets/wb_key_ch.json") as f:
        param_connect = json.load(f)

    ch = param_connect['server'][0]

    client = Client(host=ch['host'],
                    user=ch['user'],
                    password=ch['password'],
                    database='default',
                    settings={"numpy_columns":True, 'use_numpy':True},
                    compression=True,
                    port=9000)

    data = client.execute("""select shk_id
                                  , chrt_id
                                  , nm_id
                                  , dt
                                  , employee_id
                                  , place_cod
                                  , state_id
                             from shkCreate_full final
                             where dt_load >= now() - interval 1 day
                             limit 5000
                          """)

    for row in data:
        msg = json.dumps(
            {
                'shk_id': int(row[0]),
                'chrt_id': int(row[1]),
                'nm_id': int(row[2]),
                'dt': row[3],
                'employee_id': int(row[4]),
                'place_cod': int(row[5]),
                'state_id': row[6]
            }, default=str, ensure_ascii=False)
        send_message(msg)
        producer.flush()

if __name__ == '__main__':
    main()