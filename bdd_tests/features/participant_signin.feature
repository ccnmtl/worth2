Feature: Participant Sign In Page
  Scenario: Participant Sign In
    Given I am signed in as a facilitator
    When I access the url "/sign-in-participant/"
    Then I see the text "Sign In My Participant"

    When I sign in as a participant
    Then I see the text "Welcome to Session 1"
