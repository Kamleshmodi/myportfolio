from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages  # New import for handling success/error alerts
from django.templatetags.static import static
from django.urls import reverse
from .models import Profile, Project
from .forms import ContactForm       # Import the secure form we just created

def build_portfolio_projects(stored_projects):
    curated_projects = [
        {
            'title': 'Stock Market Analytics Dashboard',
            'image_url': static('img/port7.jpg'),
            'description': 'A stock market web app focused on market snapshots, trend tracking, and clean data-driven analysis for quick decision-making.',
            'tag': 'Latest Project',
            'stack': 'Market Data, Dashboard UI, Trend Analysis',
            'github_link': 'https://www.github.com/Kamleshmodi',
            'live_link': 'https://stock-tracker-dashboard.onrender.com/',
            'sort_order': 10,
        },
        {
            'title': 'VASU Store (Django)',
            'image_url': static('img/port1.jpg'),
            'description': 'Full-featured e-commerce platform with variations, cart, and admin panel using Django MVT.',
            'tag': 'Django',
            'stack': 'Django, Cart Flow, Admin Panel',
            'github_link': 'https://www.github.com/Kamleshmodi',
            'live_link': '',
            'sort_order': 20,
        },
        {
            'title': 'Student Record System',
            'image_url': static('img/port2.jpg'),
            'description': 'Multi-role Laravel dashboard for Admin, Teacher, and Student workflows with full CRUD operations.',
            'tag': 'Laravel',
            'stack': 'Laravel, Multi-role Auth, CRUD',
            'github_link': 'https://www.github.com/Kamleshmodi',
            'live_link': '',
            'sort_order': 30,
        },
        {
            'title': 'Natural Fruity Bites',
            'image_url': static('img/port6.jpg'),
            'description': 'A responsive e-commerce showcase platform for organic and natural fruit-based healthy treats.',
            'tag': 'Live Project',
            'stack': 'Responsive Design, Product Showcase',
            'github_link': '',
            'live_link': 'https://kamleshmodi-naturalfruitybite-official.onrender.com/',
            'sort_order': 40,
        },
        {
            'title': 'QuizHunt',
            'image_url': static('img/port3.jpg'),
            'description': 'Dynamic quiz application for IT professionals to test knowledge and track learning progress.',
            'tag': 'Interactive App',
            'stack': 'Quiz Logic, Dynamic Flow, UX',
            'github_link': 'https://www.github.com/Kamleshmodi',
            'live_link': '',
            'sort_order': 50,
        },
        {
            'title': 'Make in India Portal',
            'image_url': static('img/port4.jpg'),
            'description': 'Informative web platform highlighting core sectors driving domestic manufacturing.',
            'tag': 'Informational Site',
            'stack': 'Content Design, Responsive Pages',
            'github_link': 'https://www.github.com/Kamleshmodi',
            'live_link': '',
            'sort_order': 60,
        },
        {
            'title': 'Transport Services Hub',
            'image_url': static('img/port5.jpg'),
            'description': 'Explores logistics and operational functionalities of five major transportation services.',
            'tag': 'Web Project',
            'stack': 'Research, UI Layout, Service Mapping',
            'github_link': 'https://www.github.com/Kamleshmodi',
            'live_link': '',
            'sort_order': 70,
        },
    ]

    portfolio_projects = {
        project['title'].strip().lower(): project
        for project in curated_projects
    }

    for project in stored_projects:
        normalized_title = project.title.strip().lower()
        existing = portfolio_projects.get(normalized_title, {})

        portfolio_projects[normalized_title] = {
            'title': project.title,
            'image_url': project.image.url if getattr(project, 'image', None) else existing.get('image_url', static('img/port7.jpg')),
            'description': project.summary.strip() if project.summary else existing.get('description', 'Custom portfolio project added from the admin panel.'),
            'tag': project.badge.strip() if project.badge else existing.get('tag', 'Admin Project'),
            'stack': project.stack.strip() if project.stack else existing.get('stack', 'Custom Portfolio Entry'),
            'github_link': project.github_link or existing.get('github_link', ''),
            'live_link': project.live_link or existing.get('live_link', ''),
            'sort_order': project.sort_order if project.sort_order is not None else existing.get('sort_order', 100),
        }

    return sorted(
        portfolio_projects.values(),
        key=lambda project: (project.get('sort_order', 100), project['title'].lower())
    )

def build_shared_context():
    profile = Profile.objects.first()
    stored_projects = list(Project.objects.all())
    portfolio_projects = build_portfolio_projects(stored_projects)
    has_resume_file = bool(profile and profile.resume)

    return {
        'profile': profile,
        'projects': stored_projects,
        'portfolio_projects': portfolio_projects,
        'project_count': len(portfolio_projects),
        'has_resume_file': has_resume_file,
        'resume_url': profile.resume.url if has_resume_file else reverse('resume'),
    }

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
    return render(request, 'index.html', build_shared_context())

def resume_page(request):
    return render(request, 'resume.html', build_shared_context())
