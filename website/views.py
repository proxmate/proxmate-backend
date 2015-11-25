import threading
import string
import json
from utils.smtp2go import send_mail
from datetime import timedelta, datetime
from django.http.response import HttpResponse
from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from django.views.generic import View
from proxmate.models import Signer, Package, Subscription
from django.core.cache import get_cache
from django.contrib.auth.models import User
from utils import paypal, elastic

from django.conf import settings
from urlparse import parse_qs

channels_cache = get_cache('channels')

class Home(View):
    @staticmethod
    def get(request):
        return render_to_response('home.html', {
            "page_section": "home"
        }, context_instance=RequestContext(request))


class Channels(View):
    @staticmethod
    def get(request):
        payment = request.GET.get('payment')
        activation = request.GET.get('activation')
        browser = request.GET.get('browser')
        activation_key = request.GET.get('activation_key')

        packages = Package.objects.filter(is_private=False)

        _packages = channels_cache.get('packages_list')
        _netflix_packages = channels_cache.get('netflix_countries')

        if not _packages or not _netflix_packages:
            _packages = []
            _netflix_packages = []
            for package in packages:
                _packages.append({
                    'popular': package.popular,
                    'name': package.name,
                    'small_icon': package.small_icon,
                    'country': package.country.short_hand[:2],
                    'url': package.page_url
                })

                if package.name == 'Netflix':
                    package.country.title = package.country.title.replace('Netflix', '')
                    _netflix_packages.append({
                        'name': package.country.title,
                        'short_hand': package.country.short_hand,
                        'small_icon': package.small_icon,
                        'url': package.page_url
                    })
                    for netflix_country in package.additional_countries.all():
                        netflix_country.title = netflix_country.title.replace('Netflix', '')
                        _netflix_packages.append({
                            'name': netflix_country.title,
                            'short_hand': netflix_country.short_hand,
                            'small_icon': package.small_icon,
                            'url': package.page_url
                        })

            channels_cache.set('packages_list', _packages)
            channels_cache.set('netflix_countries', _netflix_packages)

        return render_to_response('channels.html', {
            "page_section": "packages",
            "channels": _packages,
            "activation": activation,
            "payment": payment,
            "browser": browser,
            "key": activation_key,
            "netflix_packages": _netflix_packages,
            "WEBSITE_URL": settings.WEBSITE_URL
        }, context_instance=RequestContext(request))


class Pricing(View):
    @staticmethod
    def get(request):
        activation = request.GET.get('activation')
        return render_to_response('pricing.html', {
            "page_section": "pricing",
            "PAYPAL_MERCHANT_ID": settings.PAYPAL_MERCHANT_ID,
            "PAYPAL_ACTION_URL": settings.PAYPAL_ACTION_URL,
            "STRIPE_PUBLISHABLE_KEY": settings.STRIPE_PUBLISHABLE_KEY,
            "WEBSITE_URL": settings.WEBSITE_URL,
            "activation": activation
        }, context_instance=RequestContext(request))


class Confirm(View):
    @staticmethod
    def get(request, key):
        try:
            browser = Signer.loads(key)["browser"]
        except:
            browser = ""

        return render_to_response('confirm.html', {
            "key": key,
            "browser": browser,
        }, context_instance=RequestContext(request))


class Uninstall(View):
    @staticmethod
    def get(request, key):
        key_json = Signer.loads(key)

        try:
            user = User.objects.get(username=key_json['email'])
            elastic.ElasticThread(doc_type='user_uninstall', user=user, req=request).start()
        except:
            pass

        return render_to_response(
            'uninstall.html',
            {},
            context_instance=RequestContext(request)
        )


class Removal(View):
    @staticmethod
    def get(request):

        elastic.ElasticThread(doc_type='user_removal', user=False, req=request).start()

        return render_to_response(
            'uninstall.html',
            {},
            context_instance=RequestContext(request)
        )


class About(View):
    @staticmethod
    def get(request):
        return render_to_response('about.html', {
            "page_section": "about"
        }, context_instance=RequestContext(request))


class Unsubscribe(View):
    @staticmethod
    def get(request, key):
        return render_to_response('unsubscribe.html', {
            'unsubscribe_key': key
        }, context_instance=RequestContext(request))


class ChangeCard(View):
    @staticmethod
    def get(request, key):
        return render_to_response('change-card.html', {
            'api_key': key
        }, context_instance=RequestContext(request))


