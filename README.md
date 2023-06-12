# LeoMatch

## Описание
Руководство по использованию сервиса LeoMatch.  
Для работы с сервисом рекомендуется использовать веб-интрефейс REST framework.  

При работе с ним можно выполнить все указанные запросы, в том числе:    
Авторизация/Выход в правом верхнем углу;  
Загрузка аватара при регистрации;  
Указание пола человека по его усмотрению.  

Админ-панель Django:  
http://51.250.103.122/admin/  
login: leva, password: 123456  

*Регистрация нового участника :*  
http://51.250.103.122/api/clients/create  
При регистрации участника использована обычная модель регистрации, добавлены координаты, указывать которые необязательно.  
`{"latitude": 0.0, "longitude": 0.0}` - стандартное значение.  

*Оценивание участником другого участника:*    
http://51.250.103.122/api/clients/{id}/match  
В качестве параметра `{id}` принимается целое число обозначающее id пользователя в системе, найти его можно в списке участников.  

*Список участников:*     
http://51.250.103.122/api/list      
Доступны фильтры по следующим параметрам:    
Пол;  
Имя;  
Фамилия;  
Максимальное расстояние от текущего пользователя (в метрах).  
Работа с фильтрами доступна при нажатии на кнопку Filters в веб-интерфейсе REST framework.(распологается в правом верхнем углу)  
## Установка
GIT install
```
sudo apt install git
```

GDAL install
```
sudo add-apt-repository ppa:ubuntugis/ppa
sudo apt-get update
sudo apt-get install gdal-bin
```

libpq-dev install
```
sudo apt install libpq-dev
```

docker
https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-20-04-ru

postgis inside docker

```
docker run -d --name postgis \
-e POSTGRES_PASSWORD=postgres \
-e POSTGRES_DB=leomatch \
-p 127.0.0.1:5432:5432 postgis/postgis
```

## Приложение
Ссылка на тестовое задание: https://docs.google.com/document/d/1LpUf2cZdtDAZKgDP9zw7i8Qn98r7og0p8QqizZkMfhE/edit
