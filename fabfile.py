from fabric.api import cd, run, get, put, sudo, hosts


remote_host = 'unfeed.wolege.ca'
remote_repo = '/srv/unfeed.wolege.ca'
remote_user = 'unfeed'
remote_proc = 'unfeed:*'


@hosts(remote_host)
def sync():
    with cd(remote_repo):
        get('production/*.cfg', 'production/')


@hosts(remote_host)
def deploy():
    with cd(remote_repo):
        sudo('git pull --ff-only origin master', user=remote_user)
        run('pip install -r requirements.txt')
        get('production/*.cfg', 'production/%(basename)s.cfg.last')
        put('production/*.cfg', 'production/', use_sudo=True)
    sudo('supervisorctl restart %s' % remote_proc)
