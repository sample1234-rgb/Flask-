from flask import Flask, render_template, make_response
from reportlab.pdfgen import canvas
from reportlab.platypus.flowables import Image

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('hello.html')

class RotatedImage(Image):
    def wrap(self, availWidth, availHeight):
        h, w = Image.wrap(self, availHeight, availWidth)
        return w, h

    def draw(self):
        self.canv.rotate(90)
        Image.draw(self)


def ruler(pdf):
    for i in range(0, 600):
        if i%100 == 0:
            pdf.drawString(i, 830, '+'+str(i))
        elif i%5 == 0:
            pdf.drawString(i, 842, '|')

    for i in range(0, 1000):
        if i%100 == 0:
            pdf.drawString(2, i, '+'+str(i))
        elif i%5 == 0:
            pdf.drawString(1, i, '--')

    pdf.drawString(570, 830, '-> x')
    pdf.drawString(2, 0, 'v\ny')


@app.route('/pdf')
def pdf_file():
    pdf = canvas.Canvas('my_profile.pdf')
    pdf.setTitle('Profile')
    # ruler(pdf)
    pdf.setFillColor('#fffee8')
    pdf.rect(10, 10, 500, 800, stroke=0, fill=1)

    pdf.setFillColor('black')
    intro = ["I am Gaurav Bhardwaj, 21 yo Software Developer", "currently pursuing my B. Tech. Degree in Computer",
             "Science and Engineering from Dr. B.R. Ambedkar", "National Institute of Technology, Jalandhar."]
    y = 790
    for t in intro:
        pdf.drawString(200, y, t)
        y -= 12

    pdf.drawImage('static/20181223_081218.jpg', 50, 740, width=60, height=60,showBoundary=True)
    pdf.line(25, 730, 475, 730)

    # # Education Table:
    edu = {'name': 'Education', 'points': [
        {'quali': "Bachelor's of Technology (CSE)", 'duration': '7/2018 - -', 'name': 'Dr.B.R. Ambedkar National Institute of Technology, Jalandhar', 'score': '7.01'},
        {'quali': 'Higher', 'duration': '4/2016 - 4/2018', 'name': 'APEEJAY School', 'score': '9.35'},
        {'quali': 'Matrix', 'duration': '4/2015 - 4/2016', 'name': 'APEEJAY School', 'score': '8.8'},
    ]}
    # for i in edu.keys():
    #     if i == 'name':
    pdf.setFont('Courier', 24)
    pdf.drawString(28, 710, edu['name'])
        # else:
        #     for p in i:
    y = 710
    for i in edu['points']:
        pdf.setFont('Helvetica', 12)
        pdf.drawString(200, y, i['duration'])
        pdf.drawString(300, y, i['quali'])
        pdf.setFont('Helvetica', 10)
        pdf.drawString(300, y-10, i['name'])
        pdf.setFont('Courier', 9)
        pdf.drawString(300, y-20, "CGPA: " + i['score'])
        y -= 35

    pdf.line(25, y-10, 475, y-10)

    skil = {'name': 'Skills', 'points': [{'name': 'C/C++', 'status': 'Advance'}, {'name': 'Python', 'status': 'Advance'}
        , {'name': 'Django', 'status': 'Beginner'}, {'name': 'Data Analytics', 'status': 'Beginner'},
         {'name': 'OOPs', 'status': 'Advance'}, {'name': 'Data Structures and Algorithms', 'status': 'Intermediate'},
         {'name': 'DBMS', 'status': 'Intermediate'}, {'name': 'Flask', 'status': 'Beginner'},
         {'name': 'Operating System', 'status': 'Advance'}, {'name': 'ReactJs', 'status': 'Beginner'},
         {'name': '3* CodeChef', 'status': 'Beginner'}]}

    pdf.setFont('Courier', 24)
    pdf.drawString(28, 570, skil['name'])
    y = 570
    for i in skil['points']:
        w = i['name'].__len__()
        pdf.setFont('Helvetica', 12)
        pdf.drawString(200, y, i['name'])
        pdf.setFont('Helvetica', 8)
        pdf.drawString(200, y-8, i['status'])
        y -= 22
    pdf.save()

    response = make_response(pdf)
    return

@app.route('/resume')
def Resume():
    abt = {'name': 'About', 'about': "A brief paragraph about my-self I am interested in enhancing my knowledge and learning new things. I was very passionate from the young age and I want to built my career in this field. From the beginning of my higher studies I start learning about this field. I find myself very connected towards computers and that moment i decided to chase my goals and so I started learning new languages and increase my skillset, I want to experience beyond my studies. I'm confident that I can perform my best and can fully utilize the knowledge into practical application.<br/>"
    "I am sincere and honest, hard working person that want to enhance one's skillset and help my country develop in this field, so with your opportunity, I think I can progress more towards my goals."}
    edu = {'name': 'Education', 'points': [
        {'quali': "Bachelor's of Technology (CSE)", 'duration': '7/2018 - -', 'name': 'Dr.B.R. Ambedkar National Institute of Technology, Jalandhar', 'score': '7.01'},
        {'quali': 'Higher', 'duration': '4/2016 - 4/2018', 'name': 'APEEJAY School', 'score': '9.35'},
        {'quali': 'Matrix', 'duration': '4/2015 - 4/2016', 'name': 'APEEJAY School', 'score': '8.8'},
    ]}
    skil = {'name': 'Skills', 'points': [{'name': 'C/C++', 'status': 'Advance'}, {'name': 'Python', 'status': 'Advance'}
         , {'name': 'Django', 'status': 'Beginner'}, {'name': 'Data Analytics', 'status': 'Intermediate'},
         {'name': 'OOPs', 'status': 'Advance'}, {'name': 'Data Structures and Algorithms', 'status': 'Intermediate'},
         {'name': 'DBMS', 'status': 'Intermediate'}, {'name': 'Flask', 'status': 'Beginner'},
         {'name': 'Operating System', 'status': 'Advance'}, {'name': 'Amazon Web Services', 'status': 'Beginner'},
         {'name': 'ReactJs', 'status': 'Beginner'}, {'name': '3* CodeChef', 'status': 'Intermediate'}]}

    data = [abt, edu, skil]
    return render_template('resume.html', data=data)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('not_found.html'), 404

@app.route('/cam')
def cam():
    return render_template('model.html')

@app.route('/m')
def mn():
    return render_template('Learning.html')

@app.route('/projects')
def project():
    projects = [
        {'no': 1, 'name': 'Resume builder GUI', 'desc': 'Resume builder for desktops build with Python + Tkinter'},
        {'no': 2, 'name': 'Search Visualizer', 'desc':'Using various Algorithms used for searching and finding elements'
         },
        {'no': 3, 'name': 'Record keeper', 'desc': 'A simple record keeping application for schools/colleges/organizations'
         }
    ]
    return render_template('Project.html', projects=projects)

@app.route('/exp')
def exp():
    courses = [{'name': 'AWS Fundamentals', 'img': 'AWS-1.jpg'}]
    return render_template('exp.html', courses=courses)


if __name__ == '__main__':
    app.run(debug=True)