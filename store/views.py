from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Attraction, Review, Region, Booking


def home(request):
    # Featured attractions for carousel (random or first few)
    featured = Attraction.objects.all()[:5]

    # Regions with 3 famous places each
    regions = Region.objects.all()
    region_attractions = []
    for region in regions:
        top_places = Attraction.objects.filter(region=region)[:3]
        region_attractions.append((region, top_places))

    context = {
        "featured": featured,
        "region_attractions": region_attractions,
    }
    return render(request, "store/home.html", context)

def about(request):
    return render(request, 'store/about.html')

@login_required
def contact(request):
    if request.method == 'POST':
        messages.success(request, "Message sent successfully!")
        return redirect('contact')
    return render(request, 'store/contact.html')

def attractions_list(request):
    attractions = Attraction.objects.all()
    return render(request, 'store/attractions_list.html', {'attractions': attractions})

def attraction_detail(request, slug):
    attraction = Attraction.objects.get(slug=slug)
    reviews = Review.objects.filter(attraction=attraction)
    
    if request.method == 'POST' and request.user.is_authenticated:
        content = request.POST.get('review')
        Review.objects.create(user=request.user, attraction=attraction, content=content)
        messages.success(request, "Review added successfully!")
        return redirect('attraction_detail', slug=slug)
    
    return render(request, 'store/attraction_detail.html', {'attraction': attraction, 'reviews': reviews})

# ---------- AUTH ----------
def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists!')
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, 'Account created successfully! Please log in.')
            return redirect('signin')
    return render(request, 'store/signup.html')

def signin_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials.')
    return render(request, 'store/signin.html')

def signout_view(request):
    logout(request)
    messages.info(request, 'Logged out successfully.')
    return redirect('home')


@login_required
def book_attraction(request, slug):
    attraction = get_object_or_404(Attraction, slug=slug)
    if request.method == "POST":
        visit_date = request.POST.get("visit_date")
        tickets = int(request.POST.get("tickets", 1))
        total = attraction.ticket_price * tickets

        Booking.objects.create(
            user=request.user,
            attraction=attraction,
            visit_date=visit_date,
            number_of_tickets=tickets,
            total_price=total
        )
        messages.success(request, "✅ Booking confirmed!")
        return redirect('my_bookings')

    return render(request, 'store/book_attractions.html', {"attraction": attraction})

@login_required
def my_bookings(request):
    confirmed = Booking.objects.filter(user=request.user, status="CONFIRMED")
    cancelled = Booking.objects.filter(user=request.user, status="CANCELLED")
    return render(request, 'store/my_bookings.html', {"confirmed": confirmed, "cancelled": cancelled})

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    booking.status = "CANCELLED"
    booking.save()
    messages.info(request, "❌ Booking canceled.")
    return redirect('my_bookings')