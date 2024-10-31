from datetime import timezone
from django.db import models

# https://dev.to/bikramjeetsingh/soft-deletes-in-django-a9j
# https://tomisin.dev/blog/implementing-soft-delete-in-django-an-intuitive-guide
# https://medium.com/@dineshs91/django-soft-delete-options-864082511918
# https://www.geeksforgeeks.org/nulltrue-django-built-in-field-validation/
# https://ugur.ozyilmazel.com/blog/tr/2021/08/22/django-model-ipuclari/


class SoftDeleteQuerySet(models.QuerySet):
    def delete(self):
        for obj in self:
            obj.deleted_at = timezone.now()
            obj.save()


class SoftDeleteManager(models.Manager):

    def get_queryset(self):
        return SoftDeleteQuerySet(self.model, using=self._db).filter(deleted_at__isnull=True)


class SoftDeleteModel(models.Model):

    deleted_at = models.DateTimeField(null=True, default=None)
    objects = SoftDeleteManager()
    all_objects = models.Manager()

    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.save()

    def restore(self):
        self.deleted_at = None
        self.save()

    class Meta:
        abstract = True
