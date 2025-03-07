$(function() {
    $("#toolsQuestion").hide();

    $("#button").click(refreshQuizList);

    function remplirQuestionnaires(repjson) {
      console.log(JSON.stringify(repjson));
      $('#questionnaires').empty();
      $('#questionnaires').append($('<ul>'));
      for(quiz of repjson.questionnaires){
          console.log(quiz);
          $('#questionnaires ul')
                .append($('<li>')
                .append($('<a>')
                .text(quiz.name)
                    ).on("click", quiz, details)
                );
        }
    }

    function viderQuestions() {
        $('#questions').empty();
    }

    function onerror(err) {
        $("#questionnaires").html("<b>Impossible de récupérer les questionnaires à réaliser !</b>"+err);
    }

    function remplirQuestions(repjson) {
        console.log(JSON.stringify(repjson));
        $('#questions').empty();
        $('#questions').append($('<ul>'));
        for(question of repjson.questions){
            console.log(question);
            $('#questions ul')
                  .append($('<li>')
                  .append($('<a>')
                  .text(question.title)
                      ).on("click", question, detailsQuestion)
                  );
          }
        }

    function refreshQuizList(){
        $("#toolsQuestion").hide();
        $("#currentquestionnaire").empty();
        $("#currentquestion").empty();
        requete = "http://127.0.0.1:5000/quiz/api/v1.0/questionnaires";
        fetch(requete)
        .then( response => {
                  if (response.ok) return response.json();
                  else throw new Error('Problème ajax: '+response.status);
                }
            )
        .then(remplirQuestionnaires)
        .then(viderQuestions)
        .catch(onerror);
    }

    function details(event){
        $("#toolsQuestion").show();
        $("#currentquestionnaire").empty();
        formQuiz();
        fillFormQuiz(event.data);
        fetch(event.data.questions_uri)
        .then( response => {
                  if (response.ok) return response.json();
                  else throw new Error('Problème ajax: '+response.status);
                }
            )
        .then(remplirQuestions)
        .catch(onerror);
        }
    
    function detailsQuestion(event){ 
        $("#currentquestion").empty();
        formQuestion();
        fillFormQuestion(event.data)
    }


    class Quiz{
        constructor(name, uri){
            this.name = name;
            this.uri = uri;
            console.log(this.uri);
        }
    }

    class Question{
        constructor(idQuestionnaire, title, type, uri){
            this.idQuestionnaire = idQuestionnaire;
            this.title = title;
            this.type = type;
            this.uri = uri;
        }
    }


    $("#tools #add").on("click", formQuiz);
    $('#tools #del').on('click', delQuiz);

    $("#toolsQuestion #addQuestion").on("click", formQuestion);
    $('#toolsQuestion #delQuestion').on('click', delQuestion);

    function formQuiz(isnew){
        $("#currentquestionnaire").empty();
        $("#currentquestionnaire")
            .append($('<span><input type=hidden id="id"><br></span>'))
            .append($('<span>Nom<input type="text" id="name"><br></span>'))
            .append(isnew?$('<span><input type="button" value="Save Quiz"><br></span>').on("click", saveNewQuiz)
                        :$('<span><input type="button" value="Modify Quiz"><br></span>').on("click", saveModifiedQuiz)
                )
            .append($('<span><input type="hidden" id="turi"><br></span>'));
        $('#currentquestion').empty();
        }


    function fillFormQuiz(t){
        $("#currentquestionnaire #name").val(t.name);
        //  t.uri=(t.uri == undefined)?"http://127.0.0.1:5000/quiz/api/v1.0/questionnaires"+t.id:t.uri;
         $("#currentquestionnaire #turi").val(t.uri);
         console.log(t.uri);
    }

    function formQuestion(isnew) {
        $("#currentquestion").empty();
        $("#currentquestion")
            .append($('<span>Titre<input type="text" id="titre"><br></span>'))
            .append($('<span>Type<input type="text" id="qtype"><br></span>'))
            .append(isnew?$('<span><input type="button" value="Save Question"><br></span>').on("click", saveNewQuestion)
                        :$('<span><input type="button" value="Modify Question"><br></span>').on("click", saveModifiedQuestion)
                )
            .append($('<span><input type="hidden" id="quri"><br></span>'))
            .append($('<span><input type="hidden" id="turi"><br></span>'));
    }

    function fillFormQuestion(q) {
        $("#currentquestion #titre").val(q.title);
        $("#currentquestion #qtype").val(q.type);
        $("#currentquestion #quri").val(q.uri);
        $("#currentquestion #turi").val(q.idQuestionnaire);
    }

    function saveNewQuiz(){
        var quiz = new Quiz(
            $("#currentquestionnaire #name").val()
            );
        console.log(JSON.stringify(quiz));
        fetch("http://127.0.0.1:5000/quiz/api/v1.0/questionnaires",{
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        method: "POST",
        body: JSON.stringify(quiz)
            })
        .then(res => { console.log('Save Success') ;
                       $("#result").text(res['contenu']);
                       refreshQuizList();
                   })
        .catch( res => { console.log(res) });
    }
    
    function saveNewQuestion() {
        var question = new Question(
            $("#currentquestionnaire #id").val(),
            $("#currentquestion #titre").val(),
            $("#currentquestion #qtype").val(), 
            $("#currentquestionnaire #turi").val()
        );
        console.log(JSON.stringify(question));
        fetch(question.uri + "/questions", {
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            method: "POST",
            body: JSON.stringify(question)
        })
        .then(res => res.json())
        .then(res => {
            console.log('Save Success');
            $("#result").text(res['contenu']);
            refreshQuizList();
        })
        .catch(res => {
            console.log(res);
        });
    }

    function saveModifiedQuiz(){
        var quiz = new Quiz(
            $("#currentquestionnaire #name").val(),
            $("#currentquestionnaire #turi").val()
            );
        console.log("PUT");
        console.log(quiz.uri);
        console.log(JSON.stringify(quiz));
        fetch(quiz.uri,{
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        method: "PUT",
        body: JSON.stringify(quiz)
            })
        .then(res => { console.log('Update Success');  refreshQuizList();} )
        .catch( res => { console.log(res) });
    }

    function saveModifiedQuestion(){
        var question = new Question(
            $("#currentquestionnaire #turi").val(),
            $("#currentquestion #titre").val(),
            $("#currentquestion #qtype").val(),
            $("#currentquestion #quri").val()
            );
        console.log(JSON.stringify(question));
        fetch(question.uri,{
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        method: "PUT",
        body: JSON.stringify(question)
            })
        .then(res => { console.log('Update Success');  refreshQuizList();} )
        .catch( res => { console.log(res) });
    }

    function delQuiz(){
        if ($("#currentquestionnaire #turi").val()){
        url = $("#currentquestionnaire #turi").val();
        fetch(url,{
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        method: "DELETE"
            })
        .then(res => { console.log('Delete Success:' + res); } )
        .then(refreshQuizList)
        .catch( res => { console.log(res);  });
    }
  }

  function delQuestion(){
    if ($("#currentquestion #quri").val()){
    url = $("#currentquestion #quri").val();
    fetch(url,{
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
    method: "DELETE"
        })
    .then(res => { console.log('Delete Success:' + res); } )
    .then(refreshQuizList)
    .catch( res => { console.log(res);  });
    }
  }
});


