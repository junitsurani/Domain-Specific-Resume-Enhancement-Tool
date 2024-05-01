from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('upload_pdf1', views.upload_pdf1, name='upload_pdf1'),
    path('register', views.register, name='register'),
    path('dashboard', views.upload_pdf1, name='dashboard'),
    path('faq', views.faq, name='faq'),
    path('contact', views.contact, name='contact'),
    path('send_email/', views.send_email, name='send_email'),
    path('fgt-pass/', views.fgt_pwd, name='forgot-pass'),
    path('scrape/', views.scrape_website, name='scrape_website'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)