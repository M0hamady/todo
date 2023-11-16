import json
from typing import Any
import requests
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.views import LoginView
from todo.forms import RegisterForm
from todo.serializers import CompanyDetailSerializer, CompanyDetailsSerializer, CompanySerializer, ProjectRoadMapMiniSerializer, ProjectRoadMapSerializer, ProjectRoadMapSprintSerializer, ProjectWithRoadMapSerializer, SprintSerializer, TaskSerializer
from.models import Company, Duration, Employee, Meeting, Project, RoadMapItem, Section, Sprint, Task, TaskComment, TaskDuration, TaskFeedback
import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.http.response import HttpResponse, HttpResponsePermanentRedirect
import geocoder
from django.contrib.auth import login
from .models import FCMToken
from firebase_admin import messaging
from django.shortcuts import redirect

class Login(LoginView):
    template_name = 'registration/login.html'
    
    def form_valid(self, form):
        # Log in the user
        user = form.get_user()
        login(self.request, user)
        is_employee = False
        is_company = False
        
        try:
            is_employee = Employee.objects.get(user=user)
            print("is_employee")
            is_employee = 1
        except:
            try:
                is_company = Company.objects.get(user=user)
                print("is_company")
                is_company = 1
            except:
                pass
        
        if is_employee:
            return redirect("profile")
        elif is_company:
            print(is_company)
            return redirect('company')
        
        return super().form_valid(form)
    #    if err he must return to unauthorized
        # Retrieve the FCM token from the request (assuming it's sent in the request data)
        # fcm_token = self.request.POST.get('fcm_token')

        # Store the FCM token in the FCMToken model
        # FCMToken.objects.update_or_create(user=user, defaults={'token': fcm_token})


def showFirebaseJS(request):
    data='importScripts("https://www.gstatic.com/firebasejs/8.2.0/firebase-app.js");' \
         'importScripts("https://www.gstatic.com/firebasejs/8.2.0/firebase-messaging.js"); ' \
         'var firebaseConfig = {' \
         '        apiKey: "AIzaSyApvFodMuj4hzIO7J9MR7zhLyn7fuQwsKw",' \
         '        authDomain: "codeocean-390413.firebaseapp.com",' \
         '        databaseURL: "",' \
         '        projectId: "codeocean-390413",' \
         '        storageBucket: "codeocean-390413.appspot.com",' \
         '        messagingSenderId: "71759842402",' \
         '        appId: "1:71759842402:web:356b8ee1bc882fa19f553b",' \
         '        measurementId: "G-GP776ELHZP"' \
         ' };' \
         'firebase.initializeApp(firebaseConfig);' \
         'const messaging=firebase.messaging();' \
         'messaging.setBackgroundMessageHandler(function (payload) {' \
         '    console.log(payload);' \
         '    const notification=JSON.parse(payload);' \
         '    const notificationOption={' \
         '        body:notification.body,' \
         '        icon:notification.icon' \
         '    };' \
         '    return self.registration.showNotification(payload.notification.title,notificationOption);' \
         '});'

    return HttpResponse(data,content_type="text/javascript")
def check_sav_fcm(request,token):
    fcm_token = token
    if request.user:
        fcm_token_ob = FCMToken.objects.get_or_create(user=request.user,fcm_token=fcm_token)
        
        

    print(555555555555555,fcm_token,444444444444)
    print(FCMToken.objects.all())
    return fcm_token


