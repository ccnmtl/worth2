Feature: Index Page
  Scenario: Index Page Load
    When I access the url "/"
    Then I get a 200
    Then I see the text "Get Started"

  Scenario: Facilitator Sign In
    When I sign in as a facilitator
    Then I see the text "View as Facilitator"
