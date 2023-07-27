from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse, HttpResponseBadRequest, Http404, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.template.defaulttags import register

from reddit.forms import SubmissionForm
from reddit.models import Submission, Comment, Vote
from reddit.utils.helpers import post_only
from users.models import RedditUser
from django.urls import reverse

@register.filter
def get_item(dictionary, key):  # pragma: no cover
    """
    Needed because there's no built-in .get in Django templates
    when working with dictionaries.

    :param dictionary: python dictionary
    :param key: valid dictionary key type
    :return: value of that key or None
    """
    return dictionary.get(key)

def frontpage(request):
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

    submission_votes = {}
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

    # Ensure submission_votes is a dictionary
    if not isinstance(submission_votes, dict):
        submission_votes = {}

    return render(request, 'public/frontpage.html', {'submissions': submissions, 'submission_votes': submission_votes})

def submission_detail(request, submission_id):
    """
    Handles the detailed submission page.
    """
    submission = get_object_or_404(Submission, id=submission_id)
    return render(request, 'public/submission_detail.html', {'submission': submission})

def comments(request, thread_id=None):
    """
    Handles comment view when user opens the thread.
    On top of serving all comments in the thread it will
    also return all votes user made in that thread
    so that we can easily update comments in the template
    and display via CSS whether user voted or not.

    :param thread_id: Thread ID as it's stored in the database
    :type thread_id: int
    """
    this_submission = get_object_or_404(Submission, id=thread_id)
    thread_comments = Comment.objects.filter(submission=this_submission)

    reddit_user = RedditUser.objects.get(user=request.user) if request.user.is_authenticated else None
    sub_vote_value = None
    comment_votes = {}

    if reddit_user:
        try:
            vote = Vote.objects.get(
                vote_object_type=ContentType.objects.get_for_model(this_submission),
                vote_object_id=this_submission.id,
                user=reddit_user)
            sub_vote_value = vote.value
        except Vote.DoesNotExist:
            pass

        try:
            user_thread_votes = Vote.objects.filter(user=reddit_user, submission=this_submission)
            for vote in user_thread_votes:
                comment_votes[vote.vote_object.id] = vote.value
        except:
            pass

    return render(request, 'public/comments.html', {'submission': this_submission, 'comments': thread_comments, 'comment_votes': comment_votes, 'sub_vote': sub_vote_value})

@post_only
def post_comment(request):
    if not request.user.is_authenticated:
        return JsonResponse({'msg': "You need to log in to post new comments."})

    parent_type = request.POST.get('parentType', None)
    parent_id = request.POST.get('parentId', None)
    raw_comment = request.POST.get('commentContent', None)

    if not all([parent_id, parent_type]) or \
            parent_type not in ['comment', 'submission'] or \
        not parent_id.isdigit():
        return HttpResponseBadRequest()

    if not raw_comment:
        return JsonResponse({'msg': "You have to write something."})
    author = RedditUser.objects.get(user=request.user)
    parent_object = None
    try:  # try and get comment or submission we're voting on
        if parent_type == 'comment':
            parent_object = Comment.objects.get(id=parent_id)
        elif parent_type == 'submission':
            parent_object = Submission.objects.get(id=parent_id)

    except (Comment.DoesNotExist, Submission.DoesNotExist):
        return HttpResponseBadRequest()

    comment = Comment.create(author=author,
                             raw_comment=raw_comment,
                             parent=parent_object)

    comment.save()
    return JsonResponse({'msg': "Your comment has been posted."})


