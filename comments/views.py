from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from .models import Comment
from .forms import CommentForm

# Create your views here.
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid() and request.user == comment.user:
            form.save()
            return redirect('comment_detail', comment_id=comment.id)
        elif not request.user == comment.user:
            raise PermissionDenied("You do not have permission to edit this comment.")
    else:
        form = CommentForm(instance=comment)

    return render(request, 'edit_comment.html', {'form': form})


def update_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid() and request.user == comment.user:
            form.save()

            # Return JSON response with success flag and updated comment data
            comment_data = {
                'id': comment.id,
                'content': comment.content,
                'timestamp': comment.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                'author_name': comment.author_name,
                # Add other relevant comment data here
            }
            return JsonResponse({'success': True, 'comment': comment_data})
        elif not request.user == comment.user:
            return JsonResponse({'success': False, 'msg': 'You do not have permission to edit this comment.'})
    else:
        # If it's a GET request, return the comment form as HTML
        form = CommentForm(instance=comment)
        return JsonResponse({'success': False, 'html': render(request, 'edit_comment.html', {'form': form}).content})
    