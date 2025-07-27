from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegisterForm, LoginForm, TourPackageForm, BookingForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import CustomUser, TourPackage, Booking
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import razorpay
from django.conf import settings

# Role checks
def is_vendor(user):
    return user.is_authenticated and user.role == 'vendor'

def is_user(user):
    return user.is_authenticated and user.role == 'user'

# Home
def home(request):
    return render(request, 'core/home.html')

# Register
def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'core/register.html', {'form': form})

# Login
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.role == 'vendor':
                return redirect('vendor_dashboard')
            else:
                return redirect('user_dashboard')
    else:
        form = LoginForm()
    return render(request, 'core/login.html', {'form': form})

# Logout
def logout_view(request):
    logout(request)
    return redirect('login')

# User Dashboard
@login_required
@user_passes_test(is_user)
def user_dashboard(request):
    from datetime import date
    packages = TourPackage.objects.filter(is_approved=True, expiry_date__gte=date.today())
    return render(request, 'core/user_dashboard.html', {'packages': packages})


# Vendor Dashboard
@login_required
@user_passes_test(is_vendor)
def vendor_dashboard(request):
    return render(request, 'core/vendor_dashboard.html')

# Vendor View Own Packages
@login_required
@user_passes_test(is_vendor)
def vendor_packages(request):
    packages = TourPackage.objects.filter(vendor=request.user)
    return render(request, 'core/vendor_packages.html', {'packages': packages})

# Vendor: Add Package
@login_required
@user_passes_test(is_vendor)
def add_package(request):
    if request.method == 'POST':
        form = TourPackageForm(request.POST, request.FILES)
        if form.is_valid():
            package = form.save(commit=False)
            package.vendor = request.user
            form.save()
            return redirect('vendor_packages')
    else:
        form = TourPackageForm()
    return render(request, 'core/add_package.html', {'form': form})

# Vendor Edit Package
@login_required
@user_passes_test(is_vendor)
def edit_package(request, pk):
    package = get_object_or_404(TourPackage, pk=pk, vendor=request.user)
    if request.method == 'POST':
        form = TourPackageForm(request.POST, request.FILES, instance=package)
        if form.is_valid():
            form.save()
            return redirect('vendor_packages')
    else:
        form = TourPackageForm(instance=package)
    return render(request, 'core/edit_package.html', {'form': form})

# Vendor Delete Package
@login_required
@user_passes_test(is_vendor)
def delete_package(request, pk):
    package = get_object_or_404(TourPackage, pk=pk, vendor=request.user)
    package.delete()
    return redirect('vendor_packages')

# Browse Packages User
from django.utils import timezone
from .models import TourPackage

@login_required
@user_passes_test(is_user)
def browse_packages(request):
    today = timezone.now().date()
    packages = TourPackage.objects.filter(is_approved=True, expiry_date__gt=today)
    return render(request, 'core/browse_packages.html', {'packages': packages})


# Package Detail
@login_required
def package_detail(request, pk):
    package = get_object_or_404(TourPackage, pk=pk)
    return render(request, 'core/package_detail.html', {'package': package})

# Book Package
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import TourPackage, Booking
from .forms import BookingForm


@login_required
def book_package(request, pk):
    package = get_object_or_404(TourPackage, id=pk, is_approved=True)

    # Check if the package is expired
    if package.expiry_date <= timezone.now().date():
        return render(request, 'core/package_expired.html', {'package': package})

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.package = package
            booking.save()
            return redirect('payment_page', booking_id=booking.id)
    else:
        form = BookingForm()

    return render(request, 'core/book_package.html', {'form': form, 'package': package})


# Razorpay Payment
@login_required
@user_passes_test(is_user)
def payment_page(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id, user=request.user)

    amount = int(booking.package.price * 100)  # in paisa

    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    payment = client.order.create({
        'amount': amount,
        'currency': 'INR',
        'payment_capture': '1'
    })

    return render(request, 'core/payment_page.html', {
        'booking': booking,
        'payment': payment,
        'key': settings.RAZORPAY_KEY_ID
    })

# Payment Success
@login_required
def payment_success(request):
    return render(request, 'core/payment_success.html')

# User Bookings
@login_required
@user_passes_test(is_user)
def user_bookings(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'core/user_bookings.html', {'bookings': bookings})

# Vendor Bookings
@login_required
@user_passes_test(is_vendor)
def vendor_bookings(request):
    bookings = Booking.objects.filter(package__vendor=request.user)
    return render(request, 'core/vendor_bookings.html', {'bookings': bookings})

# Download Invoice
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import io


@login_required
def download_invoice(request, booking_id):
    booking = Booking.objects.get(id=booking_id, user=request.user)
    template_path = 'core/invoice.html'
    context = {'booking': booking}

    template = get_template(template_path)
    html = template.render(context)

    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode('UTF-8')), result)

    if not pdf.err:
        response = HttpResponse(result.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename=invoice_{booking_id}.pdf'
        return response
    else:
        return HttpResponse('Error generating PDF')

