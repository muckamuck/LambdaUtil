import os
import logging
import json
import datetime

import boto3

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
sts_client = boto3.client('sts')


def lambda_handler(event, context):
    '''
    This is the function that gets called when the lambda is invoked.
    Note: the name of the function is important for the deployment so only
    change it if you grok the consequences.

    Args:
        event - the dictionary filled with the bits of data from the invocation
        context - the context object of the invocation. For more information
        see http://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns:
        Whatever you want
    '''
    if context is not None:
        logger.info(f'invoked_function_arn = {context.invoked_function_arn}')
        logger.info(f'     log_stream_name = {context.log_stream_name}')
        logger.info(f'      log_group_name = {context.log_group_name}')

    logger.info(json.dumps(event, default=date_converter))

    answer = os.environ.get('ANSWER', -1)  # injected from the stage's config file [parameters]
    logger.info('answer: %s', answer)

    print('################################################################################')
    print('## START                                                                      ##')
    print('################################################################################')
    for key, value in os.environ.items():
        print(f'{key} => {value}')
    print('################################################################################')
    print('## FINISH                                                                     ##')
    print('################################################################################')

    response = sts_client.get_caller_identity()
    return {
        'statusCode': 200,
        'body': json.dumps(response, default=date_converter, indent=2)
    }


def date_converter(o):
    '''
    Helper thing to convert dates for JSON module.

    Args:
        o - the thing to dump as string.

    Returns:
        if an instance of datetime the a string else None
    '''
    if isinstance(o, datetime.datetime):
        return o.__str__()
