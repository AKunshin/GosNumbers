# Сервис генерации государственных номеров автомобилей
-------

# Задание

REST-API (Python)
1. Развернуть локальную базу данных PostgreSQL с созданием архитектуры под следующие пункты задания
2. Реализовать следующий метод: GET | /PLATE/GENERATE (Генерация государственных номеров автомобилей)
* Метод должен принимать следующие параметры: token, amount
* Где: token – Bearer-токен авторизации, amount – количество государственных номеров автомобилей в ответе
* Примечание: token – любой формат, amount – int or null, если не указано, вернуть один номер. Если не указан токен, вернуть соответствующий ответ клиенту.
3. Реализовать следующий метод: GET | /PLATE/GET (Получение государственных номеров автомобилей)
* Метод должен принимать следующие параметры: token, id
* Вернуть в JSON формате все данные по записи
* Где: token – Bearer-токен авторизации, id – идентификатор записи о государственном номере авто
* Примечание: token – любой формат, id – любой (Предпочтительно uuid4 😊). Если не указан токен, вернуть соответствующий ответ клиенту.

4. Реализовать следующий метод: POST | /PLATE/ADD (Добавление государственных номеров автомобилей в базу данных)
* Метод должен принимать следующие параметры: token, plate
* Перед добавлением должна проводиться проверка на корректность государственного номера автомобиля
* Где: token – Bearer-токен авторизации, plate – государственный номер
* Примечание: token – любой формат, plate – str. Оба значения обязательны к передаче, если не указаны, вернуть соответствующие ответы клиенту.
* Технологии: Любые с использование языка Python
* В случае ошибок выдавать в ответе с понятным объяснением проблемы.

# Установка и запуск
-------
```
git clone https://github.com/AKunshin/GosNumbers.git
cd avto_numbers
python3 -m venv env
```
Для Linux:
```
. ./env/bin/activate
```

Для Windows:
```
.\env\Scripts\activate
```
Необходимо создать файл .env и заполнить его своими данными, по образцу .env_example:

```
DJ_SECRET_KEY = your_django_secret_key
DB_NAME = db_name
DB_USER = db_user
DB_PASSWORD = db_password
```
Далее снова в консоли:
```
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
#### Создание учетной записи администратора

```
python manage.py createsuperuser
```
Перейти на  страницу:
```
http://localhost:8000/token/
```
Ввести свои учетные данные, для получения пары ключей
refresh и access.

Либо с помощью curl:
```
curl -X POST -H "Content-Type: application/json" -d '{"username":"admin", "password":"1234"}' http://localhost:8000/token/ 
```
Для выполнения запросов, вам необходимы данные access-ключа. Срок его действия - 5 минут.
После окончания срока действия access-ключа, необходимо перейти на 
```
http://localhost:8000/token/refresh/
```
И ввести refresh ключ, для получения нового access-ключа.
```
curl -X POST -H "Content-Type: application/json" -d '{"refresh":"Ваш refresh-ключ"}' http://localhost:8000/token/refresh/
```

При обращении по http://localhost:8000/plate/generate/
```
curl -X GET -H "Authorization: Bearer Ваш access-token" -H "Content-Type: application/json" http://localhost:8000/plate/generate/?amount=желаемое количество номеров
```