import smtplib
from email.mime.text import MIMEText
from email.header import Header

def send_email(subject, content, sender_email, sender_password, receiver_email):
    try:
        message = MIMEText(content, 'plain', 'utf-8')
        message['Subject'] = Header(subject, 'utf-8')
        message['From'] = sender_email
        message['To'] = receiver_email

        smtp_obj = smtplib.SMTP_SSL('smtp.qq.com', 465)
        smtp_obj.login(sender_email, sender_password)
        smtp_obj.sendmail(sender_email, [receiver_email], message.as_string())
        smtp_obj.quit()
        return True
    except Exception as e:
        print(f"发送邮件失败：{e}")
        return False