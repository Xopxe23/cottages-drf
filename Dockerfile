FROM python:latest

COPY requirements.txt /temp/requirements.txt

COPY . /cottages-app

WORKDIR /cottages-app

EXPOSE 8000

RUN pip install -r requirements.txt

# RUN ./manage.py migrate
# RUN ./manage.py loaddata fixtures/users.json fixtures/categories.json fixtures/towns.json fixtures/cottages.json fixtures/likes.json fixtures/rents.json fixtures/reviews.json
# RUN ./manage.py search_index --create
# RUN ./manage.py search_index --update

RUN adduser --disabled-password cottages-user

USER cottages-user