def send_notification_to_user(user , title, body):
    # Retrieve the FCM token for the user
    client_token = get_object_or_404(FCMToken, user=user).fcm_token

    # Create a notification message
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body
        ),
        token=client_token
    )

    # Send the message
    messaging.send(message)
    fcm_api = ""
    url = "https://fcm.googleapis.com/fcm/send"
    
    headers = {
    "Content-Type":"application/json",
    "Authorization": 'key='+"AAAAELU4TGI:APA91bG9vn58kGiDrnUaQWPhkP7A0Aosbs2A1rzgP6-3IaSgEeVRxVB72VwcxUX67IIcSb4SUpIqrJRb5PAlCV2UtK8py-oebDpGL2Hk0jgudR5n_g9xD5NFuJU2pngJSGIIYijj1XAL"}

    payload = {
        "registration_ids" :[client_token],
        "priority" : "high",
        "notification" : {
            "body" : body,
            "title" : title,
            # "image" : "https://i.ytimg.com/vi/m5WUPHRgdOA/hqdefault.jpg?sqp=-oaymwEXCOADEI4CSFryq4qpAwkIARUAAIhCGAE=&rs=AOn4CLDwz-yjKEdwxvKjwMANGk5BedCOXQ",
            # "icon": "https://yt3.ggpht.com/ytc/AKedOLSMvoy4DeAVkMSAuiuaBdIGKC7a5Ib75bKzKO3jHg=s900-c-k-c0x00ffffff-no-rj",
            
        }
    }

    result = requests.post(url,  data=json.dumps(payload), headers=headers )
    print(result.json())

class Profile(LoginRequiredMixin, TemplateView):
    template_name = 'registration/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        employee = Employee.objects.filter(user=self.request.user).first()
        
        if employee:
            tasks = Task.objects.filter(assigned_to=employee)
            def calculate_duration_current_month():
                durations = Duration.objects.filter(assigned_to= employee).values()
                current_month = datetime.datetime.now().month
                total_seconds = sum((duration['end_time'] - duration['start_time']).total_seconds()
                                for duration in durations
                                if duration['start_time'] and duration['end_time']
                                and duration['start_time'].month == current_month
                                and duration['end_time'].month == current_month)
                total_hours = total_seconds / 3600  # Convert seconds to hours
                return round(total_hours, 2)
            def calculate_duration(durations):
                total_seconds = sum((duration['end_time'] - duration['start_time']).total_seconds() for duration in durations if duration['start_time'] and duration['end_time'])
                total_hours = total_seconds / 3600  # Convert seconds to hours
                return round(total_hours, 2)

            meetings_all = []
            activity_timeLine = []
            for task in tasks:
                durations = Duration.objects.filter(task=task, assigned_to=employee.id)
                meetings = Meeting.objects.filter(task=task)
                meetings_all.append([item for item in meetings])
                try:
                    sprint = task.sprints.first().name
                except AttributeError:
                    sprint = None
                data = {
                    "type": "task",
                    "name": task.title,
                    "memo": task.memo,
                    "sprint": sprint,
                    "durations": calculate_duration(durations.values()),
                    "start_time_task": str(durations.first().start_time) if durations else None,
                    "meeting_link": "",
                    "meeting_date": ""
                }
                activity_timeLine.append(data)

            for meetings in meetings_all:
                for meeting in meetings:
                    data = {
                        "type": "meeting",
                        "name": meeting.task.sprints.first().name if meeting.task.sprints.first() else None,
                        "durations": None,
                        "start_time_task": None,
                        "meeting_link": meeting.meeting_link,
                        "meeting_date": meeting.start_time
                    }
                    activity_timeLine.append(data)

            activity_timeLine = sorted(activity_timeLine, key=lambda x: x['name'])
            context['employee'] = employee
            context['month_durations'] = calculate_duration_current_month()
            context['tasks'] = tasks
            context['activity_timeLine'] = activity_timeLine

            ip_address = self.request.META.get('REMOTE_ADDR')
            location = geocoder.ip(ip_address)
            if location and location.latlng:
                context['location'] = {
                    'latitude': location.latlng[0],
                    'longitude': location.latlng[1],
                    'address': location.address,
                    'city': location.city,
                    'country': location.country
                }
        # print(context)
        return context
class ProfileCompanyProjects(LoginRequiredMixin, TemplateView):
    template_name = 'company/all_projects.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        company = get_object_or_404(Company, user=self.request.user)
        projects= Project.objects.filter(company=company)
        # print(context)
        context['projects'] = projects
        return context
