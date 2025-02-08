import sys
import json
import subprocess
import logging
import pdb

import boto3

logger = logging.getLogger(__name__)

def get_creds():
    try:
        session = boto3.Session()
        credentials = session.get_credentials()
        current_credentials = credentials.get_frozen_credentials()

        access_key_id = current_credentials.access_key
        secret_access_key = current_credentials.secret_key
        session_token = current_credentials.token

        logger.debug(f'AWS_ACCESS_KEY_ID: {access_key_id}')
        logger.debug(f'AWS_SECRET_ACCESS_KEY: {secret_access_key}')
        logger.debug(f'AWS_SESSION_TOKEN: {session_token}')
        answer = {
            'AWS_ACCESS_KEY_ID': access_key_id,
            'AWS_SECRET_ACCESS_KEY': secret_access_key
        }

        if session_token:
            answer['AWS_SESSION_TOKEN'] = session_token

        return answer
    except Exception as wtf:
        logger.critical(f'get_creds() problem: {wtf}', exc_info=False)
        sys.exit(1)

def build_image():
    try:
        cmd = [
            'docker',
            'build',
            '-f', '.lambdautil-Dockerfile',
            '-t', 'simple-example-function',
            '.'
        ]
        subprocess.run(cmd, text=True)
    except Exception as wtf:
        logger.critical(f'build_image() problem: {wtf}', exc_info=False)
        sys.exit(1)

    return True

def run_image(creds):
    try:
        pdb.set_trace()
        access_key = creds['AWS_ACCESS_KEY_ID']
        secret = creds['AWS_SECRET_ACCESS_KEY']
        token = creds.get('AWS_SESSION_TOKEN')
        cmd = [
            'docker',
            'run',
            '-d',
            '--rm',
            '--name', 'simple-example-invocation',
            '-p', '9000:8080',
            '-e', f'AWS_ACCESS_KEY_ID={access_key}',
            '-e', f'AWS_SECRET_ACCESS_KEY={secret}',
            # '-e', f'AWS_SESSION_TOKEN={token}',
            'simple-example-function'
        ]
        result = subprocess.run(cmd, text=True)
        logger.info(result.returncode)
    except Exception as wtf:
        logger.critical(f'run_image() problem: {wtf}', exc_info=False)
        sys.exit(1)

if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        stream=sys.stdout,
        format='[%(levelname)s] %(asctime)s (%(module)s) %(message)s',
        datefmt='%Y/%m/%d-%H:%M:%S'
    )

    creds = get_creds()
    logger.debug(json.dumps(creds, indent=2))
    build_image()
    run_image(creds)

'''
import subprocess
import os

# Create a dictionary with the new environment variables
# You can start with os.environ.copy() to inherit the current environment,
# or create a new dict if you want a clean environment
new_env = os.environ.copy()
new_env['MY_VAR'] = 'my_value'
new_env['ANOTHER_VAR'] = 'another_value'

# Use subprocess.run with the new environment
result = subprocess.run(['echo', '$MY_VAR'], 
                         env=new_env, 
                         capture_output=True, 
                         text=True)

# Print the result
print(result.stdout.strip())
 '''
