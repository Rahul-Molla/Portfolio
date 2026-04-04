from django.http import HttpResponse
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.db.models import Count
from django.contrib.staticfiles import finders
from django.templatetags.static import static
from django.urls import reverse
from urllib.parse import urlencode
from django.utils.safestring import mark_safe

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
	UGCNetPYQ,
)


PAPER_CATALOG = [
	{
		"value": "paper-1",
		"label": "Paper 1",
		"subtitle": "General Paper on Teaching and Research Aptitude",
		"description": "Choose a Paper 1 unit to practice concept-focused PYQs and topic-wise questions.",
		"subjects": [
			{"title": "Teaching Aptitude", "icon": "TA", "tone": "tone-teaching", "description": "Learner characteristics, methods, and evaluation."},
			{"title": "Reading Comprehension", "icon": "RC", "tone": "tone-reading", "description": "Passages, inference, and interpretation."},
			{"title": "Communication", "icon": "CM", "tone": "tone-communication", "description": "Verbal, non-verbal, barriers, and mass media."},
			{"title": "Mathematical Reasoning and Aptitude", "icon": "MR", "tone": "tone-math", "description": "Series, codes, relations, and number patterns."},
			{"title": "Logical Reasoning", "icon": "LR", "tone": "tone-logic", "description": "Syllogisms, analogies, and argument forms."},
			{"title": "Data Interpretation", "icon": "DI", "tone": "tone-data", "description": "Tables, charts, and graphical analysis."},
			{"title": "Information and Communication Technology", "icon": "ICT", "tone": "tone-ict", "description": "Terminology, email, digital initiatives, and tools."},
			{"title": "People, Development and Environment", "icon": "PDE", "tone": "tone-environment", "description": "Development goals, pollution, and natural hazards."},
		],
	},
	{
		"value": "paper-2",
		"label": "Paper 2",
		"subtitle": "Computer Science and Applications",
		"description": "Choose a Computer Science unit to open PYQs with subject-specific practice questions.",
		"subjects": [
			{"title": "Discrete Structures and Optimization", "icon": "DS", "tone": "tone-discrete", "description": "Logic, set theory, and graph theory."},
			{"title": "Computer System Architecture", "icon": "CSA", "tone": "tone-architecture", "description": "Digital logic, data representation, and CPU design."},
			{"title": "Programming Languages & Graphics", "icon": "PLG", "tone": "tone-programming", "description": "C++, Java, OOP, and transformations."},
			{"title": "Database Management Systems", "icon": "DBMS", "tone": "tone-dbms", "description": "SQL, ER models, normalization, and transactions."},
			{"title": "System Software and Operating System", "icon": "OS", "tone": "tone-os", "description": "Processes, memory, assemblers, and compilers."},
			{"title": "Software Engineering", "icon": "SE", "tone": "tone-software", "description": "SDLC, testing, project management, and CASE tools."},
			{"title": "Data Structures and Algorithms", "icon": "DSA", "tone": "tone-dsa", "description": "Search, sort, complexity, and data structures."},
			{"title": "Theory of Computation and Compilers", "icon": "TOC", "tone": "tone-toc", "description": "DFA, NFA, parsing, and Turing machines."},
			{"title": "Data Communication and Computer Networks", "icon": "CN", "tone": "tone-network", "description": "OSI, TCP/IP, security, and protocols."},
			{"title": "Artificial Intelligence", "icon": "AI", "tone": "tone-ai", "description": "Knowledge representation, search, and fuzzy logic."},
		],
	},
]


def _get_paper_catalog(value):
	for paper in PAPER_CATALOG:
		if paper["value"] == value:
			return paper
	return PAPER_CATALOG[0]


