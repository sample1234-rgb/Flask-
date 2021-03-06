from flask import Flask, render_template, make_response, request, redirect, url_for
from reportlab.pdfgen import canvas
from reportlab.platypus.flowables import Image
from flask_mail import Mail, Message
from wtforms import Form, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
# from model import make_model
from setting import initiate

application = Flask(__name__)


@application.route('/')
def index():
    return render_template('hello.html')


application = initiate(application)

# app.config['SECRET_KEY'] = '****************'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///****.db'
# app.config['MAIL_SERVER'] = 'smtp.gmail.com'
# app.config['MAIL_PORT'] = 465
# app.config['MAIL_USERNAME'] = '***********@gmail.com'
# app.config['MAIL_PASSWORD'] = 'da************rc'
# app.config['MAIL_USE_TLS'] = False
# app.config['MAIL_USE_SSL'] = True
# ['bhardwajg2411@gmail.com', 'gauravxprogram@gmail.com']
Path = 'C:/Users/hp/PycharmProjects/FlaskProject/static'
# model = make_model(train_path='', test_path='')
model = None
mail = Mail(application)

db = SQLAlchemy(application)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(20), nullable=False, unique=True)
    comment = db.Column(db.String(1200))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<NAME %r>' % self.name


class forms(Form):
    name = StringField('Your Name', validators=[DataRequired()])
    email = StringField('Your Email', validators=[DataRequired(), Email()])
    context = TextAreaField('Your Suggestions:')
    btn = SubmitField('Send')


@application.route('/reach', methods=['GET', 'POST'])
def reach():
    name, email, context = None, None, None
    form = forms(request.form)

    if request.method == 'POST' and form.validate():
        name, email, context = form.name.data, form.email.data, form.context.data
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            user = Users(name=name, email=email, comment=context)
            db.session.add(user)
            db.session.commit()
        form.name.data, form.email.data, form.context.data = '', '', ''

        # sending(sender=email, message=context)
        # return render_template('form.html', name=name, email=email, context=context, form=form)
    all_users = Users.query.order_by(Users.date_added)
    return render_template('form.html', name=name, email=email, context=context, form=form, users=all_users)


@application.route("/mail")
def sending(sender, message):
    recievers = sender
    try:
        msg = Message(
            'Hello Gaurav | Response to your website',
            sender='bhardwajg2411@gmail.com',
            recipients=recievers
        )
        msg.body = message
        mail.send(msg)
        return redirect(url_for('reach'))
    except Exception as e:
        return str(e)


class RotatedImage(Image):
    def wrap(self, availWidth, availHeight):
        h, w = Image.wrap(self, availHeight, availWidth)
        return w, h

    def draw(self):
        self.canv.rotate(90)
        Image.draw(self)


def ruler(pdf):
    for i in range(0, 600):
        if i % 100 == 0:
            pdf.drawString(i, 830, '+' + str(i))
        elif i % 5 == 0:
            pdf.drawString(i, 842, '|')

    for i in range(0, 1000):
        if i % 100 == 0:
            pdf.drawString(2, i, '+' + str(i))
        elif i % 5 == 0:
            pdf.drawString(1, i, '--')

    pdf.drawString(570, 830, '-> x')
    pdf.drawString(2, 0, 'v\ny')


