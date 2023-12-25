from flask import Flask, render_template, request
from constraint import Problem

app = Flask(__name__)

def generate_schedule_csp(classes, faculties, resources, time_slots, rooms, departments, semester):
    problem = Problem()

    # Define variables
    for c in classes:
        problem.addVariable(f"{c}_class", classes)
        problem.addVariable(f"{c}_time", time_slots)
        problem.addVariable(f"{c}_room", rooms)
        problem.addVariable(f"{c}_faculty", faculties)
        problem.addVariable(f"{c}_department", departments)
        problem.addVariable(f"{c}_semester", semester)
        problem.addVariable(f"{c}_resource", resources)

    # Define constraints
    for c in classes:
        problem.addConstraint(lambda *args: len(set(args)) == len(args), [f"{c}_{comp}" for comp in ['class','time', 'room', 'faculty', 'department', 'semester', 'resource']])

    # Solve the CSP
    solutions = problem.getSolutions()
    
    # Use a set to store unique schedule rows
    unique_schedule_rows = set()

    # Convert solutions to a readable format
    for sol in solutions:
        schedule_row = [sol[f"{c}_{comp}"] for c in classes for comp in ['class','time', 'room', 'faculty', 'department', 'semester', 'resource']]
        unique_schedule_rows.add(tuple(schedule_row))

    # Convert the set back to a list
    timetable = [['Class', 'Time Slot', 'Room', 'Faculty', 'Department', 'Semester', 'Resource']]
    timetable.extend(list(unique_schedule_rows))

    return timetable

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_schedule', methods=['POST'])
def generate_schedule_csp_route():
    user_classes = request.form['classes'].split(',')
    user_faculties = request.form['faculties'].split(',')
    user_resources = request.form['resources'].split(',')
    user_time_slots = request.form['time_slots'].split(',')
    user_rooms = request.form['rooms'].split(',')
    user_departments = request.form['departments'].split(',')
    user_semester = request.form['semesters'].split(',')

    schedules = generate_schedule_csp(user_classes, user_faculties, user_resources,
                                       user_time_slots, user_rooms, user_departments, user_semester)

    return render_template('result.html', schedules=schedules)

if __name__ == '__main__':
    app.run(debug=True)
