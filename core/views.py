import json
from decimal import Decimal, InvalidOperation

from django.contrib.auth.hashers import check_password, make_password
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .models import User, Admin, Service, Appointment, Payment, Feedback, Combo


def _get_request_data(request):
    if request.body:
        try:
            parsed = json.loads(request.body.decode("utf-8"))
            if isinstance(parsed, dict):
                return parsed
        except (json.JSONDecodeError, UnicodeDecodeError):
            pass
    return request.POST


def _text(value):
    return "" if value is None else str(value).strip()


def _check_password(password, stored_password):
    if not stored_password:
        return False
    try:
        if check_password(password, stored_password):
            return True
    except Exception:
        pass
    # Compatibility with any old accounts that may still contain plaintext.
    return password == stored_password


def _decimal(value, default="0"):
    try:
        return Decimal(str(value if value not in (None, "") else default))
    except (InvalidOperation, ValueError, TypeError):
        return Decimal(default)


# PAGE VIEWS

def home_page(request): return render(request, "home.html")
def signup_page(request): return render(request, "signup.html")
def login_page(request): return render(request, "login.html")
def forgot_password_page(request): return render(request, "forgot-password.html")
def services_page(request): return render(request, "services.html")
def booking_page(request): return render(request, "booking.html")
def admin_page(request): return render(request, "admin.html")
def dashboard_page(request): return render(request, "dashboard.html")
def feedback_page(request): return render(request, "feedback.html")
def combo_page(request): return render(request, "combo.html")
def contact_page(request): return render(request, "contact.html")
def about_page(request): return render(request, "about.html")


@csrf_exempt
def register_user(request):
    if request.method != "POST":
        return JsonResponse({"success": False, "message": "Only POST request is allowed."}, status=405)
    try:
        data = _get_request_data(request)
        name = _text(data.get("name"))
        email = _text(data.get("email")).lower()
        phone = _text(data.get("phone"))
        password = _text(data.get("password"))
        if not name or not email or not phone or not password:
            return JsonResponse({"success": False, "message": "All fields are required."})
        if User.objects.filter(email=email).exists():
            return JsonResponse({"success": False, "message": "Email already registered."})
        if User.objects.filter(phone=phone).exists():
            return JsonResponse({"success": False, "message": "Phone number already registered."})
        user = User.objects.create(name=name, email=email, phone=phone, password=make_password(password))
        user_data = {"id": user.id, "name": user.name, "email": user.email, "phone": user.phone or ""}
        return JsonResponse({"success": True, "message": "Registration successful.", "user": user_data, **user_data})
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=500)


@csrf_exempt
def login_user(request):
    if request.method != "POST":
        return JsonResponse({"success": False, "message": "Only POST request is allowed."}, status=405)
    try:
        data = _get_request_data(request)
        email = _text(data.get("email")).lower()
        password = _text(data.get("password"))
        if not email or not password:
            return JsonResponse({"success": False, "message": "Email and password are required."})
        user = User.objects.filter(email=email).first()
        if not user or not _check_password(password, user.password):
            return JsonResponse({"success": False, "message": "Invalid email or password."})
        user_data = {"id": user.id, "name": user.name, "email": user.email, "phone": user.phone or ""}
        return JsonResponse({"success": True, "message": "Login successful.", "user": user_data, **user_data})
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=500)


@csrf_exempt
def reset_password(request):
    if request.method != "POST":
        return JsonResponse({"success": False, "message": "Only POST request is allowed."}, status=405)
    try:
        data = _get_request_data(request)
        email = _text(data.get("email")).lower()
        new_password = _text(data.get("new_password") or data.get("password"))
        if not email or not new_password:
            return JsonResponse({"success": False, "message": "Email and new password are required."})
        user = User.objects.filter(email=email).first()
        if not user:
            return JsonResponse({"success": False, "message": "User not found."})
        user.password = make_password(new_password)
        user.save(update_fields=["password"])
        return JsonResponse({"success": True, "message": "Password reset successfully."})
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=500)


