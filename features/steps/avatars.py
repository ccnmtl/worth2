from behave import when


@when(u'I select the first avatar')
def i_select_the_first_avatar(context):
    context.driver.find_element_by_class_name(
        'avatar-input-label').click()
