# This file contains the business logic for test APIs

def process_get_test():
    """Logic for GET test API"""
    return {'status': 'success', 'message': 'API is working!'}


def process_get_test_abc():
    """Logic for GET test API"""
    return {'status': 'success', 'message': 'Test- ABC ......API is working!'}


def process_post_test(data):
    """Logic for POST test API"""
    if not data:
        return {'status': 'error', 'message': 'No JSON data provided'}, 400
    
    # Here you can add more business logic (DB, validation, etc.)
    print("Processing POST data:", data)
    
    return {
        'status': 'success',
        'message': 'POST API is working!',
        'received_data': data
    }
