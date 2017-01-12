# Need to parse gmail inbox messages to pull additional data to feed back into dynamo DB for revised notification history in v0.3
# Some code plagarized from http://www.ripariandata.com/blog/how-to-export-your-gmail-to-excel

import mailbox
import csv
import pprint

pp = pprint.PrettyPrinter(indent=4)
writer = csv.writer(open("IGNORE_clean_mail.csv", "wb"))

for message in mailbox.mbox('IGNORE_CloudCrier.mbox'):
    if message['from'].lower() != "citycloud@cloudcrier.com":
        continue;
    event_type = ""
    if message.is_multipart():
        if message.get_payload()[0].as_string().find("doesn't") > 1:
            event_type = "short"
#            pp.pprint("multi-short")
        elif message.get_payload()[0].as_string().find("bubble") > 1:
            event_type = "double"
#            pp.pprint("multi-double")
        elif message.get_payload()[0].as_string().find("bacon") > 1:
            event_type = "long"
#            pp.pprint("multi-long")
        else:
            pp.pprint("multi-unknown")
#            pp.pprint(message.get_payload()[0].as_string())

    else:
        if message.get_payload().find("doesn't") > 1:
            event_type = "short"
#            pp.pprint("short")
        elif message.get_payload().find("bubble") > 1:
            event_type = "double"
#            pp.pprint("double")
        elif message.get_payload().find("bacon") > 1:
            event_type = "long"
#            pp.pprint("long")
        else:
            pp.pprint("unknown")
#            pp.pprint(message.get_payload())


    pp.pprint([event_type, message['from'], message['date']])
    writer.writerow([event_type, message['from'], message['date']])