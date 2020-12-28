// 用户验证的功能，登录、注册、注销等

$(function () {
    const inputAccount = $("#inputAccount");
    const inputPassword = $("#inputPassword");
    const teacherButton = $('#teacherButton')[0];
    const studentButton = $('#studentButton')[0];
    const systemAdmButton = $('#systemAdmButton')[0];
    const loginButton = $("#loginBtn");

    inputAccount.popover({
        content: '用户名不能为空',
        placement: 'top',
        trigger: 'manual',
    });
    inputAccount.focus(function () {
        $('.popover').popover('hide');
    });

    inputPassword.popover({
        content: '密码不能为空',
        placement: 'top',
        trigger: 'manual',
    });
    inputPassword.focus(function () {
        $('.popover').popover('hide');
    });


    loginButton.click(function () {
        loginButton.attr('disabled', true);
        loginButton.popover('hide');

        //数据校验
        let identity;
        let account = $.trim(inputAccount.val());
        let password = $.trim(inputPassword.val());
        if (account.length === 0) {
            inputAccount.popover('show');
            $('.popover').removeClass('popover-success popover-success-left')
                .removeClass('popover-danger-left')
                .addClass('popover-danger')
                .addClass('popover-danger-top');
            loginButton.removeAttr('disabled');
            return false;
        }

        if (password.length === 0) {
            inputPassword.popover('show');
            $('.popover').removeClass('popover-success popover-success-left')
                .removeClass('popover-danger-left')
                .addClass('popover-danger')
                .addClass('popover-danger-top');
            loginButton.removeAttr('disabled');

            return false;
        }

        if(teacherButton.checked === true)
            identity = 'mentor';
        else if(studentButton.checked === true)
            identity = 'student';
        else
            identity = 'admin';

        password = hex_md5(password);

        let remember_me = $('#remember').prop('checked');

        $.ajax({
            url: '/auth/login',
            method: 'post',
            data: {
                'username': account,
                'password': password,
                'remember_me': remember_me,
                'role': identity
            },
            success: function (data) {
                if (data === 'success')
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



        // let data = 'fa';
        //
        // if (data === 'success')
        // {
        //     loginButton.popover('dispose').popover({
        //         offset: '0,10',
        //         content: '登陆成功',
        //         placement: 'left',
        //         trigger: 'manual'
        //     });
        //     loginButton.popover('show');
        //     $('.popover').removeClass('popover-danger popover-danger-top')
        //         .addClass('popover-success popover-success-left');
        //     setTimeout(function () {
        //         location.href = '/index'
        //     }, 500);
        // }
        // else
        // {
        //     loginButton.removeAttr('disabled');
        //     loginButton.popover('dispose').popover({
        //         offset: '0,10',
        //         content: '用户名或密码错误',
        //         placement: 'left',
        //         trigger: 'manual'
        //     });
        //     loginButton.popover('show');
        //     $('.popover').removeClass('popover-danger-top')
        //         .addClass('popover-danger popover-danger-left');
        // }

    });
});

