from behave import when, then

from worth2.main.tests.factories import (
    ParticipantFactory,
    LocationFactory, UserFactory, WorthModuleFactory
)


@when(u'I sign in as a facilitator')
def i_sign_in_as_a_facilitator(context):
    facilitator = UserFactory()
    facilitator.set_password('test_pass')
    facilitator.save()

    b = context.browser
    b.visit(context.browser_url('/accounts/login/'))
    b.fill('username', facilitator.username)
    b.fill('password', 'test_pass')
    b.find_by_css('.form-signin button[type="submit"]').first.click()


@when(u'I sign in as a participant')
def i_sign_in_as_a_participant(context):
    i_sign_in_as_a_facilitator(context)

    location = LocationFactory()
    participant = ParticipantFactory()
    WorthModuleFactory()

    b = context.browser
    b.visit(context.browser_url('/sign-in-participant/'))
    b.select('participant_id', participant.pk)
    b.select('participant_location', location.pk)
    b.choose('participant_destination', 'next_new_session')
    b.choose('session_type', 'regular')
    b.find_by_css(
        '.worth-facilitator-sign-in-participant button[type="submit"]'
    ).first.click()


@when(u'I access the url "{url}"')
def i_access_the_url(context, url):
    context.browser.visit(context.browser_url(url))


@when(u'I click the next button')
def i_click_the_next_button(context):
    context.browser.find_by_css('li.next>a').first.click()


@then(u'I see the text "{text}"')
def i_see_the_text(context, text):
    context.browser.is_text_present(text)


@then(u'I get a {status_code}')
def i_get_a(context, status_code):
    assert context.browser.status_code == int(status_code)


@then(u'I am at the url "{url}"')
def i_am_at_the_url(context, url):
    assert context.browser.url == context.browser_url(url)
