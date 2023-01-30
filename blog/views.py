from itertools import chain

from blog import forms, models
from blog.models import CustomUser

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import Q


@login_required
def logout_user(request):
    logout(request)
    return redirect('login')


class LoginPageView(View):
    template_name = 'blog/login.html'
    form_class = forms.LoginForm

    def get(self, request):
        form = self.form_class()
        message = ''
        return render(request, self.template_name, context={'form': form, 'message': message})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password'],
                                )
            if user is not None:
                login(request, user)
                return redirect('flux')
        message = 'Identifiants invalides.'
        user = False
        return render(request, self.template_name, context={'form': form, 'message': message, 'user': user})


class SignupPageView(View):
    template_name = 'blog/signup.html'
    form_class = forms.SignupForm

    def get(self, request):
        form = self.form_class()
        message = ''
        return render(request, self.template_name, context={'form': form, 'message': message})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)


class FluxView(ListView):
    model = models.Ticket
    template_name = 'blog/flux.html'
    context_object_name = "tickets"


class PostsView(ListView):
    model = models.Ticket
    template_name = 'blog/posts.html'
    context_object_name = "tickets"


class TicketCreateView(CreateView):
    model = models.Ticket
    template_name = 'blog/ticket-create.html'
    form_class = forms.TicketForm
    success_url = reverse_lazy("flux")

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.user = self.request.user
        return super().form_valid(form)


class TicketUpdateView(UpdateView):
    model = models.Ticket
    template_name = 'blog/ticket-create.html'
    form_class = forms.TicketForm
    success_url = reverse_lazy("posts")


class TicketDeleteView(DeleteView):
    model = models.Ticket
    template_name = 'blog/ticket-delete.html'
    context_object_name = "ticket"
    form_class = forms.TicketForm
    success_url = reverse_lazy("posts")


class ReviewUpdateView(UpdateView):
    model = models.Ticket
    template_name = 'blog/review-create.html'
    form_class = forms.ReviewForm
    success_url = reverse_lazy("posts")


class ReviewDeleteView(DeleteView):
    model = models.Ticket
    template_name = 'blog/review-delete.html'
    context_object_name = "review"
    form_class = forms.ReviewForm
    success_url = reverse_lazy("posts")


def flux(request):
    tickets = models.Ticket.objects.filter(Q(user__in=request.user.follows.all()))
    reviews = models.Review.objects.filter(user__in=request.user.follows.all()).exclude(ticket__in=tickets)

    tickets = models.Ticket.objects.all()
    reviews = models.Review.objects.all()
    tickets_and_reviews = sorted(chain(tickets, reviews), key=lambda instance: instance.time_created, reverse=True)
    return render(request, 'blog/flux.html', context={'tickets_and_reviews': tickets})


def posts(request):
    tickets = models.Ticket.objects.all()
    reviews = models.Review.objects.all()
    tickets_and_reviews = sorted(chain(tickets, reviews), key=lambda instance: instance.date_created, reverse=True)
    for t in tickets_and_reviews:
        print(t)
    return render(request, 'blog/flux.html', context={'t': tickets_and_reviews})


def follow_users(request):
    form = forms.FollowUsersForm(instance=request.user)
    if request.method == 'POST':
        form = forms.FollowUsersForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('posts')
    return render(request, 'blog/follow-users-form.html', context={'form': form})


class ReviewCreateView(CreateView):
    form_class = forms.TicketForm
    second_form_class = forms.ReviewForm
    template_name = 'blog/review-create.html'
    success_url = reverse_lazy('flux')

    def get(self, request, *args, **kwargs):
        ticket_form = self.form_class()
        review_form = self.second_form_class()
        return render(request, self.template_name, {'ticket_form': ticket_form, 'review_form': review_form})

    def post(self, request, *args, **kwargs):
        ticket_form = forms.TicketForm(request.POST, request.FILES)
        review_form = forms.ReviewForm(request.POST)
        if all([ticket_form.is_valid(), review_form.is_valid()]):
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            review = review_form.save(commit=False)
            ticket_1 = models.Ticket.objects.get(pk=ticket.pk)
            user = models.CustomUser.objects.get(username=request.user)
            review.user = user
            review.ticket = ticket_1
            review_form.save()
            return redirect(self.success_url)
        context = {'ticket_form': ticket_form, 'review_form': review_form}
        return render(request, 'blog/review-create.html', context=context)


def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 != password2:
            return render(request, 'blog/signup.html', {"error": "Les mots de passe ne correspondent pas"})
        CustomUser.objects.create_user(username=username, password=password1)

    return render(request, 'blog/signup.html')