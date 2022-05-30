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
        `
        <li class="option-li" id="question_${questionNumber}_option_${options + 1}">
            <div class="option-check">
                <input class="var-checkbox" type="checkbox" name="optionValueForQuestion_${questionNumber}_${options + 1}">
            </div>
            <div class="option-value">
                <input class="form-control" type="text" name="optionForQuestion_${questionNumber}_${options + 1}" placeholder="Варіант" required>
            </div>
            <div>
                <input class="btn-danger option-delete-btn" type="button" value="-" onclick="eraseOption('question_${questionNumber}_option_${options + 1}');">
            </div>   
        </li>
    `
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
        <div class="row quiz-row">
            <div class="col">
                <label for="question_${questionCounter}">Питання:</label>
                <input class="form-control" type="text" name="question_${questionCounter}" placeholder="Питання" required>
            </div>
            <div class="col-md-2 mark-container">
                <div class="row">
                    <div class="col">
                        <label for="price_${questionCounter}">Оцінка:</label>
                        <input class="form-control" type="number" name="price_${questionCounter}" placeholder="Бали" required>
                    </div>
                    <div class="col-md-3">
                        <input class="btn-danger question-delete-btn" type="button" value="-" onclick="eraseQuestion('questionNumber_${questionCounter}');">
                    </div>
                </div>
            </div>
            <div class="col-md-2">
                <input class="quiz-button" type="button" id="addOptionId" name="optionForQuestion_${questionCounter}" value="Додати варіант" onclick="addOption(${questionCounter});">
            </div>
            <div class="col-md-2 description-check-container">
                <input class="form-check-input" type="checkbox" id="textOnly_${questionCounter}" name="textOnlyFor_${questionCounter}" onchange="eraseOptions('questionOptions_${questionCounter}')">
                <label class="form-check-label" for="textOnly_${questionCounter}">Описове завдання</label>
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

function closePreviousDropdowns(currentDropdown) {
    let dropdowns = document.getElementsByClassName("dropdown-content");
    for (let i = 0; i < dropdowns.length; i++) {
        if (dropdowns[i] != currentDropdown && dropdowns[i].classList.contains("show")) {
            dropdowns[i].classList.remove("show");
        }
    }
}

function showCreatedCourses() {
    let dropdown = document.getElementById("createdCoursesDropdown");
    dropdown.classList.toggle("show");
    closePreviousDropdowns(dropdown);
}

function showAddedCourses() {
    let dropdown = document.getElementById("addedCoursesDropdown");
    dropdown.classList.toggle("show");
    closePreviousDropdowns(dropdown);
}

window.onclick = function(event) {
    if (!event.target.matches(".drop-button")) {
        let dropdowns = document.getElementsByClassName("dropdown-content");
        for (let i = 0; i < dropdowns.length; i++) {
            let openDropdown = dropdowns[i];
            if (openDropdown.classList.contains("show")) {
                openDropdown.classList.remove("show")
            }
        }
    }
}

function showPassword() {
    let password = document.getElementById('register_password');
    let confirmPassword = document.getElementById('register_confirm_password');
    let cehckbox = document.getElementById('show_password');

    if (cehckbox.checked) {
        password.type = "text";
        confirmPassword.type = "text";
    }
    else {
        password.type = "password";
        confirmPassword.type = "password";
    }
}