@csrf_exempt
def admin_login(request):
    if request.method != "POST":
        return JsonResponse({"success": False, "message": "Only POST request is allowed."}, status=405)
    try:
        data = _get_request_data(request)
        username = _text(data.get("username"))
        password = _text(data.get("password"))
        if not username or not password:
            return JsonResponse({"success": False, "message": "Username and password are required."})
        admin = Admin.objects.filter(username=username).first()
        if not admin or not _check_password(password, admin.password):
            return JsonResponse({"success": False, "message": "Invalid admin username or password."})
        return JsonResponse({"success": True, "message": "Admin login successful.", "admin": {"id": admin.id, "username": admin.username}})
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=500)


@csrf_exempt
def add_service(request):
    if request.method != "POST":
        return JsonResponse({"success": False, "message": "Only POST request is allowed."}, status=405)
    try:
        data = _get_request_data(request)
        name = _text(data.get("name"))
        description = _text(data.get("description"))
        price_value = _decimal(data.get("price"))
        if not name:
            return JsonResponse({"success": False, "message": "Service name is required."})
        service = Service.objects.filter(name=name).first()
        if service:
            return JsonResponse({"success": True, "message": "Service already exists in database.", "service": {
                "id": service.id, "name": service.name, "description": service.description,
                "price": str(service.price), "duration": service.duration,
            }})
        service = Service.objects.create(name=name, description=description, price=price_value, duration=0)
        return JsonResponse({"success": True, "message": "Service added successfully.", "service": {
            "id": service.id, "name": service.name, "description": service.description,
            "price": str(service.price), "duration": service.duration,
        }})
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=500)


@csrf_exempt
def add_combo(request):
    if request.method != "POST":
        return JsonResponse({"success": False, "message": "Only POST request is allowed."}, status=405)
    try:
        data = _get_request_data(request)
        name = _text(data.get("name"))
        description = _text(data.get("description"))
        price_value = _decimal(data.get("price"))
        if not name:
            return JsonResponse({"success": False, "message": "Combo name is required."})
        combo = Combo.objects.filter(name=name).first()
        if combo:
            return JsonResponse({"success": True, "message": "Combo already exists in database.", "combo": {
                "id": combo.id, "name": combo.name, "description": combo.description, "price": str(combo.price)
            }})
        combo = Combo.objects.create(name=name, description=description, price=price_value)
        return JsonResponse({"success": True, "message": "Combo added successfully.", "combo": {
            "id": combo.id, "name": combo.name, "description": combo.description, "price": str(combo.price)
        }})
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=500)


@csrf_exempt
def book_appointment(request):
    if request.method != "POST":
        return JsonResponse({"success": False, "message": "Only POST request is allowed."}, status=405)
    try:
        data = _get_request_data(request)
        customer_name = _text(data.get("customer_name"))
        phone = _text(data.get("phone"))
        date = _text(data.get("date"))
        time = _text(data.get("time"))
        payment_method = _text(data.get("payment_method")) or "Not Selected"
        services = data.get("services", [])
        if not customer_name: return JsonResponse({"success": False, "message": "Customer name is required."})
        if not phone: return JsonResponse({"success": False, "message": "Phone number is required."})
        if not date: return JsonResponse({"success": False, "message": "Date is required."})
        if not time: return JsonResponse({"success": False, "message": "Time is required."})
        if not isinstance(services, list) or not services:
            return JsonResponse({"success": False, "message": "Please select at least one service."})
        names = []
        total = Decimal("0")
        for item in services:
            if not isinstance(item, dict):
                continue
            service_name = _text(item.get("name")) or "Service"
            price = _decimal(item.get("price"))
            try:
                quantity = max(1, int(item.get("quantity", 1)))
            except (TypeError, ValueError):
                quantity = 1
            names.append(f"{service_name} × {quantity}")
            total += price * quantity
        if not names:
            return JsonResponse({"success": False, "message": "Please select at least one service."})
        appointment = Appointment.objects.create(
            customer_name=customer_name, phone=phone, service=", ".join(names),
            date=date, time=time, amount=total, status="Booked", payment_status="Pending"
        )
        Payment.objects.create(customer_name=customer_name, amount=total, payment_method=payment_method, payment_status="Pending")
        return JsonResponse({"success": True, "message": "Appointment booked successfully.", "appointment": {
            "id": appointment.id, "customer_name": appointment.customer_name, "phone": appointment.phone,
            "service": appointment.service, "date": appointment.date, "time": appointment.time,
            "amount": str(appointment.amount), "status": appointment.status, "payment_status": appointment.payment_status,
        }})
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=500)


