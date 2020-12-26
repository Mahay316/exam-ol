from functools import wraps
from flask import abort, session, redirect, url_for
from flask_login import current_user


def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def should_be(roles:list):
    """
    确保用户身份的装饰器

    example:
    @should_be(['teacher', 'student'])
    def teacher_do():
        pass

    :param role: 用户身份表示，暂定字符串全程，后期可以改进为类等
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            cur_role = session.get('role')
            if cur_role is None:
                return redirect(url_for('auth.login'))

            if cur_role not in roles:
                abort(403)

            return f(*args, **kwargs)
        return decorated_function
    return decorator
