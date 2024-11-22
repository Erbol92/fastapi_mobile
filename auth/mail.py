import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from auth.celery import app_celery
# Укажите ваши учетные данные
username = 'erbolbaik@mail.ru'  # Ваш email
from config import password

# Настройка параметров письма
sender_email = username
password = password

# Создание MIME-объекта
msg = MIMEMultipart()
msg['From'] = sender_email



@app_celery.task
def send_email(token: str, email_to: str,text:str, subject:str):
    try:
        # Создаем SSL-соединение
        with smtplib.SMTP_SSL("smtp.mail.ru", 465) as server:
            body = text
            msg['Subject'] = subject
            # Добавление текста в письмо
            msg.attach(MIMEText(body, 'plain'))
            server.login(username, password)  # Вход в почтовый ящик
            print("Соединение успешно установлено и аутентификация прошла успешно.")
            server.sendmail(sender_email, email_to,
                            msg.as_string())  # Отправка письма
    except smtplib.SMTPException as e:
        print(f"Ошибка при подключении или аутентификации: {e}")
