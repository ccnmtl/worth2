from behave import when

from worth2.goals.models import GoalOption, GoalSettingBlock


@when(u'I fill in a goal option')
def i_fill_in_a_goal_option(context):
    b = context.browser
    option = GoalOption.objects.first()
    goalsettingblock = GoalSettingBlock.objects.first()
    pageblock_pk = goalsettingblock.pageblock().pk

    b.select('pageblock-%d-0-option' % pageblock_pk, option.pk)
    b.fill('pageblock-%d-0-text' % pageblock_pk,
           'I will make it happen somehow')


@when(u'I click the goal submit button')
def i_click_the_goal_submit_button(context):
    context.browser.driver.find_element_by_css_selector(
        '.goal-submit-button button[type="submit"]').click()
