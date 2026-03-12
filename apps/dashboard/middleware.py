# apps/dashboard/middleware.py

class DashboardCompanyMiddleware:
    """
    Совместима и с Django (через MIDDLEWARE), и с прямым вызовом в тестах:
        DashboardCompanyMiddleware().process_request(request)
    """
    def __init__(self, get_response=None):
        # get_response может отсутствовать в тестах
        self.get_response = get_response or (lambda r: r)

    def __call__(self, request):
        self.process_request(request)
        return self.get_response(request)

    def process_request(self, request):
        # По умолчанию company = None
        request.company = None
        u = getattr(request, "user", None)
        if not getattr(u, "is_authenticated", False):
            return

        prof = getattr(u, "manager_profile", None)
        if prof and getattr(prof, "is_active", False):
            request.company = getattr(prof, "company", None)
