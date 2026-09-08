# =========================================================
# CAMPUS SKILL GAP ANALYZER
# COMPLETE APP.PY
# =========================================================


# =========================================================
# IMPORTS
# =========================================================

from flask import Flask, render_template, request, redirect, session

import mysql.connector

import os
# =========================================================
# FLASK APPLICATION
# =========================================================

app = Flask(__name__)


# =========================================================
# SECRET KEY
# =========================================================

app.secret_key = "campus-skill-gap-secret"


# =========================================================
# MYSQL DATABASE CONNECTION
# =========================================================

import os


def get_db_connection():

    return mysql.connector.connect(

        host=os.environ.get("DB_HOST"),

        user=os.environ.get("DB_USER"),

        password=os.environ.get("DB_PASSWORD"),

        database=os.environ.get("DB_NAME"),

        port=int(os.environ.get("DB_PORT", 3306))

    )


# =========================================================
# HOME PAGE
# =========================================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# =========================================================
# STUDENT REGISTER
# =========================================================

@app.route(
    "/register",
    methods=["GET", "POST"]
)
def register():

    if request.method == "POST":

        name = request.form.get("name")

        email = request.form.get("email")

        password = request.form.get("password")


        connection = get_db_connection()

        cursor = connection.cursor()


        cursor.execute(
            """
            SELECT id
            FROM students
            WHERE email = %s
            """,
            (email,)
        )


        existing_student = cursor.fetchone()


        if existing_student:

            cursor.close()

            connection.close()

            return "Email already registered."


        cursor.execute(
            """
            INSERT INTO students
            (
                name,
                email,
                password
            )
            VALUES
            (
                %s,
                %s,
                %s
            )
            """,
            (
                name,
                email,
                password
            )
        )


        connection.commit()


        cursor.close()

        connection.close()


        return redirect("/login")


    return render_template(
        "register.html"
    )


# =========================================================
# STUDENT LOGIN
# =========================================================

@app.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    if request.method == "POST":

        email = request.form.get("email")

        password = request.form.get("password")


        connection = get_db_connection()

        cursor = connection.cursor(
            dictionary=True
        )


        cursor.execute(
            """
            SELECT *
            FROM students
            WHERE email = %s
            AND password = %s
            """,
            (
                email,
                password
            )
        )


        student = cursor.fetchone()


        cursor.close()

        connection.close()


        if student:

            session["student_id"] = student["id"]

            session["student_name"] = student["name"]

            return redirect("/dashboard")


        return "Invalid email or password."


    return render_template(
        "login.html"
    )


# =========================================================
# STUDENT LOGOUT
# =========================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")


# =========================================================
# STUDENT DASHBOARD
# =========================================================

@app.route("/dashboard")
def dashboard():

    if "student_id" not in session:

        return redirect("/login")


    student_id = session["student_id"]


    connection = get_db_connection()

    cursor = connection.cursor(
        dictionary=True
    )


    cursor.execute(
        """
        SELECT
            s.skill_name,
            ss.proficiency

        FROM student_skills ss

        JOIN skills s
        ON ss.skill_id = s.id

        WHERE ss.student_id = %s

        ORDER BY s.skill_name
        """,
        (student_id,)
    )


    skills = cursor.fetchall()


    level_percentage = {

        "Beginner": 33,

        "Intermediate": 66,

        "Advanced": 100

    }


    for skill in skills:

        skill["percentage"] = level_percentage.get(
            skill["proficiency"],
            0
        )


    cursor.execute(
        """
        SELECT
            ar.id,
            ar.match_percentage,
            ar.assessment_date,
            c.career_name

        FROM assessment_results ar

        JOIN careers c
        ON ar.career_id = c.id

        WHERE ar.student_id = %s

        ORDER BY ar.assessment_date DESC

        LIMIT 1
        """,
        (student_id,)
    )


    latest_result = cursor.fetchone()


    cursor.close()

    connection.close()


    return render_template(

        "dashboard.html",

        student_name=session["student_name"],

        skills=skills,

        latest_result=latest_result

    )


# =========================================================
# ASSESSMENT
# =========================================================

