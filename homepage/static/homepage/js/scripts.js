let optionCounter = 0;
let questionCounter = 1;


function countItemsInList(ul) {
    let i = 0, itemCount = 0;

    while (ul.getElementsByTagName('li') [i++]) itemCount++;
    return itemCount;
}

function addOption(questionNumber) {
    if (document.getElementById(`textOnly_${questionNumber}`).checked == true) {
        return 0;
    }
    optionCounter++;
    let questionOptionsUL = document.getElementById(`questionOptions_${questionNumber}`);
    let options = countItemsInList(questionOptionsUL);

    questionOptionsUL.insertAdjacentHTML('beforeend',
        `<li id="question_${questionNumber}_option_${options + 1}">
            <input type="checkbox" id="optionValueForQuestion_${questionNumber}_${options + 1}">
            <input type="text" name="optionForQuestion_${questionNumber}_${options + 1}" required>
            <input type="button" value="-" onclick="eraseOption('question_${questionNumber}_option_${options + 1}');">
        </li>`
    );
}

function eraseOption(optionID) {
    document.getElementById(optionID).remove();
}

function addQuestion() {
    questionCounter++;
    let questionsList = document.getElementById("questionsList");

    questionsList.insertAdjacentHTML('beforeend', 
    `
    <li id="questionNumber_${questionCounter}">
        <div class="row">
            <div class="col">
                <input type="text" name="question_${questionCounter}" required>
                <input type="number" name="price_${questionCounter}" required>
                <input type="button" value="-" onclick="eraseQuestion('questionNumber_${questionCounter}');">
            </div>
            <div class="col">
                <input type="button" id="addOptionId" value="+Option" onclick="addOption('${questionCounter}');">
                <input type="checkbox" id="textOnly_${questionCounter}" name="textOnlyFor_${questionCounter}" onchange="eraseOptions('questionOptions_${questionCounter}')"> Text Answer
            </div>
        </div>
        <div class="row">
            <ul id="questionOptions_${questionCounter}"></ul>
        </div>
    </li>
    `
    );
}

function eraseQuestion(questionID) {
    document.getElementById(questionID).remove();
}

function eraseOptions(questionOptionsId) {
    let questionOptions = document.getElementById(questionOptionsId).getElementsByTagName('li');
    while (questionOptions.length != 0) {
        for (i = 0; i < questionOptions.length; i++) {
            eraseOption(questionOptions[i].id);
        }
        questionOptions = document.getElementById(questionOptionsId).getElementsByTagName('li');
    }
}

function optionsValidation() {
    let all_checked = true
    for (let i = 0; i < questionCounter; i++) {
        let questionOptions = document.getElementById(`questionOptions_${i+1}`).getElementsByTagName('li');

        for (let j = 0; j < questionOptions.length; j++) {
            option_checkbox = document.getElementById(`optionValueForQuestion_${i+1}_${j+1}`)
            if (option_checkbox.checked) {
                all_checked = true
                break;
            }
            all_checked = false
        }

        if (all_checked == false) {
            alert("Each question must have at least 1 right option")
            return false
        }
    }
    return true
}