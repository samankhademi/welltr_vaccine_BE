from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from django.utils.translation import ugettext_lazy as _


def trigger_error(request):
    division_by_zero = 1 / 0


urlpatterns = [
    path("api/v1/mocks/", include("mocks.urls")),
    path('api/v1/sentry-debug/', trigger_error),
    path("admin/vaccine/60cf32c2-6fe4-4970-b0af-2709fb8c3c82/", admin.site.urls),
    path("o/", include("oauth2_provider.urls", namespace="oauth2_provider")),
    path("api/v1/auth/", include("authentication.urls")),
    path("api/v1/order/", include("order.urls")),
    path("api/v1/pay/", include("payment.urls")),
    path("panel/", include(("panel.urls", "panel"), namespace="panel")),
    path("api/v1/exchange/", include(("exchange.urls", "exchange"), namespace="exchange")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + \
              static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Text to put at the end of each page's <title>.
admin.site.site_title = _("Admin")

# Text to put in each page's <h1> (and above login form).
admin.site.site_header = _("Vaccine | Vaccine Admin Panel")

# Text to put at the top of the admin index page.
admin.site.index_title = _("Vaccine")