class ProfileCompanyTimeLine(LoginRequiredMixin, TemplateView):
    template_name = 'company/meetings.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        company = get_object_or_404(Company, user=self.request.user)
        meetings = set()
        
        tasks = Task.objects.filter(company=company)
        
        for task in tasks:
            try:
                meeting = Meeting.objects.filter(task=task).first()
                if meeting and meeting.id not in meetings:
                    meetings.add(meeting)
            except:
                pass

        current_datetime = datetime.datetime.now()
        current_meetings = Meeting.objects.filter(start_time__lte=current_datetime, )
        meetings.update(current_meetings)
        
        context['meetings'] = meetings

        current_meeting = Meeting.objects.filter(start_time__lte=current_datetime, end_time__gte=current_datetime)
        context['current_meeting'] = current_meeting
        
        return context
class ProfileCompanyTeam(LoginRequiredMixin, TemplateView):
    template_name = 'company/projects.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        company = get_object_or_404(Company, user=self.request.user)
        sprints = []

        tasks = Task.objects.filter(company=company)
        for task in tasks:
            for sprint in task.sprints.all().values():
                sprint_id = sprint['id']
                new_sprint = get_object_or_404(Sprint, id=sprint_id)
                if sprint_id not in [sprinted['sprint'].id for sprinted in sprints]:
                    sprints.append({'sprint': new_sprint,
                                    'tasks': Task.objects.filter(sprints=new_sprint),
                                    'dates': new_sprint.dates_data()})
        
        context['sprints'] = sprints
        # print(context)
        return context
    
def add_feed_task(request):
    id = request.POST.get('task_id')
    user = request.user
    company=Company.objects.get(user=user.id)
    feedback_text =request.POST.get('feed')
    
    task = Task.objects.get(id=id)
    if feedback_text:

    # add the feeds to the task list
        print('done',company,feedback_text, task.id)
        feed = TaskFeedback.objects.create(
            task =task,
            feedback_text=feedback_text,
            company=company

        )
        print('done',company,feedback_text, task)
        feed.save()
    sprints = []
    tasks = Task.objects.filter(company=company)
    for task in tasks:
        for sprint in task.sprints.all().values():
            sprint_id = sprint['id']
            new_sprint = get_object_or_404(Sprint, id=sprint_id)
            if sprint_id not in [sprinted['sprint'].id for sprinted in sprints]:
                sprints.append({'sprint': new_sprint,
                                    'tasks': Task.objects.filter(sprints=new_sprint),
                                    'dates': new_sprint.dates_data()})
    context= {}     
    context['sprints'] = sprints
    # return template fragment with all the user's films
    return render(request, 'registration/profile_partial/list_links _company.html', context=context)
class ProfileTeam(LoginRequiredMixin,TemplateView):
    template_name = 'registration/profile_teams.html'
    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        employee = Employee.objects.filter(user=self.request.user).first()
        if employee:
            sprints= []
            tasks = Task.objects.filter(assigned_to=employee)
            for task in tasks:
                for sprint in task.sprints.all().values():
                    new_sprint = Sprint.objects.get(id = sprint['id'])
                    # new_sprint['dates_data'] = new_sprint.dates_data()
                    if new_sprint not in sprints:
                        sprints.append({'sprint':new_sprint,'tasks':Task.objects.filter(sprints=new_sprint),"dates":new_sprint.dates_data()})
            context['sprints'] = sprints
        # print(context['sprints'])
        return context
class ProfileProjects(LoginRequiredMixin,TemplateView):
    template_name = 'registration/profile_projects.html'

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        employee = Employee.objects.filter(user=self.request.user).first()
        if employee:
            sprints= []
            tasks = Task.objects.filter(assigned_to=employee)
            for task in tasks:
                for sprint in task.sprints.all().values():
                    new_sprint = Sprint.objects.get(id = sprint['id'])
                    # new_sprint['dates_data'] = new_sprint.dates_data()
                    if new_sprint not in sprints:
                        sprints.append({'sprint':new_sprint,'tasks':new_sprint.tasks(),"dates":new_sprint.dates_data()})
            context['sprints'] = sprints
            
        return context