@app.route(
    "/assessment",
    methods=["GET", "POST"]
)
def assessment():

    if "student_id" not in session:

        return redirect("/login")


    if request.method == "POST":

        student_id = session["student_id"]


        skills = {

            "Python":
                request.form.get("python"),

            "Java":
                request.form.get("java"),

            "C++":
                request.form.get("cpp"),

            "DSA":
                request.form.get("dsa"),

            "HTML":
                request.form.get("html"),

            "CSS":
                request.form.get("css"),

            "JavaScript":
                request.form.get("javascript"),

            "React":
                request.form.get("react"),

            "SQL":
                request.form.get("sql"),

            "MongoDB":
                request.form.get("mongodb"),

            "Excel":
                request.form.get("excel"),

            "Power BI":
                request.form.get("powerbi"),

            "Statistics":
                request.form.get("statistics"),

            "Pandas":
                request.form.get("pandas"),

            "Machine Learning":
                request.form.get(
                    "machine_learning"
                ),

            "Git & GitHub":
                request.form.get("git"),

            "OOP":
                request.form.get("oop"),

            "DBMS":
                request.form.get("dbms"),

            "Operating Systems":
                request.form.get("os"),

            "Computer Networks":
                request.form.get("networks")

        }


        connection = get_db_connection()

        cursor = connection.cursor()


        cursor.execute(
            """
            DELETE FROM student_skills
            WHERE student_id = %s
            """,
            (student_id,)
        )


        for skill_name, proficiency in skills.items():

            if proficiency:

                cursor.execute(
                    """
                    SELECT id
                    FROM skills
                    WHERE skill_name = %s
                    """,
                    (skill_name,)
                )


                result = cursor.fetchone()


                if result:

                    skill_id = result[0]


                    cursor.execute(
                        """
                        INSERT INTO student_skills
                        (
                            student_id,
                            skill_id,
                            proficiency
                        )
                        VALUES
                        (
                            %s,
                            %s,
                            %s
                        )
                        """,
                        (
                            student_id,
                            skill_id,
                            proficiency
                        )
                    )


        connection.commit()


        cursor.close()

        connection.close()


        return redirect("/career")


    return render_template(
        "assessment.html"
    )


# =========================================================
# CAREER / SKILL GAP ANALYSIS
# =========================================================

@app.route(
    "/career",
    methods=["GET", "POST"]
)
def career():

    if "student_id" not in session:

        return redirect("/login")


    student_id = session["student_id"]


    connection = get_db_connection()

    cursor = connection.cursor(
        dictionary=True
    )


    if request.method == "GET":

        cursor.execute(
            """
            SELECT
                id,
                career_name

            FROM careers

            ORDER BY career_name
            """
        )


        careers = cursor.fetchall()


        cursor.close()

        connection.close()


        return render_template(

            "career.html",

            careers=careers

        )


    selected_career_id = request.form.get(
        "career"
    )


    if not selected_career_id:

        cursor.close()

        connection.close()

        return "Please select a career."


    cursor.execute(
        """
        SELECT
            career_name

        FROM careers

        WHERE id = %s
        """,
        (selected_career_id,)
    )


    career_result = cursor.fetchone()


    if not career_result:

        cursor.close()

        connection.close()

        return "Career not found."


    selected_career = career_result[
        "career_name"
    ]


    cursor.execute(
        """
        SELECT
            s.skill_name,
            ss.proficiency

        FROM student_skills ss

        JOIN skills s
        ON ss.skill_id = s.id

        WHERE ss.student_id = %s
        """,
        (student_id,)
    )


    student_skills = cursor.fetchall()


    student_skill_dict = {

        row["skill_name"]:
            row["proficiency"]

        for row in student_skills

    }


    cursor.execute(
        """
        SELECT
            s.skill_name,
            cs.required_level

        FROM career_skills cs

        JOIN skills s
        ON cs.skill_id = s.id

        WHERE cs.career_id = %s
        """,
        (selected_career_id,)
    )


    required_skills = cursor.fetchall()


    level_values = {

        "Beginner": 1,

        "Intermediate": 2,

        "Advanced": 3

    }


    matched_skills = []

    missing_skills = []


    for skill in required_skills:

        skill_name = skill["skill_name"]

        required_level = skill["required_level"]

        student_level = student_skill_dict.get(
            skill_name
        )


        if student_level:

            student_value = level_values.get(
                student_level,
                0
            )

            required_value = level_values.get(
                required_level,
                0
            )


            if student_value >= required_value:

                matched_skills.append(
                    f"{skill_name} "
                    f"({student_level})"
                )

            else:

                missing_skills.append(
                    f"{skill_name} "
                    f"(Required: {required_level}, "
                    f"Your level: {student_level})"
                )

        else:

            missing_skills.append(
                f"{skill_name} "
                f"(Required: {required_level})"
            )


    total_required = len(
        required_skills
    )


    if total_required > 0:

        match_percentage = round(

            len(matched_skills)
            /
            total_required
            *
            100

        )

    else:

        match_percentage = 0


    cursor.execute(
        """
        INSERT INTO assessment_results
        (
            student_id,
            career_id,
            match_percentage
        )
        VALUES
        (
            %s,
            %s,
            %s
        )
        """,
        (
            student_id,
            selected_career_id,
            match_percentage
        )
    )


    connection.commit()


    cursor.close()

    connection.close()


    return render_template(

        "results.html",

        career=selected_career,

        matched_skills=matched_skills,

        missing_skills=missing_skills,

        match_percentage=match_percentage

    )


