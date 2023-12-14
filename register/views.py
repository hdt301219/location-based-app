'''''
from django.shortcuts import render, redirect
import json
from django.http import JsonResponse

times = 0
registration_success = False

def register(request):
    global times, registration_success
    print('Register Page Opened!')
    times += 1
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        password1 = request.POST.get('password1')
        
        json2 = open('user_data.json',)
        data = json.load(json2) 
        l1 = data['u_data'][0]
        emails = list(l1.keys())
        passwords = list(l1.values())
        json2.close() 
        print('Read data from JSON')
        
        if email in emails:
            print('The Username or Email ID is already taken, returning JSON response')
            
            # Return a JSON response with an error message
            return JsonResponse({'error': 'Sorry. The Username or Email ID is already taken.'})
        
        if password != password1:
            print('Passwords do not match, returning JSON response')
            
            # Return a JSON response with an error message
            return JsonResponse({'error': 'Sorry. The Passwords do not match.'})
        
        # Registration success logic
        emails.append(email)
        passwords.append(password)
        d4 = {emails[i]: passwords[i] for i in range(len(emails))}
        
        json_object = {'u_data': [d4]}
        with open('user_data.json', 'w') as file:
            json.dump(json_object, file, indent=4)
        
        times = 0
        registration_success = True
        print('Registered new user, redirecting to login page')
        
        # Redirect to the root URL (default login page) with a success message
        return redirect('login')  # Update with your actual login URL name
    
    # Render the register page template
    return render(request, 'res.html', {'error': ''})
'''

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
import json
from django.http import JsonResponse

times = 0
registration_success = False

def register(request):
    global times, registration_success
    print('Register Page Opened!')
    times += 1
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        password1 = request.POST.get('password1')
        
        # Read data from JSON
        with open('user_data.json') as json_file:
            data = json.load(json_file)
            l1 = data['u_data'][0]
            emails = list(l1.keys())
            passwords = list(l1.values())
        
        if email in emails:
            print('The Username or Email ID is already taken, returning JSON response')
            
            # Return a JSON response with an error message
            return JsonResponse({'error': 'Sorry. The Username or Email ID is already taken.'})
        
        if password != password1:
            print('Passwords do not match, returning JSON response')
            
            # Return a JSON response with an error message
            return JsonResponse({'error': 'Sorry. The Passwords do not match.'})
        
        # Registration success logic
        user = User.objects.create_user(username=email, email=email, password=password)
        customer = Customer.objects.create(user=user, name=email, email=email)

        # Update user_data.json with the new registration data
        emails.append(email)
        passwords.append(password)
        d4 = {emails[i]: passwords[i] for i in range(len(emails))}
        
        json_object = {'u_data': [d4]}
        with open('user_data.json', 'w') as file:
            json.dump(json_object, file, indent=4)

        times = 0
        registration_success = True
        print('Registered new user, redirecting to login page')
        
        # Redirect to the root URL (default login page) with a success message
        return redirect('login')  # Update with your actual login URL name
    
    # Render the register page template
    return render(request, 'res.html', {'error': ''})