def task_comments(request,pk):
    # search_text = request.POST.get('search')
    print(pk)
    comments = TaskComment.objects.filter(id= pk)
    context = {"comments": comments}
    return render(request, 'registration/profile_partial/list_tasks_update.html', context)

# class TaskCommentsList(LoginRequiredMixin,ListView):
#     template_name = 'home.html'
#     model = TaskComment
#     context_object_name = 'comments'

#     def get_queryset(self, pk):
#         comments = TaskComment.objects.filter(id= pk)
#         return comments
class RegisterView(FormView):
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.save()  # save the user
        return super().form_valid(form)

def check_username(request):
    username = request.POST.get('username')
    if get_user_model().objects.filter(username=username).exists():
        return HttpResponse("This username already exists")
    else:
        return HttpResponse("")

def calculate_total_duration(request):
    task_duration = None
    
    if request.method == 'POST':
        employee_id = request.POST.get('employee_id')
        company_id = request.POST.get('company_id')
        section_id = request.POST.get('section_id')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        
        tasks = Task.objects.all()
        
        if employee_id != "" and company_id != "":
            tasks = tasks.filter(assigned_to__id=employee_id, company__id=company_id)
        
        if section_id != "":
            tasks = tasks.filter(assigned_to__section__id=section_id)

        if start_date and end_date:
            start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
            duration_range = (end_date - start_date).days
            tasks_with_duration = [task for task in tasks if any(Duration.objects.filter(task=task, at=(start_date + datetime.timedelta(days=duration))).exists() for duration in range(duration_range+1))]
            tasks = tasks_with_duration
                
        total_duration = sum(task.calculate_task_durations() for task in tasks)
        task_duration = TaskDuration.objects.create(duration=total_duration)
    
    return render(request, 'calculate_total_duration.html', {'task_duration': task_duration, "companies": Company.objects.all(), "employees": Employee.objects.all(), "sections": Section.objects.all()})
from django.views.generic.list import ListView
class TaskList(LoginRequiredMixin,ListView):
    template_name = 'registration/profile_projects.html'
    model = Task
    context_object_name = 'tasks'

    def get_queryset(self,):
        print(1)
        user = self.request.user
        employee = Employee.objects.get(user= user)
        list_tasks = Task.objects.filter(assigned_to= employee)
        tasks = []

        for task in list_tasks:
            last_durations= Duration.objects.filter(assigned_to = employee, task =task).last()
            tasks.append({"task":task, "last_duration":last_durations})

        print(tasks)
        return tasks
    
def change_status(request, pk):
    user = request.user
    employee = get_object_or_404(Employee, user=user)
    task = get_object_or_404(Task, pk=pk)
    tasks = Task.objects.filter(assigned_to=employee)
    current_time = timezone.now()
    ongoing_duration = Duration.objects.filter(task=task, assigned_to=employee, end_time__isnull=True).last()
    print('ongoing_duration', ongoing_duration)
    
    if not ongoing_duration:
        duration = Duration.objects.create(task=task, start_time=current_time)
        duration.assigned_to.add(employee)
        duration.save()
        print(5)
        try:
            send_notification_to_user(user=user,title=f"Start working hard", body=f"{task.title}")
        except:pass
        return HttpResponse(f"<div id='btn{task.pk}' class='bg-label-danger'>Stop</div>")
    else:
        ongoing_duration.end_time = current_time
        ongoing_duration.save()
    context = {
        "task":{'task':task}
    }
    return HttpResponse(f"<div id='btn{task.pk}' class='bg-label-success'>Start</div>")
from datetime import date, timedelta
from django.utils import timezone

from django.http import JsonResponse
from django.views import View

