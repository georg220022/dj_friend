1) Склонировать репозиторий
2) перейти в папку с проектом, выполнить docker-compose up  
  
  
При запуске докера выполнятся автоматически миграции, пройдут тесты, следом запустится сервер  
Документация по API(Использовать как ручки для постмана :) ):  
https://app.swaggerhub.com/templates/BHKKCFGB/11111/1.0.0#/  
Выполнять запросы лучше через Postman, тк я не ставил самоподписанные сертификаты что бы локально поддерживался https  
Все запросы кроме регистрации не имеют тела, тело регистрации {"username": "Ivan"}  
Запросы выполнять без авторизаций  
P.s контрибьютора в проекте нет, просто забыл ключ знакомого удалить при пуше  
