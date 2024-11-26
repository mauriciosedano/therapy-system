import boto3
from datetime import datetime, timedelta

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('AccessDelegation')

def delegate_access(master_id, apprentice_id, permission_type, expiry_days):
    expiry_date = (datetime.now() + timedelta(days=expiry_days)).strftime('%Y-%m-%d')
    table.put_item(
        Item={
            'DelegationID': f"{master_id}_{apprentice_id}_{permission_type}",
            'MasterID': master_id,
            'ApprenticeID': apprentice_id,
            'PermissionType': permission_type,
            'ExpiryDate': expiry_date,
        }
    )
    return f"Access granted to {apprentice_id} for {permission_type} until {expiry_date}."

