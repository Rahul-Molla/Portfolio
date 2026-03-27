from django.test import TestCase
from django.urls import reverse

from .models import ContactMessage, Profile


class PortfolioViewTests(TestCase):
	def setUp(self):
		Profile.objects.create(
			full_name="Rahul Molla",
			headline="Full-Stack Django Developer",
			intro="Building robust web applications.",
			email="rahul@example.com",
		)

	def test_home_page_renders(self):
		response = self.client.get(reverse("home"))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "Rahul Molla")

	def test_contact_form_saves_message(self):
		response = self.client.post(
			reverse("home"),
			{
				"name": "Test User",
				"email": "test@example.com",
				"message": "I would like to collaborate.",
				"honeypot": "",
			},
		)
		self.assertEqual(response.status_code, 302)
		self.assertEqual(ContactMessage.objects.count(), 1)

	def test_robots_and_sitemap_routes(self):
		robots = self.client.get(reverse("robots_txt"))
		sitemap = self.client.get(reverse("sitemap_xml"))
		self.assertEqual(robots.status_code, 200)
		self.assertEqual(sitemap.status_code, 200)
		self.assertContains(sitemap, "<urlset", html=False)
