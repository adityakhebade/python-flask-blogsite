# 📝 Flask Blogsite

A simple and secure blog web application built with **Python Flask**, featuring user registration, login, password reset via email, and blog posting functionality.

---

## 🚀 Features

- ✅ User Registration & Login
- 🔐 Password Reset via Email (using Flask-Mail)
- ✍️ Create, Edit, Delete Blog Posts
- 👤 User Dashboard
- 📧 Environment-based configuration using `.env`
- 📦 Requirements managed via `requirements.txt`

---

## 🛠 Tech Stack

- **Backend:** Python, Flask
- **Authentication:** Flask-Login, Werkzeug
- **Email Service:** Flask-Mail
- **Templating:** Jinja2
- **Database:** SQLite (default, configurable)

---

## 📁 Project Structure

```bash
flasku/
├── static/             # CSS, JS, images
├── templates/          # HTML templates
├── __init__.py         # App factory
├── routes.py           # Route handlers
├── models.py           # Database models
├── forms.py            # WTForms classes
├── email.py            # Email sending logic
instance/
├── config.py           # Configuration (e.g. secret keys)
.env                    # Environment variables

1. Clone the repo
bash
Copy
Edit
git clone https://github.com/adityakhebade/python-flask-blogsite.git
cd python-flask-blogsite


2. Create and activate a virtual environment
bash
Copy
Edit
python -m venv env
# Windows
env\Scripts\activate
# Linux/Mac
source env/bin/activate


3. Install dependencies
bash
Copy
Edit
pip install -r requirements.txt


4. Set up environment variables
Create a .env file in the root directory:
env
Copy
Edit
SECRET_KEY=your_secret_key
MAIL_USERNAME=your_email@example.com
MAIL_PASSWORD=your_email_password
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
⚠️ Use App Passwords if you're using Gmail.


5.▶️ Running the App
bash
Copy
Edit
flask run
Then open http://127.0.0.1:5000 in your browser.

📬 Contact
Made with ❤️ by Aditya Khebade
📧 adityakhebade9@gmail.com
🌐 GitHub
requirements.txt        # Python dependencies
run.py                  # Entry point to start the app
