import boto3
from decimal import Decimal
from datetime import datetime

REGION='us-west-1'
IDS=[]

'''
item = {
    'id': int,
    'username': String,
    'sessions': JSON array
}

session = {
    'id': int,
    'name': String,
    'images': S3 bucket link -> .zip,
    'data': JSON
}

data = {
    'summary': String,
    'confused': double
}
'''

dynamodb = boto3.resource('dynamodb', region_name=REGION)
table_name = 'attention-data'
user_table = dynamodb.Table(table_name)

# class User:
#     current_id = 0
#     def __init__(self, name):
#         self.id = User.current_id
#         User.current_id += 1
#         self.name = name
#         self.sessions = []

class Session:
    def __init__(self, name):
        if len(IDS) == 0:
            self.id = 0
        else:
            self.id = max(IDS) + 1
        IDS.append(self.id)
        self.name = name
        self.images = ""
        self.data = None
        self.datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# def add_user(user_item):
#     try:
#         response = user_table.put_item(Item=user_item)
#         print("Item added successfully:")
#         print(response)
#     except Exception as e:
#         print(f"Error adding item: {e}")

def add_session(session_name):
    session = create_session(session_name)
    session_item = create_session_item(session)
    try:
        response = user_table.put_item(Item=session_item)
        print("Session added successfully:")
        print(response)
        return session.id, session.datetime
    except Exception as e:
        print(f"Error adding session: {e}")

def delete_session(session_id):
    try:
        response = user_table.scan()
        items = response.get('Items', [])
        while 'LastEvaluatedKey' in response:
            response = user_table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            items = response.get('Items', [])
        user_name = None
        for item in items:
            kv_pairs = dict(zip([str(key) for key in item.keys()], [val for val in item.values()]))
            if int(kv_pairs['id']) == int(session_id):
                user_name = kv_pairs['name']
                break
        response = user_table.delete_item(Key = {'name' : user_name})
        print("Session deleted successfully") 
        print (response)
    except Exception as e:
        print(f"Error deleting session: {e}")


def create_user_item(user):
    item = {
        'id': user.id,
        'name': user.name,
        'sessions': []
    }
    return item

def create_session_item(session):
    item = {
        'id': session.id,
        'name': session.name,
        'images': "",
        'data': None,
        'datetime': session.datetime
    }
    return item

def create_user(name):
    return User(name)

def create_session(name):
    return Session(name)

def add_session_to_user(user_name, session):
    try:
        response = user_table.get_item(Key={'name': user_name})
        item = response.get('Item')
        sessions = item['sessions'] + [session]
        if item is None:
            print(f"No item found for id: {id}")
            return None
        response = user_table.update_item(  
            Key={'name': user_name},
            UpdateExpression='SET #sessions = :sessions_val',
            ExpressionAttributeNames={
                '#sessions': 'sessions'
            },
            ExpressionAttributeValues={
                ':sessions_val': sessions
            },
            ReturnValues='UPDATED_NEW'
        )
    except Exception as e:
        print(f"Error getting item: {e}")
        return None

def db_session_ids():
    try:
        response = user_table.scan()
        items = response.get('Items', [])
        while 'LastEvaluatedKey' in response:
            response = user_table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            items = response.get('Items', [])
        ids = [int(item['id']) for item in items]
        IDS = ids
    except Exception as e:
        print(f"Error scanning table: {e}")
