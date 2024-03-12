from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login, logout
from .forms import *
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.contrib.auth.forms import AuthenticationForm
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def index(request):
    latest_update = LatestUpdate.objects.latest('date')
    return render(request,"index.html",{'latest_update':latest_update})

def register_view(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			email = form.cleaned_data.get('email')
			######################### mail system ####################################
			htmly = get_template('email.html')
			d = { 'username': username }
			subject, from_email, to = 'welcome', 'your_email@gmail.com', email
			html_content = htmly.render(d)
			msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
			msg.attach_alternative(html_content, "text/html")
			msg.send()
            
			##################################################################
			return redirect('/')
	else:
		form = UserRegisterForm()
		messages.warning(request, f'something went wrong, please try again..')
	return render(request, 'index.html', {'form': form, 'title':'register here'})

################ login forms###################################################

def login_view(request):
	if request.method == 'POST':
		# AuthenticationForm_can_also_be_used__
		email = request.POST['email']
		password = request.POST['password']
		user = authenticate(request, email = email, password = password)
		if user is not None:
			form = login(request, user)
			messages.success(request, f' welcome {email} !!')
			return redirect('/')
		else:
			messages.info(request, f'username or password is incorrect')
	form = AuthenticationForm()
	return render(request, 'index.html', {'form':form, 'title':'log in'})


def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to login page after logout



def contact(request):
    if request.method=="POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject2 = request.POST.get('subject')
        message1 = request.POST.get('message')
        print(name)
        query = Contact(name=name,email=email,subject=subject2,message=message1)
        query.save()

        subject = 'THANK YOU FOR CONTACTING ME '
        message = f'Hi {name}, Thank you so much for reaching out to me. we will get back to you soon.. '
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email, ]
        send_mail( subject, message, email_from, recipient_list )

        
        subject1 = 'HELLOW SIR SOMEONE CONTACTED YOU'
        message = f'Hi k satyanarayana chary,  Some one contacted you details are:- \n username - {name},\n  email - {email},\n subject - {subject2},\n message - {message1} \n'
        email_from = settings.EMAIL_HOST_USER
        recipient_list1 = ['acadamicfolio@gmail.com', ]
        send_mail( subject1, message, email_from, recipient_list1 )

        messages.success(request,"Thanks for contacting us ,we will contact you soon..")
        return redirect('/contact/')
    return render(request,"contact.html")



def blogs(request):
    blog_list = Blogs.objects.all()
      
    paginator = Paginator(blog_list, 10)  # Show 10 blogs per page

    page_number = request.GET.get('page')
    try:
        blogs = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        blogs = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        blogs = paginator.page(paginator.num_pages)

    query = request.GET.get('q','')
    results = Blogs.objects.filter(title__icontains=query) 
    return render(request,"blogs.html",{'blogs':blogs,'results':results,'query':query})

def singleBlog(request, blog_id):
      blog = get_object_or_404(Blogs, pk=blog_id)
      blog.views += 1
      blog.save()
      return render(request,"singleBlog.html",{'blog':blog})


def tutorials(request):
     tutorials = TutorialName.objects.all()
     return render(request,"tutorials.html",{'tutorials':tutorials})


def tutorialView(request,tut_id):
    tutorialName_id = get_object_or_404(TutorialName, pk=tut_id)
    posts = TutorialPost.objects.filter(tutorialName_id=tutorialName_id)
    return render(request,"tutorialView.html",{'tutorialName_id':tutorialName_id,'posts':posts})



def tutorialPost(request,post_id):
     post = get_object_or_404(TutorialPost,pk=post_id)
     return render(request,"post.html",{'post':post})


@login_required
def comment(request,blog_id):
      blog = get_object_or_404(Blogs, pk=blog_id)
      if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.blog = blog
            comment.user = request.user
            comment.save()
            
      else:
            form = CommentForm()
      return render(request,"singleBlog.html",{'blog':blog})     

@login_required
def post_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            new_blog = form.save(commit=False)
            new_blog.user = request.user
            new_blog.save()
            return redirect('/blog_detail/')  # Redirect to a view that lists all blogs
    else:
        form = BlogForm()
    return render(request, 'addBlog.html', {'form': form})	


def meme(request):
     meme = Meme.objects.all()
     query = request.GET.get('q','')
     results = Meme.objects.filter(description__icontains=query)
     return render(request,"meme.html",{'meme':meme,'results': results, 'query': query})


@login_required
def upload_meme(request):
    if request.method == 'POST':
        form = MemeForm(request.POST, request.FILES)
        if form.is_valid():
            meme=form.save(commit=False)
            meme.user = request.user
            meme.save()
            return redirect('/meme/')
    else:
        form = MemeForm()
    return render(request, 'upload_meme.html', {'form': form})

def code(request):
    return render(request,"code.html")

def code_page(request):
     code = Language.objects.all()
     return render(request,"code_display.html",{'code':code})

def code_pages(request,lan_id):
    language_id = get_object_or_404(Language, pk=lan_id)
    codes = CodeSnippet.objects.filter(language_id=language_id)
    query = request.GET.get('q','')
    results = CodeSnippet.objects.filter(title__icontains=query)
    return render(request,"code_display1.html",{'language_id':language_id,'codes':codes,'results': results, 'query': query})

def code_view(request,code_id):
     codes = get_object_or_404(CodeSnippet,pk=code_id)
     return render(request,"code_view.html",{'codes':codes})