# =========================================================
# CAREER RECOMMENDATIONS
# =========================================================

@app.route("/recommendations")
def recommendations():

    if "student_id" not in session:

        return redirect("/login")


    student_id = session["student_id"]


    connection = get_db_connection()

    cursor = connection.cursor(
        dictionary=True
    )


    cursor.execute(
        """
        SELECT
            s.skill_name,
            ss.proficiency

        FROM student_skills ss

        JOIN skills s
        ON ss.skill_id = s.id

        WHERE ss.student_id = %s
        """,
        (student_id,)
    )


    student_skills = cursor.fetchall()


    student_skill_dict = {

        row["skill_name"]:
            row["proficiency"]

        for row in student_skills

    }


    cursor.execute(
        """
        SELECT
            id,
            career_name

        FROM careers

        ORDER BY career_name
        """
    )


    careers = cursor.fetchall()


    level_values = {

        "Beginner": 1,

        "Intermediate": 2,

        "Advanced": 3

    }


    recommendations = []


    for career in careers:

        career_id = career["id"]

        career_name = career["career_name"]


        cursor.execute(
            """
            SELECT
                s.skill_name,
                cs.required_level

            FROM career_skills cs

            JOIN skills s
            ON cs.skill_id = s.id

            WHERE cs.career_id = %s
            """,
            (career_id,)
        )


        required_skills = cursor.fetchall()


        matched_count = 0

        total_required = len(
            required_skills
        )


        for skill in required_skills:

            skill_name = skill["skill_name"]

            required_level = skill[
                "required_level"
            ]

            student_level = student_skill_dict.get(
                skill_name
            )


            if student_level:

                student_value = level_values.get(
                    student_level,
                    0
                )

                required_value = level_values.get(
                    required_level,
                    0
                )


                if student_value >= required_value:

                    matched_count += 1


        if total_required > 0:

            match_percentage = round(

                matched_count
                /
                total_required
                *
                100

            )

        else:

            match_percentage = 0


        recommendations.append({

            "career_name":
                career_name,

            "match_percentage":
                match_percentage,

            "matched_count":
                matched_count,

            "total_required":
                total_required

        })


    recommendations.sort(

        key=lambda x:
            x["match_percentage"],

        reverse=True

    )


    cursor.close()

    connection.close()


    return render_template(

        "recommendations.html",

        recommendations=recommendations

    )


# =========================================================
# LEARNING RESOURCES
# =========================================================

