import smtplib
from email.mime.text import MIMEText


class EmailClient():

    def __init__(self, email_config):
        self.from_email = email_config.get("from email")
        self.username = email_config.get("username")
        self.password = email_config.get("password")
        self.receiver = email_config.get("receiver")
        self.smtp_server = email_config.get("smtp server")
        self.smtp_port = email_config.get("smtp port")

    # Sends an email with links and info of new ads
    def mail_ads(self, ad_dict, email_title):
        subject = self.__create_email_subject(email_title, len(ad_dict))
        body = self.__create_email_body(ad_dict)

        msg = MIMEText(body, 'html')
        msg['Subject'] = subject
        msg['From'] = self.from_email
        msg['To'] = self.receiver

        server = smtplib.SMTP_SSL(self.smtp_server, self.smtp_port)

        server.ehlo()
        server.login(self.username, self.password)
        server.send_message(msg)

        server.quit()

    def __create_email_subject(self, email_title, ad_count):
        if ad_count > 1:
            return str(ad_count) + ' New ' + email_title + ' Ads Found!'

        return 'One New ' + email_title + ' Ad Found!'

    def __create_email_body(self, ad_dict):
        body = '<!DOCTYPE html> \n<html> \n<body>'
        try:
            for ad_id in ad_dict:
                body += '<p><b>' + ad_dict[ad_id]['Title'] + '</b>' + \
                    ' - ' + ad_dict[ad_id]['Location']

                if ad_dict[ad_id]['Date'] != "":
                    body += ' - ' + ad_dict[ad_id]['Date']
                body += '<br /></p>'

                body += '<a href="' + ad_dict[ad_id]['Url'] + '">'

                body += ad_dict[ad_id]['Image'] + '</a>'

                body += '<p>' + ad_dict[ad_id]['Description'] + '<br />'

                if ad_dict[ad_id]['Details'] != '':
                    body += ad_dict[ad_id]['Details'] + '<br />'

                body += ad_dict[ad_id]['Price'] + \
                    '<br /><br /><br /><br /></p>'

        except KeyError:
            body += '<p>' + ad_dict[ad_id]['Title'] + '<br />'
            body += ad_dict[ad_id]['Url'] + '<br /><br />' + '</p>'

        body += '<p>This is an automated message, \
            please do not reply to this message.</p>'

        return body
