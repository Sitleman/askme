from prometheus_client import start_http_server, Counter
import random
import time


class RPSMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.counter = Counter('my_failures', 'Description of counter')
        start_http_server(9001)

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        self.counter.inc()  # Increment by 1

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