@app.route("/resources")
def resources():

    if "student_id" not in session:

        return redirect("/login")


    resources = {

        "Python": {

            "topics": [
                "Python Basics",
                "Functions",
                "Lists and Dictionaries",
                "Object-Oriented Programming",
                "File Handling",
                "Exception Handling"
            ],

            "project":
                "Student Record Management System"

        },

        "Java": {

            "topics": [
                "Java Basics",
                "Variables and Data Types",
                "OOP Concepts",
                "Inheritance and Polymorphism",
                "Exception Handling",
                "Collections Framework"
            ],

            "project":
                "Student Management System"

        },

        "SQL": {

            "topics": [
                "SELECT Queries",
                "WHERE and ORDER BY",
                "GROUP BY",
                "JOIN Operations",
                "Subqueries",
                "Aggregate Functions",
                "Database Design"
            ],

            "project":
                "Student Database Management System"

        },

        "DSA": {

            "topics": [
                "Arrays",
                "Strings",
                "Linked Lists",
                "Stacks and Queues",
                "Trees",
                "Sorting and Searching",
                "Basic Graphs"
            ],

            "project":
                "DSA Problem Solving Practice"

        },

        "HTML": {

            "topics": [
                "HTML Basics",
                "Forms",
                "Tables",
                "Semantic HTML",
                "HTML5"
            ],

            "project":
                "Personal Portfolio Website"

        },

        "CSS": {

            "topics": [
                "CSS Basics",
                "Selectors",
                "Flexbox",
                "Grid",
                "Responsive Design"
            ],

            "project":
                "Responsive Portfolio Website"

        },

        "JavaScript": {

            "topics": [
                "Variables",
                "Functions",
                "Arrays and Objects",
                "DOM Manipulation",
                "Events",
                "Fetch API"
            ],

            "project":
                "Interactive To-Do Application"

        },

        "React": {

            "topics": [
                "Components",
                "Props",
                "State",
                "Hooks",
                "Events",
                "API Integration"
            ],

            "project":
                "React Task Management App"

        },

        "MongoDB": {

            "topics": [
                "MongoDB Basics",
                "Collections and Documents",
                "CRUD Operations",
                "Queries",
                "Indexes",
                "MongoDB with Node.js"
            ],

            "project":
                "MERN Student Management System"

        },

        "Machine Learning": {

            "topics": [
                "Machine Learning Basics",
                "Data Preprocessing",
                "Regression",
                "Classification",
                "Decision Trees",
                "Model Evaluation"
            ],

            "project":
                "Student Placement Prediction"

        },

        "Git & GitHub": {

            "topics": [
                "Git Basics",
                "Repositories",
                "Commit and Push",
                "Branches",
                "Merge",
                "Pull Requests"
            ],

            "project":
                "Upload and Manage a GitHub Project"

        },

        "OOP": {

            "topics": [
                "Classes and Objects",
                "Encapsulation",
                "Inheritance",
                "Polymorphism",
                "Abstraction"
            ],

            "project":
                "Bank Management System"

        },

        "DBMS": {

            "topics": [
                "Database Basics",
                "Keys",
                "Normalization",
                "ER Diagrams",
                "Transactions",
                "SQL Queries"
            ],

            "project":
                "College Database Management System"

        },

        "Operating Systems": {

            "topics": [
                "Processes",
                "Threads",
                "CPU Scheduling",
                "Deadlocks",
                "Memory Management",
                "File Systems"
            ],

            "project":
                "CPU Scheduling Simulator"

        },

        "Computer Networks": {

            "topics": [
                "OSI Model",
                "TCP/IP Model",
                "IP Addressing",
                "TCP and UDP",
                "HTTP and HTTPS",
                "DNS"
            ],

            "project":
                "Network Monitoring Dashboard"

        }

    }


    return render_template(

        "resources.html",

        resources=resources

    )


# =========================================================
# ADMIN LOGIN
# =========================================================

@app.route(
    "/admin/login",
    methods=["GET", "POST"]
)
def admin_login():

    if request.method == "POST":

        email = request.form.get("email")

        password = request.form.get("password")


        connection = get_db_connection()

        cursor = connection.cursor(
            dictionary=True
        )


        cursor.execute(
            """
            SELECT *
            FROM admins
            WHERE email = %s
            AND password = %s
            """,
            (
                email,
                password
            )
        )


        admin = cursor.fetchone()


        cursor.close()

        connection.close()


        if admin:

            session["admin_id"] = admin["id"]

            session["admin_name"] = admin["name"]

            return redirect("/admin")


        return "Invalid admin email or password."


    return render_template(
        "admin_login.html"
    )


# =========================================================
# ADMIN LOGOUT
# =========================================================

@app.route("/admin/logout")
def admin_logout():

    session.pop(
        "admin_id",
        None
    )

    session.pop(
        "admin_name",
        None
    )


    return redirect(
        "/admin/login"
    )


# =========================================================
# ADMIN DASHBOARD
# =========================================================

