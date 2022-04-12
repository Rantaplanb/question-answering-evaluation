var questionCounter = 0;

$('#add-button').on('click', () => {
    $questions = $('.questions-section');
    questionCounter++;

    $questions.append('<div class="question" id="' + questionCounter + '">' +
        '<h3 class="question-counter">Question #' + (questionCounter + 1) + '</h3>' +
        '<div class="question-field">' +
        '<input class="input" type="text" value=" ">' +
        '<button class="remove-question" id="remove-' + questionCounter + '" name="' + questionCounter + '"> - </button>' +
        '</div>' +
        '<output></output>');

    $('#remove-' + questionCounter).on('click', (question) => {
        var removeId = question.currentTarget["name"];
        $('#' + removeId).remove();
        question_list = $('.question-counter');
        for (let i = 0; i < question_list.length; i++) {
            question_list.get(i).innerText = 'Question #' + (i + 2);
        }
    });

    question_list = $('.question-counter');
    for (let i = 0; i < question_list.length; i++) {
        question_list.get(i).innerText = 'Question #' + (i + 2);
    }
});

$('#answer-button').on('click', () => {
    inputList = $('.input');
    context = $('#context').val();


    let request = {}
    request.context = context;
    for (let i = 0; i < inputList.length; i++) {
        request["question" + i] = inputList.get(i).value;
    }

    $.ajax({
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(request),
        dataType: 'json',
        url: 'http://127.0.0.1:8080/questions',
        success: (e) => {
            console.log(e);
        },
        error: (e) => {
            console.log(e);
        }
    });
});