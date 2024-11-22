from celery import Celery

# Создаем экземпляр Celery
app_celery = Celery('tasks', broker='redis://localhost:6379/0')