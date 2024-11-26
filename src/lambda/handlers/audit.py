def log_action(user_id, action_type, details):
    table = dynamodb.Table('AuditLog')
    table.put_item(
        Item={
            'AuditID': f"{user_id}_{datetime.now().isoformat()}",
            'UserID': user_id,
            'ActionType': action_type,
            'Timestamp': datetime.now().isoformat(),
            'Details': details,
        }
    )
    return "Action logged successfully."

