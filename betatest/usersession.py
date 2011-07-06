from betatest import *

def login(username):
    session['logged_in'] = True
    session['username'] = username

def logout():
    session.pop('logged_in', None)
    session.pop('username', None)

def getCurrentUser():
    if 'username' in session:
        return models.user.User.query.filter_by(username = session['username']).first_or_404()
    else:
        return None


def loginCheck(action = "error", # error | warning | none
        users = [],
        error_code = 403,         # abort(??):
        warning_none = "You have to be logged in to view this page.",
        warning_wrong = "You are not allowed to view this page."):
    logged = getCurrentUser()
    if (logged == None) or (users and not logged in users):
        if action == "error":
            abort(error_code)
        elif action == "warning":
            flash((warning_none if not users else warning_wrong), "warning")
        return False
    else:
        return True
