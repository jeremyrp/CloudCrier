# Overview
I wanted to play around with the Amazon IoT/Dash buttons (https://aws.amazon.com/iotbutton/), so bought one and this is the initial playground I used it for.  One of the few enjoyables aspects of my current job is that I work with a bunch of jerks
that share the same snarky attitude as I, and we tend to share our opinions and current mood quite openly amongst ourselves over IM.  But I'm lazy, and typing is hard, so I wanted to simply my broadcasts.  Hence the IoT button.

The IoT button has 3 possible states it can generate (single press, double press, long press) and communicate to the AWS IoT cloud.  So I boiled the plethora of proclamations I can produce down to three:

* I don't give a shit about whatever I'm currently having to deal with
* I'm currently happy and enjoying whatever has my attention for the moment
* There is something I'm currently craving; most likely beer, pizza, or something along those lines

One of the capabilities of AWS IoT is to trigger an AWS Lambda function.  So now with the press of a button I can trigger a python script in "the cloud", and it will know some basic parameters around what manner I pressed the button.  What should I do with this power?  Send an email of course!

Just for the sake of complicating things even further, lets grab some basic stats from the event (type of button press; timestamp) and capture in dynamodb (cause I wanted to excuse to play with this instead of RDS) and include some metrics in the emails.  Maybe some future day I'll get fancy and do something with these stats...

The AWS lambda function will use AWS SES to send an email to beloved coworkers to share the declaration I have made with but the mear press of a button.

tldr; I reinvented a shittier version of twitter married to a Staples easy-button

## AWS SES Restrictions
One of the 'limitations' around AWS SES is that it can only send to 'approved' email addresses and it has a 200/day rolling max for emails.  I totally get (and support) why these limitations are put in place (AWS doesn't want to be a spamhaus), but I can't have the beneficiaries of words of wisdom being notified/authorized *before* they start to receive the emails, let alone have an easy way of opting out.

This is where custom domain comes into play.  SES will allow you to verify a domain (by creating a TXT DNS entry with a specific value).  By then creating forwarders off my custom domain that send the emails on to their intended ~~victim~~ winner, I can now have SES send an email to mike@myhostname.com and it gets forwarded to mike@gmail.com .  I'm winning!

The 200/day max is not a consideration for me, as I can only press the button so many times per day before I invite revenge communications.  Plus, the battery on the button only lasts ~1000 presses.

## Additional Content
[Permissions](./docs/permissions.md)
[Deployment Harness](./docs/deployment_harness.md)