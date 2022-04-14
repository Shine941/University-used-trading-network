window.addEventListener('load', function () {
    var regTelphone = document.getElementById('reg_telphone');
    var regCcode = document.getElementById('reg_code');
    var password = document.getElementById('password');
    var confirmPd = document.getElementById('confirm_pd');
    var telphone = /^(13[0-9]|14[0-9]|15[0-9]|16[0-9]|17[0-9]|18[0-9]|19[0-9])\d{8}$/;
    var pd = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,10}$/;
    message(regTelphone, telphone);
    message(password, pd);
    function message(ele, reg) {
        ele.onblur = function () {
            if (reg.test(this.value)) {

                this.nextElementSibling.className = 'success';
                this.nextElementSibling.innerHTML = '恭喜您输入正确';

            } else {
                this.nextElementSibling.className = 'error';
                this.nextElementSibling.innerHTML = '输入的格式错误';
            }
            return reg.test(this.value)
        }

    }
    confirmPd.onblur = function () {
        if (password.value == confirmPd.valuev) {
            confirmPd.nextElementSibling.className = 'success';
            confirmPd.nextElementSibling.innerHTML = '密码输入正确';
        } else {
            confirmPd.nextElementSibling.className = 'success';
            confirmPd.nextElementSibling.innerHTML = '密码输入不一致';
        }
    }
    var form = document.querySelector('form');
    var btn = document.querySelector('.btn');
    form.onsubmit = function () {
        if (regTelphone.nextElementSibling.className == 'success' && password.nextElementSibling.className == 'success' && confirmPd.nextElementSibling.className == 'success') {
            return true;
        }
    }

})


window.addEventListener('load', function () {
    var sendCode = document.querySelector('.send_code');
    var time = 60;
    sendCode.addEventListener('click', function () {
        sendCode.disabled = true;
        setInterval(function () {
            if (time == 0) {
                clearInterval(time);
                sendCode.disabled = false;
                sendCode.innerHTML = '发送验证码';
                time = 60;
            } else {
                sendCode.innerHTML = '还剩下' + time + '秒';
                time--;
            }
        }, 1000);
    });

});
window.addEventListener('load', function () {
    var userBtn = document.getElementById('user_btn');
    var userConfirm = document.querySelector('.user_confirm');
    var close = document.querySelector('.close')
    userBtn.onclick = function () {
        userConfirm.style.display = 'block';
    }
    close.onclick = function () {
        userConfirm.style.display = 'none';
    }
})