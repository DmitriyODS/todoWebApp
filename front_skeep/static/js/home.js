textField = document.getElementById('user_keep')
btnUsers = document.getElementById('btn_users')
isAdmin = localStorage.getItem('is_admin')

if (isAdmin === 'true') {
    btnUsers.className = "btn btn-outline"
} else {
    btnUsers.className = "hide"
}

function logout() {
    localStorage.clear()
    document.location.replace('/promo/logout')
}

function goToAdmin() {
    document.location.href = '/admin'
}

async function processing_res_data(data) {
    if (!data.ok) {
        alert(data.description)
        return
    }

    document.location.reload();
}

function removeKeep(keep_id) {
    let request = fetch(`/delKeep:${keep_id}`, {method: 'DELETE'})

    request.then(response => response.json(), () => alert('Сервер не отвечает, попробуйте позже'))
        .then(processing_res_data, () => alert('Ошибка данных'))
}

function addNewKeep() {
    if (textField.value === '') {
        alert('Нельзя записать пустой текст :)');
        return;
    }

    const request_data = {
        keep_text: textField.value
    }
    let request = fetch('/addNewKeep', {
        headers: {
            'Content-Type': 'application/json;charset=utf-8'
        },
        method: 'POST',
        body: JSON.stringify(request_data)
    })

    request.then(response => response.json(), () => alert('Сервер не отвечает, попробуйте позже'))
        .then(processing_res_data, () => alert('Ошибка данных'))
        .finally(() => textField.value = '')
}
