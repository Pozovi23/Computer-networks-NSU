Запуск производится с помощью start.sh

Для проверки работоспособности запустить test.sh, должно вывести "wrote successfully""[\"https://youtube.com\"]"

Для остановки используемых приложением docker-контейнеров использовать stop_and_delete.sh

чтобы расшарить локальный сервер в интернете:

sudo apt install npm

npx localtunnel --port 80 --password compseti

выдаст URl, через которого производится доступ к серверу


curl 127.0.0.1/get_url?url="a"
curl -g "http://[::1]/get_url?url=a"


результатом word файл, со сравнением и кратким резюме