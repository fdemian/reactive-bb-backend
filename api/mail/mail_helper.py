from os import path
from email.utils import formatdate, make_msgid
from email.message import EmailMessage
from api.utils.utils import async_file_read
import mimetypes

# Templates path.
file_path = path.dirname(__file__)
template_files_path = path.join(file_path, "templates")
logo_svg_path = path.join(template_files_path, "logo.png")

# Subject dict.
subject_dict = {
    "activation": "Activate your account",
    "resetpass": "Reset your password",
}


async def get_mail_data(mail_type, user, url):
    full_path = path.join(template_files_path, (mail_type + ".html"))
    template_text = await async_file_read(full_path)

    plain_text_arr = {
        "activation": f"Hi, {user.username}.Welcome to Morpheus. You're almost there. But we need to complete the "
        f"registration process to check that it really is you. \n In order to complete the registration "
        f"process, you must follow this link: {url} \n You won't be able to log in to the forums until "
        f"you complete this process.",
        "resetpass": f"Hi, {user.username}. You requested a password reset. \n In order to reset your password follow "
        f"this link: {url} \n Once you introduce the new password you will recieve confirmation \n And "
        f"won't be able to log in to the forums with your own password.",
    }

    return {
        "subject": subject_dict[mail_type],
        "plain": plain_text_arr[mail_type],
        "template_text": template_text,
    }


def get_message_headers(mail_info, mail_settings, template):
    return {
        "To": mail_info["user"].email,
        "From": mail_settings["mailAddress"],
        "Date": formatdate(localtime=True),
        "Subject": subject_dict[template],
    }


async def get_multipart_message(mail_info):
    mail_url = f"{mail_info['url']}/{mail_info['type']}/{mail_info['code']}"
    mail_data = await get_mail_data(mail_info["type"], mail_info["user"], mail_url)
    template = mail_data["template_text"].decode("utf-8")

    # Recipient username.
    recepient_username = str(mail_info["user"].username)

    # now create a Content-ID for the image
    image_cid = make_msgid(domain=mail_info["url"])

    html_message = (
        template.replace("{user}", recepient_username)
        .replace("{link}", mail_url)
        .replace("{image_cid}", image_cid[1:-1])
    )

    return {"html": html_message, "text": mail_data["plain"], "image_cid": image_cid}


async def get_message(mail_info, mail_settings):
    # Obtain Message headers and multipart message.
    msg_headers = get_message_headers(mail_info, mail_settings, mail_info["type"])
    multipart_msg = await get_multipart_message(mail_info)

    # Create message
    message = EmailMessage()
    message.set_content(multipart_msg["text"])
    message.add_alternative(multipart_msg["html"], subtype="html")

    # Attach logo to message.
    logo_file_contents = await async_file_read(logo_svg_path)
    maintype, subtype = mimetypes.guess_type(logo_svg_path)[0].split("/")
    # attach it
    message.get_payload()[1].add_related(
        logo_file_contents,
        maintype=maintype,
        subtype=subtype,
        cid=multipart_msg["image_cid"],
    )

    # Set message headers (To/From/Subject/Date and Message-Id headers).
    # message['From'] = msg_headers['From']
    message["To"] = msg_headers["To"]
    message["Subject"] = msg_headers["Subject"]
    message["Date"] = msg_headers["Date"]
    message["Message-Id"] = make_msgid()

    return message
