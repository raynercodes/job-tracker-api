def success_response(data=None, message="Success", meta=None, status=200):
    return {
        "success": True,
        "message": message,
        "data": data,
        "meta": meta or {}
    }, status

def error_response(message, meta=None, status=400):
    return {
        "success": False,
        "error": message,
        "data": None,
        "meta": meta or {}
    }, status
