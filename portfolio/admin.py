from django.contrib import admin
from .models import (
	AboutSection,
	Achievement,
	Certification,
	ContactMessage,
	EducationEntry,
	FocusArea,
	ImpactStat,
	Profile,
	Project,
	SiteSettings,
	Skill,
	SkillCategory,
)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
	list_display = ("full_name", "headline", "email", "location")


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
	list_display = ("name", "level")
	list_editable = ("level",)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
	list_display = ("title", "featured", "created_at")
	list_filter = ("featured",)
	search_fields = ("title", "summary", "tech_stack")


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
	list_display = ("site_title", "analytics_domain", "robots_allow_indexing")


@admin.register(AboutSection)
class AboutSectionAdmin(admin.ModelAdmin):
	list_display = ("title",)


@admin.register(SkillCategory)
class SkillCategoryAdmin(admin.ModelAdmin):
	list_display = ("title", "order")
	list_editable = ("order",)


@admin.register(FocusArea)
class FocusAreaAdmin(admin.ModelAdmin):
	list_display = ("title", "order")
	list_editable = ("order",)


@admin.register(ImpactStat)
class ImpactStatAdmin(admin.ModelAdmin):
	list_display = ("label", "value", "suffix", "order")
	list_editable = ("order",)


@admin.register(EducationEntry)
class EducationEntryAdmin(admin.ModelAdmin):
	list_display = ("degree", "institution", "duration", "order")
	list_editable = ("order",)


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
	list_display = ("text", "order")
	list_editable = ("order",)


@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
	list_display = ("text", "order")
	list_editable = ("order",)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
	list_display = ("name", "email", "is_read", "created_at")
	list_filter = ("is_read", "created_at")
	search_fields = ("name", "email", "message")
