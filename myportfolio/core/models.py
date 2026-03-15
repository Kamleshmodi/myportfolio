from django.db import models

# 1. Tumhari Profile aur Resume ke liye
class Profile(models.Model):
    name = models.CharField(max_length=100)
    about_text = models.TextField()
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)

    def __str__(self):
        return self.name

# 2. Tumhare Projects upload karne ke liye
class Project(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='portfolio_images/')
    summary = models.TextField(blank=True)
    stack = models.CharField(max_length=255, blank=True)
    badge = models.CharField(max_length=60, blank=True)
    sort_order = models.PositiveIntegerField(default=100)
    github_link = models.URLField(blank=True, null=True)
    live_link = models.URLField(blank=True, null=True)

    class Meta:
        ordering = ['sort_order', 'title']

    def __str__(self):
        return self.title

# 3. Website se aane wale Contact Messages ke liye
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    date_sent = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} - {self.subject}"
        