@app.route("/admin")
def admin_dashboard():

    if "admin_id" not in session:

        return redirect(
            "/admin/login"
        )


    connection = get_db_connection()

    cursor = connection.cursor(
        dictionary=True
    )


    cursor.execute(
        """
        SELECT COUNT(*) AS total_students
        FROM students
        """
    )


    total_students = cursor.fetchone()[
        "total_students"
    ]


    cursor.execute(
        """
        SELECT COUNT(*) AS total_assessments
        FROM assessment_results
        """
    )


    total_assessments = cursor.fetchone()[
        "total_assessments"
    ]


    cursor.execute(
        """
        SELECT COUNT(*) AS total_careers
        FROM careers
        """
    )


    total_careers = cursor.fetchone()[
        "total_careers"
    ]


    cursor.execute(
        """
        SELECT
            ar.id,
            s.name AS student_name,
            c.career_name,
            ar.match_percentage,
            ar.assessment_date

        FROM assessment_results ar

        JOIN students s
        ON ar.student_id = s.id

        JOIN careers c
        ON ar.career_id = c.id

        ORDER BY ar.assessment_date DESC

        LIMIT 10
        """
    )


    recent_assessments = cursor.fetchall()


    cursor.close()

    connection.close()


    return render_template(

        "admin.html",

        admin_name=session["admin_name"],

        total_students=total_students,

        total_assessments=total_assessments,

        total_careers=total_careers,

        recent_assessments=recent_assessments

    )


# =========================================================
# ADMIN - VIEW STUDENTS
# =========================================================

@app.route("/admin/students")
def admin_students():

    if "admin_id" not in session:

        return redirect(
            "/admin/login"
        )


    connection = get_db_connection()

    cursor = connection.cursor(
        dictionary=True
    )


    cursor.execute(
        """
        SELECT
            s.id,
            s.name,
            s.email,

            COUNT(ar.id)
            AS assessment_count,

            (
                SELECT
                    ar2.match_percentage

                FROM assessment_results ar2

                WHERE ar2.student_id = s.id

                ORDER BY
                    ar2.assessment_date DESC

                LIMIT 1

            ) AS latest_match

        FROM students s

        LEFT JOIN assessment_results ar

        ON s.id = ar.student_id

        GROUP BY
            s.id,
            s.name,
            s.email

        ORDER BY s.id DESC
        """
    )


    students = cursor.fetchall()


    cursor.close()

    connection.close()


    return render_template(

        "admin_students.html",

        students=students,

        admin_name=session["admin_name"]

    )


# =========================================================
# ADMIN - VIEW STUDENT DETAILS
# =========================================================

@app.route(
    "/admin/students/<int:student_id>"
)
def admin_student_details(student_id):

    if "admin_id" not in session:

        return redirect(
            "/admin/login"
        )


    connection = get_db_connection()

    cursor = connection.cursor(
        dictionary=True
    )


    cursor.execute(
        """
        SELECT
            id,
            name,
            email

        FROM students

        WHERE id = %s
        """,
        (student_id,)
    )


    student = cursor.fetchone()


    if not student:

        cursor.close()

        connection.close()

        return "Student not found."


    cursor.execute(
        """
        SELECT
            s.skill_name,
            ss.proficiency

        FROM student_skills ss

        JOIN skills s
        ON ss.skill_id = s.id

        WHERE ss.student_id = %s

        ORDER BY s.skill_name
        """,
        (student_id,)
    )


    student_skills = cursor.fetchall()


    cursor.execute(
        """
        SELECT
            ar.id,
            c.career_name,
            ar.match_percentage,
            ar.assessment_date

        FROM assessment_results ar

        JOIN careers c
        ON ar.career_id = c.id

        WHERE ar.student_id = %s

        ORDER BY ar.assessment_date DESC
        """,
        (student_id,)
    )


    assessments = cursor.fetchall()


    cursor.close()

    connection.close()


    return render_template(

        "admin_student_details.html",

        student=student,

        student_skills=student_skills,

        assessments=assessments,

        admin_name=session["admin_name"]

    )


# =========================================================
# ADMIN - VIEW ALL ASSESSMENTS
# =========================================================

