from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pymongo import MongoClient
from datetime import datetime
from collections import defaultdict
from fastapi.responses import FileResponse
import os
import csv


app = FastAPI()
templates = Jinja2Templates(directory="templates")

# MongoDB setup
client = MongoClient("mongodb+srv://riyaz:riyaz1234@cluster0.ru8dnkk.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["student_db"]
student_collection = db["students"]
attendance_collection = db["attendance"]

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html lang="en">
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>Student Attendance Tracker</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background-color: #f0f4f8;
                color: #2c3e50;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                min-height: 100vh;
                margin: 0;
                padding: 20px;
            }
            h1 {
                font-size: 2.5rem;
                margin-bottom: 40px;
                color: #34495e;
                text-align: center;
            }
            .btn-container {
                display: flex;
                flex-direction: column;
                gap: 20px;
                width: 100%;
                max-width: 320px;
            }
            a.button {
                text-decoration: none;
                background-color: #2980b9;
                color: white;
                padding: 15px 20px;
                border-radius: 8px;
                font-weight: 600;
                font-size: 1.1rem;
                text-align: center;
                box-shadow: 0 4px 8px rgba(41, 128, 185, 0.4);
                transition: background-color 0.3s ease, box-shadow 0.3s ease;
                display: block;
            }
            a.button:hover {
                background-color: #1c5980;
                box-shadow: 0 6px 14px rgba(28, 89, 128, 0.7);
            }
            @media (max-width: 400px) {
                h1 {
                    font-size: 2rem;
                    margin-bottom: 30px;
                }
                .btn-container {
                    max-width: 100%;
                }
            }
        </style>
    </head>
    <body>
        <h1>Student Attendance Tracker</h1>
        <div class="btn-container">
            <a href="/add_student" class="button">Add Student</a>
            <a href="/mark_attendance" class="button">Mark Attendance</a>
            <a href="/generate-report" class="button">Generate Attendance Report</a>
        </div>
    </body>
    </html>
    """

# Form to add student
@app.get("/add_student", response_class=HTMLResponse)
def add_student(request: Request):
    return templates.TemplateResponse("add_student.html", {"request": request})

# Handle student form
@app.post("/add_student", response_class=HTMLResponse)
async def save_student(request: Request, name: str = Form(...), roll: int = Form(...)):
    student_collection.insert_one({"name": name, "roll": roll})
    return templates.TemplateResponse("success.html", {"request": request, "name": name})

# Show mark attendance form
@app.get("/mark_attendance", response_class=HTMLResponse)
def show_attendance_form(request: Request):
    students = list(student_collection.find({}, {"_id": 0}))
    return templates.TemplateResponse("mark_attendance.html", {"request": request, "students": students})

# Handle attendance form submission
@app.post("/mark_attendance", response_class=HTMLResponse)
async def handle_attendance(request: Request):
    form = await request.form()
    present_rolls = form.getlist("present")
    date = datetime.now().strftime("%Y-%m-%d")

    students = list(student_collection.find({}, {"_id": 0}))

    for student in students:
        status = "Present" if str(student["roll"]) in present_rolls else "Absent"
        attendance_collection.insert_one({
            "roll": student["roll"],
            "name": student["name"],
            "date": date,
            "status": status
        })

    return HTMLResponse("<h3>Attendance Marked!</h3><p><a href='/'>Go Home</a></p>")


@app.get("/generate-report", response_class=HTMLResponse)
def get_report_form(request: Request):
    return templates.TemplateResponse("report_form.html", {"request": request})


@app.post("/generate-report")
async def create_report(request: Request, month: str = Form(...)):
    """
    month: in format 'YYYY-MM' (e.g., 2025-06)
    """
    records = list(attendance_collection.find({"date": {"$regex": f"^{month}"}}))

    summary = defaultdict(lambda: {"name": "", "total": 0, "present": 0})

    for rec in records:
        roll = rec["roll"]
        summary[roll]["name"] = rec["name"]
        summary[roll]["total"] += 1
        if rec["status"].lower() == "present":
            summary[roll]["present"] += 1

    filename = f"attendance_report_{month}.csv"
    filepath = os.path.join("reports", filename)
    os.makedirs("reports", exist_ok=True)

    with open(filepath, mode="w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Roll", "Name", "Total Days", "Present Days", "Attendance %"])
        for roll, data in summary.items():
            percentage = (data["present"] / data["total"]) * 100 if data["total"] else 0
            writer.writerow([roll, data["name"], data["total"], data["present"], f"{percentage:.2f}%"])

    return FileResponse(path=filepath, filename=filename, media_type="text/csv")