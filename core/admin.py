from functools import update_wrapper
from django.contrib.admin import AdminSite as BaseAdminSite, ModelAdmin as BaseModelAdmin, TabularInline as BaseTabularInline
from django.urls import path, reverse
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy

from inventory.models import Item
from transactions.models import PurchaseItem, Component


class AdminSite(BaseAdminSite):
    index_title = gettext_lazy("Reagent-DB")

    def each_context(self, request):
        context = super().each_context(request)
        if request.get_full_path() == reverse('admin:index'):
            data, labels = self.get_item_data()
            context.update({
                'labels': labels, 'data': data,
                'purchases': PurchaseItem.objects.order_by('-billno'),
                'sales': Component.objects.order_by('-billno')
            })
        return context

    def _build_app_dict(self, request, label=None):
        app_dict = super()._build_app_dict(request, label)
        icon_dict = {"inventory": "pe-7s-box1", "transactions": "pe-7s-ticket", "auth": "pe-7s-users"}
        if label:
            app_dict['icon'] = icon_dict.get(label, "pe-7s-rocket")
        else:
            for label in app_dict:
                app_dict[label]['icon'] = icon_dict.get(label, "pe-7s-rocket")
        return app_dict

    @staticmethod
    def get_item_data():
        data, labels = [], []
        for item in Item.objects.filter(status='d').order_by('-quantity'):
            labels.append(item.name)
            data.append(item.quantity)
        return data, labels


class TabularInline(BaseTabularInline):
    extra = 0

    def get_fieldsets(self, request, obj=None):
        if not obj and hasattr(self, 'add_fieldsets'):
            return self.add_fieldsets
        return super().get_fieldsets(request, obj)


class ModelAdmin(BaseModelAdmin):
    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.info = self.model._meta.app_label, self.model._meta.model_name

    def get_wrap(self):
        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)

            wrapper.model_admin = self
            return update_wrapper(wrapper, view)
        return wrap
    
    def get_urls(self):
        urls = super().get_urls()
        urls[-1:] = [
            path(
                "<path:object_id>/",
                self.get_wrap()(self.change_view),
                name="%s_%s_view" % self.info,
            ),
        ]
        return urls

    def has_change_permission(self, request, obj=None):
        if obj and 'change' not in request.get_full_path():
            return False
        return super().has_change_permission(request, obj)

    def get_fieldsets(self, request, obj=None):
        if not obj and hasattr(self, 'add_fieldsets'):
            return self.add_fieldsets
        return super().get_fieldsets(request, obj)

    def model_actions(self, obj):
        view_link = "<a class='btn btn-sm btn-outline-info' href='{}'>View Details</a>".format(reverse('admin:%s_%s_view' % self.info, kwargs={'object_id': obj.id}))
        edit_link = "<a class='btn btn-sm btn-outline-success' href='{}'>Edit Details</a>".format(reverse('admin:%s_%s_change' % self.info, kwargs={'object_id': obj.id}))
        return mark_safe("<div class='d-flex justify-content-between'>{}{}</div>".format(view_link, edit_link))

    model_actions.short_description = 'Action'
    model_actions.allow_tags = True