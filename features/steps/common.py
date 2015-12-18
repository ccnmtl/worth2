import urlparse
import time
from behave import when, then
from selenium.common.exceptions import NoSuchElementException


@when(u'I access the url "{url}"')
def i_access_the_url(context, url):
    old_url = context.browser.url
    new_url = urlparse.urljoin(context.base_url, url)
    context.browser.driver.get(new_url)

    if old_url == context.browser.url:
        # Try again
        time.sleep(1)
        context.browser.driver.get(new_url)


@when(u'I click the next button')
def i_click_the_next_button(context):
    context.browser.driver.find_element_by_css_selector(
        'li.next>a').click()


@when(u'I click the submit button')
def i_click_the_submit_button(context):
    context.browser.driver.find_element_by_css_selector(
        '.pagetree-form-submit-area input[type="submit"]').click()


@when(u'I click the first participant journal button')
def i_click_the_first_participant_journal_button(context):
    context.browser.driver.find_element_by_css_selector(
        'button[data-target^="#view-participant-journal-modal-"]'
    ).click()


@when(u'I click the link "{text}"')
def i_click_the_link(context, text):
    link = context.browser.find_link_by_partial_text(text).first
    old_url = context.browser.url

    link.click()
    # If the url didn't change, it might need another click
    if old_url == context.browser.url:
        link.click()


@when(u'I click the button "{text}"')
def i_click_the_button(context, text):
    context.browser.find_by_text(text).first.click()


@then(u'I see the text "{text}"')
def i_see_the_text(context, text):
    try:
        el = context.browser.driver.find_element_by_xpath(
            '//*[contains(text(),"' + text + '")]')
    except NoSuchElementException:
        time.sleep(1)
        el = context.browser.driver.find_element_by_xpath(
            '//*[contains(text(),"' + text + '")]')

    assert el


@then(u'I don\'t see the text "{text}"')
def i_dont_see_the_text(context, text):
    assert context.browser.is_text_not_present(text)


@then(u'I get a {status_code}')
def i_get_a(context, status_code):
    assert context.browser.status_code == int(status_code)


@then(u'I am at the url "{url}"')
def i_am_at_the_url(context, url):
    assert context.browser.url.endswith(url)
