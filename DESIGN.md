- Overview

    This website are help school to manage article, anouncement, and feedback.
    First load you will got home page and you can navigate to other page (Profile, Teacher, Activity, Contact Us and Login)
    In the login area, you can login/register and will riderect to home page for teacher.
    In the teacher area it's based on the role can do this activity

    Role : Teacher
        Create, Edit, Delete your Article

    Role : Administrator
        Create, Edit, Delete, and Publish All Article
        Create, Edit, Delete, and Publish All Anouncement
        Edit, Delete All Feedback
        Add, Edit, Delete, Users

- Major Components

    Role : Users
        View Home Page, Profile, Teacher, Activity, Contact Us and Login
        Can do register, but it will be confirm by administrator

    Role : Teacher
        Create, Edit, Delete your Article

    Role : Administrator
        Create, Edit, Delete, and Publish All Article
        Create, Edit, Delete, and Publish All Anouncement
        Edit, Delete All Feedback
        Add, Edit, Delete, Users

- Algorithms and Data Structures:

    Front End
        HTML, JavaScript, CSS, Bootstrap, Python (Flask), Jinja
    Back End
        HTML, JavaScript, CSS, Bootstrap, Python (Flask), Jinja, DataTables, TinyMCE

    - Database Schema

        CREATE TABLE feedback (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, name TEXT NOT NULL, email TEXT NOT NULL, title TEXT NOT NULL, message TEXT NOT NULL, status TEXT NOT NULL);
        CREATE TABLE sqlite_sequence(name,seq);
        CREATE TABLE teacher (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, name TEXT NOT NULL, email  TEXT NOT NULL, password  TEXT NOT NULL, picture TEXT, subject TEXT, role TEXT NOT NULL);
        CREATE TABLE article (id INTEGER PRIMARY KEY AUTOINCREMENT, type TEXT NOT NULL, title TEXT NOT NULL, content TEXT NOT NULL, status TEXT NOT NULL, time TIMESTAMP DEAFULT CURRENT_TIMESTAMP NOT NULL, user_id INTEGER NOT NULL, FOREIGN KEY(user_id) REFERENCES teacher(id));

        Home Page
        - Article / Anouncement : Simple query to print all the data from database for artcile with spesific type
        - Contact US : Simple POST request to store all feedback data to feedback table
        Login Page
        - Login : Compare user prompt with database, if success will redirect to teacher area, and if failed will give warning massage
        Register Page
        - Register : Insert data from prompt user and default role is Teacher to teacher table, and only Administrator can approve the register
        Teacher Area
        - Home : Welcome message with simple jinja
        - Article : List all of article data with GET request. Can Add artcile with POST request. Edit, Publish, and Delete the data
        - Anouncement : List all of anouncement data with GET request. Can Add anouncement with POST request. Edit, Publish, and Delete the data
        - Feedback : List all of feedback data with GET request. Can Edit, and Delete the data.
        - Teacher/USer : List all of teacher data with GET request. Can Edit, Approve, and Delete (only Teacher role) the data.

- Challenges : Make anouncement and article interface interesting to read. Another could be handling large amounts of feedback and ensuring it's displayed in a manageable way. Handling all data to edit, and delete.
