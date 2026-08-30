from django.shortcuts import render
from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from decimal import Decimal, InvalidOperation

from .models import (
    User,
    Admin,
    Service,
    Appointment,
    Payment,
    Feedback,
    Combo
)


# =========================================================
# PAGE VIEWS
# =========================================================

def home_page(request):
    return render(request, "home.html")


def signup_page(request):
    return render(request, "signup.html")


def login_page(request):
    return render(request, "login.html")


def forgot_password_page(request):
    return render(request, "forgotpassword.html")


def services_page(request):
    return render(request, "services.html")


def booking_page(request):
    return render(request, "Booking.html")


def admin_page(request):
    return render(request, "admin.html")


def dashboard_page(request):
    return render(request, "dashboard.html")


def feedback_page(request):
    return render(request, "feedback.html")


def combos_page(request):
    return render(request, "combo.html")


def contact_page(request):
    return render(request, "contact.html")


def about_page(request):
    return render(request, "about.html")


# =========================================================
# REGISTER USER
# =========================================================

@csrf_exempt
def register_user(request):

    if request.method != "POST":
        return JsonResponse({
            "success": False,
            "message": "Invalid request."
        })

    try:
        data = json.loads(request.body)

        name = data.get("name", "").strip()
        email = data.get("email", "").strip()
        phone = data.get("phone", "").strip()
        password = data.get("password", "")

        if not name:
            return JsonResponse({
                "success": False,
                "message": "Please enter your full name."
            })

        if not all(char.isalpha() or char.isspace() for char in name):
            return JsonResponse({
                "success": False,
                "message": "Please enter alphabets only in the name."
            })

        if not email:
            return JsonResponse({
                "success": False,
                "message": "Please enter your email address."
            })

        if not phone:
            return JsonResponse({
                "success": False,
                "message": "Please enter your phone number."
            })

        if not phone.isdigit():
            return JsonResponse({
                "success": False,
                "message": "Phone number must contain digits only."
            })

        if len(phone) != 10:
            return JsonResponse({
                "success": False,
                "message": "Phone number must contain exactly 10 digits."
            })

        if not password:
            return JsonResponse({
                "success": False,
                "message": "Please enter your password."
            })

        if len(password) < 8:
            return JsonResponse({
                "success": False,
                "message": "Password must contain at least 8 characters."
            })

        if User.objects.filter(email=email).exists():
            return JsonResponse({
                "success": False,
                "message": "Email already registered."
            })

        if User.objects.filter(phone=phone).exists():
            return JsonResponse({
                "success": False,
                "message": "Phone number already registered."
            })

        User.objects.create(
            name=name,
            email=email,
            phone=phone,
            password=make_password(password)
        )

        return JsonResponse({
            "success": True,
            "message": "Registration successful!"
        })

    except json.JSONDecodeError:
        return JsonResponse({
            "success": False,
            "message": "Invalid data received."
        })

    except Exception as e:
        return JsonResponse({
            "success": False,
            "message": str(e)
        })


# =========================================================
# LOGIN USER
# =========================================================

@csrf_exempt
def login_user(request):

    if request.method != "POST":
        return JsonResponse({
            "success": False,
            "message": "Invalid request."
        })

    try:
        data = json.loads(request.body)

        email = data.get("email", "").strip()
        password = data.get("password", "")

        if not email or not password:
            return JsonResponse({
                "success": False,
                "message": "Please enter email and password."
            })

        try:
            user = User.objects.get(email=email)

        except User.DoesNotExist:
            return JsonResponse({
                "success": False,
                "message": "Email not registered."
            })

        if not check_password(password, user.password):
            return JsonResponse({
                "success": False,
                "message": "Invalid password."
            })

        return JsonResponse({
            "success": True,
            "message": "Login successful!",
            "name": user.name,
            "email": user.email,
            "phone": user.phone
        })

    except json.JSONDecodeError:
        return JsonResponse({
            "success": False,
            "message": "Invalid data received."
        })

    except Exception as e:
        return JsonResponse({
            "success": False,
            "message": str(e)
        })


# =========================================================
# RESET PASSWORD
# =========================================================

