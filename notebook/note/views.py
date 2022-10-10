from multiprocessing import context
from django.shortcuts import render, redirect, get_object_or_404
from soupsieve import select
from .models import Inscription, Category
from django.contrib.auth.forms import User
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.db.models import Q

def index(request):
    return render(request, 'note/index.html')

@login_required
def search(request):
    query = request.GET.get('query')
    search_results = Inscription.objects.filter(title__icontains=query).filter(reader=request.user)
    return render(request, 'note/search.html', {'inscriptions': search_results, 'query': query})

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            # tikriname, ar neužimtas username
            if User.objects.filter(username=username).exists():
                messages.error(request, f'Vartotojo vardas {username} užimtas!')
                return redirect('note:register')
            else:
                # tikriname, ar nėra tokio pat email
                if User.objects.filter(email=email).exists():
                    messages.error(request, f'Vartotojas su el. paštu {email} jau užregistruotas!')
                    return redirect('note:register')
                else:
                    # jeigu viskas tvarkoje, sukuriame naują vartotoją
                    User.objects.create_user(username=username, email=email, password=password)
                    messages.info(request, 'Registracija sėkminga')
        else:
            messages.error(request, 'Slaptažodžiai nesutampa!')
            return redirect('note:register')

    return render(request, 'note/register.html')


class MyNotesByUserListView(LoginRequiredMixin,generic.ListView):
    model = Inscription
    template_name ='note/user_notes.html'
    
    def get_queryset(self):
        return Inscription.objects.filter(reader=self.request.user)

class NoteByUserDetailView(LoginRequiredMixin, generic.DetailView):
    model = Inscription
    template_name = 'note/user_note.html'


class NoteByUserCreateView(LoginRequiredMixin, generic.CreateView):
    model = Inscription
    fields = ['title', 'text', 'category',]
    success_url = reverse_lazy('note:mynotes')
    template_name = 'note/user_note_form.html'


    def form_valid(self, form):
        form.instance.reader = self.request.user
        return super().form_valid(form)

class NoteByUserUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Inscription
    fields = ['title', 'text', 'category',]
    success_url = reverse_lazy('note:mynotes')
    template_name = 'note/user_note_form.html'

    def test_func(self):
        inscription = self.get_object()
        return self.request.user == inscription.reader

class NoteByUserDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Inscription
    success_url = reverse_lazy('note:mynotes')
    template_name = 'note/user_note_delete.html'

    def test_func(self):
        inscription = self.get_object()
        return self.request.user == inscription.reader

class MyCategorysByUserListView(LoginRequiredMixin, generic.ListView):
    model = Category
    template_name ='note/user_categorys.html'
    
    def get_queryset(self):
        return Category.objects.filter(reader=self.request.user)

class CategoryByUserDetailView(LoginRequiredMixin, generic.DetailView):
    model = Category
    template_name = 'note/user_category.html'

class CategoryByUserCreateView(LoginRequiredMixin, generic.CreateView):
    model = Category
    fields = ['name']
    success_url = reverse_lazy('note:mycategorys')
    template_name = 'note/user_category_form.html'

    def form_valid(self, form):
        form.instance.reader = self.request.user
        return super().form_valid(form)

class CategoryByUserUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Category
    fields = ['name']
    success_url = reverse_lazy('note:mycategorys')
    template_name = 'note/user_category_form.html'

    def test_func(self):
        category = self.get_object()
        return self.request.user == category.reader

class CategoryByUserDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Category
    success_url = reverse_lazy('note:mycategorys')
    template_name = 'note/user_category_delete.html'

    def test_func(self):
        category = self.get_object()
        return self.request.user == category.reader


