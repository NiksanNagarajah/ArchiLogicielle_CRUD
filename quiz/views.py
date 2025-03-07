from .app import app, db
from flask import jsonify, abort, request, url_for
import quiz.models as models

def make_public_questionnaire(questionnaire):
    new_task = {}
    for field in questionnaire:
        if field == 'id':
            new_task['uri'] = url_for('get_questionnaire', questionnaire_id=questionnaire['id'], _external=True)
            new_task['questions_uri'] = url_for('get_questions_from_questionnaire', id_questionnaire=questionnaire['id'], _external=True)
        else:
            new_task[field] = questionnaire[field]
    return new_task

def make_public_question(question):
    new_task = {}
    for field in question:
        if field == 'id':
            new_task['uri'] = url_for('get_question', question_id=question['id'], _external=True)
        else:
            new_task[field] = question[field]
    return new_task

@app.route('/quiz/api/v1.0/questionnaires', methods=['GET'])
def get_questionnaires():
    return jsonify(questionnaires = [make_public_questionnaire(questionnaire) for questionnaire in models.get_questionnaires()])

@app.route('/quiz/api/v1.0/questionnaire/<int:questionnaire_id>', methods=['GET'])
def get_questionnaire(questionnaire_id):
    questionnaire = models.get_questionnaire(questionnaire_id)
    if questionnaire is None:
        abort(404)
    return jsonify(make_public_questionnaire(questionnaire))

@app.route('/quiz/api/v1.0/questionnaires', methods=['POST'])
def create_questionnaire():
    if not request.json or not 'name' in request.json:
        abort(400)
    questionnaire = models.insert_questionnaire(request.json['name'])
    return jsonify({'questionnaire': questionnaire.to_json()}), 201

@app.route('/quiz/api/v1.0/questionnaire/<int:id_questionnaire>', methods=['DELETE'])
def delete_questionnaire(id_questionnaire):
    questionnaire = models.get_questionnaire(id_questionnaire)
    if questionnaire is None:
        abort(404)
    if models.aDesQuestions(id_questionnaire):
        abort(400)
    models.delete_questionnaire(id_questionnaire)
    return jsonify({'questionnaire' : questionnaire})

@app.route('/quiz/api/v1.0/questionnaire/<int:id_questionnaire>', methods=['PUT'])
def update_questionnaire(id_questionnaire):
    questionnaires = models.get_questionnaires()
    if len(questionnaires) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'name' in request.json and type(request.json['name']) != str:
        abort(400)
    questionnaire = models.updateQuestionnaire(id_questionnaire, request.json['name'])
    return jsonify({'questionnaire': questionnaire}), 201

@app.route('/quiz/api/v1.0/questionnaire/<int:id_questionnaire>/questions', methods=['GET'])
def get_questions_from_questionnaire(id_questionnaire):
    return jsonify(questions = [make_public_question(question) for question in models.get_questions_from_questionnaire(id_questionnaire)])

@app.route('/quiz/api/v1.0/questionnaire/<int:id_questionnaire>/questions', methods=['POST'])
def create_question_in_questionnaire(id_questionnaire):
    if not request.json or not 'title' in request.json or not 'type' in request.json:
        abort(400)
    if not models.inQuestionnaire(id_questionnaire):
        abort(400)
    question = models.insert_question(id_questionnaire, request.json['title'], request.json['type'])
    return jsonify({'question': question.to_json()}), 201

@app.route('/quiz/api/v1.0/questionnaire/<int:id_questionnaire>/question/<int:question_id>', methods=['DELETE'])
def delete_question_in_questionnaire(id_questionnaire, question_id):
    question = models.get_question(question_id)
    if question is None:
        abort(404)
    if question['questionnaire_id'] != id_questionnaire:
        abort(400)
    models.delete_question(question_id)
    return jsonify({'question': question})

@app.route('/quiz/api/v1.0/questionnaire/<int:id_questionnaire>/question/<int:question_id>', methods=['PUT'])
def update_question_in_questionnaire(id_questionnaire, question_id):
    questions = models.get_questions_from_questionnaire(id_questionnaire)
    if len(questions) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != str:
        abort(400)
    if 'type' in request.json and type(request.json['type']) != str:
        abort(400)
    question = models.updateQuestion(question_id, request.json['title'], request.json['type'])
    return jsonify({'question': question}), 201


@app.route('/quiz/api/v1.0/questions', methods=['GET'])
def get_questions():
    return jsonify(questions = [make_public_question(question) for question in models.get_questions()])

@app.route('/quiz/api/v1.0/question/<int:question_id>', methods=['GET'])
def get_question(question_id):
    question = models.get_question(question_id)
    if question is None:
         abort(404)
    return jsonify(question)

@app.route('/quiz/api/v1.0/questions', methods=['POST'])
def create_question():
    if not request.json or 'id_questionnaire' not in request.json or not 'title' in request.json or not 'type' in request.json:
        abort(400)
    if not models.inQuestionnaire(request.json['id_questionnaire']):
          abort(400)
    question = models.insert_question(request.json['id_questionnaire'], request.json['title'], request.json['type'])
    return jsonify({'question': question.to_json()}), 201

@app.route('/quiz/api/v1.0/question/<int:question_id>', methods=['DELETE'])
def delete_question(question_id):
    question = models.get_question(question_id)
    if question is None:
        abort(404)
    models.delete_question(question_id)
    return jsonify({'question': question})

@app.route('/quiz/api/v1.0/question/<int:question_id>', methods=['PUT'])
def update_question(question_id):
    questions = models.get_questions()
    if len(questions) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != str:
        abort(400)
    if 'type' in request.json and type(request.json['type']) != str:
        abort(400)
    question = models.updateQuestion(question_id, request.json['title'], request.json['type'])
    return jsonify({'question': question}), 201

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(400)
def not_found(error):
    return jsonify({'error': 'Bad request'}), 400