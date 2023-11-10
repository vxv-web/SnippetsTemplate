# Snippets_0609
## Инструкция по развертыванию проекта


1.Создание виртуального окружения:  
`python3 -m venv venv_name`

2.Активация виртуального окружения  
`source venv_name/bin/activate`

3.Установка пакетов в виртуальное окружение  
`pip install -r requirements.txt`

4.Применение миграций  
`python manage.py migrate`

5.Запуск сервера django  
`python manage.py runserver`

## Запуск терминала в контексте django
`python manage.py shell_plus --ipython`
