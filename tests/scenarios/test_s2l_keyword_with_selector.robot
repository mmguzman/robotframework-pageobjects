*** Settings ***
Library    widget_rel_uri_attr.Page

*** Test Cases ***

Test Click Element With Selector
    Open Widget Page
    Click Element    search
    [teardown]    Close Widget Page