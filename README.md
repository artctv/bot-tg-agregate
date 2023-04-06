# bot-tg-agregate

## Запуск

- Создать файл `.env` с следующим содержимым:
```dotenv
MONGO_DATABASE=<your_database_name>
MONGO_USER=<your_mongo_user>
MONGO_PASSWORD=<your_mongo_password>
MONGO_ADDRESS=<your_mongo_address>
MONGO_PORT=<your_mongo_port>
BOT_API_TOKEN=<your_telegram_bot_api_token>
```
- Разархивировать архив с дампом базы (в дирректории будет лежать файл `sampleDB`)
- Создать дирректорию `docker-entrypoint-initdb.d`
  - Создать в ней файл `mongorestore.sh` с следующим содержимым:
  ```bash
  mongorestore -d your_database /sampleDB
  ```
- Выполнить `docker-compose up`



## Задание: Тестовое задание junior python developer
- Время на выполнение: 4-6 часов
- Стек: Python3, Asyncio, MongoDB, любая асинхронная библиотека для телеграм бота

### Описание задачи:
Вашей задачей в рамках этого тестового задания будет написание алгоритма агрегации статистических данных о зарплатах сотрудников компании по временным промежуткам. Ссылка на скачивание коллекции со статистическими данными, которую необходимо использовать при выполнении задания, находится в конце документа.

На обычном языке пример задачи выглядит следующим образом:  
**Необходимо посчитать суммы всех выплат с 28.02.2022 по 31.03.2022, единица группировки - день.**

Ваш алгоритм должен принимать на вход:
- Дату и время старта агрегации в ISO формате (далее dt_from)
- Дату и время окончания агрегации в ISO формате (далее dt_upto)
- Тип агрегации (далее group_type). Типы агрегации могут быть следующие: hour, day, month. То есть группировка всех данных за час, день, неделю, месяц.

Пример входных данных:  
```json
{
    "dt_from":"2022-09-01T00:00:00",
    "dt_upto":"2022-12-31T23:59:00",
    "group_type":"month"
}
```

Комментарий к входным данным: 
- вам необходимо агрегировать выплаты с 1 сентября 2022 года по 31 декабря 2022 года, тип агрегации по месяцу
- На выходе ваш алгоритм формирует ответ содержащий:
- Агрегированный массив данных (далее dataset)
- Подписи к значениям агрегированного массива данных в ISO формате (далее labels)

Пример ответа:
```json
{
    "dataset": [5906586, 5515874, 5889803, 6092634], 
    "labels": ["2022-09-01T00:00:00", "2022-10-01T00:00:00", "2022-11-01T00:00:00", "2022-12-01T00:00:00"]
}
```
Комментарий к ответу: 
- в нулевом элементе датасета содержится сумма всех выплат за сентябрь
- в первом элементе сумма всех выплат за октябрь и т.д. В лейблах подписи соответственно элементам датасета.
