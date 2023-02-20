try:
    import unzip_requirements
except ImportError:
    pass

try:
    import json
    import uuid
    import os
    import boto3
except Exception as e:
    pass

global AWS_ACCESS_KEY
global AWS_SECRET_KEY
global AWS_REGION_NAME

AWS_ACCESS_KEY = os.getenv("DEV_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("DEV_SECRET_KEY")
AWS_REGION_NAME = os.getenv("DEV_REGION")

client = boto3.client("emr-serverless",
                      aws_access_key_id=AWS_ACCESS_KEY,
                      aws_secret_access_key=AWS_SECRET_KEY,
                      region_name=AWS_REGION_NAME)


def lambda_handler_test_emr(event, context):
    print("event")
    print("\n")
    print(event)

    TaskToken = json.loads(event.get("Records")[0].get("body")).get("myTaskToken")
    print("TaskToken")
    print(TaskToken)
    print("\n")

    input_payload = json.loads(event.get("Records")[0].get("body")).get("input")
    print("input_payload")
    print(input_payload)
    print("\n")

    response = client.start_job_run(
        applicationId=input_payload.get("ApplicationId"),
        clientToken=uuid.uuid4().__str__(),
        executionRoleArn=input_payload.get("ExecutionArn"),
        jobDriver={
            'sparkSubmit': {
                'entryPoint': input_payload.get("ScriptPath"),
                'entryPointArguments': [TaskToken],
                'sparkSubmitParameters': input_payload.get("SparkSubmitParameters"),
            },
        },
        executionTimeoutMinutes=input_payload.get("ExecutionTime"),
        name=input_payload.get("JobName"),
    )
    print("response")
    print(response)
    print("\n")


def success(event, context):
    print("success event ", event)


def failure(event, context):
    print("failure event ", event)
