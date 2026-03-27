from django.urls import path
from .views import home, robots_txt, sitemap_xml

urlpatterns = [
    path("", home, name="home"),
    path("robots.txt", robots_txt, name="robots_txt"),
    path("sitemap.xml", sitemap_xml, name="sitemap_xml"),
]
