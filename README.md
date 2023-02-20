# Automating orchestrating Spark Jobs for EMR Serverless with Async callback Pattern using Step functions 

![image](https://user-images.githubusercontent.com/39345855/218604764-fe853ffc-49c3-4ead-b0db-3208de6d6c87.png)

## Youtube Video 
* https://www.youtube.com/watch?v=eRkT9BPbjPo&t=3s
---------------------------------------------------------

### Sometimes customers want to take advantage of the intuitive nature of Step Functions while integrating with external systems either synchronously or asynchronously.Callback tasks provide a way to pause a workflow until a task token is returned. A task might need to wait for a human approval, integrate with a third party, or call legacy systems. For tasks like these, you can pause Step Functions until the workflow execution reaches the one year service quota (see, Quotas related to state throttling), and wait for an external process or workflow to complete. For these situations Step Functions allows you to pass a task token to the AWS SDK service integrations, and also to some Optimized service integrations. The task will pause until it receives that task token back with a SendTaskSuccess or SendTaskFailure call.I will be showing you how to orchestrate Spark job using AWS step function


## Step 1: Deploy the stack 

##### Make sure to edit ENV files
```
npm install -g serverless

npx serverless config credentials --provider aws --key XXXX  --secret XXXXX -o

npx serverless plugin install -n serverless-step-functions
npx serverless plugin install -n serverless-python-requirements

npx sls deploy --region=us-east-1
```
## Step 2: Deploy Python Package Boto3 and Botocore to S3 
Follow Steps https://docs.aws.amazon.com/emr/latest/EMR-Serverless-UserGuide/using-python-libraries.html

##### Open Cloud Shell and execute these commands 
```
python3 -m venv pyspark_venv
source pyspark_venv/bin/activate

pip install --upgrade pip
pip3 install boto3
pip3 install botocore
pip3 install venv-pack
venv-pack -f -o pyspark_venv.tar.gz
s3 cp pyspark_venv.tar.gz s3://<BUCKET NAME IN ENV FILE USE THAT BUCKET >/python-packages/
```


## Step 3: Deploy the Python script on S3 under folder called scripts 
```
try:
    import sys
    import os
    from datetime import datetime
    import json
    import boto3
    from pyspark import SparkContext
    from pyspark.sql import SparkSession

    print("All Imports okay")
except Exception as e:
    print("ERROR ", e)

sc = SparkContext()
spark = SparkSession.builder.getOrCreate()


region = 'us-east-1'


client = boto3.client("stepfunctions",
                      aws_access_key_id="XXXX",
                      aws_secret_access_key="XXXX",
                      region_name='us-east-1')


if len(sys.argv) == 1:
    print('no arguments passed')
    sys.exit()

else:
    try:

        """
        SPARK CODE GOES HERE
        """
        tasktoken = json.dumps(sys.argv[1])
        response = client.send_task_success(taskToken=tasktoken, output=tasktoken)
    except Exception as e:
        print("ERROR :{} ".format(e))
        tasktoken = json.dumps(sys.argv[1])
        response = client.send_task_failure(taskToken=tasktoken, output=tasktoken)
        raise Exception(e)

```


## Step 4: FIRE EMR JOBS VIA STEP Functions

#### input payload 

```
{
        "ApplicationId": "XXXXX",
        "ScriptPath": "s3://<BUCKET GOES HERE THE ONE IN ENV FILE>/scripts/mytest.py",
        "SparkSubmitParameters": "--conf spark.archives=s3://<BUCKET GOES HERE THE ONE IN ENV FILE>/python-packages/pyspark_venv.tar.gz#environment --conf spark.emr-serverless.driverEnv.PYSPARK_DRIVER_PYTHON=./environment/bin/python --conf spark.emr-serverless.driverEnv.PYSPARK_PYTHON=./environment/bin/python --conf spark.executorEnv.PYSPARK_PYTHON=./environment/bin/python --conf spark.hadoop.hive.metastore.client.factory.class=com.amazonaws.glue.catalog.metastore.AWSGlueDataCatalogHiveClientFactory --conf spark.sql.hive.convertMetastoreParquet=false --conf spark.serializer=org.apache.spark.serializer.KryoSerializer",
        "ExecutionTime": 600,
        "JobName": "mytest",
        "ExecutionArn": "arn:aws:iam::<ACCOUNT ID>:role/EMRServerlessS3RuntimeRole"
    }
```

## Step 5: FIRE EMR JOBS VIA STEP Functions
![image](https://user-images.githubusercontent.com/39345855/220165348-82bcdc59-0f69-472b-bf49-d0bdb6a804c5.png)



