from itertools import chain

from blog import forms, models
from blog.models import CustomUser, UsersFollows

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import CreateView, DeleteView


class LoginPageView(View):
    """Permet d'afficher la page de connexion et le lien d'inscription"""
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
    """Permet l'affichage de la page pour la création d'un compte"""
    def get(self, request):
        return render(request, 'blog/signup.html')

    def post(self, request):
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 != password2:
            return render(request, 'blog/signup.html', {"error": "Les mots de passe ne correspondent pas"})
        user = CustomUser.objects.create_user(username=username, password=password1)
        if user is not None:
            login(request, user)
            return redirect('flux')
        return redirect(settings.LOGIN_REDIRECT_URL)


@method_decorator(login_required, name='dispatch')
class FluxView(View):
    """Permet d'afficher la page flux avec l'affichage de son flux"""
    template_name = 'blog/flux.html'

    def get(self, request):
        followed_users = UsersFollows.objects.filter(user=request.user)
        followed_users_ids = [followed_user.followed_user.id for followed_user in followed_users]
        tickets_following = []
        for followed_user_id in followed_users_ids:
            tickets_following.extend(models.Ticket.objects.filter(user_id=followed_user_id))
        tickets_user = models.Ticket.objects.filter(user_id=request.user)
        tickets = list(chain(tickets_user, tickets_following))
        for ticket in tickets:
            review = ticket.review.first()
            if review is not None:
                ticket.time_created = review.time_created
        tickets_sorted = sorted(tickets, key=lambda post: post.time_created, reverse=True)

        return render(request, self.template_name, context={'tickets': tickets_sorted})


@method_decorator(login_required, name='dispatch')
class PostsView(View):
    """Permet l'affichage de la page post avec tous les posts de l'utilisateur pour les modifier et les supprimer"""
    template_name = 'blog/posts.html'

    def get(self, request):
        tickets = models.Ticket.objects.filter(user_id=request.user)
        reviews = models.Review.objects.filter(user_id=request.user)
        ticket_response = [review.ticket for review in reviews if review.user != review.ticket.user]
        tickets = list(chain(tickets, ticket_response))
        for ticket in tickets:
            if ticket.review.first() is not None:
                review = ticket.review.first()
                ticket.time_created = review.time_created
        tickets_sorted = sorted(tickets, key=lambda post: post.time_created, reverse=True)
        return render(request, self.template_name, context={'tickets': tickets_sorted})


@method_decorator(login_required, name='dispatch')
class TicketCreateView(CreateView):
    """Permet d'afficher le formulaire pour créer un ticket"""
    model = models.Ticket
    template_name = 'blog/ticket-create.html'
    form_class = forms.TicketForm
    success_url = reverse_lazy("flux")

    def get(self, request, *args, **kwargs):
        ticket_form = self.form_class()
        return render(request, self.template_name, {'ticket_form': ticket_form})

    def post(self, request, *args, **kwargs):
        ticket_form = forms.TicketForm(request.POST, request.FILES)
        if ticket_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect(self.success_url)
        context = {'ticket_form': ticket_form}
        return render(request, self.template_name, context=context)


@method_decorator(login_required, name='dispatch')
class TicketUpdateView(View):
    """Permet l'affichage d'un formulaire pour un ticket et une review afin de les modifier"""
    template_name = 'blog/review-update.html'
    form_class = forms.TicketForm
    second_form_class = forms.ReviewForm
    success_url = reverse_lazy('posts')

    def get(self, request, ticket_id):
        ticket = models.Ticket.objects.get(id=ticket_id)
        image = ticket.image.url if ticket.image else ""
        review = ticket.review.first()
        if ticket.user == request.user:
            ticket = self.form_class(instance=ticket)
        if review is not None and review.user == request.user:
            review = self.second_form_class(instance=review)
        return render(request, self.template_name, {'ticket_form': ticket, 'review_form': review,
                                                    'image': image})

    def post(self, request, ticket_id):
        ticket = models.Ticket.objects.get(id=ticket_id)
        review = ticket.review.first()
        if ticket.user == request.user:
            ticket = self.form_class(request.POST, request.FILES, instance=ticket)
            if ticket.is_valid():
                ticket = ticket.save(commit=False)
                ticket.user = request.user
                ticket.save()
            if review is not None and review.user == request.user:
                review = self.second_form_class(request.POST, instance=review)
                if review.is_valid():
                    review = review.save(commit=False)
                    review.user = request.user
                    review.ticket = ticket
                    review.save()
            return redirect(self.success_url)

        return render(request, self.template_name, {'ticket': ticket, 'review_form': review})