class EmployeeTaskView(APIView):
    def get(self, request, employee_uuid):
        try:
            employee = Employee.objects.get(uuid=employee_uuid)
        except Employee.DoesNotExist:
            return JsonResponse({'error': 'Employee not found'}, status=404)

        today = date.today()

        # Get daily tasks
        daily_tasks = Task.objects.filter(
            assigned_to=employee,
            date_in_dev_at__date=today
        )

        # Get weekly tasks
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)
        weekly_tasks = Task.objects.filter(
            assigned_to=employee,
            created__date__range=[start_of_week, end_of_week]
        )

        # Get tasks in "is_dev" status
        dev_tasks = Task.objects.filter(
            assigned_to=employee,
        )

        # Serialize tasks
        daily_tasks_data = [TaskSerializer(Task.objects.get(id = task['id'])).data for task in daily_tasks.values()]
        weekly_tasks_data = [TaskSerializer(Task.objects.get(id = task['id'])).data for task in weekly_tasks.values()]
        dev_tasks_data = [TaskSerializer(Task.objects.get(id = task['id'])).data for task in dev_tasks.values()]
        # print(daily_tasks)
        response_data = {
            'daily_tasks': daily_tasks_data,
            'weekly_tasks': weekly_tasks_data,
            'employee_tasks': dev_tasks_data
        }

        return Response(response_data)
from django.middleware.csrf import get_token
    
from rest_framework.response import Response

class EmployeeTaskUpdateView(APIView):
    def post(self, request, employee_uuid):
        if 'task_uuid' not in request.data:
            return Response({'error': 'task_uuid field is required'}, status=400)
        task_uuid = request.data.get('task_uuid')
        try:
            task = Task.objects.get(uuid=task_uuid)
        except Task.DoesNotExist:
            return Response({'error': 'Task not found'}, status=404)

        try:
            employee = Employee.objects.get(uuid=employee_uuid)
        except Employee.DoesNotExist:
            return Response({'error': 'Employee not found'}, status=404)

        # Check if the employee is assigned to the task
        if employee not in task.assigned_to.all():
            return Response({'error': 'You are not assigned to this task'}, status=403)

        task_data = request.data.dict()
        for key, value in task_data.items():
            if hasattr(task, key):
                setattr(task, key, value)

        # Update task information
       
        task.save()

        # Add a comment to the task
        comment_text = request.data.get('comment')
        if comment_text:
            comment = TaskComment.objects.create(task=task, employee=employee, feedback_text=comment_text)
            
        feedback_text = request.data.get('feedback')
        if feedback_text:
            if 'company_uuid' not in request.POST:
                return JsonResponse({'error': 'company_uuid field is  required while adding feedback'}, status=400)
            company = Company.objects.get(uuid = request.data.get('company_uuid')  )
            feedback = TaskFeedback.objects.create(task=task,company =company,  feedback_text=feedback_text)
            

        return Response({"task":TaskSerializer(task).data,'message': 'Task updated successfully'})
    

    
class TaskDetailView(APIView):
    def get(self, request, employee_uuid,task_uuid):
        try:
            task = Task.objects.get(uuid=task_uuid)
        except Task.DoesNotExist:
            return JsonResponse({'error': 'Task not found'}, status=404)
        try:
            employee = Employee.objects.get(uuid=employee_uuid)
        except Employee.DoesNotExist:
            return JsonResponse({'error': 'please contact company to get your unique id or refresh it '}, status=404)
        if employee not in task.assigned_to.all():
            return JsonResponse({'error': 'you are not assigned to this task'}, status=404)
        return Response(TaskSerializer(task).data)
    
class CheckKey(APIView):
    def post(self, request,):
        is_employee = False
        is_company = False
        is_active = False
        if 'uuid' not in request.POST:
                return JsonResponse({'error': 'uuid field is  required while adding feedback'}, status=400)
        try:
            employee = Employee.objects.get(uuid = request.data.get('uuid') )
            is_employee  = True
            is_active = employee.is_active
        except :
            pass
        try:
            company = Company.objects.get(uuid = request.data.get('uuid') )
            is_company  = True
            is_active = company.is_active
        except :
            pass
        context =  {
            'is_employee' : is_employee,
            'is_company' :is_company,
            'is_active' :is_active,
        }
        return Response(context)
