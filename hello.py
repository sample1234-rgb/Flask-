from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('hello.html')

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
         , {'name': 'Django', 'status': 'Beginner'}, {'name': 'Data Analytics', 'status': 'Beginner'},
         {'name': 'OOPs', 'status': 'Advance'}, {'name': 'Data Structures and Algorithms', 'status': 'Intermediate'},
         {'name': 'DBMS', 'status': 'Intermediate'}, {'name': 'Flask', 'status': 'Beginner'},
         {'name': 'Operating System', 'status': 'Advance'}, {'name': 'ReactJs', 'status': 'Beginner'},
                                         {'name': '3* CodeChef', 'status': 'Beginner'}]}
    data = [abt, edu, skil]
    return render_template('resume.html', data=data)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('not_found.html'), 404

@app.route('/cam')
def cam():
    return render_template('cam.html')

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


if __name__ == '__main__':
    app.run(debug=True)