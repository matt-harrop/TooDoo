from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .forms import ToDoCreationForm
from .models import ToDo
from django.utils import timezone
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'todo/home.html')


def sign_up_user(request):
    if request.method == 'GET':
        return render(request, 'todo/sign_up_user.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('current_to_dos')
            except IntegrityError:
                return render(request, 'todo/sign_up_user.html', {
                    'form': UserCreationForm(),
                    'error': 'Username supplied is not available - please select another.'
                })
        else:
            # Tell the use that their passwords did not match.
            return render(request, 'todo/sign_up_user.html', {
                'form': UserCreationForm(),
                'error': 'Passwords supplied did not match.'
            })


def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return render(request, 'todo/home.html',
                      {'form': UserCreationForm(), 'message': 'You have been logged out successfully.'})


def login_user(request):
    if request.method == 'GET':
        return render(request, 'todo/login.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'todo/login.html',
                          {'form': AuthenticationForm(), 'error': 'Username and password combination is invalid.'})
        else:
            login(request, user)
            return render(request, 'todo/current.html')


@login_required
def current_to_dos(request):
    to_dos = ToDo.objects.filter(user=request.user, completed_at__isnull=True)
    return render(request, 'todo/current.html', {'to_dos': to_dos})


@login_required
def create_to_do(request):
    if request.method == 'GET':
        return render(request, 'todo/create.html', {'form': ToDoCreationForm()})
    else:
        try:
            form = ToDoCreationForm(request.POST)
            new_to_do = form.save(commit=False)
            new_to_do.user = request.user
            new_to_do.save()
            return redirect('current_to_dos')
        except ValueError:
            return render(request, 'todo/create.html', {'form': ToDoCreationForm(),
                                                        'error': 'Some data submitted was invalid; please correct and try again.'})


@login_required
def view_to_do(request, todo_pk):
    todo = get_object_or_404(ToDo, pk=todo_pk, user=request.user)
    if request.method == 'GET':
        form = ToDoCreationForm(instance=todo)
        return render(request, 'todo/view_to_do.html', {'todo': todo, 'form': form})
    else:
        try:
            form = ToDoCreationForm(request.POST, instance=todo)
            form.save()
            return redirect('current_to_dos')
        except ValueError:
            return render(request, 'todo/view_to_do.html', {'todo': todo, 'form': form,
                                                            'error': 'Some data submitted was invalid; please correct and try again.'})


@login_required
def complete_to_do(request, todo_pk):
    todo = get_object_or_404(ToDo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.completed_at = timezone.now()
        todo.save()
        return redirect('current_to_dos')


@login_required
def delete_to_do(request, todo_pk):
    todo = get_object_or_404(ToDo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('current_to_dos')


@login_required
def completed_to_dos(request):
    to_dos = ToDo.objects.filter(user=request.user, completed_at__isnull=False).order_by('-completed_at')
    return render(request, 'todo/completed.html', {'to_dos': to_dos})
