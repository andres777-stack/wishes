
from datetime import datetime
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.urls import reverse
from acceso.models import User
from theWishingApp.forms import WishForm
from theWishingApp.models import Wish
from django.db.models import Count

def index(request):
    if request.method == 'GET':
        if 'usuario' not in request.session:
            messages.error(request, 'No estás logeado')
            return redirect(reverse('acceso:index'))
        else:
            print(request.session['usuario'])
            user = request.session['usuario']

            context = {
            #'allwishes' : Wish.objects.all(),
            'usuario' : User.objects.get(id = user['id']),
            'allwishes' : Wish.objects.annotate(numero_likes = Count('users_who_liked'))

            #'equipos_mas_doce' : Team.objects.annotate(player_count = Count('all_players'))
            }
            return render(request, 'deseos/index.html', context)

def new(request):
    if request.method == 'GET':
        if 'usuario' not in request.session:
            messages.error(request, 'No estás logeado')
            return redirect(reverse('acceso:index'))
        else:
            print(request.session['usuario'])
            user = request.session['usuario']
            context = {
            'formModel': WishForm(),
            'usuario' : User.objects.get(id = user['id']),
            
            }
            return render(request, 'deseos/form.html', context)
    
    if request.method == 'POST':
        print(request.POST)
        form = WishForm(request.POST)
        if form.is_valid():
            #hasta aquí sólo se están haciendo las validaciones
            usuario = request.session['usuario']
            print(usuario)
            id = usuario['id']
            nombre = usuario['nombre']
            print(id)
            user = User.objects.get(id=id)
            print(user)
            wish = Wish.objects.create(
                wisher = nombre, 
                item = form.cleaned_data['item'],
                desc = form.cleaned_data['desc'],
                uploaded_by = user
            )
            inst_wish = Wish.objects.last()
            inst_wish.users_who_liked.add(user)
            messages.success(request, 'Deseo añadido exitosamente')
            return redirect(reverse('wishes:index'))
        else:
            messages.error(request, 'Con errores, solucionar')
            return render(request, 'deseos/form.html', {'formModel'  : form})
def edit(request, id):

    if request.method == 'GET':
        if 'usuario' not in request.session:
            messages.error(request, 'No estás logeado')
            return redirect(reverse('acceso:index'))
        else:
            wish = Wish.objects.get(id=id)
            form = WishForm(instance=wish)

            context = {
                'formModel' : form,
            }

            return render(request, 'deseos/editar.html', context)
        
    if request.method == 'POST':
            print(request.POST)
            wish = Wish.objects.get(id=id)
            form = WishForm(request.POST, instance=wish)
            if form.is_valid():
                    form.save()
                    messages.success(request, 'Deseo editado correctamente')
                    return redirect(reverse('wishes:index'))
            else:
                    messages.error(request, 'Con errores, solucionar')
                    return render(request, 'deseos/editar.html', {'formModel'  : form})

def granted(request, id):
    if request.method == 'GET':
        if 'usuario' not in request.session:
            messages.error(request, 'No estás logeado')
            return redirect(reverse('acceso:index'))
        else:
            wish = Wish.objects.get(id = id)
            print(wish)
            wish.date_granted = datetime.now()
            wish.save()
            return redirect(reverse('wishes:index'))
def delete(request, id):
    wish = Wish.objects.get(id=id)
    if request.method =='GET':
        if 'usuario' not in request.session:
            messages.error(request, 'No estás logeado')
            return redirect(reverse('acceso:index'))
        else:
            context = {
                'wish': wish
            }
            return render(request, 'deseos/delete.html', context)

    if request.method =='POST':
        wish.delete()
        return redirect(reverse('wishes:index'))

def liked(request, id):
    if request.method == 'GET':
        if 'usuario' not in request.session:
            messages.error(request, 'No estás logeado')
            return redirect(reverse('acceso:index'))
        else:
            usuario = request.session['usuario']
            print(usuario)
            ide = usuario['id']
            nombre = usuario['nombre']
            print(id)
            user = User.objects.get(id=ide)
            wish = Wish.objects.get(id=id)
            wish.users_who_liked.add(user)
            return redirect(reverse('wishes:index'))



# Create your views here.
