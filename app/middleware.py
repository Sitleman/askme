from prometheus_client import start_http_server, Summary
import random
import time

REQUEST_TIME = Summary('request', '')

class RPSMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        start_http_server(9001)

    @REQUEST_TIME.time()
    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