class PayPalReturn(View):
    @staticmethod
    def post(request):
        ipn_data = request.body
        data = dict((k, v if len(v) > 1 else v[0])
                    for k, v in parse_qs(ipn_data).iteritems())

        key_json = Signer.loads(data['custom'])

        try:
            proxmate_user = User.objects.get(username=key_json['email'])
        except:
            return render_to_response('paypal-return.html', {
                'payment_status': 'user_not_found'
            }, context_instance=RequestContext(request))

        # for migrated users if they do not have email attached
        if not proxmate_user.email:
            proxmate_user.email = data['payer_email']
            proxmate_user.save()

        # subscription signup
        if data['txn_type'] == 'subscr_signup':
            if proxmate_user.profile.paypal_subscr_id != data['subscr_id']:
                proxmate_user.profile.paypal_payer_id = data['payer_id']
                proxmate_user.profile.paypal_subscr_id = data['subscr_id']
                proxmate_user.profile.plan_status = data['item_number']
                proxmate_user.profile.plan_expiration_date = proxmate_user.profile.plan_expiration_date + timedelta(minutes=120)
                proxmate_user.profile.payment_status = 'pending'
                proxmate_user.profile.subscription_status = 'subscribed'
                proxmate_user.profile.subscription_supplier = 'paypal'
                proxmate_user.profile.save()

            file_path = '/opt/proxmate/static/emails/confirmation_inline.html'

            with open(file_path) as email_file:
                email_template = string.Template(email_file.read())

            html_message = email_template.safe_substitute(
                subscribedemail=str(proxmate_user.email),
                subsctiptionperiod=str(settings.PROXMATE_PLANS[proxmate_user.profile.plan_status]['period_name']),
                startdate=datetime.now().strftime("%d %B %Y"),
                paymentplan=str(settings.PROXMATE_PLANS[proxmate_user.profile.plan_status]['price_string'])
            )

            send_mail(subject='Proxmate Subscription Confirmation',
                      plain_content='',
                      html_content=html_message,
                      to_list=proxmate_user.email,
                      from_list='support@proxmate.me')

        # single payment signup
        if data['txn_type'] == 'web_accept':
            proxmate_user.profile.paypal_payer_id = data['payer_id']
            proxmate_user.profile.plan_status = data['item_number']
            proxmate_user.profile.plan_expiration_date = proxmate_user.profile.plan_expiration_date + timedelta(minutes=120)
            proxmate_user.profile.payment_status = 'pending'
            proxmate_user.profile.subscription_status = 'subscribed'
            proxmate_user.profile.subscription_supplier = 'paypal'
            proxmate_user.profile.save()

            file_path = '/opt/proxmate/static/emails/confirmation_one_off_inline.html'

            with open(file_path) as email_file:
                email_template = string.Template(email_file.read())

            html_message = email_template.safe_substitute(
                subscribedemail=str(proxmate_user.email),
                subsctiptionperiod=str(settings.PROXMATE_PLANS[proxmate_user.profile.plan_status]['period_name']),
                startdate=datetime.now().strftime("%d %B %Y"),
                paymentplan=str(settings.PROXMATE_PLANS[proxmate_user.profile.plan_status]['price_string'])
            )

            send_mail(subject='Proxmate Payment Confirmation',
                      plain_content='',
                      html_content=html_message,
                      to_list=proxmate_user.email,
                      from_list='support@proxmate.me')

        return render_to_response('paypal-return.html', {
            'payment_status': 'success'
        }, context_instance=RequestContext(request))


class PayPalCancel(View):
    @staticmethod
    def get(request):
        return render_to_response('channels.html', {
            'payment': 'canceled'
        }, context_instance=RequestContext(request))


class LandingPage(View):
    @staticmethod
    def get(request):
        return render_to_response(
            'landing.html',
            {}, context_instance=RequestContext(request)
        )


class LandingPageNewUser(View):
    @staticmethod
    def get(request):
        return render_to_response(
            'landing_nu.html',
            {},
            context_instance=RequestContext(request)
        )


class Terms(View):
    @staticmethod
    def get(request):
        return render_to_response(
            'terms.html',
            {},
            context_instance=RequestContext(request)
        )


class Privacy(View):
    @staticmethod
    def get(request):
        return render_to_response(
            'privacy.html',
            {},
            context_instance=RequestContext(request)
        )

