import urlparse
from behave import when, then

from worth2.main.auth import generate_password
from worth2.main.models import Location
from worth2.main.tests.factories import UserFactory, ParticipantFactory


@when(u'I sign in as a facilitator')
def i_sign_in_as_a_facilitator(context):
    facilitator = UserFactory()
    facilitator.set_password('test_pass')
    facilitator.save()

    b = context.browser
    b.visit(urlparse.urljoin(context.base_url, '/accounts/login/'))
    b.fill('username', facilitator.username)
    b.fill('password', 'test_pass')
    b.find_by_css('.form-signin button[type="submit"]').first.click()


@when(u'I sign in as a participant')
def i_sign_in_as_a_participant(context):
    i_sign_in_as_a_facilitator(context)

    participant = ParticipantFactory()
    password = generate_password(participant.user.username)
    participant.user.set_password(password)
    participant.user.save()

    location = Location.objects.first()

    b = context.browser
    b.visit(urlparse.urljoin(context.base_url, '/sign-in-participant/'))
    b.select('participant_id', participant.pk)
    b.select('participant_location', location.pk)
    b.choose('participant_destination', '1')
    b.choose('session_type', 'regular')
    b.find_by_css(
        '.worth-facilitator-sign-in-participant button[type="submit"]'
    ).first.click()


@when(u'I access the url "{url}"')
def i_access_the_url(context, url):
    context.browser.visit(urlparse.urljoin(context.base_url, url))


@when(u'I click the next button')
def i_click_the_next_button(context):
    context.browser.find_by_css('li.next>a').first.click()


@when(u'I click the submit button')
def i_click_the_submit_button(context):
    context.browser.find_by_css(
        '.pagetree-form-submit-area input[type="submit"]').first.click()


@then(u'I see the text "{text}"')
def i_see_the_text(context, text):
    assert context.browser.is_text_present(text)


@then(u'I don\'t see the text "{text}"')
def i_dont_see_the_text(context, text):
    assert context.browser.is_text_not_present(text)


@then(u'I get a {status_code}')
def i_get_a(context, status_code):
    assert context.browser.status_code == int(status_code)


@then(u'I am at the url "{url}"')
def i_am_at_the_url(context, url):
    assert context.browser.url.endswith(url)
