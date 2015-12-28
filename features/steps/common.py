import urlparse
from behave import when, then
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions


@when(u'I access the url "{url}"')
def i_access_the_url(context, url):
    old_url = context.driver.current_url
    new_url = urlparse.urljoin(context.base_url, url)
    context.driver.get(new_url)

    if old_url == context.driver.current_url:
        # Try again
        context.driver.get(new_url)


@when(u'I click the next button')
def i_click_the_next_button(context):
    context.driver.find_element_by_css_selector(
        'li.next>a').click()


@when(u'I click the submit button')
def i_click_the_submit_button(context):
    try:
        context.driver.find_element_by_css_selector(
            'form.pagetree-form-submit-area').submit()
    except NoSuchElementException:
        context.driver.find_element_by_css_selector(
            '.pagetree-form-submit-area input[type="submit"]').click()


@when(u'I click the first participant journal button')
def i_click_the_first_participant_journal_button(context):
    try:
        context.driver.find_element_by_link_text(
            'Manage Participant IDs').click()
    except NoSuchElementException:
        pass

    if not context.driver.current_url.endswith('/manage-participants/'):
        print('navigating to /manage-participants/ from %s' %
              context.driver.current_url)
        url = urlparse.urljoin(context.base_url, '/manage-participants/')
        context.driver.get(url)

    assert context.driver.current_url.endswith('/manage-participants/'), \
        'The Manage Participants page hasn\'t loaded yet! url is: %s' % \
        context.driver.current_url

    wait = WebDriverWait(context.driver, 10)
    element = wait.until(
        expected_conditions.element_to_be_clickable(
            (By.CLASS_NAME, 'worth-view-journal-button')))
    element.click()


@when(u'I click the link "{text}"')
def i_click_the_link(context, text):
    wait = WebDriverWait(context.driver, 10)
    element = wait.until(
        expected_conditions.element_to_be_clickable(
            (By.LINK_TEXT, text)))
    element.click()

    try:
        context.driver.find_element_by_link_text(text).click()
    except NoSuchElementException:
        pass


@when(u'I click the button "{text}"')
def i_click_the_button(context, text):
    context.driver.find_by_text(text).first.click()


@then(u'I see the text "{text}"')
def i_see_the_text(context, text):
    assert text in context.driver.page_source


@then(u'I don\'t see the text "{text}"')
def i_dont_see_the_text(context, text):
    assert text not in context.driver.page_source


@then(u'I get a {status_code}')
def i_get_a(context, status_code):
    # FIXME
    assert True


@then(u'I am at the url "{url}"')
def i_am_at_the_url(context, url):
    if not context.driver.current_url.endswith(url):
        new_url = urlparse.urljoin(context.base_url, url)
        context.driver.get(new_url)

    assert context.driver.current_url.endswith(url)
