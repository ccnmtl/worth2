from behave import when
from selenium.webdriver.support.select import Select

from worth2.goals.models import GoalOption, GoalSettingBlock


@when(u'I fill in a goal option')
def i_fill_in_a_goal_option(context):
    d = context.driver
    option = GoalOption.objects.first()
    goalsettingblock = GoalSettingBlock.objects.first()
    pageblock_pk = goalsettingblock.pageblock().pk

    Select(d.find_element_by_name(
        'pageblock-%d-0-option' % pageblock_pk)).select_by_value(
            unicode(option.pk))
    el = d.find_element_by_name('pageblock-%d-0-text' % pageblock_pk)
    el.send_keys('I will make it happen somehow')


@when(u'I click the goal submit button')
def i_click_the_goal_submit_button(context):
    context.driver.find_element_by_css_selector(
        '.goal-submit-button button[type="submit"]').click()
