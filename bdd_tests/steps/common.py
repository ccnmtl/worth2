from behave import given, when, then


@given(u'I am signed in as a facilitator')
def i_am_signed_in_as_a_facilitator(context):
    from worth2.main.tests.factories import UserFactory
    u = UserFactory()
    u.set_password('test_pass')
    u.save()

    b = context.browser
    b.visit(context.browser_url('/accounts/login/'))
    b.fill('username', u.username)
    b.fill('password', 'test_pass')
    b.find_by_css('.form-signin button[type="submit"]').first.click()


@when(u'I access the url "{url}"')
def i_access_the_url(context, url):
    context.browser.visit(context.browser_url(url))


@then(u'I see the text "{text}"')
def i_see_the_text(context, text):
    context.browser.is_text_present(text)


@then(u'I get a "{status_code}"')
def i_get_a_status_code(context, status_code):
    assert context.browser.status_code == int(status_code)
