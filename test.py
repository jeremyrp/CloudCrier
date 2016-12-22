import ConfigParser
import os
import boto3
import json
import datetime
import base64

# Constants
CONFIG_FILE_PATH = "./conf/aws.cfg"
TEST_FILE_PATH = "./test/input_short.json"

def serialize(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, datetime.date):
        serial = obj.isoformat()
        return serial

    if isinstance(obj, datetime.time):
        serial = obj.isoformat()
        return serial

    return "Unknown Object Type"

# Init variables
testParameters = {}

# Check that config file exists
if os.path.exists(CONFIG_FILE_PATH) != True:
    print("ERROR: Unable to find config file")
    exit()

# Pull config data for pushing to AWS
try:
    testConfig = ConfigParser.ConfigParser()
    testConfig.read(CONFIG_FILE_PATH)
    testParameters['AWS_ACCESS_KEY_ID'] = testConfig.get('deploy_aws', 'AWS_ACCESS_KEY_ID')
    testParameters['AWS_SECRET_ACCESS_KEY'] = testConfig.get('deploy_aws', 'AWS_SECRET_ACCESS_KEY')
    testParameters['AWS_DEFAULT_REGION'] = testConfig.get('deploy_aws', 'AWS_DEFAULT_REGION')
    testParameters['AWS_LAMBDA_FUNCTION_NAME'] = testConfig.get('deploy_aws', 'AWS_LAMBDA_FUNCTION_NAME')
except:
    print("ERROR: Unable to parse all test parameters from config file")
    exit()

# Connect to Lambda
lambdaClient = boto3.client(
    service_name = 'lambda',
    aws_access_key_id = testParameters['AWS_ACCESS_KEY_ID'],
    aws_secret_access_key = testParameters['AWS_SECRET_ACCESS_KEY'],
    region_name = testParameters['AWS_DEFAULT_REGION']
)

payloadFile = open(TEST_FILE_PATH)
lambdaResponse = lambdaClient.invoke(
    FunctionName=testParameters['AWS_LAMBDA_FUNCTION_NAME'],
    InvocationType='RequestResponse',
    LogType='Tail',
    Payload=payloadFile
)

print("Finished invoke...")
#print("Response: {}".format(lambdaResponse))
#parsedJson = json.loads(lambdaResponse)
print json.dumps(lambdaResponse, skipkeys=True, indent=4, sort_keys=True, default=serialize)
print("Log Tail: {}".format(base64.b64decode(lambdaResponse['LogResult'])))