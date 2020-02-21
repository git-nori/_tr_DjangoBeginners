from django import forms
from django.test import TestCase
from ..templatetags.form_tags import field_type, input_class


class ExampleForm(forms.Form):
    name = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        fields = ('name', 'password')


class FieldTypeTests(TestCase):
    # フォームのwidgetの取得が正しくできるか確認する
    def test_field_widget_type(self):
        pass
    #     form = ExampleForm()
    #     self.assertEquals('TextInput', field_type(form['name']))
    #     self.assertEquals('PasswordInput', field_type(form['password']))


class InputClassTests(TestCase):
    # バインドがされていない場合のスタイルを確認する
    def test_unbound_field_initial_state(self):
        pass
    #     form = ExampleForm()
    #     self.assertEquals('form-control ', input_class(form['name']))

    # バインドされている場合のスタイルを確認する
    def test_valid_bound_filed(self):
        pass
    #     form = ExampleForm({
    #         'name': 'test',
    #         'password': '123'
    #     })
    #     self.assertEquals('form-control is-valid', input_class(form['name']))
    #     self.assertEquals('form-control is-valid', input_class(form['password']))
