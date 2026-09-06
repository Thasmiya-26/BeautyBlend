from django.urls import path
from . import views


urlpatterns = [

    # =====================================================
    # PAGES
    # =====================================================

    path(
        "",
        views.home_page,
        name="home_page"
    ),

    path(
        "signup/",
        views.signup_page,
        name="signup_page"
    ),

    path(
        "login/",
        views.login_page,
        name="login_page"
    ),

    path(
        "forgot-password/",
        views.forgot_password_page,
        name="forgot_password_page"
    ),

    path(
        "services/",
        views.services_page,
        name="services_page"
    ),

    path(
        "booking/",
        views.booking_page,
        name="booking_page"
    ),

    path(
        "admin-login/",
        views.admin_page,
        name="admin_page"
    ),

    path(
        "dashboard/",
        views.dashboard_page,
        name="dashboard_page"
    ),

    path(
        "feedback/",
        views.feedback_page,
        name="feedback_page"
    ),

    path(
        "combos/",
        views.combo_page,
        name="combos_page"
    ),

    path(
        "about/",
        views.about_page,
        name="about_page"
    ),

    path(
        "contact/",
        views.contact_page,
        name="contact_page"
    ),


    # =====================================================
    # USER API
    # =====================================================

    path(
        "api/register/",
        views.register_user,
        name="register_user"
    ),

    path(
        "api/login/",
        views.login_user,
        name="login_user"
    ),

    path(
        "api/reset-password/",
        views.reset_password,
        name="reset_password"
    ),


    # =====================================================
    # SERVICE API
    # =====================================================

    path(
        "api/add-service/",
        views.add_service,
        name="add_service"
    ),


    # =====================================================
    # APPOINTMENT API
    # =====================================================

    path(
        "api/book-appointment/",
        views.book_appointment,
        name="book_appointment"
    ),


    # =====================================================
    # PAYMENT API
    # =====================================================

    path(
        "api/mark-payment-paid/",
        views.mark_payment_paid,
        name="mark_payment_paid"
    ),


    # =====================================================
    # ADMIN API
    # =====================================================

    path(
        "api/admin-login/",
        views.admin_login,
        name="admin_login"
    ),


    # =====================================================
    # FEEDBACK API
    # =====================================================

    path(
        "api/submit-feedback/",
        views.submit_feedback,
        name="submit_feedback"
    ),


    # =====================================================
    # DASHBOARD API
    # =====================================================

    path(
        "api/dashboard-data/",
        views.dashboard_data,
        name="dashboard_data"
    ),

]