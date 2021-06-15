from rest_framework.response import Response


def standard_response_format(code: int, body: dict, message: str = "") -> Response:
    """标准返回格式, code, body, msg"""

    return Response({"code": code, "body": body, "message": message})
