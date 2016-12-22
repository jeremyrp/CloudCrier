__author__ = "Jeremy Phillips"
__license__ = "GPL"
__version__ = "2016.12.06.1"
__maintainer__ = "Jeremy Phillips"
__email__ = "code@cloudcrier.com"
__status__ = "Production"
###  Description:  Lambda function for initiation from IoT function for CloudCrier
###  Version:
###  Environment variables:  CC_DDB_TableName
###                          Email_List


import boto3
import datetime
import decimal
import time

def cc_lambda_event(event, context):
    dynamodb = boto3.resource("dynamodb", region_name=os.environ['AWS_REGION'])
    table = dynamodb.Table(os.environ['CC_DDB_TableName'])

    itemSingle = table.get_item(
        Key={
            'ButtonPressType': "SINGLE"
        }
    )
    itemDouble = table.get_item(
        Key={
            'ButtonPressType': "DOUBLE"
        }
    )
    itemLong = table.get_item(
        Key={
            'ButtonPressType': "LONG"
        }
    )

    emailFooter = """


Cumulative Count of Jeremy's Decrees
************************************
Don't give a shit: """ + str(itemSingle['Item']['ButtonPressCount']) + """ since """ + datetime.datetime.fromtimestamp(itemSingle['Item']['ButtonPressTimestamp']).strftime("%a, %b %w %Y at %I:%M %p") + """
Happy: """ + str(itemDouble['Item']['ButtonPressCount']) + """ since """ + datetime.datetime.fromtimestamp(itemDouble['Item']['ButtonPressTimestamp']).strftime("%a, %b %w %Y at %I:%M %p") + """
Craving XXX: """ + str(itemLong['Item']['ButtonPressCount']) + """ since """ + datetime.datetime.fromtimestamp(itemLong['Item']['ButtonPressTimestamp']).strftime("%a, %b %w %Y at %I:%M %p") + """

Learn more: www.CloudCrier.com
"""

    # determine button press to define message
    if (event["clickType"] == "SINGLE"):
        emailMessage = """
Jeremy has told the Cloud Crier that he doesn't give a shit...

"""
        #Update DB record
        response = table.update_item(
            Key={
                'ButtonPressType':"SINGLE"
            },
            UpdateExpression="set ButtonPressCount = ButtonPressCount + :i, ButtonPressTimestamp = :t",
            ExpressionAttributeValues={
                ":i": decimal.Decimal(1),
                ":t": decimal.Decimal(time.time())
            },
            ReturnValues='NONE'
        )
    elif (event["clickType"] == "DOUBLE"):
        emailMessage = """
Jeremy has told the Cloud Crier that he is happy...

"""
        #Update DB record
        response = table.update_item(
            Key={
                'ButtonPressType':"DOUBLE"
            },
            UpdateExpression="set ButtonPressCount = ButtonPressCount + :i, ButtonPressTimestamp = :t",
            ExpressionAttributeValues={
                ":i": decimal.Decimal(1),
                ":t": decimal.Decimal(time.time())
            },
            ReturnValues='NONE'
        )
    else:
        emailMessage = """
Jeremy has told the Cloud Crier that he is craving random.choice(['beer','bacon','amusement'])...

Make it happen.  Now!  *clap*clap*"""
        # Update DB record
        response = table.update_item(
            Key={
                'ButtonPressType': "LONG"
            },
            UpdateExpression="set ButtonPressCount = ButtonPressCount + :i, ButtonPressTimestamp = :t",
            ExpressionAttributeValues={
                ":i": decimal.Decimal(1),
                ":t": decimal.Decimal(time.time())
            },
            ReturnValues='NONE'
        )

    # Append footer to email
    emailMessage += emailFooter

    # Plagarized from http://mattharris.org/2016/02/introduction-aws-lambda/
    session = boto3.session.Session()
    ses = session.client('ses')
    ses.send_email(
        Source='CityCloud@CloudCrier.com',
        Destination={
            'ToAddresses': [
                os.environ['Email_List']
            ]
        },
        Message={
            'Subject': {
                'Data': 'Message from the cloud...',
            },
            'Body': {
                'Text': {
                    'Data': emailMessage,
                },
            }
        },
    )

    return "Message: ", emailMessage

#['jeremy@CloudCrier.com','mike@CloudCrier.com','jim@CloudCrier.com']