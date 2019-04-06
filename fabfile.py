import os
import subprocess
import time
from functools import partial

from fabric import task

from tim_keeler.config import get_config

config = get_config('remote')
log_config = get_config('logging')
tim_task = partial(task, hosts=[config['host']])


@tim_task()
def hostname(c):
    c.run('hostname')


@tim_task()
def deploy(c):
    response = input('Are you sure you wish to update production? (y/N) ')
    if response.strip().lower() != 'y':
        print('\033[1;31mAborting!\033[0m')
        return

    print('\n\033[1;36mBuilding static files...\033[0m')
    # You will need to modify this command if you do not have make installed
    subprocess.run(['make', 'build'])

    print('\n\033[1;32mStarting update process in 5 seconds!\033[0m')
    wait(5)

    print('\n\033[1;36mBuilding static tarball...\033[0m')
    tar_ball = 'dist.tar.gz'
    subprocess.run(['tar', 'czf', tar_ball, 'dist/'])

    with c.cd(config['app_location']):
        print('\n\033[1;36mPulling latest code and installing requirements...\033[0m')
        c.run('git pull')
        c.run('.venv/bin/pip install -r requirements.txt')

        print('\n\033[1;36mUnbundling static files...\033[0m')
        c.put(tar_ball, remote=config['app_location'])
        c.run(f'tar -xf {tar_ball}')
        c.run(f'rm {tar_ball}')

        print('\n\033[1;36mMigrating database...\033[0m')
        c.run('.venv/bin/python manage.py migrate')

    print('\n\033[1;36mRestarting services...\033[0m')
    c.sudo('systemctl restart {}.service'.format(config['gunicorn_process_name']))
    c.sudo('systemctl restart nginx')
    c.sudo('redis-cli flushall')

    print('\n\033[1;36mCleaning up local directory...\033[0m')
    wait(1)
    subprocess.run(['rm', tar_ball])

    print('\n\033[1;32mUpdate complete!\033[0m')


@tim_task()
def logs(c, log_name):
    download_log(c, log_name)
    subprocess.run(['less', f'/tmp/{log_name}.log'])
    os.remove(f'/tmp/{log_name}.log')


@tim_task()
def download_log(c, log_name):
    if log_name not in {'info', 'error'}:
        raise Exception('Not a valid log file!')
    c.get(log_config['handlers'][f'{log_name}_file_handler']['filename'],
          local=f'/tmp/{log_name}.log')


def wait(amt: int) -> None:
    for i in range(amt):
        time.sleep(1)
