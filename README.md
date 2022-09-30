# Проект Foodgram продуктовый помощник.
![example workflow](https://github.com/Straga33/foodgram-project-react/actions/workflows/foodgram_workflows.yml/badge.svg)

Проект Foodgram сайт, на котором пользователи могут публиковать рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. Сервис «Список покупок» позволяет пользователям создавать список продуктов, которые нужно купить для приготовления выбранных блюд.

Проект состоит из frontend, реализованом на на фреймворке React и backend реализованом на Django Rest Framework.
Сборка docker представляет из собой три образа: nginx, PostgreSQL и Django+Gunicorn.

![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white)
![Gunicorn](https://img.shields.io/badge/gunicorn-%298729.svg?style=for-the-badge&logo=gunicorn&logoColor=white)
![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)

## Стек технологий в проекте:
- Python
- Dajngo
- REST API
- PostgreSQL
- nginx
- Docker
- React

### Шаблон наполнения env-файла:

DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql

DB_NAME=имя базы данных

POSTGRES_USER=логин для подключения к базе данных

POSTGRES_PASSWORD=пароль для подключения к БД

DB_HOST=db # название сервиса (контейнера)

DB_PORT=5432 # порт для подключения к БД

### Как запустить проект:

Зайти на ВМ и установить docker, docker-compose

Создайте папку infra:

```
mkdir infra
```
Перенести файлы docker-compose.yml и default.conf на сервер.

```
scp docker-compose.yml username@server_ip:/home/<username>/infra
```
```
scp default.conf <username>@<server_ip>:/home/<username>/infra
```
Создайте файл .env в дериктории infra по шаблону.

Выполнить миграции:
```
sudo docker-compose exec backend python manage.py makemigrations
```
```
docker-compose exec web python manage.py migrate
```
Собрать статистику:
```
sudo docker-compose exec backend python manage.py collectstatic --no-input
```
Создать суперпользователя:
```
docker-compose exec web python manage.py createsuperuser
```

### Разработчик:

Басков Михаил (baem-festa@yandex.ru)
