ALLDIRS = ['/home/jcastor/.virtualenvs/499project/lib/python2.6/site-packages']
# the above directory depends on the location of your python installation.
# if using virtualenv, it will need to match your projects locale.
import os
import sys
import site

prev_sys_path = list(sys.path)
for directory in ALLDIRS:
    site.addsitedir(directory)
    new_sys_path = []
    for item in list(sys.path):
        if item not in prev_sys_path:
            new_sys_path.append(item)
            sys.path.remove(item)
            sys.path[:0] = new_sys_path

    # change this depending on your project.
sys.path.append('/home/jcastor/django/499project/smart_bus')

os.environ['PYTHON_EGG_CACHE'] = '/home/jcastor/.python-eggs'
os.environ['DJANGO_SETTINGS_MODULE'] = 'smart_bus.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()                                                            
