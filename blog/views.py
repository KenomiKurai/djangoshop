import random
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.timezone import now
from django.db.models import Q
from .forms import PostForm, UserEditForm, RegistrationForm, AvatarUploadForm, CategoryForm
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from .models import Post, Category, UserProfile
from django.contrib.auth import login, update_session_auth_hash


def dummy():
    return str(random.randint(1, 10))


def get_categories():
    all = Category.objects.all()
    count = all.count()
    half = count // 2 + 1
    return {"cat1": all[:half], "cat2": all[half:]}


# Create your views here.
def index(request):
    # posts = Post.objects.all()
    # posts = Post.objects.filter(title__contains='python')
    # posts = Post.objects.filter(published_date__year=2023)
    # posts = Post.objects.filter(category__name__iexact='python')
    posts = Post.objects.order_by('-published_date')
    paginator = Paginator(posts, 2)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    # post = Post.objects.get(pk=2)
    context = {'posts': page_obj}
    context.update(get_categories())

    return render(request, "blog/index.html", context=context)


def post(request, title):
    post = get_object_or_404(Post, title=title)


    context = {"post": post}
    context.update(get_categories())

    return render(request, "blog/post.html", context=context)


def category(request, name=None):
    c = get_object_or_404(Category, name=name)
    posts = Post.objects.filter(category=c).order_by('-published_date')
    context = {"posts": posts}
    context.update(get_categories())

    return render(request, "blog/index.html", context=context)


def about(request):
    return render(request, "blog/about.html")


def contacts(request):
    return render(request, "blog/contacts.html")


def search(request):
    query = request.GET.get('query')
    posts = Post.objects.filter(Q(content__icontains=query) | Q(title__icontains=query))
    context = {"posts": posts}
    context.update(get_categories())

    return render(request, "blog/index.html", context=context)


def services(request):
    return render(request, "blog/services.html")


def pro_url(request, dynamic_url):
    print(dynamic_url)
    return render(request, "blog/services.html", context={"url": dynamic_url})


# @login_required
# def create(request):
#     form = PostForm()
#     if request.method == 'POST':
#         form = PostForm(request.POST)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.published_date = now()
#             post.user = request.user
#             post.save()
#             return index(request)
#     context = {'form': form}
#     return render(request, "blog/create.html", context=context)

from django.shortcuts import render, redirect
from .forms import CategoryForm




from django.http import HttpResponseRedirect
@login_required
def create(request):
    post_form = PostForm()
    categories = Category.objects.all()  # Получить все существующие категории

    if request.method == 'POST':
        post_form = PostForm(request.POST, request.FILES)

        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.published_date = now()
            post.user = request.user

            # Получите выбранную категорию
            category_id = request.POST.get('category', None)
            if category_id:
                post.category = Category.objects.get(pk=category_id)
            post.save()
            return redirect('main')  # Перенаправление на главную страницу

    context = {'post_form': post_form, 'categories': categories}
    return render(request, "blog/create.html", context=context)
def create_category(request):
    if request.method == 'POST':
        category_form = CategoryForm(request.POST)
        if category_form.is_valid():
            category_form.save()
            return redirect('create')  # Перенаправление на страницу создания поста после создания категории
    else:
        category_form = CategoryForm()
    return render(request, 'blog/create_category.html', {'category_form': category_form})



# views.py

@login_required
def edit_profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        user_form = UserEditForm(request.POST, request.FILES, instance=user_profile)  # Учитываем файлы
        password_form = PasswordChangeForm(request.user, request.POST)

        if user_form.is_valid() and password_form.is_valid():
            user = user_form.save()
            update_session_auth_hash(request, user_form.instance)
            return redirect('profile')
    else:
        user_form = UserEditForm(instance=user_profile)
        password_form = PasswordChangeForm(request.user)

    return render(request, 'blog/edit_profile.html', {'user_form': user_form, 'password_form': password_form})


def registration_user(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
    else:
        form = RegistrationForm()

    return render(request, 'blog/registration.html', {'form': form})


@login_required
def profile(request):
    avatar_form = AvatarUploadForm()
    return render(request, "blog/profile.html", {'avatar_form': avatar_form})


def edit_avatar(request):
    if request.method == 'POST':
        form = AvatarUploadForm(request.POST, request.FILES, instance=request.user.userprofile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = AvatarUploadForm(instance=request.user.userprofile)
    return render(request, 'blog/edit_avatar.html', {'form': form})
