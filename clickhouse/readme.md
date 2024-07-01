### Поднять кликхаус в докере
`docker run -d --name local-clickhouse-server -p 8123:8123 --ulimit nofile=262144:262144 clickhouse/clickhouse-server`

### Cкриншоты данных в таблице stg и current слоя

> Stage слой

[<img src="img/img1.png" width="700"/>](Stage)

> Current слой

[<img src="img/img2.png" width="700"/>](Current)