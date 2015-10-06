import urlparse
from behave import when, then


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


@when(u'I click the first participant journal button')
def i_click_the_first_participant_journal_button(context):
    context.browser.find_by_css(
        'button[data-target^="#view-participant-journal-modal-"]'
    ).first.click()


@when(u'I click the link "{text}"')
def i_click_the_link(context, text):
    # Wait up to 10 seconds for elements to appear.
    # http://selenium-python.readthedocs.org/en/latest/waits.html#implicit-waits
    context.browser.driver.implicitly_wait(10)
    context.browser.find_link_by_partial_text(text).first.click()


@when(u'I click the button "{text}"')
def i_click_the_button(context, text):
    context.browser.find_by_text(text).first.click()


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
