# vkScrapping
Скрипт скачивает песни из плейлиста вк.

#### Алгоритм:

* Исользуя selenium логинимся в вк и запускаем по очереди треки из плейлиста.
* С помощью browsermobproxy отслеживаем network реквесты с передачей аудиофайлов.
* Скачиваем по найдым url песни.
  
#### Перед запуском скрипта необходимо:
1. Установить пакеты selenium и browsermobproxy: pip install selenium, pip install browsermobproxy.
2. Скачать chromedriver.exe <https://chromedriver.storage.googleapis.com/> и browsermob-proxy.bat <http://bmp.lightbody.net/>
3. Присвоить переменным в скрипе "CHROME_PATH", "PROXY_SERVER_PATH" адреса скачанных файлов.

После запуска скрипта python vkScrapping.py потребуется ввести: адресс плейлиста, логин и пароль от вк и количество песен для скачивания.
