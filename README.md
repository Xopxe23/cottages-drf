# REST API для Fiagdon app


## В приложении реализованы следующие концепции:
- Разработка Веб-Приложений на Python[DjangoRestFramework], следуя дизайну REST API.
- Подход Чистой Архитектуры в построении структуры приложения. Техника внедрения зависимости.
- Работа с БД Postgres. Генерация файлов миграций. 
- Работа с БД Redis. Кэширование. 
- Работа с Celery. Отложенная отправка писем на email для верификации.

### Для подготвки docker образа:

```
docker compose build
```

#### Подготавливаем БД (применяем миграции) 
```
docker-compose run web-app ./manage.py makemigrations && docker-compose run web-app ./manage.py migrate
```

#### Заполняем БД данными
```
docker-compose run web-app ./manage.py loaddata fixtures/amenities.json fixtures/categories.json fixtures/cottages.json fixtures/likes.json fixtures/rents.json fixtures/reviews.json fixtures/rules.json fixtures/towns.json fixtures/users.json

```

### Для запуска контейнера:

```
docker compose up
```