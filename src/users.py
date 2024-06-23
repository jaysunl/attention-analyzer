import boto3

REGION='us-west-1'

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

class User:
    current_id = 0
    def __init__(self, name):
        self.id = User.current_id
        User.current_id += 1
        self.name = name
        self.sessions = []

class Session:
    current_id = 0
    def __init__(self, name):
        self.id = Session.current_id
        Session.current_id += 1
        self.name = name
        self.images = None
        self.data = None

def add_user(user_item):
    try:
        response = user_table.put_item(Item=user_item)
        print("Item added successfully:")
        print(response)
    except Exception as e:
        print(f"Error adding item: {e}")

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
        'data': None
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

def add_session(session_name):
    session = create_session(session_name)
    session_item = create_session_item(session)
    try:
        response = user_table.put_item(Item=session_item)
        print("Item added successfully:")
        print(response)
    except Exception as e:
        print(f"Error adding item: {e}")