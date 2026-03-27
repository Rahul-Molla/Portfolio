from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.staticfiles import finders
from django.templatetags.static import static
from django.urls import reverse

from .forms import ContactForm
from .models import (
	AboutSection,
	Achievement,
	Certification,
	EducationEntry,
	FocusArea,
	ImpactStat,
	Profile,
	Project,
	SiteSettings,
	SkillCategory,
)


def home(request):
	default_profile_photo = "https://media.licdn.com/dms/image/v2/D5603AQFRB4ETmji78g/profile-displayphoto-crop_800_800/B56ZwxDh3iGsAI-/0/1770349536442?e=1776297600&v=beta&t=M4g5G0wPHKt5yHLg_qc32HwoVxHkz_tY8RoTdLVBAPg"

	profile = Profile.objects.first()
	projects = Project.objects.filter(featured=True)
	site_settings = SiteSettings.objects.first()
	about_section = AboutSection.objects.first()
	skill_categories = SkillCategory.objects.all()
	education_entries = EducationEntry.objects.all()
	achievement_entries = Achievement.objects.all()
	certification_entries = Certification.objects.all()
	stats_entries = ImpactStat.objects.all()
	focus_entries = FocusArea.objects.all()

	if request.method == "POST":
		contact_form = ContactForm(request.POST)
		if contact_form.is_valid():
			contact_form.save()
			return redirect(f"{reverse('home')}?contact=success#contact")
	else:
		contact_form = ContactForm()

	default_profile = {
		"full_name": "Rahul Molla",
		"headline": "MCA Student | Full-Stack Django Developer",
		"intro": "MCA student at Jadavpur University with strong programming skills in Python, C, C++, Java, and JavaScript. Experienced in building web applications, authentication systems, and responsive websites.",
		"email": "rahulmolla9339@gmail.com",
		"phone": "9339097544",
		"location": "West Bengal, India",
		"photo_url": default_profile_photo,
		"resume_url": "",
		"github_url": "https://github.com/Rahul-Molla",
		"linkedin_url": "https://www.linkedin.com/in/rahul-molla/",
		"portfolio_url": "#",
	}

	default_site_settings = {
		"site_title": "Rahul Molla | Portfolio",
		"seo_description": "Portfolio of Rahul Molla, MCA student and Django developer building modern, scalable web applications.",
		"seo_keywords": "Rahul Molla, Django developer, portfolio, Python, full-stack",
		"og_image_url": "",
		"twitter_handle": "",
		"analytics_domain": "",
		"robots_allow_indexing": True,
	}

	default_about = {
		"title": "Professional Summary",
		"summary": "MCA student at Jadavpur University with strong programming skills in Python, C, C++, Java, and JavaScript. Experienced in building web applications, authentication systems, and responsive websites.",
	}

	default_skill_groups = [
		{
			"title": "Languages",
			"items": "Python, C, C++, Java, JavaScript, HTML, CSS",
		},
		{
			"title": "Frameworks & Technologies",
			"items": "Django, CCNA, AWS",
		},
		{
			"title": "Databases",
			"items": "SQL",
		},
		{
			"title": "Tools & Platforms",
			"items": "Git, GitHub, Visual Studio Code",
		},
	]

	default_projects = [
		{
			"title": "Online Testing System",
			"summary": "Developed a web-based exam platform with user authentication, question management, and result generation. Implemented CRUD operations and secure session handling using Django, with support for multiple concurrent users.",
			"tech_stack": "Django, Python, SQLite, HTML, CSS",
			"outcome": "Reduced manual evaluation effort and improved result publishing speed for test workflows.",
			"screenshot_url": "",
			"live_url": "",
			"source_url": "",
		},
		{
			"title": "E-Commerce Website",
			"summary": "Built a full-stack Django e-commerce prototype with product images, authentication, cart and checkout flow, order tracking, and admin tools for bulk operations including delivery scheduling and tracking number assignments.",
			"tech_stack": "Django, Python, SQLite, JavaScript, HTML, CSS",
			"outcome": "Improved order processing visibility with admin workflow automation and delivery tracking updates.",
			"screenshot_url": "",
			"live_url": "",
			"source_url": "",
		},
	]

	default_education = [
		{
			"degree": "Master of Computer Application (MCA)",
			"institution": "Jadavpur University",
			"score": "7.76 (1st, 2nd & 3rd Semester)",
			"duration": "2024 - 2026",
		},
		{
			"degree": "Bachelor of Computer Application (BCA)",
			"institution": "Midnapore College (Autonomous)",
			"score": "80.45%",
			"duration": "2021 - 2024",
		},
		{
			"degree": "Secondary School",
			"institution": "Raghunathpur Sat-Sanga Vidyapith",
			"score": "64.71",
			"duration": "2019",
		},
		{
			"degree": "Higher Secondary",
			"institution": "Vidyasagar Vidyapith",
			"score": "84%",
			"duration": "2019 - 2021",
		},
	]

	default_achievements = [
		"UGC NET Qualified",
		"WB SET Qualified",
	]

	default_certifications = [
		"C & C++ Programming | IIHT | 2022",
		"Python Programming | IIHT | 2022",
		"CCNA (Networking & Security) | IIHT | 2023",
		"AWS (Cloud Computing & Deployment) | IIHT | 2023",
	]

	default_impact_stats = [
		{"label": "Projects Built", "value": 8, "suffix": "+"},
		{"label": "Certifications", "value": 4, "suffix": ""},
		{"label": "Core Languages", "value": 7, "suffix": ""},
		{"label": "Current GPA", "value": 7.76, "suffix": ""},
	]

	default_focus_areas = [
		{
			"title": "Backend Development",
			"detail": "Designing secure and scalable web applications with Django, authentication systems, and clean database modeling.",
		},
		{
			"title": "Problem Solving",
			"detail": "Strong DSA and coding practice background through competitive problem solving and interview-style challenges.",
		},
		{
			"title": "Cloud & Networking",
			"detail": "Hands-on foundations in AWS cloud workflows and CCNA concepts for deployment-ready applications.",
		},
	]

	profile_image_url = ""
	if profile and profile.photo_url:
		profile_image_url = profile.photo_url
	elif default_profile_photo:
		profile_image_url = default_profile_photo
	elif finders.find("images/profile.jpg"):
		profile_image_url = static("images/profile.jpg")
	else:
		profile_image_url = static("images/profile-placeholder.svg")

	if profile:
		github_url = profile.github_url or default_profile["github_url"]
		linkedin_url = profile.linkedin_url or default_profile["linkedin_url"]
	else:
		github_url = default_profile["github_url"]
		linkedin_url = default_profile["linkedin_url"]

	phone_for_whatsapp = (profile.phone if profile and profile.phone else default_profile["phone"])
	whatsapp_digits = "".join(ch for ch in phone_for_whatsapp if ch.isdigit())
	if len(whatsapp_digits) == 10:
		whatsapp_digits = f"91{whatsapp_digits}"
	whatsapp_url = f"https://wa.me/{whatsapp_digits}" if whatsapp_digits else f"mailto:{(profile.email if profile else default_profile['email'])}"

	skill_groups = [
		{"title": category.title, "items": category.items}
		for category in skill_categories
	]

	education = list(education_entries) if education_entries.exists() else default_education
	achievements = [item.text for item in achievement_entries] if achievement_entries.exists() else default_achievements
	certifications = [item.text for item in certification_entries] if certification_entries.exists() else default_certifications
	impact_stats = list(stats_entries) if stats_entries.exists() else default_impact_stats
	focus_areas = list(focus_entries) if focus_entries.exists() else default_focus_areas

	context = {
		"profile": profile or default_profile,
		"site_settings": site_settings or default_site_settings,
		"about": about_section or default_about,
		"skill_groups": skill_groups if skill_groups else default_skill_groups,
		"projects": projects if projects.exists() else default_projects,
		"education": education,
		"achievements": achievements,
		"certifications": certifications,
		"impact_stats": impact_stats,
		"focus_areas": focus_areas,
		"contact_form": contact_form,
		"contact_success": request.GET.get("contact") == "success",
		"profile_image_url": profile_image_url,
		"github_url": github_url,
		"linkedin_url": linkedin_url,
		"whatsapp_url": whatsapp_url,
	}
	return render(request, "portfolio/home.html", context)


def robots_txt(request):
	site_settings = SiteSettings.objects.first()
	allow_index = site_settings.robots_allow_indexing if site_settings else True
	content = [
		"User-agent: *",
		f"Disallow: {'/' if not allow_index else ''}",
		f"Sitemap: {request.build_absolute_uri(reverse('sitemap_xml'))}",
	]
	return HttpResponse("\n".join(content), content_type="text/plain")


def sitemap_xml(request):
	urls = [
		request.build_absolute_uri(reverse("home")),
	]
	xml_items = "".join([f"<url><loc>{url}</loc></url>" for url in urls])
	xml = f"<?xml version='1.0' encoding='UTF-8'?><urlset xmlns='http://www.sitemaps.org/schemas/sitemap/0.9'>{xml_items}</urlset>"
	return HttpResponse(xml, content_type="application/xml")
