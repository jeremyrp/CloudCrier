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
import logging
import os

def cc_lambda_event(event, context):

    # Check to see if test flag sent, so to enable debug info
    if "DEBUG_FLAG" in event:
        DEBUG_FLAG=True
    else:
        DEBUG_FLAG=False

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

    emailTxtFooter = """


Cumulative Count of Jeremy's Decrees
************************************
Don't give a shit: """ + str(itemSingle['Item']['ButtonPressCount']) + """ since """ + datetime.datetime.fromtimestamp(itemSingle['Item']['ButtonPressTimestamp']).strftime("%a, %b %w %Y at %I:%M %p") + """
Happy: """ + str(itemDouble['Item']['ButtonPressCount']) + """ since """ + datetime.datetime.fromtimestamp(itemDouble['Item']['ButtonPressTimestamp']).strftime("%a, %b %w %Y at %I:%M %p") + """
Craving XXX: """ + str(itemLong['Item']['ButtonPressCount']) + """ since """ + datetime.datetime.fromtimestamp(itemLong['Item']['ButtonPressTimestamp']).strftime("%a, %b %w %Y at %I:%M %p") + """

Learn more: www.CloudCrier.com
"""

    # determine button press to define message
    if (event["clickType"] == "SINGLE"):
        emailTxtMessage = """
Jeremy has told the Cloud Crier that he doesn't give a shit...

"""
        if DEBUG_FLAG != True:
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
        emailTxtMessage = """
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
        emailTxtMessage = """
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

    emailHtmlMessage = """
<!DOCTYPE html>
<html lang='en'>
<head>
    <style>
        body {{
            font-family: Arial;
        }}
        th {{
            padding: 10px;
            border: 1px solid #000000;
        }}
        td {{
            padding: 5px;
            border: 1px solid #000000;
            background-color: #FBFFF1
        }}
    </style>
    <title>Message from the cloud...</title>
</head>
<body style='background-color:#B4C5E4'>
<h1 style='background-color: #3c3744; color: #FBFFF1; margin:5%; padding:5%'>{0}
</h1>
<div style='margin:5%'>
<table style='border: 1px solid #090c9b;border-collapse: collapse;'>
    <tr>
        <th colspan='3' style='color: #FBFFF1;background-color: #090c9b'>Cumulative Count of Jeremy's Decrees</th>
    </tr>
    <tr>
        <td style='background-color: #996600'>Don't give a shit</td>
        <td><span style='font-weight:bold'>{1}</span></td>
        <td><span style='font-size: 0.7em'>since</span> {2}</td>
    </tr>
    <tr>
        <td style='background-color: #d9ffb3'>Happy</td>
        <td><span style='font-weight:bold'>{3}</span></td>
        <td><span style='font-size: 0.7em'>since</span> {4}</td>
    </tr>
    <tr>
        <td>Craving XXX</td>
        <td><span style='font-weight:bold'>{5}</span></td>
        <td><span style='font-size: 0.7em'>since</span> {6}</td>
    </tr>
</table>
</div>
<h6 style='border: 1px solid #090c9b; text-align: center;  margin:5%; '>Learn more: <a href='http://www.cloudcrier.com' style='text-decoration: none'>www.CloudCrier.com</a></h6>

</body>
</html>""".format(
        emailTxtMessage,
        str(itemSingle['Item']['ButtonPressCount']),
        datetime.datetime.fromtimestamp(itemSingle['Item']['ButtonPressTimestamp']).strftime("%a, %b %w %Y at %I:%M %p"),
        str(itemDouble['Item']['ButtonPressCount']),
        datetime.datetime.fromtimestamp(itemDouble['Item']['ButtonPressTimestamp']).strftime("%a, %b %w %Y at %I:%M %p"),
        str(itemLong['Item']['ButtonPressCount']),
        datetime.datetime.fromtimestamp(itemLong['Item']['ButtonPressTimestamp']).strftime("%a, %b %w %Y at %I:%M %p")
    )

    # Append footer to email
    emailTxtMessage += emailTxtFooter

    # Plagarized from http://mattharris.org/2016/02/introduction-aws-lambda/
    session = boto3.session.Session()
    ses = session.client('ses')
    ses.send_email(
        Source='CityCloud@CloudCrier.com',
        Destination={
            'ToAddresses': [
                'jeremy@CloudCrier.com', 'mike@CloudCrier.com', 'jim@CloudCrier.com'
            ]
        },
        Message={
            'Subject': {
                'Data': 'Message from the cloud...',
            },
            'Body': {
                'Text': {
                    'Data': emailTxtMessage,
                },
                'Html': {
                    'Data': emailHtmlMessage,
                },
            }
        },
    )

    return "Message: ", emailTxtMessage

#['jeremy@CloudCrier.com','mike@CloudCrier.com','jim@CloudCrier.com']
#os.environ['Email_List']