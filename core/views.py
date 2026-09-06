from decimal import Decimal, InvalidOperation

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .models import (
    User,
    Admin,
    Service,
    Appointment,
    Payment,
    Feedback,
    Combo,
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
    return render(request, "forgot-password.html")


def services_page(request):
    return render(request, "services.html")


def booking_page(request):
    return render(request, "booking.html")


def admin_page(request):
    return render(request, "admin.html")


def dashboard_page(request):
    return render(request, "dashboard.html")


def feedback_page(request):
    return render(request, "feedback.html")


def combo_page(request):
    return render(request, "combo.html")


def contact_page(request):
    return render(request, "contact.html")


def about_page(request):
    return render(request, "about.html")


# =========================================================
# USER REGISTRATION
# =========================================================

@csrf_exempt
def register_user(request):

    if request.method != "POST":
        return JsonResponse({
            "success": False,
            "message": "Only POST request is allowed."
        }, status=405)

    try:
        data = request.POST

        name = data.get("name", "").strip()
        email = data.get("email", "").strip().lower()
        phone = data.get("phone", "").strip()
        password = data.get("password", "").strip()

        if not name or not email or not phone or not password:
            return JsonResponse({
                "success": False,
                "message": "All fields are required."
            })

        # Check duplicate email
        if User.objects.filter(email=email).exists():
            return JsonResponse({
                "success": False,
                "message": "Email already registered."
            })

        # Check duplicate phone
        if User.objects.filter(phone=phone).exists():
            return JsonResponse({
                "success": False,
                "message": "Phone number already registered."
            })

        user = User.objects.create(
            name=name,
            email=email,
            phone=phone,
            password=password
        )

        return JsonResponse({
            "success": True,
            "message": "Registration successful.",
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "phone": user.phone,
            }
        })

    except Exception as e:
        return JsonResponse({
            "success": False,
            "message": str(e)
        }, status=500)


# =========================================================
# USER LOGIN
# =========================================================

@csrf_exempt
def login_user(request):

    if request.method != "POST":
        return JsonResponse({
            "success": False,
            "message": "Only POST request is allowed."
        }, status=405)

    try:
        data = request.POST

        email = data.get("email", "").strip().lower()
        password = data.get("password", "").strip()

        if not email or not password:
            return JsonResponse({
                "success": False,
                "message": "Email and password are required."
            })

        user = User.objects.filter(
            email=email,
            password=password
        ).first()

        if not user:
            return JsonResponse({
                "success": False,
                "message": "Invalid email or password."
            })

        return JsonResponse({
            "success": True,
            "message": "Login successful.",
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "phone": user.phone,
            }
        })

    except Exception as e:
        return JsonResponse({
            "success": False,
            "message": str(e)
        }, status=500)


# =========================================================
# RESET PASSWORD
# =========================================================

@csrf_exempt
def reset_password(request):

    if request.method != "POST":
        return JsonResponse({
            "success": False,
            "message": "Only POST request is allowed."
        }, status=405)

    try:
        data = request.POST

        email = data.get("email", "").strip().lower()
        new_password = data.get("password", "").strip()

        if not email or not new_password:
            return JsonResponse({
                "success": False,
                "message": "Email and new password are required."
            })

        user = User.objects.filter(email=email).first()

        if not user:
            return JsonResponse({
                "success": False,
                "message": "User not found."
            })

        user.password = new_password
        user.save()

        return JsonResponse({
            "success": True,
            "message": "Password reset successfully."
        })

    except Exception as e:
        return JsonResponse({
            "success": False,
            "message": str(e)
        }, status=500)


# =========================================================
# ADMIN LOGIN
# =========================================================

@csrf_exempt
def admin_login(request):

    if request.method != "POST":
        return JsonResponse({
            "success": False,
            "message": "Only POST request is allowed."
        }, status=405)

    try:
        data = request.POST

        username = data.get("username", "").strip()
        password = data.get("password", "").strip()

        if not username or not password:
            return JsonResponse({
                "success": False,
                "message": "Username and password are required."
            })

        admin = Admin.objects.filter(
            username=username,
            password=password
        ).first()

        if not admin:
            return JsonResponse({
                "success": False,
                "message": "Invalid admin username or password."
            })

        return JsonResponse({
            "success": True,
            "message": "Admin login successful.",
            "admin": {
                "id": admin.id,
                "username": admin.username
            }
        })

    except Exception as e:
        return JsonResponse({
            "success": False,
            "message": str(e)
        }, status=500)


# =========================================================
# ADD SERVICE
# =========================================================