def _subject_icon_svg(icon_key):
	icons = {
		"TA": "<svg viewBox='0 0 64 64' aria-hidden='true' focusable='false'><rect x='14' y='13' width='36' height='38' rx='6' fill='none' stroke='currentColor' stroke-width='3'/><path d='M19 24h26M19 31h26M19 38h16' stroke='currentColor' stroke-width='3' stroke-linecap='round'/><path d='M23 49l-5 6' stroke='currentColor' stroke-width='3' stroke-linecap='round'/><path d='M28 49l-2 6' stroke='currentColor' stroke-width='3' stroke-linecap='round'/></svg>",
		"RA": "<svg viewBox='0 0 64 64' aria-hidden='true' focusable='false'><path d='M26 38a12 12 0 1 1 8.5 3.5L45 52' fill='none' stroke='currentColor' stroke-width='3' stroke-linecap='round'/><circle cx='26' cy='26' r='8' fill='none' stroke='currentColor' stroke-width='3'/><path d='M22 26h8M26 22v8' stroke='currentColor' stroke-width='3' stroke-linecap='round'/></svg>",
		"RC": "<svg viewBox='0 0 64 64' aria-hidden='true' focusable='false'><path d='M14 18h18a6 6 0 0 1 6 6v26a4 4 0 0 0-4-4H14z' fill='none' stroke='currentColor' stroke-width='3' stroke-linejoin='round'/><path d='M50 18H32a6 6 0 0 0-6 6v26a4 4 0 0 1 4-4h20z' fill='none' stroke='currentColor' stroke-width='3' stroke-linejoin='round'/><path d='M24 27h-6M24 33h-6M24 39h-4M40 27h10M40 33h10M40 39h8' stroke='currentColor' stroke-width='3' stroke-linecap='round'/></svg>",
		"CM": "<svg viewBox='0 0 64 64' aria-hidden='true' focusable='false'><path d='M12 18h30a6 6 0 0 1 6 6v15a6 6 0 0 1-6 6H28l-10 8v-8h-6a6 6 0 0 1-6-6V24a6 6 0 0 1 6-6Z' fill='none' stroke='currentColor' stroke-width='3' stroke-linejoin='round'/><path d='M37 22h15a6 6 0 0 1 6 6v12a6 6 0 0 1-6 6h-4v6l-7-6' fill='none' stroke='currentColor' stroke-width='3' stroke-linejoin='round'/></svg>",
		"MR": "<svg viewBox='0 0 64 64' aria-hidden='true' focusable='false'><rect x='15' y='12' width='34' height='40' rx='5' fill='none' stroke='currentColor' stroke-width='3'/><path d='M22 21h20M22 29h6M32 29h6M22 37h6M32 37h6M22 45h10' stroke='currentColor' stroke-width='3' stroke-linecap='round'/></svg>",
		"LR": "<svg viewBox='0 0 64 64' aria-hidden='true' focusable='false'><circle cx='18' cy='20' r='4' fill='currentColor'/><circle cx='46' cy='20' r='4' fill='currentColor'/><circle cx='32' cy='44' r='4' fill='currentColor'/><path d='M22 20h20M20 23l9 16M44 23l-9 16' fill='none' stroke='currentColor' stroke-width='3' stroke-linecap='round'/></svg>",
		"DI": "<svg viewBox='0 0 64 64' aria-hidden='true' focusable='false'><path d='M14 50h36' stroke='currentColor' stroke-width='3' stroke-linecap='round'/><path d='M18 42V30M28 42V22M38 42V14M48 42V26' stroke='currentColor' stroke-width='5' stroke-linecap='round'/></svg>",
		"ICT": "<svg viewBox='0 0 64 64' aria-hidden='true' focusable='false'><rect x='14' y='16' width='36' height='22' rx='5' fill='none' stroke='currentColor' stroke-width='3'/><path d='M25 48h14M22 44h20M32 38v6' stroke='currentColor' stroke-width='3' stroke-linecap='round'/><path d='M20 23c3-3 7-5 12-5s9 2 12 5M24 28c2-2 4-3 8-3s6 1 8 3' fill='none' stroke='currentColor' stroke-width='3' stroke-linecap='round'/></svg>",
		"PDE": "<svg viewBox='0 0 64 64' aria-hidden='true' focusable='false'><circle cx='30' cy='26' r='8' fill='none' stroke='currentColor' stroke-width='3'/><path d='M14 49c4-9 10-13 16-13s12 4 16 13' fill='none' stroke='currentColor' stroke-width='3' stroke-linecap='round'/><path d='M41 16c2 2 3 4 3 7' fill='none' stroke='currentColor' stroke-width='3' stroke-linecap='round'/></svg>",
		"HES": "<svg viewBox='0 0 64 64' aria-hidden='true' focusable='false'><path d='M12 28 32 14l20 14' fill='none' stroke='currentColor' stroke-width='3' stroke-linejoin='round'/><path d='M18 28v18M28 28v18M36 28v18M46 28v18' stroke='currentColor' stroke-width='3' stroke-linecap='round'/><path d='M10 50h44' stroke='currentColor' stroke-width='3' stroke-linecap='round'/></svg>",
		"DS": "<svg viewBox='0 0 64 64' aria-hidden='true' focusable='false'><circle cx='18' cy='20' r='4' fill='currentColor'/><circle cx='46' cy='20' r='4' fill='currentColor'/><circle cx='32' cy='44' r='4' fill='currentColor'/><path d='M22 20h20M20 23l9 16M44 23l-9 16' fill='none' stroke='currentColor' stroke-width='3' stroke-linecap='round'/></svg>",
		"CSA": "<svg viewBox='0 0 64 64' aria-hidden='true' focusable='false'><rect x='18' y='14' width='28' height='36' rx='4' fill='none' stroke='currentColor' stroke-width='3'/><path d='M24 22h16M24 30h16M24 38h16' stroke='currentColor' stroke-width='3' stroke-linecap='round'/><path d='M26 50h12' stroke='currentColor' stroke-width='3' stroke-linecap='round'/></svg>",
		"PLG": "<svg viewBox='0 0 64 64' aria-hidden='true' focusable='false'><path d='M24 20 14 32l10 12' fill='none' stroke='currentColor' stroke-width='3' stroke-linecap='round' stroke-linejoin='round'/><path d='M40 20l10 12-10 12' fill='none' stroke='currentColor' stroke-width='3' stroke-linecap='round' stroke-linejoin='round'/><path d='M31 16 27 48' stroke='currentColor' stroke-width='3' stroke-linecap='round'/></svg>",
		"DBMS": "<svg viewBox='0 0 64 64' aria-hidden='true' focusable='false'><ellipse cx='32' cy='16' rx='16' ry='6' fill='none' stroke='currentColor' stroke-width='3'/><path d='M16 16v26c0 3 7 6 16 6s16-3 16-6V16' fill='none' stroke='currentColor' stroke-width='3'/><path d='M16 29c0 3 7 6 16 6s16-3 16-6M16 42c0 3 7 6 16 6s16-3 16-6' fill='none' stroke='currentColor' stroke-width='3'/></svg>",
		"OS": "<svg viewBox='0 0 64 64' aria-hidden='true' focusable='false'><circle cx='32' cy='32' r='9' fill='none' stroke='currentColor' stroke-width='3'/><path d='M32 12v7M32 45v7M12 32h7M45 32h7M19 19l5 5M40 40l5 5M45 19l-5 5M19 45l5-5' stroke='currentColor' stroke-width='3' stroke-linecap='round'/></svg>",
		"SE": "<svg viewBox='0 0 64 64' aria-hidden='true' focusable='false'><path d='M16 18h32M16 28h32M16 38h20M16 48h12' stroke='currentColor' stroke-width='3' stroke-linecap='round'/><path d='M46 18l4 4-10 10h-4v-4Z' fill='none' stroke='currentColor' stroke-width='3' stroke-linejoin='round'/></svg>",
		"DSA": "<svg viewBox='0 0 64 64' aria-hidden='true' focusable='false'><rect x='14' y='16' width='14' height='10' rx='2' fill='none' stroke='currentColor' stroke-width='3'/><rect x='35' y='16' width='14' height='10' rx='2' fill='none' stroke='currentColor' stroke-width='3'/><rect x='24' y='38' width='14' height='10' rx='2' fill='none' stroke='currentColor' stroke-width='3'/><path d='M21 26v6h22v6' stroke='currentColor' stroke-width='3' stroke-linecap='round'/></svg>",
		"TOC": "<svg viewBox='0 0 64 64' aria-hidden='true' focusable='false'><circle cx='18' cy='20' r='4' fill='currentColor'/><circle cx='32' cy='20' r='4' fill='currentColor'/><circle cx='46' cy='20' r='4' fill='currentColor'/><path d='M18 24v8M32 24v8M46 24v8M18 32h28M18 40h14M32 32v8' stroke='currentColor' stroke-width='3' stroke-linecap='round'/></svg>",
		"CN": "<svg viewBox='0 0 64 64' aria-hidden='true' focusable='false'><path d='M16 42h32M22 42c0-8 5-14 10-14s10 6 10 14' fill='none' stroke='currentColor' stroke-width='3' stroke-linecap='round'/><path d='M22 24h20M20 30h24' stroke='currentColor' stroke-width='3' stroke-linecap='round'/></svg>",
		"AI": "<svg viewBox='0 0 64 64' aria-hidden='true' focusable='false'><rect x='20' y='20' width='24' height='24' rx='6' fill='none' stroke='currentColor' stroke-width='3'/><circle cx='28' cy='28' r='2.5' fill='currentColor'/><circle cx='36' cy='28' r='2.5' fill='currentColor'/><path d='M26 38c2 2 10 2 12 0' stroke='currentColor' stroke-width='3' stroke-linecap='round'/></svg>",
	}
	icon = icons.get(icon_key, icons["TA"])
	return mark_safe(icon)


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
		request.build_absolute_uri(reverse("ugc_net_pyq")),
	]
	xml_items = "".join([f"<url><loc>{url}</loc></url>" for url in urls])
	xml = f"<?xml version='1.0' encoding='UTF-8'?><urlset xmlns='http://www.sitemaps.org/schemas/sitemap/0.9'>{xml_items}</urlset>"
	return HttpResponse(xml, content_type="application/xml")