class Employee_data(APIView):
    def post(self, request,employee_uuid):
        if 'uuid' not in request.POST:
                return JsonResponse({'error': 'uuid field is  required while adding feedback'}, status=400)
        try:
            employee = Employee.objects.get(uuid=employee_uuid)
            if not employee.is_active:
                return JsonResponse({'error': f'hi {employee.user.username} you are not active any more please contact CodeOcean'}, status=400)
        except Employee.DoesNotExist:
            return JsonResponse({'error': 'please contact company to get your unique id or refresh it '}, status=404)
        
        
        context =  {
            'username' : employee.user.username,
            'email' : employee.user.email,
            'team' : employee.section.name,
            'team_shortcut' : employee.section.shortcut,
            'is_active' :employee.is_active,
            'tasks_count' :employee.get_all_tasks().count(),
            'completed_tasks_count' :employee.get_all_non_completed_tasks().count(),
            'companies_worked_with_count' :len(employee.get_all_companies()),
            'future_sprints' :[SprintSerializer(name).data for name in employee.get_future_sprints()],
        }
        return Response(context)
from rest_framework import status
from django.urls import reverse
class TaskDurationAPIView(APIView):
    def post(self, request, employee_uuid):
        try:
            employee = Employee.objects.get(uuid=employee_uuid)
            if not employee.is_active:
                return JsonResponse({'error': f'hi {employee.user.username} you are not active anymore, please contact CodeOcean'}, status=400)
        except Employee.DoesNotExist:
            return JsonResponse({'error': 'please contact the company to get your unique ID or refresh it'}, status=404)
        
        if 'task_uuid' not in request.data:
            return Response({'error': 'task_uuid field is required'}, status=400)
        
        task_uuid = request.data.get('task_uuid')
        
        try:
            task = Task.objects.get(uuid=task_uuid)
        except Task.DoesNotExist:
            return Response({'error': 'Task not found'}, status=404)
        
        if task.calculate_task_completion_percentage() == 100:
            return Response({"error": "Task is already finished"}, status=status.HTTP_400_BAD_REQUEST)

        current_time = timezone.now()

        # Check if there is an ongoing duration for the user
        ongoing_duration = Duration.objects.filter(task=task, assigned_to=employee, end_time__isnull=True).last()

        if 'end_time' in request.data:
            if ongoing_duration:
                print(ongoing_duration.start_time,ongoing_duration.end_time)
                ongoing_duration.end_time = current_time
                ongoing_duration.save()

                return Response({
                "message": "last duration finished successfully",
                 "duration":ongoing_duration.uuid,
                "duration_start_time":ongoing_duration.start_time,
                "task": TaskSerializer(task).data
            }, status=status.HTTP_200_OK)
            else:
                return Response({"error": "No ongoing duration found"}, status=status.HTTP_400_BAD_REQUEST)
        
        # If there are no ongoing durations, start a new duration
        if 'start_time' in request.data and not ongoing_duration:
            start_time = request.data['start_time']
            duration = Duration.objects.create(task=task, start_time=current_time)
            duration.assigned_to.add(employee)
            
            return Response({
                "message": "New duration started successfully",
                "duration":duration.uuid,
                "duration_start_time":duration.start_time,
                "task": TaskSerializer(task).data
            }, status=status.HTTP_200_OK)
        elif 'start_time' in request.data and  ongoing_duration:
            return Response({
                "message": "you have an opened duration ",
                "duration":ongoing_duration.uuid,
                "duration_start_time":ongoing_duration.start_time,
                "task": TaskSerializer(task).data
            }, status=status.HTTP_200_OK)
        elif   ongoing_duration:
            return Response({
                "message": "you have an opened duration ",
                "duration":ongoing_duration.uuid,
                "duration_start_time":ongoing_duration.start_time,
                "task": TaskSerializer(task).data
            }, status=status.HTTP_200_OK)
        elif 'start_time'  not in request.data and not ongoing_duration:
            return Response({
                "message": "you have no duration",
                "task": TaskSerializer(task).data
            }, status=status.HTTP_400_BAD_REQUEST)
