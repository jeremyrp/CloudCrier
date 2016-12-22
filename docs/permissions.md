# Permissions

## Used for CloudWatch log dump
* Create S3 bucket: cloudcrier
* Create user - CloudCrierAdmin
* Create group - CC_GRP_Admin

## Used for Deployment Harness
* Create user - CloudCrierPublish
* Create group - CC_GRP_Publish
* Create IAM policy - CC_POL_Publish
~~~~
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "lambda:UpdateFunctionCode",
                "lambda:UpdateFunctionConfiguration",
                "lambda:InvokeFunction",
                "lambda:GetFunction",
                "lambda:PublishVersion",
                "lambda:UpdateAlias"
            ],
            "Resource": [
                "arn:aws:lambda:**YOUR_AWS_REGION**:**YOUR_AWS_ACCOUNT_ID**:function:**YOUR_FUNCTION_NAME**"
            ]
        }
    ]
}
~~~~