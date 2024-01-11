# REST API для Fiagdon app


## В приложении реализованы следующие концепции:
- Разработка Веб-Приложений на Python[DjangoRestFramework], следуя дизайну REST API.
- Подход Чистой Архитектуры в построении структуры приложения. Техника внедрения зависимости.
- Авторизация при помощи социальной сети VK и Yandex ID.
- Работа с БД Postgres. Генерация файлов миграций. 
- Работа с БД Redis. Кэширование. 
- Работа с Celery. Отложенная отправка писем на email для верификации.


#### Создаем виртуальное окружение
```
python3 -m venv .venv
```

#### Устаналиваем зависимости
```
pip install -r requirements.txt
```

#### Подготавливаем БД и заполняем данными
```
./manage.py migrate

```
```
./manage.py loaddata fixtures/amenities.json fixtures/categories.json fixtures/cottages.json fixtures/likes.json fixtures/rents.json fixtures/reviews.json fixtures/rules.json fixtures/towns.json fixtures/users.json

```

#### Для запуска тестов:
```
coverage run manage.py test && coverage report
```

### Docker:

```
docker-compose build
```

```
docker-compose up
```


