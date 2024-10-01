from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import SignUpForm

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

# ---------------------------------------------------------------------------------------------------
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm

@login_required
def profile_view(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'profile.html', {'form': form})


from django.contrib.auth import logout
from django.shortcuts import redirect

def log_out(request):
    logout(request)
    return redirect('login')

# ---------------------------------------------------------------------------------------
from django.shortcuts import render, redirect
from .forms import PostForm
from django.contrib.auth.decorators import login_required

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('view_posts')  # Redirect to list of posts
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})

# -------------------------------------------------------------------------------------------------
from django.core.paginator import Paginator
from .models import Post

def view_posts(request):
    posts_list = Post.objects.all().order_by('-created_at')  # Order by newest posts
    paginator = Paginator(posts_list, 5)  # Show 5 posts per page
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    return render(request, 'view_posts.html', {'posts': posts})

# ---------------------------------------------------------------------------------------------------------

from django.shortcuts import get_object_or_404

def view_single_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'view_single_post.html', {'post': post})

# -----------------------------------------------------------------------------------------------------------
@login_required
def update_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        return redirect('view_posts')  # Only allow the author to edit

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('view_single_post', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'update_post.html', {'form': form})
# ----------------------------------------------------------------------------------------------------------------

@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author == request.user:
        post.delete()
    return redirect('view_posts')


