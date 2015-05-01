Feature: Participant Intervention
  Scenario: Participant Intervention Page Load
    Given I am signed in as a participant
    Then I see the text "Welcome to Session 1"
