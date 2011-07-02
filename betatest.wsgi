activate_this = '/var/http/betatest/env/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

from betatest import app as application
