# login/views.py

from django.shortcuts import render, redirect
import json

times = 0

def login(request):
    global times
    print('Login Page Opened!')
    times += 1
    
    # Check if the register link is clicked
    if request.path == '/login/register/':
        return redirect('register')  # Assuming 'register' is the URL name for your register page
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Read data from JSON
        with open('user_data.json') as json_file:
            data = json.load(json_file)
            l1 = data['u_data'][0]
            emails = list(l1.keys())
            passwords = list(l1.values())
        
        if email in emails and passwords[emails.index(email)] == password:
            times = 0
            print('Logged in User, redirecting to find_shops/')
            return redirect('home')  # Assuming 'find_shops' is the URL name for your find_shops page
        
        print('Authentication failed, returning HTTP response')
        return render(request, 'login.html', {'loc': 'login/', 'errorclass': 'alert alert-danger', 'error': 'Sorry. The Email and Password do not match.'})
    
    # Handle GET requests separately (if needed)
    return render(request, 'login.html', {'loc': 'login/', 'error': ''})
