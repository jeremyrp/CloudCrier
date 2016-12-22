import ConfigParser
import os
import zipfile
import tempfile
import boto3
import pprint

# Constants
CONFIG_FILE_PATH = "./conf/deploy_aws.cfg"
UPLOAD_PATH = tempfile.mkdtemp()
UPLOAD_FILE = "cc_lambda_event.zip"

# Init variables
deployParameters = {}

# Check that config file exists
if os.path.exists(CONFIG_FILE_PATH) != True:
    print("ERROR: Unable to find config file")
    exit()

# Pull config data for pushing to AWS
try:
    deployConfig = ConfigParser.ConfigParser()
    deployConfig.read(CONFIG_FILE_PATH)
    deployParameters['AWS_ACCESS_KEY_ID'] = deployConfig.get('deploy_aws', 'AWS_ACCESS_KEY_ID')
    deployParameters['AWS_SECRET_ACCESS_KEY'] = deployConfig.get('deploy_aws', 'AWS_SECRET_ACCESS_KEY')
    deployParameters['AWS_DEFAULT_REGION'] = deployConfig.get('deploy_aws', 'AWS_DEFAULT_REGION')
    deployParameters['AWS_LAMBDA_FUNCTION_NAME'] = deployConfig.get('deploy_aws', 'AWS_LAMBDA_FUNCTION_NAME')
except:
    print("ERROR: Unable to parse all deployment parameters from config file")
    exit()


try:
    # Create zip file to upload
    compressFile = zipfile.ZipFile(UPLOAD_PATH + UPLOAD_FILE, "w", zipfile.ZIP_DEFLATED)
    compressFile.write("./aws/cc_lambda_event.py","cc_lambda_event.py")
    compressFile.close()
except:
    print("ERROR: Unable to create ZIP upload file")

# Upload file to Lambda
lambdaClient = boto3.client(
    service_name = 'lambda',
    aws_access_key_id = deployParameters['AWS_ACCESS_KEY_ID'],
    aws_secret_access_key = deployParameters['AWS_SECRET_ACCESS_KEY'],
    region_name = deployParameters['AWS_DEFAULT_REGION']
)

# Open zipfil
uploadFile = open(UPLOAD_PATH+UPLOAD_FILE, 'r')
lambdaResponse = lambdaClient.update_function_code(
    FunctionName=deployParameters['AWS_LAMBDA_FUNCTION_NAME'],
    ZipFile=uploadFile.read(),
    Publish=True
)
uploadFile.close()

print("Finished uploading...")
print("File Name: " + UPLOAD_PATH + UPLOAD_FILE)