from django.contrib import admin
from .models import Issue, IssueList, IssueComment, IssueLike

admin.site.register(Issue)
admin.site.register(IssueList)
admin.site.register(IssueComment)
admin.site.register(IssueLike)