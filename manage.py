from flask_script import Server
from flask_migrate import Manager, MigrateCommand
from services.app import app

manager = Manager(app)

manager.add_command('db', MigrateCommand)
manager.add_command('runserver', Server(host='0.0.0.0', port=5000))

if __name__ == '__main__':
    # manager.run()
    app.run(debug=True)
