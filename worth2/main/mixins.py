from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator


class ActiveUserRequiredMixin(object):
    @method_decorator(user_passes_test(lambda u: u.is_active))
    def dispatch(self, *args, **kwargs):
        return super(ActiveUserRequiredMixin, self).dispatch(*args, **kwargs)
