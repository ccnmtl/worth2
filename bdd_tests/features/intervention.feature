Feature: Participant Intervention
  Scenario: Session 1
    # TODO: We should really mock the sign-in process here
    # with "Given I am signed in as a participant", but I
    # haven't been able to get that to work -- it signed
    # in instead as a facilitator. So just go through the
    # sign-in steps manually for now using the "When" clause.
    When I sign in as a participant

    When I access the url "/pages/session-1/"
    When I click the next button
    Then I am at the url "/pages/session-1/orientation/"
    Then I see the text "Orientation Video"

    When I click the next button
    Then I am at the url "/pages/session-1/how-to-use-this-tablet/"
    Then I see the text "How to use this tablet"

    When I click the next button
    Then I am at the url "/pages/session-1/choose-your-avatar/"
    Then I see the text "Choose Your Avatar"
    Then I see the text "Which avatar would you like to use"

    When I click the submit button
    Then I see the text "Oops!"

    When I select the first avatar
    When I click the submit button
    Then I see the text "Here is the avatar that you selected"

  Scenario: Session 2
    When I access the url "/pages/session-2/"
    When I click the next button
    Then I am at the url "/pages/session-2/welcome-to-session-2/"
    Then I see the text "Welcome to Session 2"

    When I click the next button
    Then I am at the url "/pages/session-2/i-am-worth-it/"
    Then I see the text "I am WORTH It!"

    When I click the submit button
    Then I see the text "Oops!"

    When I select the first quiz option
    When I click the submit button
    Then I am at the url "/pages/session-2/ground-rules/"

    When I click the next button
    Then I am at the url "/pages/session-2/goal-setting-section/"

    When I click the goal submit button
    Then I don't see the text "1 goal saved"

    When I fill in a goal option
    When I click the goal submit button
    Then I see the text "1 goal saved"

    When I click the next button
    Then I am at the url "/pages/session-2/goal-check-in-section/"
    Then I see the text "Goal Check In Section"

  Scenario: Session 3
    When I access the url "/pages/session-3/"
    When I click the next button
    Then I am at the url "/pages/session-3/welcome-to-session-3/"
    Then I see the text "Welcome to Session 3"

    When I click the next button
    Then I am at the url "/pages/session-3/risk-goal-review/"
    Then I see the text "Risk Reduction Goal Review"
