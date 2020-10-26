from django.db import models
from neox_project.models import CustomUser
from django.utils.translation import gettext as _


class Post(models.Model):
    """Post - class for posts content"""

    title = models.CharField(_('Post Title'), max_length=255, unique=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField(_('Post Content'), )
    pub_date = models.DateField(_('Post Date Published'), auto_now=True)

    readonly_fields = ('pub_date',)
    ordering = ['-pub_date', '-id', 'title']

    def __repr__(self):
        return _("<Post #%s from user #%s>") % (self.id, self.user_id)
    
    def __str__(self):
        return _("<Post #%s from user #%s>") % (self.id, self.user_id)


class Rating(models.Model):
    """Rating - class for rating posts"""

    like = models.BooleanField(_("like"), null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    pub_date = models.DateField(_('Rating Date Published'), auto_now=True)
    ordering = ['-pub_date', '-id', ]

    class Meta:
        unique_together = ('user', 'post',)

    def __repr__(self):
        return _("<Rating #%s from user #%s>") % (self.id, self.user_id)

    def __str__(self):
        return _("<Rating #%s from user #%s>") % (self.id, self.user_id)

