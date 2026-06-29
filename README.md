# 🏠 HomeService

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python">
  <img src="https://img.shields.io/badge/Flask-Web%20Framework-black?style=for-the-badge&logo=flask">
  <img src="https://img.shields.io/badge/MySQL-Database-orange?style=for-the-badge&logo=mysql">
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge">
</p>

<p align="center">
  <strong>A modern web-based platform for booking trusted home services.</strong><br>
  HomeService simplifies the process of finding, booking, and managing professional home service providers through a responsive and user-friendly interface.
</p>

---

## 📖 Overview

HomeService is a web application built with **Flask** that connects customers with professional service providers for various household needs.

The platform provides a streamlined booking experience, role-based dashboards for administrators and users, invoice generation, and an intuitive interface designed to simplify service management.

---

## ✨ Features

- 🔐 User Authentication
- 👤 Role-Based Access (Admin & User)
- 🏠 Home Service Listings
- 📋 Service Detail Page
- 📅 Booking Management
- 🧾 Invoice Generation
- 📊 Dashboard for Users
- ⚙️ Dashboard for Administrators
- 📱 Responsive Interface
- ⚡ Lightweight Flask Backend

---

## 🛠 Tech Stack

| Category | Technology |
|----------|------------|
| Backend | Python, Flask |
| Frontend | HTML5, CSS3, JavaScript |
| Template Engine | Jinja2 |
| Database | MySQL |
| Styling | Custom CSS |
| Version Control | Git & GitHub |
| CI/CD | GitHub Actions |

---

## 📂 Project Structure

```text
HomeService/
│
├── app.py                          # Main Flask application
├── requirements.txt                # Python dependencies
├── yenggeeeee_homeservice.sql      # Database schema
│
├── .github/
│   └── workflows/
│       └── main_fpyeggeeeee.yml    # GitHub Actions workflow
│
├── static/
│   ├── css/
│   │   └── style.css               # Stylesheet
│   └── js/
│       └── custom.js               # Client-side JavaScript
│
└── templates/
    ├── auth.html                   # Authentication page
    ├── base.html                   # Base layout
    ├── dashboard.html              # Main dashboard
    ├── dashboard_admin.html        # Administrator dashboard
    ├── dashboard_user.html         # User dashboard
    ├── detail.html                 # Service detail page
    ├── index.html                  # Landing page
    └── invoice.html                # Booking invoice
```

---

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/LaOdhe16/HomeService.git
```

### 2. Navigate to the Project

```bash
cd HomeService
```

### 3. Create Virtual Environment (Optional)

Windows

```bash
python -m venv venv
venv\Scripts\activate
```

Linux/macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 5. Configure Database

Import the SQL file into your MySQL server.

```text
yenggeeeee_homeservice.sql
```

Update your database configuration inside **app.py** if necessary.

---

### 6. Run the Application

```bash
python app.py
```

Visit:

```
http://127.0.0.1:5000
```

---

## 📸 Application Pages

- 🏠 Landing Page
- 🔐 Login & Authentication
- 👤 User Dashboard
- 🛡️ Admin Dashboard
- 📋 Service Detail
- 🧾 Invoice

> *Screenshots can be added here for better documentation.*

---

## 🎯 Future Improvements

- 💳 Online Payment Gateway
- 📧 Email Notifications
- ⭐ User Reviews & Ratings
- 🔔 Real-time Booking Status
- 📱 Progressive Web App (PWA)
- 🌙 Dark Mode
- 📊 Analytics Dashboard
- 📍 Google Maps Integration
- 🔍 Advanced Service Search
- 📲 Mobile Application

---

## 🤝 Contributing

Contributions are always welcome.

1. Fork this repository

2. Create a new feature branch

```bash
git checkout -b feature/new-feature
```

3. Commit your changes

```bash
git commit -m "Add new feature"
```

4. Push to GitHub

```bash
git push origin feature/new-feature
```

5. Open a Pull Request 🚀

---

## 👨‍💻 Contributors

<table align="center">
<tr>

<td align="center">
<a href="https://github.com/LaOdhe16">
<img src="https://github.com/LaOdhe16.png" width="120px;" alt="Salvado"/><br>
<b>Salvado</b>
</a>
<br>
Project Owner
</td>

<td align="center">
<a href="https://github.com/marckdekeyn-source">
<img src="https://github.com/marckdekeyn-source.png" width="120px;" alt="Marck"/><br>
<b>Marck</b>
</a>
<br>
Contributor
</td>

</tr>
</table>

---

## 🌟 Support

If you like this project, consider giving it a **⭐ Star** on GitHub.

It helps support future development and encourages more open-source contributions.

---

## 📄 License

This project is licensed under the **MIT License**.

---

<p align="center">
Made with ❤️ by
<a href="https://github.com/LaOdhe16">Salvado</a>
and
<a href="https://github.com/marckdekeyn-source">Marck</a>.
</p>