@app.route("/admin/assessments")
def admin_assessments():

    if "admin_id" not in session:

        return redirect(
            "/admin/login"
        )


    connection = get_db_connection()

    cursor = connection.cursor(
        dictionary=True
    )


    cursor.execute(
        """
        SELECT
            ar.id,
            s.name AS student_name,
            s.email AS student_email,
            c.career_name,
            ar.match_percentage,
            ar.assessment_date

        FROM assessment_results ar

        JOIN students s
        ON ar.student_id = s.id

        JOIN careers c
        ON ar.career_id = c.id

        ORDER BY
            ar.assessment_date DESC
        """
    )


    assessments = cursor.fetchall()


    cursor.close()

    connection.close()


    return render_template(

        "admin_assessments.html",

        assessments=assessments,

        admin_name=session["admin_name"]

    )


# =========================================================
# ADMIN - VIEW CAREERS
# =========================================================

@app.route("/admin/careers")
def admin_careers():

    if "admin_id" not in session:

        return redirect(
            "/admin/login"
        )


    connection = get_db_connection()

    cursor = connection.cursor(
        dictionary=True
    )


    cursor.execute(
        """
        SELECT
            id,
            career_name

        FROM careers

        ORDER BY career_name
        """
    )


    careers = cursor.fetchall()


    cursor.close()

    connection.close()


    return render_template(

        "admin_careers.html",

        careers=careers,

        admin_name=session["admin_name"]

    )


# =========================================================
# ADMIN - ADD CAREER
# =========================================================

@app.route(
    "/admin/careers/add",
    methods=["GET", "POST"]
)
def admin_add_career():

    if "admin_id" not in session:

        return redirect(
            "/admin/login"
        )


    if request.method == "POST":

        career_name = request.form.get(
            "career_name"
        )


        if not career_name:

            return "Career name is required."


        connection = get_db_connection()

        cursor = connection.cursor()


        cursor.execute(
            """
            SELECT id
            FROM careers
            WHERE career_name = %s
            """,
            (career_name,)
        )


        existing_career = cursor.fetchone()


        if existing_career:

            cursor.close()

            connection.close()

            return "Career already exists."


        cursor.execute(
            """
            INSERT INTO careers
            (
                career_name
            )
            VALUES
            (
                %s
            )
            """,
            (career_name,)
        )


        connection.commit()


        cursor.close()

        connection.close()


        return redirect(
            "/admin/careers"
        )


    return render_template(

        "admin_add_career.html",

        admin_name=session["admin_name"]

    )


# =========================================================
# ADMIN - VIEW CAREER REQUIRED SKILLS
# =========================================================

@app.route(
    "/admin/careers/<int:career_id>"
)
def admin_career_skills(career_id):

    if "admin_id" not in session:

        return redirect(
            "/admin/login"
        )


    connection = get_db_connection()

    cursor = connection.cursor(
        dictionary=True
    )


    cursor.execute(
        """
        SELECT
            id,
            career_name

        FROM careers

        WHERE id = %s
        """,
        (career_id,)
    )


    career = cursor.fetchone()


    if not career:

        cursor.close()

        connection.close()

        return "Career not found."


    cursor.execute(
        """
        SELECT
            s.id AS skill_id,
            s.skill_name,
            cs.required_level

        FROM career_skills cs

        JOIN skills s
        ON cs.skill_id = s.id

        WHERE cs.career_id = %s

        ORDER BY s.skill_name
        """,
        (career_id,)
    )


    required_skills = cursor.fetchall()


    cursor.close()

    connection.close()


    return render_template(

        "admin_career_skills.html",

        career=career,

        required_skills=required_skills,

        admin_name=session["admin_name"]

    )


# =========================================================
# ADMIN - ADD REQUIRED SKILL
# =========================================================

