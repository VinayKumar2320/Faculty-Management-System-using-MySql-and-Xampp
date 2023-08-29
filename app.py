from flask import Flask, render_template, request, redirect, url_for,flash
import mysql.connector
app = Flask(__name__, template_folder='templates')


app = Flask(__name__)

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="faculty_ms_db"
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Replace this loop with database query for user validation
        cursor = db.cursor()
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()
        cursor.close()
        
        if user:
            return redirect(url_for('dashboard'))
        
        error = 'Invalid credentials. Please try again.'
        return render_template('login.html', error=error)
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/faculty_publications')
def faculty_publications():
    cursor = db.cursor()
    query = """
    SELECT f.faculty_id, f.first_name, f.last_name, rp.publication_title, rp.publication_date
    FROM Faculty f
    LEFT JOIN Research_Publication rp ON f.faculty_id = rp.faculty_id;
    """
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    return render_template('faculty_publications.html', results=results)

@app.route('/avg_credits_per_department')
def avg_credits_per_department():
    cursor = db.cursor()
    query = """
    SELECT d.department_name, AVG(c.credits) as avg_credits
    FROM Department d
    JOIN Course c ON d.department_id = c.department_id
    GROUP BY d.department_name;
    """
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    return render_template('avg_credits_per_department.html', results=results)

@app.route('/faculty_gender_count')
def faculty_gender_count():
    cursor = db.cursor()
    query = """
    SELECT d.department_name, f.gender, COUNT(f.faculty_id) as faculty_count
    FROM Department d
    LEFT JOIN Faculty f ON d.department_id = f.department_id
    GROUP BY d.department_name, f.gender;
    """
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    return render_template('faculty_gender_count.html', results=results)

@app.route('/departments_without_faculty')
def departments_without_faculty():
    cursor = db.cursor()
    query = """
    SELECT d.department_id, d.department_name
    FROM Department d
    LEFT JOIN Faculty f ON d.department_id = f.department_id
    WHERE f.faculty_id IS NULL;
    """
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    return render_template('departments_without_faculty.html', results=results)

@app.route('/faculty_multiple_qualifications')
def faculty_multiple_qualifications():
    cursor = db.cursor()
    query = """
    SELECT f.faculty_id, f.first_name, f.last_name, q.institution, COUNT(q.qualification_id) as qualification_count
    FROM Faculty f
    LEFT JOIN Qualification q ON f.faculty_id = q.faculty_id
    GROUP BY f.faculty_id, f.first_name, f.last_name, q.institution
    HAVING qualification_count > 1;
    """
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    return render_template('faculty_multiple_qualifications.html', results=results)

@app.route('/departments_most_qualifications')
def departments_most_qualifications():
    cursor = db.cursor()
    query = """
    SELECT d.department_id, d.department_name, f.faculty_id, f.first_name, f.last_name
    FROM Department d
    LEFT JOIN Faculty f ON d.department_id = f.department_id
    LEFT JOIN (
        SELECT q.faculty_id, COUNT(q.qualification_id) as qualification_count
        FROM Qualification q
        GROUP BY q.faculty_id
        ORDER BY qualification_count DESC
    ) q ON f.faculty_id = q.faculty_id
    ORDER BY d.department_id, q.qualification_count DESC;
    """
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    return render_template('departments_most_qualifications.html', results=results)

@app.route('/faculty_average_rating')
def faculty_average_rating():
    cursor = db.cursor(dictionary=True)
    query = """
    SELECT f.faculty_id, f.first_name, f.last_name, AVG(r.rating) as avg_publication_rating
    FROM Faculty f
    JOIN Research_Publication rp ON f.faculty_id = rp.faculty_id
    LEFT JOIN Rating r ON rp.publication_id = r.publication_id
    GROUP BY f.faculty_id, f.first_name, f.last_name;
    """
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    
    return render_template('faculty_average_rating.html', results=results)

@app.route('/faculty_list')
def faculty_list():
    cursor = db.cursor(dictionary=True)
    
    # Query faculty list
    query = "SELECT * FROM Faculty"
    cursor.execute(query)
    faculty_list = cursor.fetchall()

    return render_template('faculty_list.html', faculty_list=faculty_list)

@app.route('/delete_faculty/<int:faculty_id>')
def delete_faculty(faculty_id):
    cursor = db.cursor()
    
    # Check if faculty member has research publications
    cursor.execute("SELECT publication_id FROM Research_Publication WHERE faculty_id = %s", (faculty_id,))
    research_publications = cursor.fetchall()

    if research_publications:
        flash("Cannot delete faculty member with research publications.", "danger")
    else:
        # Delete faculty member
        cursor.execute("DELETE FROM Faculty WHERE faculty_id = %s", (faculty_id,))
        db.commit()
        flash("Faculty member deleted successfully.", "success")
    
    return redirect(url_for('faculty_list'))






if __name__ == '__main__':
    app.run(debug=True)
