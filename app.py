from flask import Flask
from flask_migrate import Migrate
from add import bp as add_bp
import config
from extension import db
import os

app = Flask(__name__)
app.config.from_object(config)

# Bind app to db
db.init_app(app)

#Call the blueprint
app.register_blueprint(add_bp)
#set secret key
app.config['SECRET_KEY'] = os.urandom(24)

migrate = Migrate(app,db)



if __name__ == '__main__':
    app.run()
