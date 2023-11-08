# pylint: disable=missing-function-docstring
from core.constants import ApiResponseCode


def response(code, message, data=None):
    return {"code": code, "message": message, "data": data}


def success(data=None, message="success"):
    return response(ApiResponseCode.SUCCESS, message, data)


def fail(message, code=ApiResponseCode.SYSTEM_ERROR):
    return response(code, message)

