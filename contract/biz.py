import datetime

from utils.mail import EbMail


def send_mail_from_view(task, request, mail_data):
    try:
        mail = EbMail(**mail_data)
        mail.send_email()
        task.status = '99'  # タスク完了
        task.updated_user = request.user
        task.save()
        json = {
            'error': False,
            'updated_date': datetime.datetime.now(),
            'updated_user': '%s %s' % (request.user.last_name, request.user.first_name),
        }
    except Exception as ex:
        json = {
            'error': True,
            'message': str(ex)
        }
    return json
