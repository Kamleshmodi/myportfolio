from django.test import TestCase
from django.test.utils import override_settings
from django.urls import reverse

from .models import Project


@override_settings(SECURE_SSL_REDIRECT=False, SESSION_COOKIE_SECURE=False, CSRF_COOKIE_SECURE=False)
class PortfolioPagesTests(TestCase):
    def test_homepage_uses_resume_route_when_no_pdf_exists(self):
        response = self.client.get(reverse('home'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'href="/resume/"')
        self.assertContains(response, 'Open Resume')
        self.assertContains(response, 'Stock Market Analytics Dashboard')
        self.assertContains(response, 'Transport Services Hub')

    def test_resume_page_renders(self):
        response = self.client.get(reverse('resume'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Kamlesh Kumar Ghanchi')
        self.assertContains(response, 'Stock Market Analytics Dashboard')
        self.assertContains(response, 'Natural Fruity Bites')
        self.assertContains(response, 'Transport Services Hub')

    def test_admin_added_project_syncs_to_portfolio_and_resume(self):
        Project.objects.create(
            title='AI Interview Prep',
            image='portfolio_images/ai-interview.gif',
            summary='Practice platform for interview questions, instant feedback, and progress tracking.',
            stack='Django, APIs, Interview Workflows',
            badge='New Project',
            sort_order=15,
            github_link='https://github.com/Kamleshmodi/ai-interview-prep',
            live_link='https://example.com/ai-interview-prep',
        )

        home_response = self.client.get(reverse('home'))
        resume_response = self.client.get(reverse('resume'))

        self.assertContains(home_response, 'AI Interview Prep')
        self.assertContains(home_response, 'Practice platform for interview questions')
        self.assertContains(resume_response, 'AI Interview Prep')
        self.assertContains(resume_response, 'Django, APIs, Interview Workflows')
        self.assertContains(resume_response, 'https://example.com/ai-interview-prep')
