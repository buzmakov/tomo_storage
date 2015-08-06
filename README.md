# Что делает этот модуль?

Этот модуль получает ID эксперимента из хранилища и проводит томографическую реконструкцию этого эксперимента.

Для запуска mongodb в контейнере docker 

docker run --name my-mongo3 -p 127.0.0.1:27017:27017 -v /home/makov/workspace/tomo_storage/data/db/:/data/db -d mongo:3 --storageEngine wiredTiger
