Feature: Participant Intervention
  Scenario: Going through the intervention
    # TODO: We should really mock the sign-in process here
    # with "Given I am signed in as a participant", but I
    # haven't been able to get that to work -- it signed
    # in instead as a facilitator. So just go through the
    # sign-in steps manually for now using the "When" clause.
    When I sign in as a participant

    # Session 1
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

    # Facilitator after session 1
    When I sign in as the facilitator from a session
    When I click the link "Manage Participant IDs"
    When I click the first participant journal button
    When I click the link "Session 1"
    Then I see the text "My Personal Roadmap"
    Then I see the text "Let's Talk: Sister to Sister"

    # Session 2
    When I sign in as a participant
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

    # Facilitator after session 2
    When I sign in as the facilitator from a session
    When I click the link "Manage Participant IDs"
    When I click the first participant journal button
    When I click the link "Session 2"
    Then I see the text "My Personal Roadmap"

    # Session 3
    When I sign in as a participant
    When I access the url "/pages/session-3/"
    When I click the next button
    Then I am at the url "/pages/session-3/welcome-to-session-3/"
    Then I see the text "Welcome to Session 3"

    When I click the next button
    Then I am at the url "/pages/session-3/risk-goal-review/"
    Then I see the text "Risk Reduction Goal Review"

    # Facilitator after session 3
    When I sign in as the facilitator from a session
    When I click the link "Manage Participant IDs"
    When I click the first participant journal button
    When I click the link "Session 3"
    Then I see the text "My Personal Roadmap"

    # Session 4
    When I sign in as a participant
    When I access the url "/pages/session-4/"
    Then I see the text "Welcome to Your Fourth Session!"

    When I click the next button
    Then I am at the url "/pages/session-4/risk-goal-review/"
    Then I see the text "Risk Reduction Goal Review"

    When I click the next button
    Then I am at the url "/pages/session-4/assessing-relationships-q1/"
    Then I see the text "Assessing relationships"
    Then I see the text "Test question"
    When I click the submit button
    Then I see the text "Oops!"

    # Facilitator after session 4
    When I sign in as the facilitator from a session
    When I click the link "Manage Participant IDs"
    When I click the first participant journal button
    When I click the link "Session 4"
    Then I see the text "My Personal Roadmap"

    # Session 5
    When I sign in as a participant
    When I access the url "/pages/session-5/"
    Then I see the text "Welcome to your Final Session!"

    When I click the next button
    Then I am at the url "/pages/session-5/risk-goal-review/"
    Then I see the text "Risk Reduction Goal Review"

    # Facilitator after session 5
    When I sign in as the facilitator from a session
    When I click the link "Manage Participant IDs"
    When I click the first participant journal button
    When I click the link "Session 5"
    Then I see the text "My Personal Roadmap"
