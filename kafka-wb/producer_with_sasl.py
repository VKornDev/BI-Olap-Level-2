from confluent_kafka import Producer
from ..secrets.Connect_DB import connect_CH
import json

config = {
    'bootstrap.servers': 'localhost:9093',  # адрес Kafka сервера
    'client.id': 'simple-producer',
    'sasl.mechanism':'PLAIN',
    'security.protocol': 'SASL_PLAINTEXT',
    'sasl.username': 'admin',
    'sasl.password': 'admin-secret'
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
        producer.produce('from_ch', data.encode('utf-8'), callback=delivery_report)
        producer.poll(0)  # Поллинг для обработки обратных вызовов
    except BufferError:
        print(f"Local producer queue is full ({len(producer)} messages awaiting delivery): try again")

def main():
    client = connect_CH()

    data = client.execute('select dt_date, qty_rid, weekday from tmp.kornev_puasson final limit 10')

    for row in data:
        msg = json.dumps({'dt_date': row[0], 'qty_rid': int(row[1]), 'weekday': row[2]}, default=str, ensure_ascii=False)
        send_message(msg)
        producer.flush()

if __name__ == '__main__':
    main()