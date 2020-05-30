import os
from src import bootstrap_cli

config_file = os.environ.get('FLASKELETON_CONFIG', 'config_default.yml')
env = os.environ.get('FLASKELETON_ENV', 'dev')

env_list = ['dev', 'prod']
if env not in env_list:
    raise ValueError('Expected environment in [{}], got {}'.format(','.join(env_list), env))

app = bootstrap_cli(config_file=config_file, env=env)
