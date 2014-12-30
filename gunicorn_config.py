# Gevent workers
worker_class = 'gevent'
worker_connections = 1000
timeout = 20

# Logging
log_level = 'DEBUG'


def on_exit(server):
    server.log.info("Server exiting!")
    print 'Server exiting!'

    import os
    import sys

    # Add cwd to path, so we can import eternaleve
    sys.path.append(os.getcwd())
    os.environ['DJANGO_SETTINGS_MODULE'] = 'authserver_project.settings'
