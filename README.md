# Проект Foodgram
![example workflow](https://github.com/WorkHotRoad/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL&logoColor=red)
![Django](https://img.shields.io/badge/Django-464646?style=flat-square&logo=Django&logoColor=red)
![DjangoREST](https://img.shields.io/badge/DJANGO-REST-464646??style=flat-square&logo=django&logoColor=red&color=ff1709&labelColor=gray)
![Python](https://img.shields.io/badge/Python-464646?style=flat-square&logo=python&logoColor=red)
![Nginx](https://img.shields.io/badge/Nginx-464646??style=flat-square&logo=nginx&logoColor=red)
![Docker](https://img.shields.io/badge/Docker-464646??style=flat-square&logo=docker&logoColor=red)
![Gunicorn](https://img.shields.io/badge/Gunicorn-464646??style=flat-square&logo=gunicorn&logoColor=red)
![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?style=flat-square&logo=Yandex.Cloud&logoColor=red)
![Telegram](https://img.shields.io/badge/Telegram-464646?style=flat-square&logoColor=black)

На этом сервисе пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, 
добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов,
необходимых для приготовления одного или нескольких выбранных блюд.


### Подготовка и запуск проекта
- Склонировать репозиторий на локальную машину:
```
git clone git@github.com:WorkHotRoad/foodgram-project-react.git
```
## Для запуска проекта на удаленном сервере:
- Войти на сервер
- Установить docker на сервер:
```
sudo apt install docker.io 
```
- Установите docker-compose на сервер:
```
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```
- Объявить разрешение на исполнение docker-compose
```
sudo chmod +x /usr/local/bin/docker-compose
```
- На локальной машине отредактировать файл infra/nginx.conf. В строке server_name впишите IP сервера.
- Скопировать файлы docker-compose.yml и nginx.conf из директории infra на сервер:
```
scp docker-compose.yml <username>@<host>:/home/<username>/
scp nginx.conf <username>@<host>:/home/<username>/
```
- На сервере создать .env файл в дериктории: home/<username>/
```
sudo touch .env
```
- Прописать в файле .env настройки для BD
```
DB_ENGINE=<django.db.backends.postgresql>
DB_NAME=<имя для базы данных postgres>
DB_USER=<пользователь базы>
DB_PASSWORD=<пароль>
DB_HOST=<db>
DB_PORT=<5432>
SECRET_KEY=<секретный ключ проекта django>
```
-На сервере соберить docker-compose:
```
sudo docker-compose up -d --build
```
- На сервере Выполнить слудующие команды
  
    - Сбор статических файлов:
    ```
    sudo docker-compose exec backend python manage.py collectstatic --noinput
    ```
    - Применить миграции:
    ```
    sudo docker-compose exec backend python manage.py migrate --noinput
    ```
    - Загрузить ингридиенты в базу данных:
    ```
    sudo docker-compose exec backend python manage.py load_ingredients
    ```
    - Создать суперпользователя Django:
    ```
    sudo docker-compose exec backend python manage.py createsuperuser
    ```
    - Проект готов к использованию
  ### http://<ваш хост>/admin/ под вашим логином администратора
  ### http://<ваш хост>/
  
## Для запуска проекта на локальном сервере:

  - Установить Docker, Docker-Compose на вашу локальную машину
  - Установить вир.окружение
  - Установить requirements.txt в виртуальном окружении
  - В папке infra создать фаил .env
  - Прописать в файле .env настройки для BD
  ```
  DB_ENGINE=<django.db.backends.postgresql>
  DB_NAME=<имя для базы данных postgres>
  DB_USER=<пользователь базы>
  DB_PASSWORD=<пароль>
  DB_HOST=<db>
  DB_PORT=<5432>
  SECRET_KEY=<секретный ключ проекта django> 
  ```
  - Собрать контейнеры
   ```
  docker-compose up -d --build
   ```
  - После успешного создания контейнеров открыть еще один терминал и войти в web контейнер :
   ```
    docker container ls
    Cкопировать <CONTAINER ID> контейнера : workhotroad/my_foodgram:lates
    docker exec -it <CONTAINER ID > bash
   ```  
  - Выполнить миграции, сбор статики, загрузка данных, создание superuser
  ```
  python manage.py makemigrations
  python manage.py migrate
  python manage.py collectstatic --noinput
  python manage.py load_ingredients
  python manage.py createsuperuser
  ```
  Проект готов к запуску
  http://localhost/ 
