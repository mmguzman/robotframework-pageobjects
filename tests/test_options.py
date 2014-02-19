import os
import unittest

from basetestcase import BaseTestCase


class BrowserOptionTestCase(BaseTestCase):
    """
    Tests for basic options and option handling.

    For tests outside of Robot, individual environment variables
    in the form of "$PO_" (eg. $PO_BROWSER) set options.
    A variable of $PO_VAR_FILE can be set to a path to a Python
    module that can set variables as well. Individual
    environment variables override those set in the variable file.

    For tests within the Robot context the behavior follows
    standard Robot Framework..variables can be set on the
    command-line with --variable (eg. --variable=browser=firefox, which
    override the variables set in a variable file, set with --variablefile=

    The BaseTestCase setUp removes all PO environment variables.
    tearDown restores them. It also removes po_log file in
    setUp and tearDown.

    This assures that at the beginning of each test there are no
    PO_ environment variables set and that we are running with
    default options. The tests are then free to set environment variables or
    write variable files as needed.

    This test case tests browser option, but in effect also tests option handling, assuming
    that options are gotten internally using the optionhandler.OptionHandler class.
    """

    def test_unittest_default_browser_should_be_phantomjs(self):
        run = self.run_scenario("test_unittest.py")
        self.assert_run(run, search_output="OK", expected_browser="phantomjs")

    def test_unittest_PO_BROWSER_env_var_set_to_firefox_should_run_firefox(self):
        os.environ["PO_BROWSER"] = "firefox"
        run = self.run_scenario("test_unittest.py")
        self.assert_run(run, search_output="OK", expected_browser="firefox")

    def test_unittest_variable_file_var_set_to_firefox(self):
        try:
            self.write_var_file(browser="firefox")
            os.environ["PO_VAR_FILE"] = self.test_dir + os.sep + "vars.py"
            run = self.run_scenario("test_unittest.py")
            self.assert_run(run, search_output="OK", expected_browser="firefox")

        except AssertionError, e:
            raise e

        finally:
            self.remove_vars_file()

    def test_robot_default_browser_should_be_phantomjs(self):
        run = self.run_scenario("test_robot.robot")
        self.assert_run(run, search_output="PASS", expected_browser="phantomjs")

    def test_robot_variable_set_should_run_in_firefox(self):
        run = self.run_scenario("test_robot.robot", variable="browser:firefox")
        self.assert_run(run, search_output="PASS", expected_browser="firefox")


class OpenTestCase(BaseTestCase):
    """
    Tests the page object's open method. We test in both robot context and
    unittest contexts. Possibilities:

        - No url passed and no homepage attribute set, exception.
        - No url passed but a homepage attribute is set
        - No url passed, baseurl and homepage is set. Homepage is relative
        - url passed, no basurl
        - relative url passed, baseurl
    """

    def test_no_baseurl_set_no_homepage_set_raises_exception_unittest(self):
        run = self.run_scenario("test_unittest_no_homepage.py")
        self.assert_run(run, expected_returncode=1, search_output="No homepage set")

    def test_no_baseurl_set_no_homepage_set_raises_exception_robot(self):
        run = self.run_scenario("test_robot_no_homepage.robot")
        self.assert_run(run, expected_returncode=1, search_output="No homepage set")

    def test_no_baseurl_set_homepage_set_unittest(self):
        run = self.run_scenario("test_unittest.py")
        self.assert_run(run, expected_returncode=0, search_output="OK")

    def test_no_baseurl_homepage_set_robot(self):
        run = self.run_scenario("test_robot.robot")
        self.assert_run(run, expected_returncode=0, search_output="PASS")

    def test_baseurl_set_homepage_set_unittest(self):
        os.environ["PO_BASEURL"] = "file://%s/scenarios" % self.test_dir
        run = self.run_scenario("test_unittest_relative_homepage.py")
        self.assert_run(run, expected_returncode=0, search_output="OK")

    def test_baseurl_set_homepage_set_robot(self):
        run = self.run_scenario("test_robot_relative_homepage.robot",
                                variable="baseurl:file://%s/scenarios" % self.test_dir)
        self.assert_run(run, expected_returncode=0, search_output="PASS")

    def test_url_passed_no_homepage_set_no_baseurl_set_unittest(self):
        run = self.run_scenario("test_abs_url_passed_unittest.py")
        self.assert_run(run, expected_returncode=0, search_output="OK")

    def test_url_passed_no_homepage_set_no_baseurl_set_robot(self):
        run = self.run_scenario("test_robot_abs_url_passed.robot")
        self.assert_run(run, expected_returncode=0, search_output="PASS")

    def relative_url_passed_baseurl_set_unittest(self):
        os.environ["PO_BASEURL"] = "file://%s/scenarios" % self.test_dir
        run = self.run_scenario("test_unittest_relative_url_passed.py")
        self.assert_run(run, expected_returncode=0, search_output="OK")

    def relative_url_passed_baseurl_set_robot(self):
        os.environ["PO_BASEURL"] = "file://%s/scenarios" % self.test_dir
        run = self.run_scenario("test_robot_rel_url_passed.robot", variable="baseurl:%s" % (
            "file://%s/scenarios" % self.test_dir))
        self.assert_run(run, expected_returncode=0, search_output="PASS")

if __name__ == "__main__":
    unittest.main()









