from django.http import HttpResponseRedirect


class RedirectMiddleware:
    @staticmethod
    def process_response(self, request, response):
        if isinstance(response, HttpResponseRedirect):
            if response.url.startswith('/'):
                response['Location'] = 'http://cauliflower/blast' + response.url
        return response