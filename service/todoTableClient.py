import boto3
import json
from datetime import datetime
from botocore.exceptions import ClientError

class TodoTableClient:
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table('TodoTable')

    def getAllTodos(self, filter_status=None, filter_priority=None):
        try:
            if filter_status:
                response = self.table.query(
                    IndexName='StatusIndex',
                    KeyConditionExpression='Status = :status',
                    ExpressionAttributeValues={
                        ':status': filter_status
                    }
                )
                items = response['Items']
            elif filter_priority:
                response = self.table.query(
                    IndexName='PriorityIndex',
                    KeyConditionExpression='Priority = :priority',
                    ExpressionAttributeValues={
                        ':priority': filter_priority
                    }
                )
                items = response['Items']
            else:
                response = self.table.scan()
                items = response['Items']

            return items
        except ClientError as e:
            print(f"Error getting todos: {e}")
            return []

    def getTodo(self, todo_id):
        try:
            response = self.table.get_item(
                Key={
                    'TodoId': todo_id
                }
            )
            return response['Item']
        except ClientError as e:
            print(f"Error getting todo {todo_id}: {e}")
            return None

    def completeTodo(self, todo_id):
        try:
            todo = self.getTodo(todo_id)
            if not todo:
                return {'error': 'Todo not found'}

            current_status = todo.get('Status', 'Not Started')
            new_status = 'Completed' if current_status != 'Completed' else 'In Progress'
            completed = new_status == 'Completed'

            response = self.table.update_item(
                Key={
                    'TodoId': todo_id
                },
                UpdateExpression='SET #status = :status, Completed = :completed, UpdatedAt = :updatedAt',
                ExpressionAttributeNames={
                    '#status': 'Status'
                },
                ExpressionAttributeValues={
                    ':status': new_status,
                    ':completed': completed,
                    ':updatedAt': datetime.now().strftime('%Y-%m-%d')
                },
                ReturnValues='ALL_NEW'
            )
            return response['Attributes']
        except ClientError as e:
            print(f"Error completing todo {todo_id}: {e}")
            return {'error': str(e)} 