@method_decorator(login_required, name='dispatch')
class TicketDeleteView(DeleteView):
    """Permet de supprimer les tickets"""
    model = models.Ticket
    template_name = 'blog/ticket-delete.html'
    context_object_name = "ticket"
    form_class = forms.TicketForm
    success_url = reverse_lazy("posts")


@method_decorator(login_required, name='dispatch')
class ReviewDeleteView(DeleteView):
    """Permets de supprimer les reviews"""
    model = models.Ticket
    template_name = 'blog/review-delete.html'
    context_object_name = "review"
    form_class = forms.ReviewForm
    success_url = reverse_lazy("posts")


@method_decorator(login_required, name='dispatch')
class ReviewCreateView(CreateView):
    """Permet d'afficher le formulaire pour créer un ticket et une review"""
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
        if ticket_form.is_valid() and review_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            review = review_form.save(commit=False)
            user = models.CustomUser.objects.get(username=ticket.user)
            ticket_id = models.Ticket.objects.get(id=ticket.id)
            review.ticket = ticket_id
            review.user = user
            review.save()
            return redirect(self.success_url)
        context = {'ticket_form': ticket_form}
        return render(request, self.template_name, context=context)


@method_decorator(login_required, name='dispatch')
class FollowUsersView(View):
    """Permet d'afficher la page des abonnements, de suivre, de supprimer des utilisateurs qu'in suit et de voir
     les personnes qui nous suit."""
    template_name = 'blog/follow-users-form.html'
    success_url = reverse_lazy("follow-users")

    def get(self, request):
        user = CustomUser.objects.get(id=request.user.id)
        following = UsersFollows.objects.filter(user=user)
        following_usernames = [follow.followed_user for follow in following]
        followed_by = UsersFollows.objects.filter(followed_user=user)
        followed_by_username = [follow.user.username for follow in followed_by]
        return render(request, self.template_name, {'following': following_usernames,
                                                    'followers': followed_by_username})

    def post(self, request):
        action = request.POST.get('action')
        username = request.POST.get('username')
        if username != '' and username is not None:
            if action == 'follow':
                following = CustomUser.objects.get(username=username)
                users_follow = UsersFollows(user=request.user, followed_user=following)
                users_follow.save()
            elif action == 'unfollow':
                print(username)
                following = CustomUser.objects.get(username=username)
                UsersFollows.objects.get(user=request.user, followed_user=following.id).delete()
        return redirect(self.success_url)


@method_decorator(login_required, name='dispatch')
class TicketResponseView(View):
    """Permet de répondre à un ticket"""
    template_name = 'blog/ticket-response.html'
    form_class = forms.ReviewForm
    success_url = reverse_lazy("flux")

    def get(self, request, ticket_id):
        review_form = self.form_class()
        ticket = models.Ticket.objects.get(id=ticket_id)

        return render(request, self.template_name, {'ticket': ticket, 'review_form': review_form})

    def post(self, request, ticket_id):
        ticket = models.Ticket.objects.get(id=ticket_id)
        review_form = forms.ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            user = models.CustomUser.objects.get(username=request.user)
            review.user = user
            review.ticket = ticket
            review.save()
            return redirect(self.success_url)
        return render(request, self.template_name, {'ticket': ticket, 'review_form': review_form})


@method_decorator(login_required, name='dispatch')
class LogoutUserView(View):
    """Permet la déconnexion de l'utilisateur"""

    def get(self, request):
        logout(request)
        return redirect('login')