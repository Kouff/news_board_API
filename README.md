# News_Board_API
### Это тестовый проект, написанный на Python3 с использованеим фреймворков Django и DRF (Django Rest Framework), является аналогом вот этого сайта [HackerNews](https://news.ycombinator.com/) (но без frontend). Проект предназначен для запуска как контейнер с помощью docker-compose.
Код оформлен с помощью [black](https://github.com/psf/black "Black is the uncompromising Python code formatter.").

## Heroku
Сайт можно посмотреть на Heroku - https://secure-falls-10809.herokuapp.com/ . Вот ссылка на список новостей - https://secure-falls-10809.herokuapp.com/api/v1/news/ . Более подробно узнать о url можно ниже в пункте ***URL и API***. 

Войти можно через пользователей admin или user.
| Ник | Пароль |
| ------ | ------ |
| admin | admin |
| user | user |

## Проект
Скачать проект можно с помощью команды:
```
mkdir news_board_API
cd news_board_API
git clone https://github.com/Kouff/news_board_API.git
```
## Подготовка к созданию Docker-контейнера
Создайте образ для Docker:
```
docker build .
```
Далее нужно мигрировать базу данных в Docker:
```
docker-compose run web python /news_board_API/manage.py makemigrations --noinput
docker-compose run web python /news_board_API/manage.py migrate --noinput
```
И создайте суперпользователя в Docker:
```
docker-compose run web python /news_board_API/manage.py createsuperuser
```
## Запуск Docker
Для запуска введите следующую команду:
```
docker-compose up -d --build
```
Готово! Если сделали всё правильно, то по ссылке http://127.0.0.1:8000/ можно перейти на наш сайт.
## URL и API
##### URL сайта:
>http://127.0.0.1:8000/admin/ - вход в учетную запись через Django

>http://127.0.0.1:8000/api-auth/login/ - вход в учетную запись через DRF

>http://127.0.0.1:8000/api/v1/news/ - список всех новостей

>http://127.0.0.1:8000/api/v1/news/<номер новости>/ - детали определённой новости с комментариями. Например:
>http://127.0.0.1:8000/api/v1/news/1/

##### !!!Для создания записи необходимо быть авторизованным!!!
>http://127.0.0.1:8000/api/v1/create_news/ - создание новой записи новости. Пример передачи JSON:
```
{
    "title":"news 1",
    "link":"https://maxkostinevich.com/blog/serverless-geolocation/"
}
```
>http://127.0.0.1:8000/api/v1/create_comment/ - создание нового комментария. Пример передачи JSON:
```
{
    "post":1,                           #номер id поста
    "content":"good news",
    "parent":1                          #номер id комментария, к которому мы отвечаем (поле "parent" не обязательное)
}
```
>http://127.0.0.1:8000/api/v1/create_rating/ - создание нового голоса рейтинга (один пользователь может поставить только один голос для одной новости). Пример передачи JSON:
```
{
    "post":1                           #номер id поста
}
```
## Закрыть контейнер Docker.
```
docker-compose down
```
