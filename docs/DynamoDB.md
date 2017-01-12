# DynamoDB

## Schema as of <0.3
The DB table is quite basic; 3 columns(ButtonPressType [PK], ButtonPressCount, and ButtonPressTimestamp) with a total of 3 records (one each for single, double, and long)

## Schema as of 0.3
Looking to create a running history of the entries, so moving to a different table (since will change primary key):
* [PK] eventAuthor
* [SK] eventTimestamp
* eventType
*