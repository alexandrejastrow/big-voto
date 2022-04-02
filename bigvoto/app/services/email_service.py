from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from app.settings.settings import mail_settings, app_settings
from app.security.auth import create_access_token


def get_config(email_from):
    conf = ConnectionConfig(
        MAIL_USERNAME=mail_settings.MAIL_USERNAME,
        MAIL_PASSWORD=mail_settings.MAIL_PASSWORD,
        MAIL_FROM=email_from,
        MAIL_PORT=mail_settings.MAIL_PORT,
        MAIL_SERVER=mail_settings.MAIL_SERVER,
        MAIL_TLS=mail_settings.MAIL_TLS,
        MAIL_SSL=mail_settings.MAIL_SSL,
        USE_CREDENTIALS=mail_settings.MAIL_USE_CREDENTIALS,
        VALIDATE_CERTS=mail_settings.MAIL_VALIDATE_CERTS,
    )
    return conf


def template(username: str, access_token: str) -> str:
    if app_settings.dev_mode:
        host = mail_settings.MAIL_HOST_DEV
    else:
        host = mail_settings.MAIL_HOST_PROD
    html = f'''
                <h3>Seja bem vindo {username}!</h3>
                <a style="text-decoration: none; color: #000; background: #0275d8; border-radius: 0.5rem;" href="{host}/api/users/verify/{access_token}">
                    <h3>clique aqui para confirmar seu email</h3>
                </a>
    '''
    return html


async def mail_send(id, email, username):
    access_token = await create_access_token(
        data={'sub': id}, expires_delta=30
    )
    message = MessageSchema(
        subject="Big voto - Confirmação de email",
        recipients=[email],
        body=template(username, access_token),
        subtype="html"
    )

    fm = FastMail(get_config(email))
    await fm.send_message(message)
