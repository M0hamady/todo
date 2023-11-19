import os
from django.urls import path

from main.settings import BASE_DIR
from .views import (
    CheckKey,
    CompanyDetailView,
    CompanyMiniDetailView,
    CompanyProjectRoadmapDetailView,
    CompanyProjectRoadmapSprintDataView,
    CompanyProjectRoadmapSprintsView,
    CompanyProjectRoadmapView,
    Employee_data,
    Login,
    Profile,
    ProfileCompanyProjects,
    ProfileCompanyTeam,
    ProfileCompanyTimeLine,
    ProfileProjects,
    ProfileTeam,
    RegisterView,
    TaskDurationAPIView,
    TaskList,
    add_comment_task,
    add_feed_task,
    calculate_total_duration,
    EmployeeTaskView,
    EmployeeTaskUpdateView,
    TaskDetailView,
    change_status,
    check_sav_fcm,
    check_username,
    Road_map,
    showFirebaseJS,
    task_comments,
)
from django.contrib.auth.views import LogoutView
import firebase_admin
from firebase_admin import credentials
service_account_file = os.path.join(BASE_DIR,  'servicesK.json')
# Path to your Firebase service account key file
cred = credentials.Certificate(service_account_file)
firebase_admin.initialize_app(cred)
urlpatterns = [
    path('employee/login/', Login.as_view(), name='login'),
    path('project/road-map/<uuid:project_uuid>/', Road_map.as_view(), name='road_map'),
    path('company/', ProfileCompanyTeam.as_view(), name='company'),
    path('company/projects', ProfileCompanyProjects.as_view(), name='company_projects'),
    path('company/meetings', ProfileCompanyTimeLine.as_view(), name='company_meetings'),
    path('firebase-messaging-sw.js',showFirebaseJS,name="show_firebase_js"),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('fcm_token/<str:token>/', check_sav_fcm, name='logout'),
    path("employee/register/", RegisterView.as_view(), name="register"),
    path("", Profile.as_view(), name="profile"),
    path("accounts/profile/pages-profile-sprints/", ProfileTeam.as_view(), name="profile_sprints"),
    path("accounts/profile/pages-profile-tasks/", TaskList.as_view(), name="profile_tasks"),
    path('calculate-total-duration/', calculate_total_duration, name='calculate_total_duration'),
    path('employee/<uuid:employee_uuid>/tasks/', EmployeeTaskView.as_view(), name='employee_tasks'),
    path('employee/check/', CheckKey.as_view(), name='employee_Check'),
    path('employee/<uuid:employee_uuid>/data/', Employee_data.as_view(), name='employee_Check'),
    path('task/<uuid:employee_uuid>/add-comment/', EmployeeTaskUpdateView.as_view(), name='add_comment_to_task'),
    path('task/<uuid:employee_uuid>/duration/', TaskDurationAPIView.as_view(), name='duration_of_task'),
    # path('task/<int:task_id>/update/', EmployeeTaskUpdateView.as_view(), name='employee_task_update'),
    path('task/<uuid:task_uuid>/<uuid:employee_uuid>/', TaskDetailView.as_view(), name='task_detail'),
    path('company/<uuid:company_uuid>/detail/', CompanyDetailView.as_view(), name='company_detail'),
    path('company/<uuid:company_uuid>/mini-detail/', CompanyMiniDetailView.as_view(), name='company_detail'),
    path('company/<uuid:company_uuid>/project/roadmap/', CompanyProjectRoadmapView.as_view(), name='company_detail'),
    path('company/<uuid:company_uuid>/project/roadmap/detail/', CompanyProjectRoadmapDetailView.as_view(), name='RoadmapDetail'),
    path('company/<uuid:company_uuid>/project/roadmap/sprints/', CompanyProjectRoadmapSprintsView.as_view(), name='RoadmapDetail'),
    path('company/<uuid:company_uuid>/project/roadmap/sprint/data/', CompanyProjectRoadmapSprintDataView.as_view(), name='RoadmapDetail'),
    # path('company/<uuid:company_uuid>/', CompanyDetailView.as_view(), name='company_detail'),
]

hmtx_views = [
    path("check-username/", check_username, name='check-username'),
    path('change-status/<int:pk>/', change_status, name='change_status'),
    path('task-comments/<int:pk/', task_comments, name='task_comments'),
    
    path('employee/add-comment/<str:uuid>/', add_comment_task, name='add_comment_employee'),
    path('add-feed/', add_feed_task, name='add-feed')
    # path('delete-film/<int:pk>/', views.delete_film, name='delete-film')
]

urlpatterns += hmtx_views