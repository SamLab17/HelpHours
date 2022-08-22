
"""
    Mail server settings to use for sending
    notification emails.
"""
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


class Notifier:
    """
        Creates a new Notifier object.
        Requires a credentials file for logging into the
        SMTP server. (See comment above for format)
    """
    def __init__(self, send_notifications: bool, api_key, from_address):
        # Cuts off the newline character at end of string
        self.send_notifications = send_notifications
        if send_notifications:
            self.from_addr = from_address
            self.log = None
            self.client = SendGridAPIClient(api_key)

    # Notifier is created before the Logger object, so the Logger object
    # is added afterwards
    def set_log(self, log):
        self.log = log

    """
        Send an email message to the desired "to_addr".
        The subject of the message is passed into "subject"
        The body of the email is passed into "body"
        The type of the content (either 'html' or 'plain') is passed
          through content_type
    """
    def send_message(self, to_addr, subject, body, body_type):
        if not self.send_notifications:
            return
        if body_type.lower() == 'html':
            msg = Mail(
                    from_email=self.from_addr,
                    to_emails=to_addr,
                    subject=subject,
                    html_content=body
                )
        else:
            msg = Mail(
                from_email=self.from_addr,
                to_emails=to_addr,
                subject=subject,
                plain_text_content=body
            )
        try:
            self.client.send(msg)

        except Exception as e:
            if self.log is not None:
                # Log email error
                self.log.warning(f"Could not send email to {to_addr}. Subject: {subject}.")
                self.log.debug(f"Exception message: {str(e)}")
            else:
                print(f'Could not send email to {to_addr}')
