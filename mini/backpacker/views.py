
from django.shortcuts import render, redirect
from .models import Package, CustomUser, Agent, book
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .forms import AgentSignUpForm, PackageForm, UserSignUpForm, AgentSignUpForm, AgentDetailForm
from django.contrib.auth.decorators import login_required
from .decorators import agent_only
# Create your views here.


def index(request):
    if request.user.is_authenticated:
        return redirect('package')
    return render(request, 'backpacker/index.html')


def user_signup(request):
    form = UserSignUpForm

    context = {
        'form': form

    }
    if request.method == 'POST':
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('package')
        else:
            messages.error(request, 'An error occurred during registration')
            return redirect('signup')
    else:
        return render(request, "backpacker/signup.html", context)


def agent_signup(request):
    profile_form = AgentSignUpForm
    detail_form = AgentDetailForm
    context = {
        'profile_form': profile_form,
        'detail_form': detail_form
    }
    if request.method == 'POST':
        profile_form = AgentSignUpForm(request.POST)
        detail_form = AgentDetailForm(request.POST)
        if all((profile_form.is_valid(), detail_form.is_valid())):
            profile = profile_form.save()
            detail = detail_form.save(commit=False)
            detail.User = profile
            detail.save()
            return redirect('index')

    return render(request, "backpacker/agent_signup.html", context)


def login_page(request):
    if request.user.is_authenticated:
        return redirect('package')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user = CustomUser.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
        else:
            messages.error(
                request, 'Username OR password is  not correct ,recheck and try again')
            return redirect('login')
        if user.is_customer == True:
            return redirect('package')
        elif user.is_agent == True:
            return redirect('agent_packages')

    return render(request, 'backpacker/login.html')


def logoutUser(request):
    logout(request)
    return redirect('index')


def is_valid_queryparam(param):
    return param != '' and param is not None


@login_required(login_url='login')
def package(request):
    packages = Package.objects.all()
    agents = Agent.objects.all()
    destination = request.GET.get('destination')
    departure = request.GET.get('departure')
    min_cost = request.GET.get('min_cost')
    max_cost = request.GET.get('max_cost')
    min_date = request.GET.get('min_date')
    max_date = request.GET.get('max_date')
    agent = request.GET.get('agent')
    min_dur = request.GET.get('min_dur')
    max_dur = request.GET.get('max_dur')

    if is_valid_queryparam(destination):
        packages = packages.filter(Location__icontains=destination)

    if is_valid_queryparam(departure):
        packages = packages.filter(dloc__icontains=departure)
    if is_valid_queryparam(min_cost):
        packages = packages.filter(cost__gte=min_cost)
    if is_valid_queryparam(max_cost):
        packages = packages.filter(cost__lte=max_cost)
    if is_valid_queryparam(min_date):
        packages = packages.filter(ddate__gte=min_date)
    if is_valid_queryparam(max_date):
        packages = packages.filter(ddate__lte=max_date)
    if is_valid_queryparam(agent) and agent != 'Choose...':
        packages = packages.filter(agent__name=agent)
    if is_valid_queryparam(min_dur):
        packages = packages.filter(duration__gte=min_dur)
    if is_valid_queryparam(max_dur):
        packages = packages.filter(duration__lte=max_dur)
    context = {
        'packages': packages,
        'agents': agents
    }
    return render(request, 'backpacker/contents.html', context)


@login_required(login_url='login')
def package_details(request, pk):
    package = Package.objects.get(id=pk)
    context = {'package': package}
    if request.method == "POST":

        nos = int(request.POST.get('nos'))
        if nos >= 1:
            price = nos*package.cost
            user = request.user
            package_name = package
            agent_name = package.agent
            books = book.objects.create(user=user, package=package_name, price=price,
                                        nos=nos, agent=agent_name, status=True)
            package.slots = package.slots-nos
            package.save()
            request.session['book_id'] = books.id

            return redirect('booking_success')
        else:
            messages.error(request, 'An error occured')

    return render(request, 'backpacker/package_details.html', context)


@login_required(login_url='login')
def booking_success(request):
    bookid = request.session['book_id']
    order = book.objects.get(id=bookid)
    context = {
        'order': order
    }

    return render(request, 'backpacker/booking_success.html', context)


@login_required(login_url='login')
def bookinglist(request):
    user = request.user
    order = book.objects.filter(user=user)
    context = {
        'order': order
    }

    return render(request, 'backpacker/bookinglist.html', context)


def agent_packages(request):
    user = request.user
    age = Agent.objects.get(User=user)
    pack = Package.objects.filter(agent=age)

    context = {
        'pack': pack
    }
    return render(request, "backpacker/agent_packages.html", context)


@login_required(login_url='login')
@agent_only
def create_package(request):
    form = PackageForm
    context = {
        'form': form
    }
    if request.method == 'POST':
        form = PackageForm(request.POST)
        if form.is_valid():
            package = form.save()
            return redirect('package')
        else:
            messages.error(request, 'An error occurred during registration')
            return redirect('signup')
    return render(request, "backpacker/create_package.html", context)
