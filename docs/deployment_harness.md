# Overview
Provide an automated deployment harness to push changes up to AWS.

## Plan
For initial usage, not looking at anything fancy like serverless, etc...  Just looking for single button deployment of
lambda code, so will use hardcoded python script

## Assumptions
* aws sdk installed
* Appropriate config parameters defined in ./conf/deploy_aws.cfg
  * AWS_ACCESS_KEY_ID
  * AWS_SECRET_ACCESS_KEY
  * AWS_DEFAULT_REGION

## Execution
~~~
./deploy.py
~~~

## Notes/Considerations
Using custom config file to define AWS credentials as want to limit permissions of deploy role/user

## Future
Look at existing harnesses, or possibly use AWS CodeDeploy?