@application.route('/pdf')
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

    pdf.drawImage('static/20181223_081218.jpg', 50, 740, width=60, height=60, showBoundary=True)
    pdf.line(25, 730, 475, 730)

    # # Education Table:
    edu = {'name': 'Education', 'points': [
        {'quali': "Bachelor's of Technology (CSE)", 'duration': '7/2018 - -',
         'name': 'Dr.B.R. Ambedkar National Institute of Technology, Jalandhar', 'score': '7.01'},
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
        pdf.drawString(300, y - 10, i['name'])
        pdf.setFont('Courier', 9)
        pdf.drawString(300, y - 20, "CGPA: " + i['score'])
        y -= 35

    pdf.line(25, y - 10, 475, y - 10)

    skil = {'name': 'Skills', 'points': [{'name': 'C/C++', 'status': 'Advance'}, {'name': 'Python', 'status': 'Advance'}
        , {'name': 'Django', 'status': 'Beginner'}, {'name': 'Data Analytics', 'status': 'Beginner'},
                                         {'name': 'OOPs', 'status': 'Advance'},
                                         {'name': 'Data Structures and Algorithms', 'status': 'Intermediate'},
                                         {'name': 'DBMS', 'status': 'Intermediate'},
                                         {'name': 'Flask', 'status': 'Beginner'},
                                         {'name': 'Operating System', 'status': 'Advance'},
                                         {'name': 'ReactJs', 'status': 'Beginner'},
                                         {'name': '3* CodeChef', 'status': 'Beginner'}]}

    pdf.setFont('Courier', 24)
    pdf.drawString(28, 570, skil['name'])
    y = 570
    for i in skil['points']:
        w = i['name'].__len__()
        pdf.setFont('Helvetica', 12)
        pdf.drawString(200, y, i['name'])
        pdf.setFont('Helvetica', 8)
        pdf.drawString(200, y - 8, i['status'])
        y -= 22
    pdf.save()

    response = make_response(pdf)
    return


@application.route('/resume')
def resume():
    abt = {'name': 'About',
           'about': "A brief paragraph about my-self I am interested in enhancing my knowledge and learning new things. I was very passionate from the young age and I want to built my career in this field. From the beginning of my higher studies I start learning about this field. I find myself very connected towards computers and that moment i decided to chase my goals and so I started learning new languages and increase my skillset, I want to experience beyond my studies. I'm confident that I can perform my best and can fully utilize the knowledge into practical application.<br/>"
                    "I am sincere and honest, hard working person that want to enhance one's skillset and help my country develop in this field, so with your opportunity, I think I can progress more towards my goals."}
    edu = {'name': 'Education', 'points': [
        {'quali': "Bachelor's of Technology (CSE)", 'duration': '7/2018 - 7/2022',
         'name': 'Dr.B.R. Ambedkar National Institute of Technology, Jalandhar', 'score': '7.01'},
        {'quali': 'Higher', 'duration': '4/2016 - 4/2018', 'name': 'APEEJAY School', 'score': '9.35'},
        {'quali': 'Matrix', 'duration': '4/2015 - 4/2016', 'name': 'APEEJAY School', 'score': '8.8'},
    ]}
    skil = {'name': 'Skills', 'points': [{'name': 'C/C++', 'status': 'Advance'},
                                         {'name': 'Python', 'status': 'Advance'},
                                         {'name': 'Django', 'status': 'Beginner'},
                                         {'name': 'Data Analytics', 'status': 'Intermediate'},
                                         {'name': 'OOPs', 'status': 'Advance'},
                                         {'name': 'Data Structures and Algorithms', 'status': 'Intermediate'},
                                         {'name': 'DBMS', 'status': 'Intermediate'},
                                         {'name': 'Flask', 'status': 'Beginner'},
                                         {'name': 'Operating System', 'status': 'Advance'},
                                         {'name': 'Amazon Web Services', 'status': 'Beginner'},
                                         {'name': 'ReactJs', 'status': 'Beginner'},
                                         {'name': '3* CodeChef', 'status': 'Intermediate'}
                                         ]}

    data = [abt, edu, skil]
    return render_template('resume.html', data=data)


@application.errorhandler(404)
def page_not_found(e):
    return render_template('not_found.html'), 404


@application.route('/cam', methods=['GET', 'POST'])
def cam():
    global model
    mod = None
    if request.method == "POST":
        file = request.files['file']
        path = os.path.join(
            Path, file.filename
        )
        file.save(path)
        mod = {'file': file, 'result': [0.5]}
        # mod = model.preprocess_predict(img)
        # img = request['file']
        return render_template('model.html', model=mod)
        pass

    return render_template('model.html', model=mod)


@application.route('/m', methods=['GET', 'POST'])
def mn():
    global model
    if request.method == 'POST':
        model = None
        # model = make_model(train_path='', test_path='')
        return redirect('/cam')
    return render_template('Learning.html')


@application.route('/projects')
def project():
    projects = [
        {'no': 1, 'name': 'My Profile Web-app', 'desc': "The site you are currently watching is also a project of mine."
                                                        "All the things here is created from scratch by me<br/>using the"
                                                        "development tool <code>Flask</code>, the working language"
                                                        " <code>Python</code> and Web Front-end Fundamentals.<br/><br/>"
                                                        " First of all, it will be a detailed site of my portfolio and second "
                                                        "It is build with database and a live <code>nn</code> model.",
         'img': 'img.png',
         'imgdim': [233, 300]},
        {'no': 2, 'name': 'Resume builder GUI', 'desc': 'Resume builder for desktops build with Python + Tkinter.',
         'img': 'GUI.png', 'imgdim': [555, 300]},
        {'no': 3, 'name': 'Search Visualizer',
         'desc': 'Using various Algorithms used for searching and finding elements'
         },
        {'no': 4, 'name': 'Record keeper',
         'desc': 'A simple record keeping application for schools/colleges/organizations'
         }]
    return render_template('Project.html', projects=projects)


@application.route('/exp')
def exp():
    list_courses = ['AWS', 'DeepLearning AI', 'Django for Everybody', 'Data Science']
    courses = [{'name': 'AWS Fundamentals', 'img': 'Certi/AWS-1.jpg', 'course': 'AWS'},
               {'name': 'Addressing Security Risks', 'img': 'Certi/AWS-2.jpg', 'course': 'AWS'},
               {'name': 'Migrating to the Cloud', 'img': 'Certi/AWS-3.jpg', 'course': 'AWS'},
               {'name': 'Building Serverless Applications', 'img': 'Certi/AWS-4.jpg', 'course': 'AWS'},
               {'name': 'Convolutional Neural Networks', 'img': 'Certi/CNN.jpg', 'course': 'DeepLearning AI'},
               {'name': 'Django Features & Libraries', 'img': 'Certi/Django-1.jpg', 'course': 'Django for Everybody'},
               {'name': 'Web Technologies & Django', 'img': 'Certi/Django-2.jpg', 'course': 'Django for Everybody'},
               {'name': 'Building Web Apps in Django', 'img': 'Certi/Django-3.jpg', 'course': 'Django for Everybody'},
               {'name': 'Machine Learning with Python', 'img': 'Certi/ML.jpg', 'course': 'Data Science'},
               {'name': 'Data Visualization with Python', 'img': 'Certi/DV.jpg', 'course': 'Data Science'},
               {'name': 'Data Analysis with Python', 'img': 'Certi/DA.jpg', 'course': 'Data Science'},
               {'name': 'Tools for Data Science', 'img': 'Certi/DS-Tools.jpg', 'course': 'Data Science'}]
    return render_template('exp.html', courses=courses, l=list_courses)


if __name__ == '__main__':
    application.run(debug=True)