def ugc_net_pyq(request):
	site_settings = SiteSettings.objects.first()
	default_site_settings = {
		"site_title": "Rahul Molla | UGC NET PYQ",
		"seo_description": "UGC NET Previous Year Questions for Paper 1 and Paper 2 Computer Science and Applications.",
		"seo_keywords": "UGC NET, PYQ, Paper 1, Paper 2, Computer Science",
		"og_image_url": "",
		"twitter_handle": "",
		"analytics_domain": "",
		"robots_allow_indexing": True,
	}

	papers = PAPER_CATALOG
	valid_paper_values = {item["value"] for item in papers}

	selected_paper = request.GET.get("paper", "paper-1")
	if selected_paper not in valid_paper_values:
		selected_paper = "paper-1"
	selected_paper_data = _get_paper_catalog(selected_paper)
	selected_paper_label = selected_paper_data["label"]

	selected_subject = request.GET.get("subject", "").strip()
	selected_year = request.GET.get("year", "").strip()
	if selected_year and not selected_year.isdigit():
		selected_year = ""

	all_questions = UGCNetPYQ.objects.filter(is_active=True)
	base_filtered_questions = all_questions.filter(paper=selected_paper)
	if selected_subject:
		base_filtered_questions = base_filtered_questions.filter(subject=selected_subject)

	valid_subject_titles = {item["title"] for item in selected_paper_data["subjects"]}
	if selected_subject and selected_subject not in valid_subject_titles:
		selected_subject = ""
		base_filtered_questions = all_questions.filter(paper=selected_paper)

	available_subjects = list(
		all_questions.filter(paper=selected_paper)
		.values_list("subject", flat=True)
		.distinct()
		.order_by("subject")
	)
	available_years = list(
		base_filtered_questions.values_list("year", flat=True)
		.distinct()
		.order_by("-year")
	)

	filtered_questions = base_filtered_questions
	if selected_year:
		filtered_questions = filtered_questions.filter(year=int(selected_year))

	questions = list(filtered_questions)
	question_count_map = {}
	for row in all_questions.filter(paper=selected_paper).values("subject").annotate(total=Count("id")):
		question_count_map[row["subject"]] = row["total"]

	subject_cards = []
	for subject in selected_paper_data["subjects"]:
		subject_cards.append({
			**subject,
			"question_count": question_count_map.get(subject["title"], 0),
			"is_active": subject["title"] == selected_subject,
			"icon_svg": _subject_icon_svg(subject["icon"]),
			"url": f"{reverse('ugc_net_pyq')}?{urlencode({'paper': selected_paper, 'subject': subject['title']})}",
		})

	if not questions:
		fallback_questions = [
			{
				"paper": "paper-1",
				"paper_label": "Paper 1",
				"subject": "Teaching Aptitude",
				"year": 2024,
				"question_text": "In learner-centered teaching, the role of a teacher is primarily to:",
				"option_a": "Deliver one-way lectures only",
				"option_b": "Facilitate and guide learning",
				"option_c": "Evaluate students only at the end",
				"option_d": "Avoid classroom interaction",
				"correct_option": "B",
				"solution": "Learner-centered teaching emphasizes facilitation over direct instruction.",
				"explanation": "The teacher creates learning opportunities, encourages inquiry, and supports students in constructing knowledge.",
			},
			{
				"paper": "paper-1",
				"paper_label": "Paper 1",
				"subject": "Research Aptitude",
				"year": 2023,
				"question_text": "Which of the following is a probability sampling method?",
				"option_a": "Convenience sampling",
				"option_b": "Purposive sampling",
				"option_c": "Simple random sampling",
				"option_d": "Quota sampling",
				"correct_option": "C",
				"solution": "Simple random sampling gives each unit equal chance of selection.",
				"explanation": "Probability sampling methods are based on random selection, which reduces selection bias and supports generalization.",
			},
			{
				"paper": "paper-2",
				"paper_label": "Paper 2 (Computer Science and Applications)",
				"subject": "Data Structures",
				"year": 2024,
				"question_text": "Which data structure is most suitable to implement recursion internally?",
				"option_a": "Queue",
				"option_b": "Stack",
				"option_c": "Linked list",
				"option_d": "Heap",
				"correct_option": "B",
				"solution": "Recursion uses the call stack to manage function calls.",
				"explanation": "Each recursive call pushes an activation record onto the stack and pops it after return.",
			},
			{
				"paper": "paper-2",
				"paper_label": "Paper 2 (Computer Science and Applications)",
				"subject": "Database Management Systems",
				"year": 2022,
				"question_text": "Which normal form removes transitive dependency?",
				"option_a": "1NF",
				"option_b": "2NF",
				"option_c": "3NF",
				"option_d": "BCNF",
				"correct_option": "C",
				"solution": "Third Normal Form removes transitive dependencies among non-key attributes.",
				"explanation": "In 3NF, non-key attributes depend only on candidate keys, not on other non-key attributes.",
			},
		]

		available_subjects = sorted(
			{
				item["subject"]
				for item in fallback_questions
				if item["paper"] == selected_paper
			}
		)

		fallback_filtered = [
			item
			for item in fallback_questions
			if item["paper"] == selected_paper
			and (not selected_subject or item["subject"] == selected_subject)
		]

		available_years = sorted(
			{
				item["year"]
				for item in fallback_filtered
			},
			reverse=True,
		)

		questions = [
			item
			for item in fallback_filtered
			if not selected_year or str(item["year"]) == selected_year
		]

		question_count_map = {}
		for item in fallback_questions:
			if item["paper"] == selected_paper:
				question_count_map[item["subject"]] = question_count_map.get(item["subject"], 0) + 1

		subject_cards = []
		for subject in selected_paper_data["subjects"]:
			subject_cards.append({
				**subject,
				"question_count": question_count_map.get(subject["title"], 0),
				"is_active": subject["title"] == selected_subject,
				"icon_svg": _subject_icon_svg(subject["icon"]),
				"url": f"{reverse('ugc_net_pyq')}?{urlencode({'paper': selected_paper, 'subject': subject['title']})}",
			})

	paginator = Paginator(questions, 5)
	page_number = request.GET.get("page", "1")
	page_obj = paginator.get_page(page_number)
	show_subject_grid = not selected_subject

	context = {
		"site_settings": site_settings or default_site_settings,
		"papers": papers,
		"selected_paper_data": selected_paper_data,
		"selected_paper": selected_paper,
		"selected_paper_label": selected_paper_label,
		"subjects": available_subjects,
		"selected_subject": selected_subject,
		"years": available_years,
		"selected_year": selected_year,
		"subject_cards": subject_cards,
		"show_subject_grid": show_subject_grid,
		"questions": page_obj.object_list,
		"page_obj": page_obj,
	}
	return render(request, "portfolio/ugc_net_pyq.html", context)
