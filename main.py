from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = FastAPI()

# Serve static files (like your CSS and JS)
app.mount("/docs", StaticFiles(directory="docs"), name="docs")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Contact Me</title>
        <link rel="stylesheet" href="/static/style.css">
    </head>
    <body>
        <header>
            <h1>Contact Me</h1>
        </header>
        <main>
            <form action="/send_email" method="post">
                <label for="name">Name:</label>
                <input type="text" id="name" name="name" required>
                
                <label for="email">Email:</label>
                <input type="email" id="email" name="email" required>
                
                <label for="message">Message:</label>
                <textarea id="message" name="message" required></textarea>
                
                <button type="submit">Send Message</button>
            </form>
        </main>
    </body>
    </html>
    """

@app.post("/send_email")
async def send_email(name: str = Form(...), email: str = Form(...), message: str = Form(...)):
    sender_email = "mp9597000@gmail.com"  # Replace with your email
    receiver_email = "mp9597000@gmail.com"  # Replace with your email (to receive messages)
    app_password = "cerz ydbb dutf zrbq"  # Replace with your app password

    # Create the email content
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = "New Contact Form Submission"
    
    body = f"Name: {name}\nEmail: {email}\nMessage: {message}"
    msg.attach(MIMEText(body, "plain"))

    try:
        # Connect to the SMTP server
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()  # Secure the connection
            server.login(sender_email, app_password)  # Use app password
            server.sendmail(sender_email, receiver_email, msg.as_string())
        return {"status": "Message sent successfully"}
    except smtplib.SMTPAuthenticationError:
        return {"status": "Failed to send message", "error": "Authentication failed. Check your email and password."}
    except smtplib.SMTPException as e:
        return {"status": "Failed to send message", "error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