@csrf_exempt
def reset_password(request):

    if request.method != "POST":
        return JsonResponse({
            "success": False,
            "message": "Invalid request."
        })

    try:

        data = json.loads(request.body)

        email = data.get(
            "email",
            ""
        ).strip()

        new_password = data.get(
            "new_password",
            ""
        )

        # -------------------------------------------------
        # VALIDATE EMAIL
        # -------------------------------------------------

        if not email:

            return JsonResponse({
                "success": False,
                "message": "Please enter your registered email."
            })

        # -------------------------------------------------
        # VALIDATE PASSWORD
        # -------------------------------------------------

        if not new_password:

            return JsonResponse({
                "success": False,
                "message": "Please enter a new password."
            })

        if len(new_password) < 8:

            return JsonResponse({
                "success": False,
                "message": "Password must contain at least 8 characters."
            })

        # -------------------------------------------------
        # FIND USER USING EMAIL
        # -------------------------------------------------

        try:

            user = User.objects.get(
                email__iexact=email
            )

        except User.DoesNotExist:

            return JsonResponse({
                "success": False,
                "message": "No account found with this email."
            })

        # -------------------------------------------------
        # UPDATE PASSWORD
        # -------------------------------------------------

        user.password = make_password(
            new_password
        )

        user.save(
            update_fields=["password"]
        )

        return JsonResponse({
            "success": True,
            "message": "Password reset successfully! Please login with your new password."
        })

    except json.JSONDecodeError:

        return JsonResponse({
            "success": False,
            "message": "Invalid data received."
        })

    except Exception as e:

        return JsonResponse({
            "success": False,
            "message": str(e)
        })


# =========================================================
# ADMIN LOGIN
# =========================================================

@csrf_exempt
def admin_login(request):

    if request.method != "POST":
        return JsonResponse({
            "success": False,
            "message": "Invalid request."
        })

    try:

        data = json.loads(request.body)

        username = data.get(
            "username",
            ""
        ).strip()

        password = data.get(
            "password",
            ""
        )

        if not username or not password:
            return JsonResponse({
                "success": False,
                "message": "Please enter username and password."
            })

        try:

            admin = Admin.objects.get(
                username=username
            )

        except Admin.DoesNotExist:

            return JsonResponse({
                "success": False,
                "message": "Admin not found."
            })

        if not check_password(
            password,
            admin.password
        ):

            return JsonResponse({
                "success": False,
                "message": "Incorrect Password!"
            })

        return JsonResponse({
            "success": True,
            "message": "Admin login successful!"
        })

    except json.JSONDecodeError:

        return JsonResponse({
            "success": False,
            "message": "Invalid data received."
        })

    except Exception as e:

        return JsonResponse({
            "success": False,
            "message": str(e)
        })


# =========================================================
# ADD SERVICE
# =========================================================

@csrf_exempt
def add_service(request):

    if request.method != "POST":
        return JsonResponse({
            "success": False,
            "message": "Invalid request."
        })

    try:

        data = json.loads(request.body)

        name = data.get(
            "name",
            ""
        ).strip()

        price = data.get(
            "price",
            0
        )

        description = data.get(
            "description",
            "Salon service"
        ).strip()

        if not name:

            return JsonResponse({
                "success": False,
                "message": "Service name is required."
            })

        service = Service.objects.filter(
            name=name
        ).first()

        if service:

            return JsonResponse({
                "success": True,
                "message": "Service already exists in database.",
                "service": {
                    "id": service.id,
                    "name": service.name,
                    "price": str(service.price),
                    "description": service.description
                }
            })

        service = Service.objects.create(
            name=name,
            description=description,
            price=price,
            duration=0
        )

        return JsonResponse({
            "success": True,
            "message": "Service saved to database successfully!",
            "service": {
                "id": service.id,
                "name": service.name,
                "price": str(service.price),
                "description": service.description
            }
        })

    except json.JSONDecodeError:

        return JsonResponse({
            "success": False,
            "message": "Invalid JSON data."
        })

    except Exception as e:

        return JsonResponse({
            "success": False,
            "message": str(e)
        })


# =========================================================
# BOOK APPOINTMENT
# =========================================================

