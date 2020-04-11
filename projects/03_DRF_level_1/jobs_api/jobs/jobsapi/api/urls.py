from django.urls import path
from jobsapi.api.views import CompanyListCreateAPIView,\
                              CompanyDetailAPIView,\
                              JobListCreateAPIView,\
                              JobDetailAPIView


urlpatterns = [
    path('jobs/',
         JobListCreateAPIView.as_view(),
          name='job-list'),

    path('jobs/<int:pk>',
         JobDetailAPIView.as_view(),
          name='job-detail'),

    path('companies/',
         CompanyListCreateAPIView.as_view(),
          name='company-list'),
          
    path('companies/<int:pk>',
         CompanyDetailAPIView.as_view(),
          name='company-detail'),

]