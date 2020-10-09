from django.conf import settings
from django.contrib.flatpages.models import FlatPage
from django.contrib.flatpages.views import DEFAULT_TEMPLATE
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils.safestring import mark_safe
from django.views.generic.detail import DetailView

from popularity.views import PopularityMixin


class FlatpageView(PopularityMixin, DetailView):
    context_object_name = "flatpage"

    count_hit = True

    def get_flatpage(self, request, url):
        if not hasattr(self, "_flatpage"):
            if not url.endswith("/") and settings.APPEND_SLASH:
                return HttpResponseRedirect("%s/" % request.path)
            if not url.startswith("/"):
                url = "/" + url
            self._flatpage = get_object_or_404(FlatPage, url__exact=url, sites__id__exact=settings.SITE_ID)
            # To avoid having to always use the "|safe" filter in flatpage templates,
            # mark the title and content as already safe (since they are raw HTML
            # content in the first place).
            self._flatpage.title = mark_safe(self._flatpage.title)
            self._flatpage.content = mark_safe(self._flatpage.content)
        return self._flatpage

    def dispatch(self, request, *args, **kwargs):
        # If registration is required for accessing this page, and the user isn't
        # logged in, redirect to the login page.
        self.flatpage = self.get_flatpage(request, kwargs["url"])
        if self.flatpage.registration_required and not request.user.is_authenticated:
            from django.contrib.auth.views import redirect_to_login

            return redirect_to_login(request.path)
        return super(FlatpageView, self).dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return self.flatpage

    def get_template_names(self):
        template_names = super(FlatpageView, self).get_template_names()
        if self.flatpage.template_name:
            template_names.insert(0, self.flatpage.template_name)
        template_names.append(DEFAULT_TEMPLATE)
        return template_names
