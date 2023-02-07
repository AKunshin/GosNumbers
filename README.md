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
Для примера, имя пользователя admin, пароль 1234

#### Получение jwt-token

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

#### Метод PLATE/GENERATE
Метод для генерации указаннго количества гос. номеров автомобилей

При обращении по http://localhost:8000/plate/generate/ нужно указать желаемое количество номеров
```
curl -X GET -H "Authorization: Bearer Ваш_access-token" -H "Content-Type: application/json" http://localhost:8000/plate/generate/?amount=желаемое_количество_номеров
```
Если не указать amount, будет сгенерирован 1 номер

#### Метод PLATE/GET
Метод для получения номера из БД. id – идентификатор записи в формате uuid4

```
curl -X GET -H "Authorization: Bearer Ваш_access-token" -H "Content-Type: application/json" http://localhost:8000/plate/get/?id=Нужный_вам_uuid
```

#### Метод PLATE/ADD
Метод позволяет добавить гос.номер вручную

Требования к номеру:

Буквы - только кириллица из диапазона: А,В,Е,К,М,Н,О,Р,С,Т,У,Х

Маска номера: 1 буква, 3 цифры, 2 буквы

```
curl -X POST -H "Authorization: Bearer Ваш_access-token" -H "Content-Type: application/json" -d '{"plate":"ГОСНОМЕР"}' http://localhost:8000/plate/add/ 
```

#### Тестирование
Тестирование с помощью unittest.

Coverage 95%
