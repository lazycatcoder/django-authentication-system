from django.shortcuts import redirect


class RestrictAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the user is authenticated
        if request.user.is_authenticated:
            restricted_urls = [
                '/auth/login/',
                '/auth/signup/',
                '/auth/login/forgot/',
            ]
            # If the authenticated user tries to access restricted URLs, redirect them to the home page
            if request.path in restricted_urls:
                return redirect('home')

        response = self.get_response(request)
        return response
    

class ClearFieldsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Clear form data and cookies if the request is for the signup page with a GET method
        if request.path == '/auth/signup/' and request.method == 'GET':
            request.session['signup_form_data'] = {}
            response = self.get_response(request)
            response['Cache-Control'] = 'no-store, must-revalidate'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'
            response.delete_cookie('password1')
            response.delete_cookie('password2')
            return response

        return self.get_response(request)