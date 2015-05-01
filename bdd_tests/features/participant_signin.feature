Feature: Participant Sign In Page
  Scenario: Participant Sign In Page Load
    Given I am signed in as a facilitator
    When I access the url "/sign-in-participant/"
    Then I see the text "Sign In My Participant"
