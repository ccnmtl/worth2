Feature: Index Page
  Scenario: Index Page Load
    When I access the url "/"
    Then I get a 200

  Scenario: Facilitator Sign In
    When I sign in as a facilitator
    Then I see the text "View Intervention as Facilitator"
