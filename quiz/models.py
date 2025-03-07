from .app import db

class Questionnaire(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Questionnaire(%d) %s>" % (self.id, self.name)

    def to_json(self):
        json = {
            'id': self.id,
            'name': self.name
        }
        return json

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    questionType = db.Column(db.String(120))
    questionnaire_id = db.Column(db.Integer, db.ForeignKey('questionnaire.id'))
    questionnaire = db.relationship("Questionnaire", backref=db.backref("questions", lazy="dynamic"))
    
    def to_json(self):
        json = {
            'id' : self.id, 
            'title' : self.title, 
            'type' : self.questionType, 
            'id_questionnaire' : self.questionnaire_id
        }
        return json

def get_questions():
    questions = Question.query.all()
    result = []
    for question in questions:
        result.append(question.to_json())
    return result

def get_questionnaires():
    questionnaires = Questionnaire.query.all()
    result = []
    for questionnaire in questionnaires:
        result.append(questionnaire.to_json())
    return result

def get_questionnaire(id):
    questionnaire = Questionnaire.query.get(id)
    if questionnaire is None:
        return None
    return questionnaire.to_json()

def get_classic_questionnaire(id):
    questionnaire = Questionnaire.query.get(id)
    if questionnaire is None:
        return None
    return questionnaire

def get_question(id):
    question = Question.query.get(id)
    if question is None:
        return None
    return question.to_json()

def get_classic_question(id):
    question = Question.query.get(id)
    if question is None:
        return None
    return question

def delete_question(id):
    question = get_classic_question(id)
    db.session.delete(question)
    db.session.commit()

def delete_questionnaire(id):
    questionnaire = get_classic_questionnaire(id)
    db.session.delete(questionnaire)
    db.session.commit()

def insert_questionnaire(nom):
    questionnaire = Questionnaire(name=nom)
    db.session.add(questionnaire)
    db.session.commit()
    return questionnaire

def insert_question(id_questionnaire, titre, type):
    question = Question(questionnaire_id=id_questionnaire, title=titre, questionType=type)
    db.session.add(question)
    db.session.commit()
    return question

def inQuestionnaire(idQuestionnaire):
    questionnaire = Questionnaire.query.get(idQuestionnaire)
    if questionnaire != None:
        return True
    return False

def aDesQuestions(idQuestionnaire):
    questions = Question.query.filter_by(questionnaire_id=idQuestionnaire).all()
    if len(questions) != 0:
        return True
    return False

def updateQuestionnaire(id, name):
    questionnaire = Questionnaire.query.get(id)
    questionnaire.name = name
    db.session.commit()
    return questionnaire.to_json()

def updateQuestion(id, title, type):
    question = Question.query.get(id)
    question.title = title
    question.questionType = type
    db.session.commit()
    return question.to_json()

def get_questions_from_questionnaire(id):
    questions = Question.query.filter_by(questionnaire_id=id).all()
    result = []
    for question in questions:
        result.append(question.to_json())
    return result