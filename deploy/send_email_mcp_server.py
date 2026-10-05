import os
from dotenv import load_dotenv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from fastmcp import FastMCP

load_dotenv()

mcp = FastMCP(
    name="Send Email"
)

sender_email = os.getenv("GMAIL_ADDRESS")
password = os.getenv("GMAIL_APP_PASSWORD")

def _send(email:str, subject:str, body:str) -> str:
    receiver_email = email

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    message.attach(MIMEText(body, "plain"))

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(
            sender_email,
            receiver_email,
            message.as_string()
        )

    return "Email sent successfully!"


@mcp.tool
def send_email(email:str, subject:str, body:str) -> str:
    """Can send Eamil to any email address, Just required Email Address, Subject and Body.
        Args:
            email - email address,
            subject - one line subject of email
            body - complete formated plan email body
    """
    return _send(email, subject, body)


mcp.run(transport="streamable-http",  host="0.0.0.0", port=8000)