@post_only
def vote(request):
    # The type of object we're voting on, can be 'submission' or 'comment'
    vote_object_type = request.POST.get('what', None)

    # The ID of that object as it's stored in the database, positive int
    vote_object_id = request.POST.get('what_id', None)

    # The value of the vote we're writing to that object, -1 or 1
    # Passing the same value twice will cancel the vote i.e. set it to 0
    new_vote_value = request.POST.get('vote_value', None)

    # By how much we'll change the score, used to modify score on the fly
    # client side by the javascript instead of waiting for a refresh.
    vote_diff = 0

    if not request.user.is_authenticated:
        return HttpResponseForbidden()
    else:
        user = RedditUser.objects.get(user=request.user)

    try:  # If the vote value isn't an integer that's equal to -1 or 1
        # the request is bad and we can not continue.
        new_vote_value = int(new_vote_value)

        if new_vote_value not in [-1, 1]:
            raise ValueError("Wrong value for the vote!")

    except (ValueError, TypeError):
        return HttpResponseBadRequest()

    # if one of the objects is None, 0 or some other bool(value) == False value
    # or if the object type isn't 'comment' or 'submission' it's a bad request
    if not all([vote_object_type, vote_object_id, new_vote_value]) or \
            vote_object_type not in ['comment', 'submission']:
        return HttpResponseBadRequest()

    # Try and get the actual object we're voting on.
    try:
        if vote_object_type == "comment":
            vote_object = Comment.objects.get(id=vote_object_id)

        elif vote_object_type == "submission":
            vote_object = Submission.objects.get(id=vote_object_id)
        else:
            return HttpResponseBadRequest()  # should never happen

    except (Comment.DoesNotExist, Submission.DoesNotExist):
        return HttpResponseBadRequest()

    # Try and get the existing vote for this object, if it exists.
    try:
        vote = Vote.objects.get(vote_object_type=vote_object.get_content_type(),
                                vote_object_id=vote_object.id,
                                user=user)

    except Vote.DoesNotExist:
        # Create a new vote and that's it.
        vote = Vote.create(user=user,
                           vote_object=vote_object,
                           vote_value=new_vote_value)
        vote.save()
        vote_diff = new_vote_value
        return JsonResponse({'error'   : None,
                             'voteDiff': vote_diff})

    # User already voted on this item, this means the vote is either
    # being canceled (same value) or changed (different new_vote_value)
    if vote.value == new_vote_value:
        # canceling vote
        vote_diff = vote.cancel_vote()
        if not vote_diff:
            return HttpResponseBadRequest(
                'Something went wrong while canceling the vote')
    else:
        # changing vote
        vote_diff = vote.change_vote(new_vote_value)
        if not vote_diff:
            return HttpResponseBadRequest(
                'Wrong values for old/new vote combination')

    return JsonResponse({'error'   : None,
                         'voteDiff': vote_diff})


@login_required
def submit(request):
    """
    Handles new submission.. submission.
    """
    submission_form = SubmissionForm()

    if request.method == 'POST':
        submission_form = SubmissionForm(request.POST)
        if submission_form.is_valid():
            submission = submission_form.save(commit=False)
            submission.generate_html()
            user = User.objects.get(username=request.user)
            redditUser = RedditUser.objects.get(user=user)
            submission.author = redditUser
            submission.author_name = user.username
            submission.save()
            messages.success(request, 'Submission created')
            return redirect('/comments/{}'.format(submission.id))

    return render(request, 'public/submit.html', {'form': submission_form})

@login_required
def user_profile(request):
    user = request.user
    submissions = user.submission_set.all()  # Assuming the Submission model has a ForeignKey to the User model.
    comments = Comment.objects.filter(user=user)
    return render(request, 'public/user_profile.html', {'user': user, 'submissions': submissions, 'comments': comments})

@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if request.user == comment.user:
        if request.method == 'POST':
            # Update the comment content here
            new_content = request.POST.get('content', '')  # Get the new content from the form
            comment.content = new_content
            comment.save()
            return redirect('user_profile')  # Redirect to the user profile page after saving changes
        else:
            return render(request, 'public/edit_comment.html', {'comment': comment})
    else:
        # Handle unauthorized access here (e.g., redirect to an error page)
        pass
    
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    # Add your logic here for editing the comment
    return render(request, 'public/edit_comment.html', {'comment': comment})
