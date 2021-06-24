from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('hello.html')

@app.route('/resume')
def Resume():
    edu = {'name': 'Education', 'points': [
        {'quali': 'B. Tech.', 'duration': '7/2018 - -', 'name': 'NIT J', 'score': '6.96'},
        {'quali': 'Higher', 'duration': '4/2016 - 4/2018', 'name': 'APJ School', 'score': '9.35'},
        {'quali': 'Matrix', 'duration': '4/2015 - 4/2016', 'name': 'APJ School', 'score': '8.8'},
    ]}
    skil = {'name': 'Skills', 'points': ['C/C++', 'Python', 'Django', 'Data Analytics', 'OOPs',
                                         'Data Structures and Algorithms', 'DBMS', 'Flask',
                                         'Operating System', 'ReactJs', '3* CodeChef']}
    data = [edu, skil]
    return render_template('resume.html', data=data)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('not_found.html'), 404


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