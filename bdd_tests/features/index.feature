Feature: Index Page
  Scenario: Index Page Load
    When I access the url "/"
    Then I get a "302"
