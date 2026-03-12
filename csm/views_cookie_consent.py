from typing import Iterable

from cookie_consent.conf import settings as cookie_settings
from cookie_consent.models import ACTION_ACCEPTED, ACTION_DECLINED, CookieGroup, LogItem
from cookie_consent.util import (
    delete_cookies,
    get_cookie_dict_from_request,
    set_cookie_dict_to_response,
)
from cookie_consent.views import CookieGroupBaseProcessView


def _groups(varname: str | None) -> Iterable[CookieGroup]:
    qs = CookieGroup.objects.all().prefetch_related("cookie_set")
    if varname:
        keys = varname.split(",")
        qs = qs.filter(varname__in=keys)
    return qs


class AcceptIncludingRequiredView(CookieGroupBaseProcessView):
    """
    Custom handler for the “accept all” button that also marks required groups.
    """

    def process(self, request, response, varname):
        cookie_dic = get_cookie_dict_from_request(request)
        for cookie_group in _groups(varname):
            cookie_dic[cookie_group.varname] = cookie_group.get_version()
            if cookie_settings.COOKIE_CONSENT_LOG_ENABLED:
                LogItem.objects.create(
                    action=ACTION_ACCEPTED,
                    cookiegroup=cookie_group,
                    version=cookie_group.get_version(),
                )
        set_cookie_dict_to_response(response, cookie_dic)


class DeclineOptionalKeepRequiredView(CookieGroupBaseProcessView):
    """
    Custom handler for the "only necessary" button.

    Keeps required cookie groups accepted while declining everything optional,
    so users who choose the minimal option still retain essential cookies.
    """

    def process(self, request, response, varname):
        cookie_dic = get_cookie_dict_from_request(request)
        for cookie_group in _groups(varname):
            if cookie_group.is_required:
                cookie_dic[cookie_group.varname] = cookie_group.get_version()
                if cookie_settings.COOKIE_CONSENT_LOG_ENABLED:
                    LogItem.objects.create(
                        action=ACTION_ACCEPTED,
                        cookiegroup=cookie_group,
                        version=cookie_group.get_version(),
                    )
            else:
                cookie_dic[cookie_group.varname] = cookie_settings.COOKIE_CONSENT_DECLINE
                delete_cookies(response, cookie_group)
                if cookie_settings.COOKIE_CONSENT_LOG_ENABLED:
                    LogItem.objects.create(
                        action=ACTION_DECLINED,
                        cookiegroup=cookie_group,
                        version=cookie_group.get_version(),
                    )

        set_cookie_dict_to_response(response, cookie_dic)
