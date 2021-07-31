
def initiate(app):
    app.config['SECRET_KEY'] = 'Selena | Gaurav'
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = 'bhardwajg2411@gmail.com'
    app.config['MAIL_PASSWORD'] = 'dakapqctjyffjrrc'
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

    return app