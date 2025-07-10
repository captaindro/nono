import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config.settings import settings
from loguru import logger


def send_email_notification(subject: str, message: str):
    if not settings.ENABLE_EMAIL_NOTIFICATIONS:
        logger.debug("Notifications email désactivées.")
        return

    try:
        msg = MIMEMultipart()
        msg['From'] = settings.EMAIL_FROM
        msg['To'] = settings.EMAIL_TO
        msg['Subject'] = subject

        msg.attach(MIMEText(message, 'plain'))

        with smtplib.SMTP(settings.EMAIL_SMTP_SERVER, settings.EMAIL_SMTP_PORT) as server:
            if settings.EMAIL_USE_TLS:
                server.starttls()

            server.login(settings.EMAIL_USERNAME, settings.EMAIL_PASSWORD)
            server.sendmail(settings.EMAIL_FROM, settings.EMAIL_TO, msg.as_string())

        logger.success(f"Email envoyé à {settings.EMAIL_TO} - Sujet : {subject}")

    except Exception as e:
        logger.error(f"Erreur lors de l’envoi de l’email : {e}", exc_info=True)
