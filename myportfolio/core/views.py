from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages  # New import for handling success/error alerts
from .models import Profile, Project
from .forms import ContactForm       # Import the secure form we just created

def home(request):
    if request.method == "POST":
        # Raw POST ki jagah hum secure ModelForm use kar rahe hain
        form = ContactForm(request.POST)
        
        if form.is_valid():
            # 1. Safely save validated data to the Database
            contact_msg = form.save()
            
            # 2. Prepare the email
            email_subject = f"Portfolio Contact: {contact_msg.subject} (from {contact_msg.name})"
            email_body = f"New message from your portfolio!\n\nName: {contact_msg.name}\nEmail: {contact_msg.email}\nSubject: {contact_msg.subject}\n\nMessage:\n{contact_msg.message}"
            
            # Sender email ko safe tareeqe se fetch karna (Error fix)
            sender_email = getattr(settings, 'EMAIL_HOST_USER', 'kamleshmodi7878@gmail.com')
            
            try:
                send_mail(
                    email_subject,
                    email_body,
                    sender_email,                       # Securely handled sender email
                    ['kamleshmodi7878@gmail.com'],      # Recipient (You)
                    fail_silently=False,
                )
                messages.success(request, "Message sent successfully!")
            except Exception as e:
                print(f"Message not sent. Error: {e}")
                messages.error(request, "Database saved, but failed to send Email alert.")
            
            return redirect('home')
        else:
            messages.error(request, "Invalid form data. Please check your inputs.")

    # Normal Page Load (GET request)
    profile = Profile.objects.first() 
    projects = Project.objects.all()
    
    context = {
        'profile': profile,
        'projects': projects
    }
    return render(request, 'index.html', context)