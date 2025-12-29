from passlib.context import CryptContext
import secrets
from email.message import EmailMessage
import smtplib

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def generate_temp_password() -> str:
    return secrets.token_urlsafe(8)

def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)



def send_patient_welcome_email(to_email: str, temp_password: str):
    msg = EmailMessage()
    msg["Subject"] = "Your Patient Account Credentials"
    msg["From"] = "kamruzzaman.doctorkoi@gmail.com"
    msg["To"] = to_email

    msg.set_content(
        f"""
            Your patient account has been created.
            Email: {to_email}
            Temporary password: {temp_password}

            Please log in and change your password immediately."""
    )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login("kamruzzaman.doctorkoi@gmail.com", "cqzj famm diyd vwpa")
        server.send_message(msg)