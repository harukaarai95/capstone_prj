from django.core.exceptions import PermissionDenied

class RoleRequiredMixin:
    allowed_roles = []

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise PermissionDenied("You must be logged in.")

        if self.allowed_roles and request.user.role not in self.allowed_roles:
            raise PermissionDenied("You do not have permission to access this page.")

        return super().dispatch(request, *args, **kwargs)
    
#how to use
# from django.views.generic import TemplateView
# from django.contrib.auth.mixins import LoginRequiredMixin
# from .mixins import RoleRequiredMixin

# class StaffOnlyView(LoginRequiredMixin, RoleRequiredMixin, TemplateView):
#     allowed_roles = ['STAFF', 'OWNER']
#     template_name = 'staff_page.html'