@csrf_exempt
def add_service(request):

    if request.method != "POST":
        return JsonResponse({
            "success": False,
            "message": "Only POST request is allowed."
        }, status=405)

    try:
        data = request.POST

        name = data.get("name", "").strip()
        description = data.get("description", "").strip()
        price = data.get("price", "0").strip()

        if not name:
            return JsonResponse({
                "success": False,
                "message": "Service name is required."
            })

        if Service.objects.filter(name=name).exists():
            service = Service.objects.filter(name=name).first()

            return JsonResponse({
                "success": True,
                "message": "Service already exists in database.",
                "service": {
                    "id": service.id,
                    "name": service.name,
                    "description": service.description,
                    "price": str(service.price),
                    "duration": service.duration,
                }
            })

        try:
            price_value = Decimal(price)
        except (InvalidOperation, ValueError):
            price_value = Decimal("0")

        service = Service.objects.create(
            name=name,
            description=description,
            price=price_value,
            duration=0
        )

        return JsonResponse({
            "success": True,
            "message": "Service added successfully.",
            "service": {
                "id": service.id,
                "name": service.name,
                "description": service.description,
                "price": str(service.price),
                "duration": service.duration,
            }
        })

    except Exception as e:
        return JsonResponse({
            "success": False,
            "message": str(e)
        }, status=500)


# =========================================================
# ADD COMBO
# =========================================================

@csrf_exempt
def add_combo(request):

    if request.method != "POST":
        return JsonResponse({
            "success": False,
            "message": "Only POST request is allowed."
        }, status=405)

    try:
        data = request.POST

        name = data.get("name", "").strip()
        description = data.get("description", "").strip()
        price = data.get("price", "0").strip()

        if not name:
            return JsonResponse({
                "success": False,
                "message": "Combo name is required."
            })

        # Check whether combo already exists
        combo = Combo.objects.filter(name=name).first()

        if combo:
            return JsonResponse({
                "success": True,
                "message": "Combo already exists in database.",
                "combo": {
                    "id": combo.id,
                    "name": combo.name,
                    "description": combo.description,
                    "price": str(combo.price),
                }
            })

        try:
            price_value = Decimal(price)
        except (InvalidOperation, ValueError):
            price_value = Decimal("0")

        combo = Combo.objects.create(
            name=name,
            description=description,
            price=price_value
        )

        return JsonResponse({
            "success": True,
            "message": "Combo added successfully.",
            "combo": {
                "id": combo.id,
                "name": combo.name,
                "description": combo.description,
                "price": str(combo.price),
            }
        })

    except Exception as e:
        return JsonResponse({
            "success": False,
            "message": str(e)
        }, status=500)


# =========================================================
# BOOK APPOINTMENT
# =========================================================

@csrf_exempt
def book_appointment(request):

    if request.method != "POST":
        return JsonResponse({
            "success": False,
            "message": "Only POST request is allowed."
        }, status=405)

    try:
        import json

        if request.body:
            data = json.loads(request.body.decode("utf-8"))
        else:
            data = request.POST

        customer_name = str(
            data.get("customer_name", "")
        ).strip()

        phone = str(
            data.get("phone", "")
        ).strip()

        date = str(
            data.get("date", "")
        ).strip()

        time = str(
            data.get("time", "")
        ).strip()

        services = data.get("services", [])

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

        if not date:
            return JsonResponse({
                "success": False,
                "message": "Date is required."
            })

        if not time:
            return JsonResponse({
                "success": False,
                "message": "Time is required."
            })

        if not isinstance(services, list) or len(services) == 0:
            return JsonResponse({
                "success": False,
                "message": "Please select at least one service."
            })

        service_names = []
        total_amount = Decimal("0")

        for item in services:

            service_name = str(
                item.get("name", "Service")
            ).strip()

            price = Decimal(
                str(item.get("price", 0))
            )

            quantity = int(
                item.get("quantity", 1)
            )

            service_names.append(
                service_name + " × " + str(quantity)
            )

            total_amount += price * quantity

        service_text = ", ".join(service_names)

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
            payment_method="Not Selected",
            payment_status="Pending"
        )

        return JsonResponse({
            "success": True,
            "message": "Appointment booked successfully.",
            "appointment": {
                "id": appointment.id,
                "customer_name": appointment.customer_name,
                "phone": appointment.phone,
                "service": appointment.service,
                "date": appointment.date,
                "time": appointment.time,
                "amount": str(appointment.amount),
                "status": appointment.status,
                "payment_status": appointment.payment_status,
            }
        })

    except Exception as e:
        return JsonResponse({
            "success": False,
            "message": str(e)
        }, status=500)


# =========================================================
# MARK PAYMENT AS PAID
# =========================================================

