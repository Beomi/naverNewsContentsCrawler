import boto3

client = boto3.client('lambda')

res = client.update_function_code(
    FunctionName='string',
    ZipFile=b'bytes',
    S3ObjectVersion='string',
    Publish=True,
)