@app.route(
    "/admin/careers/<int:career_id>/add-skill",
    methods=["GET", "POST"]
)
def admin_add_career_skill(career_id):

    if "admin_id" not in session:

        return redirect(
            "/admin/login"
        )


    connection = get_db_connection()

    cursor = connection.cursor(
        dictionary=True
    )


    cursor.execute(
        """
        SELECT
            id,
            career_name

        FROM careers

        WHERE id = %s
        """,
        (career_id,)
    )


    career = cursor.fetchone()


    if not career:

        cursor.close()

        connection.close()

        return "Career not found."


    if request.method == "POST":

        skill_id = request.form.get(
            "skill_id"
        )

        required_level = request.form.get(
            "required_level"
        )


        if not skill_id or not required_level:

            cursor.close()

            connection.close()

            return (
                "Please select a skill "
                "and required level."
            )


        cursor.execute(
            """
            SELECT id

            FROM career_skills

            WHERE career_id = %s

            AND skill_id = %s
            """,
            (
                career_id,
                skill_id
            )
        )


        existing_skill = cursor.fetchone()


        if existing_skill:

            cursor.close()

            connection.close()

            return (
                "This skill is already "
                "added to this career."
            )


        cursor.execute(
            """
            INSERT INTO career_skills
            (
                career_id,
                skill_id,
                required_level
            )
            VALUES
            (
                %s,
                %s,
                %s
            )
            """,
            (
                career_id,
                skill_id,
                required_level
            )
        )


        connection.commit()


        cursor.close()

        connection.close()


        return redirect(
            f"/admin/careers/{career_id}"
        )


    cursor.execute(
        """
        SELECT
            id,
            skill_name

        FROM skills

        ORDER BY skill_name
        """
    )


    skills = cursor.fetchall()


    cursor.close()

    connection.close()


    return render_template(

        "admin_add_career_skill.html",

        career=career,

        skills=skills,

        admin_name=session["admin_name"]

    )


# =========================================================
# ADMIN - EDIT REQUIRED SKILL
# =========================================================

@app.route(
    "/admin/careers/<int:career_id>/edit-skill/<int:skill_id>",
    methods=["GET", "POST"]
)
def admin_edit_career_skill(
    career_id,
    skill_id
):

    if "admin_id" not in session:

        return redirect(
            "/admin/login"
        )


    connection = get_db_connection()

    cursor = connection.cursor(
        dictionary=True
    )


    cursor.execute(
        """
        SELECT
            id,
            career_name

        FROM careers

        WHERE id = %s
        """,
        (career_id,)
    )


    career = cursor.fetchone()


    if not career:

        cursor.close()

        connection.close()

        return "Career not found."


    cursor.execute(
        """
        SELECT
            cs.id,
            cs.skill_id,
            cs.required_level,
            s.skill_name

        FROM career_skills cs

        JOIN skills s
        ON cs.skill_id = s.id

        WHERE cs.career_id = %s

        AND cs.skill_id = %s
        """,
        (
            career_id,
            skill_id
        )
    )


    career_skill = cursor.fetchone()


    if not career_skill:

        cursor.close()

        connection.close()

        return "Career skill not found."


    if request.method == "POST":

        required_level = request.form.get(
            "required_level"
        )


        allowed_levels = [

            "Beginner",

            "Intermediate",

            "Advanced"

        ]


        if required_level not in allowed_levels:

            cursor.close()

            connection.close()

            return "Invalid skill level."


        cursor.execute(
            """
            UPDATE career_skills

            SET required_level = %s

            WHERE career_id = %s

            AND skill_id = %s
            """,
            (
                required_level,

                career_id,

                skill_id
            )
        )


        connection.commit()


        cursor.close()

        connection.close()


        return redirect(
            f"/admin/careers/{career_id}"
        )


    cursor.close()

    connection.close()


    return render_template(

        "admin_edit_career_skill.html",

        career=career,

        career_skill=career_skill,

        admin_name=session["admin_name"]

    )


# =========================================================
# ADMIN - DELETE REQUIRED SKILL
# =========================================================

@app.route(
    "/admin/careers/<int:career_id>/delete-skill/<int:skill_id>",
    methods=["POST"]
)
def admin_delete_career_skill(
    career_id,
    skill_id
):

    if "admin_id" not in session:

        return redirect(
            "/admin/login"
        )


    connection = get_db_connection()

    cursor = connection.cursor()


    cursor.execute(
        """
        SELECT id

        FROM career_skills

        WHERE career_id = %s

        AND skill_id = %s
        """,
        (
            career_id,
            skill_id
        )
    )


    career_skill = cursor.fetchone()


    if not career_skill:

        cursor.close()

        connection.close()

        return "Career skill not found."


    cursor.execute(
        """
        DELETE FROM career_skills

        WHERE career_id = %s

        AND skill_id = %s
        """,
        (
            career_id,
            skill_id
        )
    )


    connection.commit()


    cursor.close()

    connection.close()


    return redirect(
        f"/admin/careers/{career_id}"
    )


