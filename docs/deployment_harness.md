# Overview
Provide an automated deployment harness to push changes up to AWS.

## Plan
For initial usage, not looking at anything fancy like serverless, etc...  Just looking for single button deployment of lambda code, so will use hardcoded AWS CLI

## Assumptions
* awscli installed
* Appropriate environment variables configured for awscli
  * AWS_ACCESS_KEY_ID
  * AWS_SECRET_ACCESS_KEY
  * AWS_DEFAULT_REGION

## Execution
~~~
./deploy.sh
~~~

## Future
Look at existing harnesses, or possibly use AWS CodeDeploy?

