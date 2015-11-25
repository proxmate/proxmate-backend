from django.core import signing
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver
from django.core.cache import get_cache

ROUTE_TYPES = (
    ('startsWith', 'startsWith'),
    ('host', 'host'),
    ('contains', 'contains'),
)

message_cache = get_cache('message')
package_version_cache = get_cache('packages_version')
server_list_cache = get_cache('server_list')
channels_cache = get_cache('channels')


def check_key(key):
    try:
        obj = Signer.loads(key)
    except:
        return False

    try:
        User.objects.get(username=obj['email'])
    except:
        return False

    return True


class Signer(object):
    @staticmethod
    def dumps(**kwargs):
        key = signing.dumps(kwargs)
        return key

    @staticmethod
    def loads(key, max_age=None):
        try:
            signing.loads(key)
        except signing.BadSignature:
            # log.warning("Tampering detected for conversion key: %s", key)
            raise ValueError

        try:
            data = signing.loads(key, max_age=max_age)
        except signing.BadSignature:
            # log.warning("Signature expired: %s", key)
            raise KeyError

        return data


class PaypalIPNLog(models.Model):
    """
    Raw ipn data from paypal
    """

    class Meta:
        app_label = 'proxmate'
        verbose_name = 'User status information'

    timestamp = models.DateTimeField(null=False, default=datetime.utcnow)
    ipn_message = models.TextField(null=True, blank=True)


class StripeWebhookLog(models.Model):
    """
    Raw ipn data from paypal
    """

    class Meta:
        app_label = 'proxmate'
        verbose_name = 'User status information'

    timestamp = models.DateTimeField(null=False, default=datetime.utcnow)
    webhook_message = models.TextField(null=True, blank=True)


class Profile(models.Model):
    """
    Profile model stores user information like
    stripe identification, PayPal identification, subscription status etc
    """

    class Meta:
        app_label = 'proxmate'
        verbose_name = 'User status information'

    user = models.OneToOneField(User)

    stripe_customer_id = models.TextField(null=True, blank=True)
    stripe_subscription_id = models.CharField(max_length=256, null=True, blank=True)
    paypal_payer_id = models.TextField(null=True, blank=True)
    paypal_subscr_id = models.TextField(null=True, blank=True)
    activation_code = models.CharField(max_length=256, null=True, blank=True)
    plan_expiration_date = models.DateTimeField(null=False, default=datetime.utcnow)
    plan_status = models.CharField(max_length=128, null=False, default='')
    subscription_status = models.CharField(max_length=128, null=False, default='')
    subscription_supplier = models.CharField(max_length=128, null=False, default='')
    payment_status = models.CharField(max_length=128, null=False, default='')
    is_updated_user = models.BooleanField(default=False)
    last_active_check = models.CharField(max_length=128, null=False, default='')
    last_channel_check = models.CharField(max_length=128, null=False, default='')

    @receiver(post_save, sender=User)
    def create_profile_for_user(sender, instance=None, created=False, **kwargs):
        """
        Creates profile on user creation
        """
        if created:
            Profile.objects.get_or_create(user=instance)

    @receiver(pre_delete, sender=User)
    def delete_profile_for_user(sender, instance=None, **kwargs):
        """
        Deletes profile on user deletion
        """
        if instance:
            user_profile = Profile.objects.get(user=instance)
            user_profile.delete()


class Message(models.Model):
    """
    Messages to be sent to users
    """

    class Meta:
        app_label = 'proxmate'

    date_created = models.DateTimeField(null=False, default=datetime.utcnow)
    title = models.CharField(max_length=256, null=False, blank=False, default="Message Title")
    content = models.TextField(null=False, blank=True, default="Message Content")
    has_url = models.BooleanField(default=False)
    is_sticky = models.BooleanField(default=False)
    is_closable = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_generic = models.BooleanField(default=True)
    time_shown = models.IntegerField(default=1, null=True, blank=False)
    specific_to_plan = models.CharField(max_length=256, null=False, blank=True)
    url = models.CharField(max_length=256, null=True, blank=True)

    def __unicode__(self):
        return self.title + ' - ' + self.content


# method for updating
def invalidate_cache(sender, instance, **kwargs):
    """
    Clears cache when a message is deleted
    """
    if instance.is_generic:
        message_cache.delete('generic')
    if instance.specific_to_plan:
        message_cache.delete(instance.specific_to_plan)

# register the signal
post_save.connect(invalidate_cache, sender=Message, dispatch_uid="message_cache_invalidation")


class Country(models.Model):
    """
    Countries available for service
    """

    class Meta:
        app_label = 'proxmate'
        verbose_name_plural = 'Countries'

    title = models.CharField(max_length=128, null=True, blank=True)
    flag = models.ImageField(
        upload_to="flags",
        help_text="Please upload an image (.jpg, .png, .gif)."
    )
    short_hand = models.CharField(max_length=10, null=True, blank=True)
    created_at = models.DateTimeField(null=False, default=datetime.utcnow)

    def __unicode__(self):
        return self.title


