from behave import when


@when(u'I select the first avatar')
def i_select_the_first_avatar(context):
    context.browser.find_by_css('.avatar-input-label').first.click()
