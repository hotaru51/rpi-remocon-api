from os import path

repo_root = path.dirname(path.realpath(__file__ + '/..'))

proc_name = 'rpi-remocon-api'

bind = 'unix:' + repo_root + '/tmp/' + proc_name + '.sock'

workers = 1

accesslog = repo_root + '/log/access.log'
errorlog = repo_root + '/log/error.log'
loglevel = 'info'
pidfile = repo_root + '/tmp/' + proc_name + '.pid'
