from django.db import models

from django.utils.translation import ugettext_lazy as _
from erm_auth.models import Profile


class UserRole(models.Model):
    role = models.CharField(max_length=255, null=False, blank=False)
    active = models.BooleanField(default=True)
    user_profile = models.ForeignKey(Profile, null=True, blank=True,
                                     related_name="roles",
                                     on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, blank=True)
    modified = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        verbose_name = "Role"
        verbose_name_plural = "Roles"

    def __str__(self):
        return self.role


class Employee(models.Model):
    employee = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="user_employees",
        null=True)
    parent = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="user_parent_employee",
        null=True)

    class Meta:
        '''
            Meta class for the model.
        '''
        verbose_name = _('Employee')
        verbose_name_plural = _('Employees')
