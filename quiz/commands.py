import click
from .app import app, db
from .models import Questionnaire, Question

@app.cli.command()
def syncdb():
    """Create all missing tables."""
    db.create_all()


@app.cli.command()
def loaddb():
    '''Creates the tables and populates them with data.'''
    db.create_all()
    db.session.add(Questionnaire(name='Questionnaire 1'))
    db.session.add(Questionnaire(name='Questionnaire 2'))
    db.session.commit()
    db.session.add(Question(title='Question 1', questionType='Type 1', questionnaire_id=1))
    db.session.add(Question(title='Question 2', questionType='Type 2', questionnaire_id=1))
    db.session.add(Question(title='Question 3', questionType='Type 1', questionnaire_id=2))
    db.session.commit()


