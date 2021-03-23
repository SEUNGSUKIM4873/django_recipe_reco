from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static


app_name = 'mldl_main'

urlpatterns = [
    path('', views.index, name='index'),



    path('dl_cnn/', views.dl_cnn, name='dl_cnn'),
    path('dl_cnn/predict/', views.predict_cnn, name='predict_cnn'),
    path('dl_cnn/delete/<str:file_name>/', views.delete_cnn, name='delete_cnn'),
    path('dl_cnn/recommend/', views.recommend_recipe, name='recommend_recipe'),
    path('dl_cnn/recommend/delete/', views.recommend_delete, name='recommend_delete'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
