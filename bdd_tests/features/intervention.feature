Feature: Participant Intervention
  Scenario: Participant Intervention Page Load
    Given I am signed in as a facilitator
    When I sign in as a participant
    Then I see the text "Welcome to Session 1"

  Scenario: Session 1
    Given I am signed in as a participant
    When I access the url "/pages/session-1/"
    When I click the next button
    Then I am at the url "/pages/session-1/orientation/"
    Then I see the text "Orientation Video"
