from django.contrib import admin
from django.urls import path
from apps.accounts import views as accounts_views
from apps.courses import views as courses_views
from apps.learning import views as learning_views
from apps.staff import views as staff_views

urlpatterns = [
    # Django Admin
    path('django-admin/', admin.site.urls),

    # Public Pages
    path('', learning_views.homepage, name='homepage'),
    path('about-us/', learning_views.about_us, name='about_us'),

    # Authentication
    path('login/', accounts_views.login_view, name='login'),
    path('logout/', accounts_views.logout_view, name='logout'),
    path('signup/', accounts_views.signup_view, name='signup'),
    path('profile/', accounts_views.profile_view, name='profile'),

    # Courses & Checkout
    path('marketplace/', courses_views.courses_catalog, name='courses_catalog'),
    path('courses/<slug:slug>/', courses_views.course_details, name='course_details'),
    path('courses/<slug:slug>/checkout/', courses_views.checkout, name='checkout'),

    # Student Learning Portal
    path('dashboard/', learning_views.dashboard, name='dashboard'),
    path('dashboard/onboarding/', learning_views.onboarding, name='onboarding'),
    path('dashboard/career-paths/', learning_views.career_paths, name='career_paths'),
    path('dashboard/internship/', learning_views.internship_track, name='internship_track'),
    path('dashboard/internship/player/', learning_views.course_player, name='course_player'),
    path('dashboard/internship/submit/<int:task_id>/', learning_views.submit_task, name='submit_task'),
    path('dashboard/evaluations/', learning_views.evaluation_center, name='evaluation_center'),
    path('dashboard/wallet/', learning_views.skills_wallet, name='skills_wallet'),

    # Training Portal
    path('dashboard/training/', learning_views.training_dashboard, name='training_dashboard'),
    path('dashboard/training/module/<int:module_id>/', learning_views.training_module, name='training_module'),
    path('dashboard/training/interview/', learning_views.training_interview, name='training_interview'),
    path('dashboard/training/score/', learning_views.training_score, name='training_score'),

    # Staff Portals
    path('educator/studio/', staff_views.educator_studio, name='educator_studio'),
    path('hr/talent-intelligence/', staff_views.hr_dashboard, name='hr_dashboard'),
    path('admin/overview/', staff_views.admin_overview, name='admin_overview'),
    path('admin/students/', staff_views.admin_student_profile, name='admin_student_profile'),
    path('admin/evaluations/', staff_views.admin_evaluation_center, name='admin_evaluation_center'),
    path('admin/system-health/', staff_views.admin_health_monitor, name='admin_health_monitor'),
]
