from django.contrib import admin
from proxmate.models import Message, Country, Payment, Server, Package, PackageRoute, PackageHost, ContentScript, Profile, Subscription
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from blog.models import Post


class MessageAdmin(admin.ModelAdmin):
    pass

class PostAdmin(admin.ModelAdmin):
    pass


class CountryAdmin(admin.ModelAdmin):
    pass


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'user',
    )


class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        'user',
    )

    pass

class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        'user',
    )

    pass


class ServerAdmin(admin.ModelAdmin):
    pass


class RouteInline(admin.TabularInline):
    model = PackageRoute
    extra = 0


class HostInline(admin.TabularInline):
    model = PackageHost
    extra = 0


class ContentScriptInline(admin.TabularInline):
    model = ContentScript
    extra = 0


class ProfileInline(admin.StackedInline):
    model = Profile
    fk_name = 'user'
    max_num = 1

class CustomUserAdmin(UserAdmin):
    inlines = [ProfileInline, ]

    def plan_status(self, obj):
       return obj.profile.plan_status

    plan_status.allow_tags = True
    plan_status.short_description = "Status Plan"

    list_display = (
        'username',
        'email',
        'date_joined',
        'is_active',
        'plan_status',
    )

    search_fields = ['email']


class PackageAdmin(admin.ModelAdmin):
    inlines = [RouteInline, HostInline, ContentScriptInline]

    list_display = (
        'name',
        'country',
    )

    list_filter = (
        'country__title',
    )

    search_fields = ['name']


class PackageRouteAdmin(admin.ModelAdmin):
    pass


admin.site.unregister(User)
admin.site.register(Message, MessageAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(Server, ServerAdmin)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Package, PackageAdmin)
admin.site.register(PackageRoute, PackageRouteAdmin)

#admin.site.register(Post, PostAdmin)
