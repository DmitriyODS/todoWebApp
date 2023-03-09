function logout() {
    localStorage.clear()
    document.location.replace('/promo/logout')
}

function goToKeeps() {
    document.location.href = '/'
}

async function processing_res_data(data) {
    if (!data.ok) {
        alert(data.description)
        return
    }

    document.location.reload();
}

function removeUser(user_id) {
    let request = fetch(`/delUser:${user_id}`, {method: 'DELETE'})

    request.then(response => response.json(), () => alert('Сервер не отвечает, попробуйте позже'))
        .then(processing_res_data, () => alert('Ошибка данных'))
        .finally(() => textField.value = '')
}
