from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from lss import settings
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from . tokens import generate_token
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.contrib.auth.hashers import make_password


def home(request):
    # Check if the user is authenticated
    if request.session.get('is_authenticated', False):
        username = request.session.get('username')
        return render(request, "authentication/index.html", {'username': username})
    else:
        return render(request, "authentication/index.html")


def auth(request, form_type):
    # Check the form_type parameter
    if form_type == 'signup':
        return render(request, "authentication/auth.html", {'form_type': 'signup'})
    elif form_type == 'login':
        return render(request, "authentication/auth.html", {'form_type': 'login'})
    else:
        return render(request, "authentication/index.html")


def signup_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']

        # Check if the username already exists
        if User.objects.filter(username=username):
            messages.error(request, "Username already exist! Please try some other username.")
            return redirect('home')
        
        # Check if the email is already registered
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Registered!!")
            return redirect('home')
        
        # Check if the username is longer than 20 characters
        if len(username)>20:
            messages.error(request, "Username must be under 20 charcters!!")
            return redirect('home')
        
        # Check if the passwords match
        if password1 != password2:
            messages.error(request, "Passwords didn't matched!!")
            return redirect('home')
        
        # Check if the username is alphanumeric
        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric!!")
            return redirect('home')

        # If the passwords match create a new user
        if password1 == password2:
            myuser = User.objects.create_user(username, email, password1)
            myuser.is_active = False
            myuser.save()
            messages.success(request, "Your account has been successfully created. Please check your email to confirm your email address in order to activate your account.")
  
            # Email confirmation
            subject = "Welcome to Django Login!"
            message = "Hello " + myuser.username + "!\nThank you for visiting our website. We have also sent you a confirmation email, please confirm your email address."        
            from_email = settings.EMAIL_HOST_USER
            to_list = [myuser.email]
            send_mail(subject, message, from_email, to_list, fail_silently=True)
            
            # Confirmation Email address
            current_site = get_current_site(request)
            email_subject = "Confirm your Email - Django Login!"
            message2 = render_to_string('authentication/email_confirmation.html', {
                
                'name': myuser.username,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
                'token': generate_token.make_token(myuser)
            })
            email = EmailMessage(
                email_subject,
                message2,
                settings.EMAIL_HOST_USER,
                [myuser.email],
            )
            email.fail_silently = True
            email.send()

            return redirect('home')
        else:
            messages.error(request, "Passwords do not match.")
            return redirect('auth', form_type='signup')
    else:
        return render(request, "authentication/auth.html", {'form_type': 'signup'})


def login_view(request):
    # Get the username and password from the request
    if request.method == "POST":
        username = request.POST['user-login']
        password = request.POST['password']

        # Authenticate the user
        user = authenticate(username=username, password=password)

        # If the user is authenticated
        if user is not None:
            # Log in the user
            login(request, user)
            username = user.username
            request.session['is_authenticated'] = True
            request.session['username'] = username
            return redirect('home')
        else:
            # If authentication fails, display an error message and redirect to the home page
            messages.error(request, "Bad Credentials!")
            return redirect('home')
    
    # If the request method is not POST, render the login template
    return render(request, "authentication/auth.html", {'form_type': 'login'})


def signout(request):
    # Log out the user
    logout(request)

    messages.success(request, "Logged Out Successfully!")
    return redirect('home')


def forgot(request):
    if request.method == "POST":
        email = request.POST.get('pass-forgot')
        
        if email:
            try:
                user = User.objects.get(email=email)
                
                # Generate the unique URL for password reset
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                current_site = get_current_site(request)
                reset_url = reverse('change', kwargs={'uidb64': uid, 'token': token})
                reset_link = f'http://{current_site.domain}{reset_url}'
                
                mail_subject = 'Password Reset'
                # Render the email template with the reset link
                message = render_to_string('authentication/reset_password_email.html', {
                    'user': user,
                    'reset_link': reset_link,
                })

                # Send the password reset email to the user
                user.email_user(mail_subject, message)

                messages.success(request, "The password reset email has been sent successfully.")
                return redirect('home')

            except User.DoesNotExist:
                messages.error(request, "Sorry, the user with this email address is not registered.")
                return redirect('home')
        else:
            messages.error(request, "Please try to enter a valid email address next time.")
            return redirect('home')
    
    return render(request, "authentication/forgot.html")


def change(request, uidb64, token):
    try:
        # Decode the uid from the URL and retrieve the user
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
        if default_token_generator.check_token(user, token):
            if request.method == "POST":
                password1 = request.POST.get('password1')
                password2 = request.POST.get('password2')

                if password1 and password2 and password1 == password2:
                    # Set the new password for the user
                    user.password = make_password(password1)
                    user.save()
                    messages.success(request, f"Password changed successfully for user: {user.username}")
                    return redirect('home')
                else:
                    messages.error(request, "Passwords do not match or some fields are empty. Please try again.")
                    return redirect('home')
            else:
                return render(request, "authentication/change_password.html", {'user': user, 'uidb64': uidb64, 'token': token})
        else:
            messages.error(request, "The password reset link is no longer valid.")
            return redirect('home')
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        messages.error(request, "The password reset link is no longer valid.")
        return redirect('home')


def activate(request, uidb64, token):
    try:
        # Decode the uidb64 parameter to get the user ID
        uid = urlsafe_base64_decode(uidb64).decode()
        # Get the user with the corresponding ID
        myuser = User.objects.get(pk=uid)
    except (TypeError,ValueError,OverflowError,User.DoesNotExist):
        # Handle exceptions if the decoding or user retrieval fails
        myuser = None

    if myuser is not None and generate_token.check_token(myuser,token):
        # If the user exists and the token is valid
        myuser.is_active = True
        myuser.save() # Activate the user
        login(request,myuser) # Log in the user
        messages.success(request, "Your Account has been activated!")
        username = myuser.username
        return render(request, "authentication/index.html", {'username': username})
    else:
        # If the activation fails, render the activation failed template
        return render(request,'authentication/activation_failed.html')