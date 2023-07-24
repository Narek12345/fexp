from flask_mail import Message
from fexp import mail


class MessageBodyNotPassedError(Exception):
	def __init__(self):
		self.message = 'No text for the message was passed to the "text" or "html" arguments.'
		super().__init__(self.message)


def send_email_msg(title, recipients, text=None, html=None):
	# Создаем форму письма с помощью экземпляра класса Message.
	msg = Message(title, recipients)

	# Добавляем переданное сообщение в тело формы для сформулировки сообщения.
	if html:
		msg.html = html
	elif text:
		msg.body = text
	else:
		raise MessageBodyNotPassedError()

	# Отправляем сообщение.
	mail.send(msg)