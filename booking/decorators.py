from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse_lazy

def staff_required(view_func):
    return user_passes_test(
        lambda u: u.is_authenticated and u.is_staff,
        login_url='/admin/login/',  # ✅ Redirects to Django admin login
        redirect_field_name=None
    )(view_func)
