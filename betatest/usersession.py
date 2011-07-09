from betatest import *
from betatest.models.user import User

def login(username):
    session['logged_in'] = True
    session['username'] = username

def logout():
    session.pop('logged_in', None)
    session.pop('username', None)


def getCurrentUser():
    if has_request_context() and 'username' in session:
        return User.query.filter_by(username = session['username']).first_or_404()
    return None


def loginCheck(action = "error", # error | warning | none
        users = [],
        error_code = 403,         # abort(??):
        warning_none = "You have to be logged in to view this page.",
        warning_wrong = "You are not allowed to view this page."):
    logged = getCurrentUser()
    if (logged == None) or (users and not logged in users):
        if action == "error":
            abort_reason(error_code, warning_none if not users else warning_wrong)
        elif action == "warning":
            flash((warning_none if not users else warning_wrong), "warning")
        return False
    else:
        return True
