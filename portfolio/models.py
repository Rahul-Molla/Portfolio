from django.db import models


class Profile(models.Model):
	full_name = models.CharField(max_length=120)
	headline = models.CharField(max_length=160)
	intro = models.TextField()
	email = models.EmailField()
	phone = models.CharField(max_length=32, blank=True)
	location = models.CharField(max_length=120, blank=True)
	photo_url = models.URLField(blank=True)
	resume_url = models.URLField(blank=True)
	portfolio_url = models.URLField(blank=True)
	github_url = models.URLField(blank=True)
	linkedin_url = models.URLField(blank=True)

	class Meta:
		verbose_name = "Profile"
		verbose_name_plural = "Profile"

	def __str__(self):
		return self.full_name


class Skill(models.Model):
	name = models.CharField(max_length=80)
	level = models.PositiveSmallIntegerField(default=80)

	class Meta:
		ordering = ["-level", "name"]

	def __str__(self):
		return f"{self.name} ({self.level}%)"


class Project(models.Model):
	title = models.CharField(max_length=120)
	summary = models.TextField()
	tech_stack = models.CharField(max_length=255)
	outcome = models.CharField(max_length=220, blank=True)
	screenshot_url = models.URLField(blank=True)
	live_url = models.URLField(blank=True)
	source_url = models.URLField(blank=True)
	featured = models.BooleanField(default=True)
	created_at = models.DateField(null=True, blank=True)

	class Meta:
		ordering = ["-featured", "-id"]

	def __str__(self):
		return self.title


class SiteSettings(models.Model):
	site_title = models.CharField(max_length=120, default="Rahul Molla Portfolio")
	seo_description = models.TextField(blank=True)
	seo_keywords = models.CharField(max_length=255, blank=True)
	og_image_url = models.URLField(blank=True)
	twitter_handle = models.CharField(max_length=60, blank=True)
	analytics_domain = models.CharField(max_length=160, blank=True)
	robots_allow_indexing = models.BooleanField(default=True)

	class Meta:
		verbose_name = "Site settings"
		verbose_name_plural = "Site settings"

	def save(self, *args, **kwargs):
		self.pk = 1
		super().save(*args, **kwargs)

	def __str__(self):
		return "Site settings"


class AboutSection(models.Model):
	title = models.CharField(max_length=120, default="Professional Summary")
	summary = models.TextField()

	class Meta:
		verbose_name = "About section"
		verbose_name_plural = "About section"

	def save(self, *args, **kwargs):
		self.pk = 1
		super().save(*args, **kwargs)

	def __str__(self):
		return self.title


class SkillCategory(models.Model):
	title = models.CharField(max_length=100)
	items = models.TextField(help_text="Comma separated values")
	order = models.PositiveSmallIntegerField(default=1)

	class Meta:
		ordering = ["order", "id"]

	def __str__(self):
		return self.title


class FocusArea(models.Model):
	title = models.CharField(max_length=120)
	detail = models.TextField()
	order = models.PositiveSmallIntegerField(default=1)

	class Meta:
		ordering = ["order", "id"]

	def __str__(self):
		return self.title


class ImpactStat(models.Model):
	label = models.CharField(max_length=80)
	value = models.DecimalField(max_digits=8, decimal_places=2)
	suffix = models.CharField(max_length=8, blank=True)
	order = models.PositiveSmallIntegerField(default=1)

	class Meta:
		ordering = ["order", "id"]

	def __str__(self):
		return self.label


class EducationEntry(models.Model):
	degree = models.CharField(max_length=140)
	institution = models.CharField(max_length=160)
	score = models.CharField(max_length=80)
	duration = models.CharField(max_length=60)
	order = models.PositiveSmallIntegerField(default=1)

	class Meta:
		ordering = ["order", "id"]

	def __str__(self):
		return self.degree


class Achievement(models.Model):
	text = models.CharField(max_length=180)
	order = models.PositiveSmallIntegerField(default=1)

	class Meta:
		ordering = ["order", "id"]

	def __str__(self):
		return self.text


class Certification(models.Model):
	text = models.CharField(max_length=220)
	order = models.PositiveSmallIntegerField(default=1)

	class Meta:
		ordering = ["order", "id"]

	def __str__(self):
		return self.text


class ContactMessage(models.Model):
	name = models.CharField(max_length=120)
	email = models.EmailField()
	message = models.TextField()
	honeypot = models.CharField(max_length=120, blank=True)
	is_read = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ["-created_at"]

	def __str__(self):
		return f"{self.name} <{self.email}>"


class UGCNetPYQ(models.Model):
	PAPER_CHOICES = [
		("paper-1", "Paper 1"),
		("paper-2", "Paper 2 (Computer Science and Applications)"),
	]

	OPTION_CHOICES = [
		("A", "Option A"),
		("B", "Option B"),
		("C", "Option C"),
		("D", "Option D"),
	]

	paper = models.CharField(max_length=12, choices=PAPER_CHOICES, default="paper-1")
	subject = models.CharField(max_length=120)
	year = models.PositiveSmallIntegerField(default=2026)
	question_text = models.TextField()
	option_a = models.CharField(max_length=255)
	option_b = models.CharField(max_length=255)
	option_c = models.CharField(max_length=255)
	option_d = models.CharField(max_length=255)
	correct_option = models.CharField(max_length=1, choices=OPTION_CHOICES)
	solution = models.TextField(help_text="Short solution or approach")
	explanation = models.TextField(help_text="Detailed explanation")
	is_active = models.BooleanField(default=True)
	order = models.PositiveIntegerField(default=1)

	class Meta:
		ordering = ["paper", "subject", "-year", "order", "id"]
		verbose_name = "UGC NET PYQ"
		verbose_name_plural = "UGC NET PYQs"

	def __str__(self):
		return f"{self.get_paper_display()} | {self.subject} | {self.year}"
