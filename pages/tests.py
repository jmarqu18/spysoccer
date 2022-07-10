from django.test import SimpleTestCase
from django.urls import reverse, resolve

from .views import HomePageView, AboutPageView


class HomePageTest(SimpleTestCase):
    def setUp(self):
        url = reverse("home")
        self.response = self.client.get(url)

    def test_url_exist_at_correct_location(self):
        self.assertEqual(self.response.status_code, 200)

    def test_homepage_template(self):
        self.assertTemplateUsed(self.response, "home.html")

    def test_homepage_contains_correct_html(self):
        self.assertContains(self.response, "Landing Page")

    def test_homepage_does_not_contains_incorrect_html(self):
        self.assertNotContains(
            self.response, "Test de que no está en la página correcta."
        )

    def test_homepage_url_resolves_homepageview(self):
        view = resolve("/")
        self.assertEqual(view.func.__name__, HomePageView.as_view().__name__)


class AboutPageTest(SimpleTestCase):
    def setUp(self):
        url = reverse("about")
        self.response = self.client.get(url)

    def test_aboutpage_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_aboutpage_template(self):
        self.assertTemplateUsed(self.response, "about.html")

    def test_aboutpage_contains_correct_html(self):
        self.assertContains(self.response, "Información")

    def test_aboutpage_does_not_contains_incorrect_html(self):
        self.assertNotContains(
            self.response, "Test de que no está en la página correcta."
        )

    def test_aboutpage_url_resolves_aboutpageview(self):
        view = resolve("/")
        self.assertEqual(view.func.__name__, AboutPageView.as_view().__name__)
