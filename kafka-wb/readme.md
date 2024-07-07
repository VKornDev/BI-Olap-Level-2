### 1) поднять в docker-compose, из репозитория + sasl 
`docker compose -f docker-compose-kafka-sasl.yml up -d`

[<img src="img/1.docker-compose.png" width="900"/>](docker-compose)

### 2) создать топик

[<img src="img/2.topic1.png" width="900"/>](topic1)

### 3) написать python скрипт для заливки данных из небольшой таблицы клика (пегас) в топик кафка в формате json

[<img src="img/3.kafka-broker.png" width="900"/>](from_ch)

### 4) программа Offset Explorer, просмотреть данные в топике

[<img src="img/4.offset-exp.png" width="900"/>](offset-exp)

### 5) чтение из топика питоном

[<img src="img/5.kafka-consumer.png" width="900"/>](from_ch)