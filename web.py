import os
from src import bootstrap_web

config_file = os.environ.get('FLASKELETON_CONFIG', 'config_default.yml')
env = os.environ.get('FLASKELETON_ENV', 'dev')

env_list = ['dev', 'prod']
if env not in env_list:
    raise ValueError('Expected environment in [{}], got {}'.format(','.join(env_list), env))

app = bootstrap_web(config_file=config_file, env=env)

if __name__ == '__main__':
    app.run(
        host=app.config['app']['host'],
        port=app.config['app']['port'],
        threaded=True,
    )
