from datetime import date
from rest_framework.permissions import BasePermission
from .models import ApiKey


class HasAPIKey(BasePermission):

    def has_permission(self, request, view):
        try:
            key = request.headers['Authorization'].split()[1]
        except KeyError:
            return False

        try:
            k = ApiKey.objects.get(key=key)
            k.n_requests += 1
            k.save()

            if k.n_allowed_requests and k.n_requests > k.n_allowed_requests:
                return False

            if k.start_date and k.start_date > date.today():
                return False

            if k.end_date and k.end_date < date.today():
                return False

        except ApiKey.DoesNotExist:
            return False

        return True
