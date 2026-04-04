from django.urls import path
from .views import home, robots_txt, sitemap_xml, ugc_net_pyq

urlpatterns = [
    path("", home, name="home"),
    path("ugc-net-pyq/", ugc_net_pyq, name="ugc_net_pyq"),
    path("robots.txt", robots_txt, name="robots_txt"),
    path("sitemap.xml", sitemap_xml, name="sitemap_xml"),
]