# =========================================================
# ADMIN - VIEW ALL SKILLS
# =========================================================

@app.route("/admin/skills")
def admin_skills():

    if "admin_id" not in session:

        return redirect(
            "/admin/login"
        )


    connection = get_db_connection()

    cursor = connection.cursor(
        dictionary=True
    )


    cursor.execute(
        """
        SELECT
            id,
            skill_name

        FROM skills

        ORDER BY skill_name
        """
    )


    skills = cursor.fetchall()


    cursor.close()

    connection.close()


    return render_template(

        "admin_skills.html",

        skills=skills,

        admin_name=session["admin_name"]

    )


# =========================================================
# ADMIN - REPORTS & ANALYTICS
# =========================================================

@app.route("/admin/reports")
def admin_reports():

    # -----------------------------------------------------
    # ADMIN LOGIN CHECK
    # -----------------------------------------------------

    if "admin_id" not in session:

        return redirect(
            "/admin/login"
        )


    # -----------------------------------------------------
    # DATABASE CONNECTION
    # -----------------------------------------------------

    connection = get_db_connection()

    cursor = connection.cursor(
        dictionary=True
    )


    # =====================================================
    # TOTAL STUDENTS
    # =====================================================

    cursor.execute(
        """
        SELECT
            COUNT(*) AS total_students

        FROM students
        """
    )


    total_students = cursor.fetchone()[
        "total_students"
    ]


    # =====================================================
    # TOTAL ASSESSMENTS
    # =====================================================

    cursor.execute(
        """
        SELECT
            COUNT(*) AS total_assessments

        FROM assessment_results
        """
    )


    total_assessments = cursor.fetchone()[
        "total_assessments"
    ]


    # =====================================================
    # TOTAL CAREERS
    # =====================================================

    cursor.execute(
        """
        SELECT
            COUNT(*) AS total_careers

        FROM careers
        """
    )


    total_careers = cursor.fetchone()[
        "total_careers"
    ]


    # =====================================================
    # OVERALL AVERAGE MATCH
    # =====================================================

    cursor.execute(
        """
        SELECT
            AVG(match_percentage)
            AS average_match

        FROM assessment_results
        """
    )


    average_result = cursor.fetchone()


    average_match = average_result[
        "average_match"
    ]


    if average_match is None:

        average_match = 0

    else:

        average_match = round(
            float(average_match),
            2
        )


    # =====================================================
    # CAREER-WISE REPORT
    # =====================================================

    cursor.execute(
        """
        SELECT

            c.id,

            c.career_name,

            COUNT(ar.id)
            AS students_assessed,

            AVG(ar.match_percentage)
            AS average_match

        FROM careers c

        LEFT JOIN assessment_results ar

        ON c.id = ar.career_id

        GROUP BY

            c.id,

            c.career_name

        ORDER BY

            average_match DESC
        """
    )


    career_reports = cursor.fetchall()


    # =====================================================
    # FORMAT AVERAGE MATCH
    # =====================================================

    for career in career_reports:

        if career["average_match"] is not None:

            career["average_match"] = round(
                float(career["average_match"]),
                2
            )


    # =====================================================
    # MOST SELECTED CAREER
    # =====================================================

    cursor.execute(
        """
        SELECT

            c.career_name,

            COUNT(ar.id)
            AS selection_count

        FROM assessment_results ar

        JOIN careers c

        ON ar.career_id = c.id

        GROUP BY

            c.id,

            c.career_name

        ORDER BY

            selection_count DESC

        LIMIT 1
        """
    )


    popular_career = cursor.fetchone()


    # =====================================================
    # CLOSE DATABASE
    # =====================================================

    cursor.close()

    connection.close()


    # =====================================================
    # SHOW REPORTS PAGE
    # =====================================================

    return render_template(

        "admin_reports.html",

        admin_name=session["admin_name"],

        total_students=total_students,

        total_assessments=total_assessments,

        total_careers=total_careers,

        average_match=average_match,

        career_reports=career_reports,

        popular_career=popular_career

    )


# =========================================================
# RUN FLASK APPLICATION
# =========================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )