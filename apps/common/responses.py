from rest_framework import status as rest_status
from rest_framework.response import Response


class APIResponse:

    def __init__(self, status, code, message, extra_fields=None, errors=None):
        self.status = status
        self.code = code
        self.message = message
        self.extra_fields = extra_fields
        self.errors = errors

    @property
    def json(self):
        fields = {
            "status": self.status,
            "code": self.code,
            "message": self.message
        }
        if self.extra_fields:
            fields.update(self.extra_fields)
        if self.errors:
            fields["errors"] = self.errors
        return Response(data=fields, status=rest_status.HTTP_200_OK)


def exception_handler(exc, context):
    response = APIResponse(status='FAILED', message='Internal Server Error', code=500,
                           extra_fields={"message": str(exc)})
    return response.json
