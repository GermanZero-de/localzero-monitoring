import threading


# From https://stackoverflow.com/a/50380461/6159921
class ModelAdminRequestMixin(object):
    def __init__(self, *args, **kwargs):
        # let's define this so there's no chance of AttributeErrors
        self._request_local = threading.local()
        self._request_local.request = None
        super(ModelAdminRequestMixin, self).__init__(*args, **kwargs)

    def get_request(self):
        return self._request_local.request

    def set_request(self, request):
        self._request_local.request = request

    def changeform_view(self, request, *args, **kwargs):
        self.set_request(request)
        return super(ModelAdminRequestMixin, self).changeform_view(
            request, *args, **kwargs
        )

    def add_view(self, request, *args, **kwargs):
        self.set_request(request)
        return super(ModelAdminRequestMixin, self).add_view(request, *args, **kwargs)

    def change_view(self, request, *args, **kwargs):
        self.set_request(request)
        return super(ModelAdminRequestMixin, self).change_view(request, *args, **kwargs)

    def changelist_view(self, request, *args, **kwargs):
        self.set_request(request)
        return super(ModelAdminRequestMixin, self).changelist_view(
            request, *args, **kwargs
        )

    def delete_view(self, request, *args, **kwargs):
        self.set_request(request)
        return super(ModelAdminRequestMixin, self).delete_view(request, *args, **kwargs)

    def history_view(self, request, *args, **kwargs):
        self.set_request(request)
        return super(ModelAdminRequestMixin, self).history_view(
            request, *args, **kwargs
        )

    def get_formset(self, request, *args, **kwargs):
        self.set_request(request)
        return super(ModelAdminRequestMixin, self).get_formset(request, *args, **kwargs)
