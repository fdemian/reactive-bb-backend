import logging
import smtplib
import ssl

from .mail_helper import get_message


async def send_email(mail_info):
    # Mail options
    mail_settings = mail_info["options"]
    server_url = mail_settings["url"]
    port = mail_settings["port"]

    # Construct message from headers and mail info.
    message = await get_message(mail_info, mail_settings)

    # If mail delivery is local, do nothing.
    if bool(mail_info["local"]) is True:
        logging.info("[LOCAL EMAIL] - No action taken.")
        return
    else:
        # SEND EMAIL
        sender_email = mail_settings["mailAddress"]
        receiver_email = mail_info["user"].email

        # Try to log in to server and send email
        smtp_client = smtplib.SMTP(server_url, port)
        logging.info(f"Email - Sending {mail_info['type']} email to {receiver_email}.")

        try:
            context = ssl.create_default_context()
            smtp_client.ehlo()
            smtp_client.starttls(context=context)
            smtp_client.ehlo()
            smtp_client.login(
                mail_settings["auth"]["username"], mail_settings["auth"]["password"]
            )
            smtp_client.sendmail(sender_email, receiver_email, message.as_string())
            smtp_client.quit()
            logging.info("Email successfully sent.")
        except Exception as e:
            # Log exception
            logging.error("Email message could not be sent. Exception thrown.")
            logging.error(f"Caught exception:{type(e)}. MESSAGE={e}")
