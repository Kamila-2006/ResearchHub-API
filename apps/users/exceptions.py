from rest_framework.exceptions import APIException

class TokenExpiredOrInvalid(APIException):
    status_code = 400
    default_detail = "Token is expired or invalid."
    default_code = "token_invalid"