@csrf_exempt
def mark_payment_paid(request):

    if request.method != "POST":
        return JsonResponse({
            "success": False,
            "message": "Only POST request is allowed."
        }, status=405)

    try:
        import json

        if request.body:
            data = json.loads(request.body.decode("utf-8"))
        else:
            data = request.POST

        appointment_id = data.get("appointment_id")

        if not appointment_id:
            return JsonResponse({
                "success": False,
                "message": "Appointment ID is required."
            })

        appointment = Appointment.objects.filter(
            id=appointment_id
        ).first()

        if not appointment:
            return JsonResponse({
                "success": False,
                "message": "Appointment not found."
            })

        appointment.payment_status = "Paid"
        appointment.save()

        Payment.objects.filter(
            customer_name=appointment.customer_name,
            amount=appointment.amount
        ).update(
            payment_status="Paid",
            payment_method="Online"
        )

        return JsonResponse({
            "success": True,
            "message": "Payment marked as paid."
        })

    except Exception as e:
        return JsonResponse({
            "success": False,
            "message": str(e)
        }, status=500)


# =========================================================
# SUBMIT FEEDBACK
# =========================================================

@csrf_exempt
def submit_feedback(request):

    if request.method != "POST":
        return JsonResponse({
            "success": False,
            "message": "Only POST request is allowed."
        }, status=405)

    try:
        data = request.POST

        customer_name = data.get(
            "customer_name", ""
        ).strip()

        rating = data.get(
            "rating", "0"
        ).strip()

        message = data.get(
            "message", ""
        ).strip()

        if not customer_name:
            return JsonResponse({
                "success": False,
                "message": "Customer name is required."
            })

        feedback = Feedback.objects.create(
            customer_name=customer_name,
            rating=int(rating),
            message=message
        )

        return JsonResponse({
            "success": True,
            "message": "Feedback submitted successfully.",
            "feedback": {
                "id": feedback.id,
                "customer_name": feedback.customer_name,
                "rating": feedback.rating,
                "message": feedback.message,
            }
        })

    except Exception as e:
        return JsonResponse({
            "success": False,
            "message": str(e)
        }, status=500)


# =========================================================
# DASHBOARD DATA
# =========================================================

def dashboard_data(request):

    try:

        users = User.objects.all()
        services = Service.objects.all()
        combos = Combo.objects.all()
        feedback = Feedback.objects.all()
        appointments = Appointment.objects.all()
        payments = Payment.objects.all()

        # -------------------------------------------------
        # USERS
        # -------------------------------------------------

        users_data = []

        for user in users:
            users_data.append({
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "phone": user.phone or "",
            })

        # -------------------------------------------------
        # SERVICES
        # -------------------------------------------------

        services_data = []

        for service in services:
            services_data.append({
                "id": service.id,
                "name": service.name,
                "description": service.description,
                "price": str(service.price),
                "duration": service.duration,
            })

        # -------------------------------------------------
        # COMBOS
        # -------------------------------------------------

        combos_data = []

        for combo in combos:
            combos_data.append({
                "id": combo.id,
                "name": combo.name,
                "description": combo.description,
                "price": str(combo.price),
            })

        # -------------------------------------------------
        # FEEDBACK
        # -------------------------------------------------

        feedback_data = []

        for item in feedback:
            feedback_data.append({
                "id": item.id,
                "customer_name": item.customer_name,
                "rating": item.rating,
                "message": item.message,
            })

        # -------------------------------------------------
        # APPOINTMENTS
        # -------------------------------------------------

        appointments_data = []

        for appointment in appointments:
            appointments_data.append({
                "id": appointment.id,
                "customer_name": appointment.customer_name,
                "phone": appointment.phone,
                "service": appointment.service,
                "date": appointment.date,
                "time": appointment.time,
                "amount": str(appointment.amount),
                "status": appointment.status,
                "payment_status": appointment.payment_status,
            })

        # -------------------------------------------------
        # PAYMENTS
        # -------------------------------------------------

        payments_data = []

        for payment in payments:
            payments_data.append({
                "id": payment.id,
                "customer_name": payment.customer_name,
                "amount": str(payment.amount),
                "payment_method": payment.payment_method,
                "payment_status": payment.payment_status,
            })

        # -------------------------------------------------
        # REVENUE
        # -------------------------------------------------

        total_revenue = Decimal("0")

        for appointment in appointments:
            if appointment.payment_status.lower() == "paid":
                total_revenue += appointment.amount

        # -------------------------------------------------
        # FINAL RESPONSE
        # -------------------------------------------------

        return JsonResponse({
            "success": True,

            "totalUsers": users.count(),
            "totalServices": services.count(),
            "totalCombos": combos.count(),
            "totalFeedback": feedback.count(),
            "totalAppointments": appointments.count(),
            "totalPayments": payments.count(),

            "totalRevenue": str(total_revenue),

            "users": users_data,
            "services": services_data,
            "combos": combos_data,
            "feedback": feedback_data,
            "appointments": appointments_data,
            "payments": payments_data,
        })

    except Exception as e:

        return JsonResponse({
            "success": False,
            "message": str(e)
        }, status=500)