class Server(models.Model):
    """
    Servers available for service that are associated with countries
    """

    class Meta:
        app_label = 'proxmate'

    host = models.CharField(max_length=128, null=True, blank=True)
    port = models.CharField(max_length=128, null=True, blank=True)
    user = models.CharField(max_length=256, null=True, blank=True)
    password = models.CharField(max_length=256, null=True, blank=True)
    country = models.ForeignKey(Country)
    ip = models.CharField(max_length=256, null=True, blank=True)
    require_key = models.BooleanField(default=True)
    return_type = models.CharField(max_length=128, null=True, blank=True, default="PROXY")
    is_private = models.BooleanField(default=True)
    created_at = models.DateTimeField(null=False, default=datetime.utcnow)
    version = models.CharField(max_length=256, null=True, blank=True)

    def __unicode__(self):
        return self.host


# method for updating
def invalidate_server_cache(sender, instance, **kwargs):
    """
    Clears cache when a server is deleted
    """
    server_list_cache.delete('latest')
    server_list_cache.delete('version')

# register the signal
post_save.connect(invalidate_server_cache, sender=Server, dispatch_uid="server_cache_invalidation")


class Package(models.Model):
    """
    Packages/channels available for service that are associated with countries
    """

    class Meta:
        app_label = 'proxmate'

    version = models.CharField(max_length=128, null=True, blank=True)
    name = models.CharField(max_length=128, null=False, blank=True, default="")
    page_url = models.CharField(max_length=128, null=True, blank=True)
    big_icon = models.ImageField(
        upload_to="big_icons",
        help_text="Please upload an image (.jpg, .png, .gif)."
    )
    small_icon = models.ImageField(
        upload_to="small_icons",
        help_text="Please upload an image (.jpg, .png, .gif)."
    )
    created_at = models.DateTimeField(null=True)
    description = models.TextField(null=True)
    allow_multiple_countries = models.BooleanField(default=False)
    popular = models.BooleanField(default=False)
    ##content_scripts = models.ForeignKey(ContentScripts)
    country = models.ForeignKey(Country, related_name="%(app_label)s_%(class)s_related")
    additional_countries = models.ManyToManyField(Country, blank=True)
    return_type = models.CharField(max_length=128, null=False, blank=True, default="PROXY")
    require_key = models.BooleanField(default=True)
    is_private = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name


# method for updating
def invalidate_package_cache(sender, instance, **kwargs):
    """
    Clears cache when a package is saved
    """
    package_version_cache.delete('latest')
    channels_cache.delete('packages_list')
    channels_cache.delete('netflix_countries')

# register the signal
post_save.connect(invalidate_package_cache, sender=Package, dispatch_uid="package_cache_invalidation")


class ContentScript(models.Model):
    """
    Content script for packages/channels that require javascript code for unblocking
    """

    class Meta:
        app_label = 'proxmate'

    match = models.CharField(max_length=128, null=True, blank=True, default="")
    script = models.TextField(null=True, blank=True, default="")
    package = models.ForeignKey(Package)

    def __unicode__(self):
        return self.package.name + " - " + self.match


class PackageRoute(models.Model):
    """
    Routes and hosts needed for unblocking
    """

    class Meta:
        app_label = 'proxmate'

    route = models.CharField(max_length=120, null=False, blank=False, default="")
    type = models.CharField(
        max_length=25, null=False, blank=False, default='host', choices=ROUTE_TYPES,
        help_text="The default currency for this advertiser"
    )
    package = models.ForeignKey(Package)

    def __unicode__(self):
        return self.route


class PackageHost(models.Model):
    """
    Hosts needed where content scripts need to be placed
    """

    class Meta:
        app_label = 'proxmate'

    host = models.CharField(max_length=120, null=False, blank=False, default="")
    package = models.ForeignKey(Package)

    def __unicode__(self):
        return self.host


class Payment(models.Model):
    """
    Payments data associated with user
    """

    class Meta:
        app_label = 'proxmate'

    transaction_id = models.CharField(max_length=128, null=True, blank=True)
    user = models.ForeignKey(User)
    created_at = models.DateTimeField(null=False, auto_now_add=True)
    transaction_date = models.DateTimeField(blank=True, null=True, default=datetime.utcnow)
    payer_email = models.CharField(max_length=256, null=True, blank=True)
    subscription_plan = models.CharField(max_length=64, null=True, blank=True)
    subscription_id = models.CharField(max_length=64, null=True, blank=True)
    amount = models.CharField(max_length=16, null=True, blank=True)
    currency = models.CharField(max_length=3, null=True, blank=True)
    description = models.CharField(max_length=256, null=True, blank=True)

    def __unicode__(self):
        return self.user.email


class Subscription(models.Model):
    """
    Subscription data associated with user
    """

    class Meta:
        app_label = 'proxmate'

    user = models.ForeignKey(User)
    created_at = models.DateTimeField(null=False, auto_now_add=True)
    transaction_date = models.DateTimeField(blank=True, null=True, default=datetime.utcnow)
    payer_email = models.CharField(max_length=256, null=True, blank=True)
    description = models.CharField(max_length=64, null=True, blank=True)
    subscription_plan = models.CharField(max_length=64, null=True, blank=True)
    subscription_id = models.CharField(max_length=64, null=True, blank=True)
    supplier = models.CharField(max_length=256, null=True, blank=True)

    def __unicode__(self):
        return self.user.email
