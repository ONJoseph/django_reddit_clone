from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest, Http404, HttpResponseForbidden
from django.template.defaulttags import register
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from reddit.forms import SubmissionForm
from reddit.models import Submission, Comment, Vote
from reddit.utils.helpers import post_only
from users.models import RedditUser
from functools import wraps

def home(request):
    """
    Serves the frontpage and all additional submission listings
    with a maximum of 25 submissions per page.
    """
    all_submissions = Submission.objects.order_by('-score').all()
    paginator = Paginator(all_submissions, 25)

    page = request.GET.get('page', 1)
    try:
        submissions = paginator.page(page)
    except PageNotAnInteger:
        raise Http404
    except EmptyPage:
        submissions = paginator.page(paginator.num_pages)

    submission_votes = {}  # Initialize the submission_votes dictionary
    if request.user.is_authenticated:
        reddit_user = RedditUser.objects.get(user=request.user)
        for submission in submissions:
            try:
                vote = Vote.objects.get(
                    vote_object_type=ContentType.objects.get_for_model(submission),
                    vote_object_id=submission.id,
                    user=reddit_user)
                submission_votes[submission.id] = vote.value
            except Vote.DoesNotExist:
                pass

    return render(request, 'public/frontpage.html', {'submissions': submissions, 'submission_votes': submission_votes})

def submit(request):
    if request.method == 'POST':
        form = SubmissionForm(request.POST)
        if form.is_valid():
            # Create a new submission object but don't save it yet
            new_submission = form.save(commit=False)

            # Set the author of the submission (assuming you have a RedditUser object for the current user)
            new_submission.author = request.user.reddituser  # Replace 'reddituser' with the actual related name for RedditUser model

            # Save the submission to the database
            new_submission.save()

            # Add a success message and redirect to the homepage or the newly created submission detail page
            messages.success(request, 'Your submission has been posted successfully!')
            return redirect('home')  # Replace 'home' with the name of the URL pattern for your homepage
    else:
        form = SubmissionForm()

    return render(request, 'submissions/submit.html', {'form': form})

def submission_detail(request, pk):
    """
    Display the details of a specific submission.
    """
    submission = get_object_or_404(Submission, pk=pk)
    return render(request, 'submission_detail.html', {'submission': submission})

def post_only(view_func):
    """
    Decorator to ensure that the view function can only be accessed via POST method.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.method != 'POST':
            return HttpResponseBadRequest('Only POST requests are allowed for this view.')
        return view_func(request, *args, **kwargs)

    return _wrapped_view

# Add the post_comment view to handle comment submissions
@post_only
def post_comment(request):
    if not request.user.is_authenticated:
        return JsonResponse({'msg': "You need to log in to post new comments."})

    parent_type = request.POST.get('parentType', None)
    parent_id = request.POST.get('parentId', None)
    raw_comment = request.POST.get('commentContent', None)

    if not all([parent_id, parent_type]) or parent_type not in ['comment', 'submission'] or not parent_id.isdigit():
        return HttpResponseBadRequest()

    if not raw_comment:
        return JsonResponse({'msg': "You have to write something."})
    author = RedditUser.objects.get(user=request.user)
    parent_object = None
    try:
        if parent_type == 'comment':
            parent_object = Comment.objects.get(id=parent_id)
        elif parent_type == 'submission':
            parent_object = Submission.objects.get(id=parent_id)
    except (Comment.DoesNotExist, Submission.DoesNotExist):
        return HttpResponseBadRequest()

    comment = Comment.create(author=author, raw_comment=raw_comment, parent=parent_object)
    comment.save()
    return JsonResponse({'msg': "Your comment has been posted."})
