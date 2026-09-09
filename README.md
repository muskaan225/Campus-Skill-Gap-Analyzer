# 🎓 Campus Skill Gap Analyzer

A web-based platform that helps students identify skill gaps based on their skills and career goals. The system allows students to manage their skills, assess their readiness, and understand which skills they need to improve for selected career paths.

## 🚀 Live Demo

**[Try Campus Skill Gap Analyzer](https://campus-skill-gap-analyzer-production.up.railway.app/)**

## 📌 Features

* 👨‍🎓 Student registration and login
* 🔐 Admin registration and login
* 🧑‍💼 Career and skill management
* 📊 Skill-gap analysis
* 📝 Assessment results
* 🎯 Career-oriented skill recommendations
* 🗄️ MySQL database integration
* ☁️ Cloud deployment using Railway

## 🛠️ Technologies Used

### Frontend

* HTML
* CSS
* JavaScript

### Backend

* Python
* Flask

### Database

* MySQL

### Deployment

* Railway

### Version Control

* Git
* GitHub

## 🗂️ Project Structure

```text
Campus-Skill-Gap-Analyzer/
│
├── app.py
├── templates/
│   ├── admin_login.html
│   ├── admin_register.html
│   └── ...
│
├── static/
│   ├── css/
│   ├── js/
│   └── ...
│
├── campus_skill_gap.sql
├── requirements.txt
└── README.md
```

## ⚙️ How to Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/muskaan225/Campus-Skill-Gap-Analyzer.git
cd Campus-Skill-Gap-Analyzer
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
```

### 3. Activate the virtual environment

```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure database variables

Set the required MySQL environment variables:

```text
DB_HOST
DB_USER
DB_PASSWORD
DB_NAME
DB_PORT
```

### 6. Run the application

```bash
python app.py
```

Open the local application in your browser.

## ☁️ Deployment

The application is deployed using Railway and connected to the GitHub repository.

Every update pushed to the `main` branch can trigger a new deployment.

## 🎯 Purpose

The Campus Skill Gap Analyzer is designed to help students understand the difference between their current skills and the skills expected for their desired career paths.

## 👩‍💻 Author

**Muskaan**

B.Tech – Information Technology
