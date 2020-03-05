# TEST CONVERTER

## base_converter_script

Версия для локальной работы, ориентировчно в среде Windows. 
Для работы скрипт требует установленный и прописанный в системной переменной PATH `Python3`.

### Установка для работы

1.Копируем в директорию, файлы _test_file_converter.py_ и _test_file_converter.bat_ лежали рядом. **Важно!** Имя директории не должно содержать пробелов.
Например:
 - `D:/script`
 - `E:/converter_script`
 - `D:/Скрипт_для_конвертации`

### Описание работы.
1. Перетаскиваем мышкой txt-файл с тестом в формате АСТ на иконку файла test_file_converter.bat
2. В появившемся окне появится информация о исходном файле, и, после обработки, сообщение о том, что файл в формате GIFT создан.
3. Результирующий файл сохраняется в той же директории, что и исходный файл, с префиксом 'GIFT_' и окончанием имени с датой конвертации.

## Django version

### Установка для тестового запуска

1. Клонируем репозиторий:

    `git clone https://github.com/Alexander586951/FUN_test_converter`

2. Устанавливаем зависимости:

    `pip install -r requirements.txt`

3. Для создания базы данных проводим миграцию

    `python manage.py makemigrations`

    `python manage.py migrate`

4. Запускаем сервер :

    `python manage.py runserver`
    
5. По умолчанию тестовый сервер запускается по линку:

    `http://127.0.0.1:8000/` 

### Описание работы

![screenshot_1](https://github.com/Alexander586951/FUN_test_converter/blob/master/media/images/2020-01-30_16-23-36.png?raw=true "Вид формы")

1. Нажать кнопку "Выбрать файл" - система предложит выбрать файл с исходным тестом.
2. Нажать кнопку "Сконвертировать" -  браузер предложит скачать файл с результатом работы.

![screenshot_2](https://github.com/Alexander586951/FUN_test_converter/blob/master/media/images/2020-01-30_16-23-56.png?raw=true "Сохранение файла")


### Очистка места и базы данных

Команда `manage.py clean_data` - очищает записи в БД и промежуточные файлы в папке `media`. До её применения файлы с результатом конвертации не удаляются, возможно - пригодится при внештатных ситуациях для восстановления данных. 

Обрабатывается скриптом, лежащим в `converter_app/management/commands/clean_data.py`