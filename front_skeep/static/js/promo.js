const fields = {
    login: document.getElementById('user_email'),
    password: document.getElementById('user_pass'),
    keepText: document.getElementById('user_keep')
}

const backdrop = document.getElementById('backdrop');

function showBackdrop() {
    backdrop.className = 'show-loading';
}

function hideBackdrop() {
    backdrop.className = 'hide';
}

function validation() {
    if (fields.login.value === '') {
        hideBackdrop();
        alert('Заполните поле: "Email"')
        return false;
    }
    if (fields.password.value === '') {
        hideBackdrop();
        alert('Заполните поле: "Пароль"')
        return false;
    }
    return true;
}

async function processing_res_data(data) {
    if (!data.ok) {
        alert(`Ошибка входа: ${data.description}`)
        return;
    }

    console.log(data)

    // так делать вообще нельзя, не надо так!
    // но в целях ученического проекта - можно
    localStorage.setItem('user_id', data.data.user_id)
    localStorage.setItem('is_admin', data.data.is_admin)

    document.location.href = '/'
}

function login(isRegister = false) {
    showBackdrop();
    if (!validation()) {
        return;
    }
    const request_data = {
        login: fields.login.value,
        password: fields.password.value,
        keep: fields.keepText.value,
        is_register: isRegister
    }
    let request = fetch(`/promo/auth`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json;charset=utf-8'
        },
        body: JSON.stringify(request_data)
    })

    request.then(response => response.json(), (res) => alert(`Сервер не отвечает, попробуйте позже: ${res}`))
        .then(processing_res_data, () => alert('Ошибка данных'))
        .finally(hideBackdrop)
}