@csrf_exempt
def book_appointment(request):

    if request.method != "POST":
        return JsonResponse({
            "success": False,
            "message": "Invalid request."
        })

    try:

        data = json.loads(request.body)

        customer_name = data.get(
            "customer_name",
            ""
        ).strip()

        phone = data.get(
            "phone",
            ""
        ).strip()

        date = data.get(
            "date",
            ""
        ).strip()

        time = data.get(
            "time",
            ""
        ).strip()

        payment_method = data.get(
            "payment_method",
            ""
        ).strip()

        services = data.get(
            "services",
            []
        )

        if not customer_name:

            return JsonResponse({
                "success": False,
                "message": "Customer name is required."
            })

        if not phone:

            return JsonResponse({
                "success": False,
                "message": "Phone number is required."
            })

        if not phone.isdigit() or len(phone) != 10:

            return JsonResponse({
                "success": False,
                "message": "Phone number must contain exactly 10 digits."
            })

        if not date:

            return JsonResponse({
                "success": False,
                "message": "Appointment date is required."
            })

        if not time:

            return JsonResponse({
                "success": False,
                "message": "Appointment time is required."
            })

        if not payment_method:

            return JsonResponse({
                "success": False,
                "message": "Payment method is required."
            })

        if not services or not isinstance(services, list):

            return JsonResponse({
                "success": False,
                "message": "Please select at least one service."
            })

        service_names = []

        total_amount = Decimal("0.00")

        for item in services:

            service_name = str(
                item.get(
                    "name",
                    "Service"
                )
            ).strip()

            price = Decimal(
                str(
                    item.get(
                        "price",
                        0
                    )
                )
            )

            quantity = int(
                item.get(
                    "quantity",
                    1
                )
            )

            if quantity < 1:
                quantity = 1

            service_names.append(
                service_name +
                " × " +
                str(quantity)
            )

            total_amount += (
                price * quantity
            )

        service_text = ", ".join(
            service_names
        )

        appointment = Appointment.objects.create(
            customer_name=customer_name,
            phone=phone,
            service=service_text,
            date=date,
            time=time,
            amount=total_amount,
            status="Booked",
            payment_status="Pending"
        )

        Payment.objects.create(
            customer_name=customer_name,
            amount=total_amount,
            payment_method=payment_method,
            payment_status="Pending"
        )

        return JsonResponse({
            "success": True,
            "message": "Appointment booked successfully!",
            "appointment": {
                "id": appointment.id,
                "customer_name": appointment.customer_name,
                "phone": appointment.phone,
                "service": appointment.service,
                "date": appointment.date,
                "time": appointment.time,
                "amount": str(
                    appointment.amount
                ),
                "status": appointment.status,
                "payment_status": appointment.payment_status,
                "payment_method": payment_method
            }
        })

    except json.JSONDecodeError:

        return JsonResponse({
            "success": False,
            "message": "Invalid JSON data."
        })

    except (
        InvalidOperation,
        ValueError,
        TypeError
    ):

        return JsonResponse({
            "success": False,
            "message": "Invalid service or price data."
        })

    except Exception as e:

        return JsonResponse({
            "success": False,
            "message": str(e)
        })


# =========================================================
# MARK PAYMENT AS PAID
# =========================================================

@csrf_exempt
def mark_payment_paid(request):

    if request.method != "POST":

        return JsonResponse({
            "success": False,
            "message": "Invalid request."
        })

    try:

        data = json.loads(request.body)

        appointment_id = data.get(
            "appointment_id"
        )

        if not appointment_id:

            return JsonResponse({
                "success": False,
                "message": "Appointment ID is required."
            })

        try:

            appointment = Appointment.objects.get(
                id=appointment_id
            )

        except Appointment.DoesNotExist:

            return JsonResponse({
                "success": False,
                "message": "Appointment not found."
            })

        if appointment.payment_status == "Paid":

            return JsonResponse({
                "success": True,
                "message": "Payment is already marked as paid.",
                "payment_status": "Paid"
            })

        appointment.payment_status = "Paid"

        appointment.save(
            update_fields=[
                "payment_status"
            ]
        )

        payment = Payment.objects.filter(
            customer_name=appointment.customer_name,
            amount=appointment.amount,
            payment_status="Pending"
        ).order_by("-id").first()

        if payment:

            payment.payment_status = "Paid"

            payment.save(
                update_fields=[
                    "payment_status"
                ]
            )

        return JsonResponse({
            "success": True,
            "message": "Payment marked as paid successfully!",
            "appointment_id": appointment.id,
            "payment_status": appointment.payment_status
        })

    except json.JSONDecodeError:

        return JsonResponse({
            "success": False,
            "message": "Invalid JSON data."
        })

    except Exception as e:

        return JsonResponse({
            "success": False,
            "message": str(e)
        })