#+++++++++++++++++++++++++++++++++++++++++++++++++++++
#company

class CompanyDetailView(APIView):
    def get(self, request, company_uuid,):
        try:
            company = Company.objects.get(uuid=company_uuid)
        except Company.DoesNotExist:
            return JsonResponse({'error': 'company not found'}, status=404)
        
        return Response(CompanySerializer(company).data)
    def put(self, request, company_uuid,):
        try:
            company = Company.objects.get(uuid=company_uuid)
        except Company.DoesNotExist:
            return JsonResponse({'error': 'company not found'}, status=404)
        if 'project_uuid' in request.data:
            return Response(CompanyDetailSerializer(company).data)
        else:    return JsonResponse({'error': 'project_uuid is required'}, status=404)
class CompanyMiniDetailView(APIView):
    def get(self, request, company_uuid,):
        try:
            company = Company.objects.get(uuid=company_uuid)
        except Company.DoesNotExist:
            return JsonResponse({'error': 'company not found'}, status=404)
        
        return Response(CompanyDetailsSerializer(company).data)
    
class CompanyProjectRoadmapView(APIView):
    def get(self, request, company_uuid,):
        uuid_project = request.data['uuid_project']
        if not uuid_project:
            return Response({'error': 'uuid_project field is required'}, status=400)
        try:
            company = Company.objects.get(uuid=company_uuid)
        except Company.DoesNotExist:
            return JsonResponse({'error': 'company not found'}, status=404)
        
        project = Project.objects.get(uuid = uuid_project)
        project_serializer = ProjectWithRoadMapSerializer(project)
        
        return Response(project_serializer.data)
    
class CompanyProjectRoadmapSprintsView(APIView):
    def get(self, request, company_uuid,):
        roadmap_uuid = request.data['roadmap_uuid']
        if not roadmap_uuid:
            return Response({'error': 'roadmap_uuid field is required'}, status=400)
        try:
            company = Company.objects.get(uuid=company_uuid)
        except Company.DoesNotExist:
            return JsonResponse({'error': 'company not found'}, status=404)
        
        RoadMap = RoadMapItem.objects.get(uuid = roadmap_uuid)
        project_serializer = ProjectRoadMapSerializer(RoadMap)
        
        return Response(project_serializer.data)
    
class CompanyProjectRoadmapDetailView(APIView):
    def get(self, request, company_uuid,):
        roadmap_uuid = request.data['roadmap_uuid']
        if not roadmap_uuid:
            return Response({'error': 'roadmap_uuid field is required'}, status=400)
        try:
            company = Company.objects.get(uuid=company_uuid)
        except Company.DoesNotExist:
            return JsonResponse({'error': 'company not found'}, status=404)
        
        RoadMap = RoadMapItem.objects.get(uuid = roadmap_uuid)
        project_serializer = ProjectRoadMapMiniSerializer(RoadMap)
        
        return Response(project_serializer.data)
    
class CompanyProjectRoadmapSprintDataView(APIView):
    def get(self, request, company_uuid,):
        sprint_uuid = request.data['sprint_uuid']
        if not sprint_uuid:
            return Response({'error': 'sprint_uuid field is required'}, status=400)
        try:
            company = Company.objects.get(uuid=company_uuid)
        except Company.DoesNotExist:
            return JsonResponse({'error': 'company not found'}, status=404)
        
        sprint = Sprint.objects.get(uuid = sprint_uuid)
        project_serializer = ProjectRoadMapSprintSerializer(sprint)
        
        return Response(project_serializer.data)
    