$(function () {
        const account = $('#inputText');
        const password = $('#inputPassword');
        const autoLogin = $('#exampleCheck');
        const loginButton = $('#loginButton');
        const student = $('#student');
        const mentor = $('#mentor');
        const admin = $('#admin');

        account.popover({
            content: '用户名不能为空',
            placement: 'top',
            trigger: 'manual',
        });

        password.popover({
            content: '密码不能为空',
            placement: 'top',
            trigger: 'manual',
        });

        account.focus(function () {
            $('.popover').popover('hide');
        });

        password.focus(function () {
            $('.popover').popover('hide');
        })


        student.click(function () {
            loginButton.html('学生登录');
        });

        mentor.click(function () {
            loginButton.html('教师登录');
        });

        admin.click(function () {
            loginButton.html('管理员登录');
        });

        loginButton.click(function () {
            loginButton.attr('disabled', true);
            loginButton.popover('hide');

            let account_value = $.trim(account.val());
            if (account_value.length === 0) {
                account.popover('show');
                $('.popover').removeClass('popover-success popover-success-left')
                    .removeClass('popover-danger-left')
                    .addClass('popover-danger')
                    .addClass('popover-danger-top');
                loginButton.removeAttr('disabled');
                return false;
            }

            let password_value = $.trim(password.val());
            if (password_value.length === 0) {
                password.popover('show');
                $('.popover').removeClass('popover-success popover-success-left')
                    .removeClass('popover-danger-left')
                    .addClass('popover-danger')
                    .addClass('popover-danger-top');
                loginButton.removeAttr('disabled');
                return false;
            }

            let role;
            let identity = $.trim(loginButton.text());
            if(identity === '教师登录')
                role = 'mentor';
            else if(identity === '学生登录')
                role = 'student';
            else
                role = 'admin';



            let remember_me = autoLogin[0].checked;
            password_value = hex_md5(password_value);

            console.log('username:' + account_value);
            console.log('password:' + password_value);
            console.log('remember_me:' + remember_me);
            console.log('role:' + role);

            $.ajax({
            url: '/auth/login',
            method: 'post',
            data: {
                'username': account_value,
                'password': password_value,
                'remember_me': remember_me,
                'role': role
            },
            success: function (data) {
                console.log(data);
                if (data['code'] === 200)
                {
                    loginButton.popover('dispose').popover({
                        offset: '0,10',
                        content: '登陆成功',
                        placement: 'left',
                        trigger: 'manual'
                    });
                    loginButton.popover('show');
                    $('.popover').removeClass('popover-danger popover-danger-top')
                        .addClass('popover-success popover-success-left');
                    setTimeout(function () {
                        location.href = '/index'
                    }, 500);
                }
                else
                {
                    loginButton.removeAttr('disabled');
                    loginButton.popover('dispose').popover({
                        offset: '0,10',
                        content: '用户名或密码错误',
                        placement: 'left',
                        trigger: 'manual'
                    });
                    loginButton.popover('show');
                    $('.popover').removeClass('popover-danger-top')
                        .addClass('popover-danger popover-danger-left');
                }
            }
        });
        });

    })