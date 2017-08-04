from flask_script import Manager # class for handling a set of commands
from flask_migrate import Migrate, MigrateCommand
from app.app import db, create_app

# pylint: disable=C0103
app = create_app(config_name="development")
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command("db", MigrateCommand)

if __name__ == "__main__":
    manager.run()
    db.create_all()