@csrf_exempt
def mark_payment_paid(request):
    if request.method != "POST":
        return JsonResponse({"success": False, "message": "Only POST request is allowed."}, status=405)
    try:
        data = _get_request_data(request)
        appointment_id = data.get("appointment_id")
        if not appointment_id:
            return JsonResponse({"success": False, "message": "Appointment ID is required."})
        appointment = Appointment.objects.filter(id=appointment_id).first()
        if not appointment:
            return JsonResponse({"success": False, "message": "Appointment not found."})
        appointment.payment_status = "Paid"
        appointment.save(update_fields=["payment_status"])
        payment = Payment.objects.filter(customer_name=appointment.customer_name, amount=appointment.amount).order_by("-id").first()
        if payment:
            payment.payment_status = "Paid"
            payment.save(update_fields=["payment_status"])
        return JsonResponse({"success": True, "message": "Payment marked as paid."})
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=500)


@csrf_exempt
def submit_feedback(request):
    if request.method != "POST":
        return JsonResponse({"success": False, "message": "Only POST request is allowed."}, status=405)
    try:
        data = _get_request_data(request)
        customer_name = _text(data.get("customer_name"))
        message = _text(data.get("message"))
        try:
            rating = int(data.get("rating", 0))
        except (TypeError, ValueError):
            rating = 0
        if not customer_name:
            return JsonResponse({"success": False, "message": "Customer name is required."})
        rating = max(0, min(5, rating))
        feedback = Feedback.objects.create(customer_name=customer_name, rating=rating, message=message)
        return JsonResponse({"success": True, "message": "Feedback submitted successfully.", "feedback": {
            "id": feedback.id, "customer_name": feedback.customer_name, "rating": feedback.rating, "message": feedback.message
        }})
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=500)


def dashboard_data(request):
    try:
        users = User.objects.all().order_by("id")
        services = Service.objects.all().order_by("id")
        combos = Combo.objects.all().order_by("id")
        feedback = Feedback.objects.all().order_by("id")
        appointments = Appointment.objects.all().order_by("id")
        payments = Payment.objects.all().order_by("id")
        total_revenue = sum((a.amount for a in appointments if a.payment_status.lower() == "paid"), Decimal("0"))
        return JsonResponse({
            "success": True,
            "totalUsers": users.count(), "totalServices": services.count(), "totalCombos": combos.count(),
            "totalFeedback": feedback.count(), "totalAppointments": appointments.count(), "totalPayments": payments.count(),
            "totalRevenue": str(total_revenue),
            "users": [{"id": u.id, "name": u.name, "email": u.email, "phone": u.phone or ""} for u in users],
            "services": [{"id": s.id, "name": s.name, "description": s.description, "price": str(s.price), "duration": s.duration} for s in services],
            "combos": [{"id": c.id, "name": c.name, "description": c.description, "price": str(c.price)} for c in combos],
            "feedback": [{"id": f.id, "customer_name": f.customer_name, "rating": f.rating, "message": f.message} for f in feedback],
            "appointments": [{"id": a.id, "customer_name": a.customer_name, "phone": a.phone, "service": a.service, "date": a.date, "time": a.time, "amount": str(a.amount), "status": a.status, "payment_status": a.payment_status} for a in appointments],
            "payments": [{"id": p.id, "customer_name": p.customer_name, "amount": str(p.amount), "payment_method": p.payment_method, "payment_status": p.payment_status} for p in payments],
        })
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=500)