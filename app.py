from flask import Flask, render_template, request
import PyPDF2

app = Flask(__name__)

# Step 1: Extract text from PDF
def extract_text(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# Step 2: Analyze resume
def analyze_resume(text):
    skills_list = ["python", "java", "html", "css", "javascript", "sql"]

    found_skills = []
    for skill in skills_list:
        if skill in text.lower():
            found_skills.append(skill)

    score = len(found_skills) * 15
    if score > 100:
        score = 100

    missing_skills = list(set(skills_list) - set(found_skills))

    result = f"""
Resume Score: {score}/100

Skills Found:
{', '.join(found_skills)}

Missing Skills:
{', '.join(missing_skills)}

Suggestions:
- Add more technical skills
- Include projects
- Improve formatting
"""
    return result

# Step 3: Connect backend to frontend
@app.route('/', methods=['GET', 'POST'])
def index():
    result = ""

    if request.method == 'POST':
        file = request.files['resume']
        text = extract_text(file)
        result = analyze_resume(text)

    return render_template('index.html', result=result)

# Step 4: Run app
if __name__ == "__main__":
    app.run(debug=True)
    