import base64
import json
import re
import boto3
import os
from botocore.exceptions import ClientError
from genson import SchemaBuilder

AWS_DEFAULT_REGION = os.getenv('AWS_DEFAULT_REGION')
CWD = os.getcwd()
S3_REGEX = '^s3://([^/]+)/(.*?([^/]+)/?)$'


def generate_schema(secret_name, region=AWS_DEFAULT_REGION):
    secret = __retrieve_secret(secret_name, region)
    builder = SchemaBuilder()
    builder.add_object(secret)
    schema = builder.to_schema()
    print(f"Schema for secret: \n{schema}")
    return schema


def write_schema(secret_name, json_schema, file_path=CWD):
    file_name = f"{secret_name}_schema.json"

    # TODO impement s3 uploads
    # if file_path.split(':')[0] == 's3':
    #     __s3_write_file(file_name, json_schema, file_path)

    try:
        file = open(f"{file_path}/{file_name}", "w")
        file.write(json.dumps(json_schema))
        file.close
    except ClientError as e:
        raise e
    return True


# TODO Implement S3 uploads
# def __s3_write_file(file_name, json_schema, file_path):
#     parts = re.search('^s3://([^/]+)/(.*?([^/]+)/?)$', file_path)
#     bucket, path = parts(1), parts(2)


def __retrieve_secret(secret_name, region):
    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager', region_name=region)
    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name)
    except ClientError as e:
        raise e
    else:
        # Decrypts secret using the associated KMS key.
        # Depending on whether the secret is a string or binary, one of these fields will be populated.
        if 'SecretString' in get_secret_value_response:
            return json.loads(get_secret_value_response['SecretString'])
        else:
            return base64.b64decode(get_secret_value_response['SecretBinary'])
