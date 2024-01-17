const csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}


$(document).ready(function() {
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $('.js-vote').click(function() {
        let model = $(this).data('model'),
            action = $(this).data('action'),
            id = $(this).data('id');

        let data = {'model': model, 'action': action, 'id': id};
        $.ajax({
            type: "POST",
            url: "/change_rating/",
            data: data,
            dataType: 'json',
            success: function(response) {
                let new_rating = response['rating']
                document.getElementById(model + id).innerHTML = new_rating;
            },
            error: function() {
                // pass
            }
        });
    });


    $('.js-correct').click(function () {
        let id = $(this).data('id'),
            qid = $(this).data('qid'),
            correct = document.getElementById('correct' + id).checked,
            data = {id: id, correct: correct, qid: qid};

        $.ajax({
            type: "POST",
            url: "/correct/",
            data: data,
            dataType: 'json',
            success: function(response) {
                document.getElementById('correct' + id).checked = response['correct'];
            },
            error: function() {
                // pass
            }
        });
    });

});


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
