from datetime import datetime


class Logger():

    # The various logging levels to mask out log entries.
    # e.g. Using LEVEL_WARNING will mask out all DEBUG and INFO messages.
    LEVEL_DEBUG = 10
    LEVEL_INFO = 20
    LEVEL_WARNING = 30
    LEVEL_ERROR = 40
    LEVEL_FATAL = 50

    DEBUG_PREFIX = "[Debug]"
    INFO_PREFIX = "[ Info]"
    WARNING_PREFIX = "[ WARN]"
    ERROR_PREFIX = "[ERROR]"
    FATAL_PREFIX = "[FATAL]"

    def __init__(self, email_notifier, admin_emails, log_file, log_level=0):
        '''
            Creates a new Logger instance.
            email_notifier -- An instance of the Notifier class to send emails to admins
            admin_emails -- List of email addresses to send select error and fatal messages to
            log_file -- The name of the log file to create or append to
            log_level -- Logging level. Used to mask out lower severity messages.
                         Should be one of the LEVEL_* class constants defined above.
        '''
        self.email = email_notifier
        self.admin_emails = admin_emails
        self.log_file = log_file
        self.log_level = log_level

    # Helper Methods
    def format_message(severity_prefix, message):
        now = datetime.now()
        time_string = now.strftime("[%b %d, %Y][%H:%M:%S]")
        return f"{time_string}{severity_prefix}: {message}\n"

    def notify_admins(self, message):
        for email in self.admin_emails:
            self.email.send_message(email, "Help Hours Queue Error", message, 'plain')

    def output(self, message):
        with open(self.log_file, 'a') as f:
            f.write(message)

    # Call one of these methods for logging messages

    def debug(self, message):
        if Logger.LEVEL_DEBUG >= self.log_level:
            self.output(Logger.format_message(Logger.DEBUG_PREFIX, message))

    def info(self, message):
        if Logger.LEVEL_INFO >= self.log_level:
            self.output(Logger.format_message(Logger.INFO_PREFIX, message))

    def warning(self, message):
        if Logger.LEVEL_WARNING >= self.log_level:
            self.output(Logger.format_message(Logger.WARNING_PREFIX, message))

    def error(self, message, notify=False):
        if Logger.LEVEL_ERROR >= self.log_level:
            self.output(Logger.format_message(Logger.ERROR_PREFIX, message))
            if notify:
                self.notify_admins()

    def fatal(self, message):
        if Logger.LEVEL_FATAL >= self.log_level:
            self.output(Logger.format_message(Logger.FATAL_PREFIX, message))
            self.notify_admins()
