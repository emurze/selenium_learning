from django.contrib.auth.models import AnonymousUser
from django.test import TestCase
from django.test.client import RequestFactory
from django.urls import resolve, reverse

from apps.panel.forms import CreateEmailForm
from apps.panel.views import PanelView


class PanelViewTest(TestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()

    def test_view_connection(self):
        resolver = resolve(reverse('panel'))
        self.assertEqual(resolver.func.view_class, PanelView)

    def test_view_template(self):
        request = self.factory.get('panel')
        request.user = AnonymousUser()
        response = PanelView.as_view()(request)
        self.assertEqual(response.template_name[0], 'panel.html')


class CreateEmailFormTest(TestCase):
    def test_form(self):
        form = CreateEmailForm(data={'email': 'efwfwefwe'})
        self.assertEqual(
            form.errors['email'],
            ['Enter a valid email address.']
        )
