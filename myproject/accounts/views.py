from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm, LoginForm


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)  # получаем данные из формы
        if form.is_valid():              # проверяем их
            user = form.save()           # сохраняем пользователя в БД
            login(request, user)         # сразу логиним
            return redirect('home')      # перенаправляем на главную
    else:
        form = SignUpForm()              # если GET-запрос, просто показываем форму

    return render(request, 'accounts/signup.html', {'form': form})



def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")   # Измени на твой URL
    else:
        form = LoginForm()

    return render(request, "accounts/login.html", {"form": form})


def logout_view(request):
    logout(request)               # разлогиниваем пользователя
    return redirect('login')      # перенаправляем на страницу логина