# =========================================================
# SUBMIT FEEDBACK
# =========================================================

@csrf_exempt
def submit_feedback(request):

    if request.method != "POST":

        return JsonResponse({
            "success": False,
            "message": "Invalid request."
        })

    try:

        data = json.loads(request.body)

        rating = data.get(
            "rating",
            0
        )

        message = data.get(
            "message",
            ""
        ).strip()

        customer_name = data.get(
            "customer_name",
            "Customer"
        ).strip()

        if (
            not rating
            or int(rating) < 1
            or int(rating) > 5
        ):

            return JsonResponse({
                "success": False,
                "message": "Please select a valid rating."
            })

        if not message:

            return JsonResponse({
                "success": False,
                "message": "Please write your feedback."
            })

        Feedback.objects.create(
            customer_name=customer_name,
            rating=int(rating),
            message=message
        )

        return JsonResponse({
            "success": True,
            "message": "Thank you for your feedback!"
        })

    except json.JSONDecodeError:

        return JsonResponse({
            "success": False,
            "message": "Invalid data received."
        })

    except Exception as e:

        return JsonResponse({
            "success": False,
            "message": str(e)
        })


# =========================================================
# DASHBOARD DATA
# =========================================================

def dashboard_data(request):

    if request.method != "GET":

        return JsonResponse({
            "success": False,
            "message": "Invalid request."
        })

    users = User.objects.all()
    services = Service.objects.all()
    combos = Combo.objects.all()
    feedback = Feedback.objects.all()
    appointments = Appointment.objects.all()
    payments = Payment.objects.all()

    # -----------------------------------------------------
    # USERS
    # -----------------------------------------------------

    users_data = []

    for user in users:

        users_data.append({
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "phone": user.phone
        })

    # -----------------------------------------------------
    # SERVICES
    # -----------------------------------------------------

    services_data = []

    for service in services:

        services_data.append({
            "id": service.id,
            "name": service.name,
            "description": service.description,
            "price": str(
                service.price
            ),
            "duration": service.duration
        })

    # -----------------------------------------------------
    # COMBOS
    # -----------------------------------------------------

    combos_data = []

    for combo in combos:

        combos_data.append({
            "id": combo.id,
            "name": combo.name,
            "description": combo.description,
            "price": str(
                combo.price
            )
        })

    # -----------------------------------------------------
    # FEEDBACK
    # -----------------------------------------------------

    feedback_data = []

    for item in feedback:

        feedback_data.append({
            "id": item.id,
            "customer_name": item.customer_name,
            "rating": item.rating,
            "message": item.message
        })

    # -----------------------------------------------------
    # APPOINTMENTS
    # -----------------------------------------------------

    appointments_data = []

    for appointment in appointments:

        appointments_data.append({
            "id": appointment.id,
            "customer_name": appointment.customer_name,
            "phone": appointment.phone,
            "service": appointment.service,
            "date": appointment.date,
            "time": appointment.time,
            "amount": str(
                appointment.amount
            ),
            "status": appointment.status,
            "payment_status": appointment.payment_status
        })

    # -----------------------------------------------------
    # PAYMENTS
    # -----------------------------------------------------

    payments_data = []

    for payment in payments:

        payments_data.append({
            "id": payment.id,
            "customer_name": payment.customer_name,
            "amount": str(
                payment.amount
            ),
            "payment_method": payment.payment_method,
            "payment_status": payment.payment_status
        })

    # -----------------------------------------------------
    # TOTAL REVENUE
    # -----------------------------------------------------

    total_revenue = Decimal("0.00")

    for appointment in appointments:

        if appointment.payment_status == "Paid":

            total_revenue += appointment.amount

    # -----------------------------------------------------
    # RESPONSE
    # -----------------------------------------------------

    return JsonResponse({

        "success": True,

        "totalUsers": users.count(),

        "totalServices": services.count(),

        "totalCombos": combos.count(),

        "totalFeedback": feedback.count(),

        "totalAppointments": appointments.count(),

        "totalPayments": payments.count(),

        "totalRevenue": str(
            total_revenue
        ),

        "users": users_data,

        "services": services_data,

        "combos": combos_data,

        "feedback": feedback_data,

        "appointments": appointments_data,

        "payments": payments_data

    })
