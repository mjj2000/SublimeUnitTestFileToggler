import os
import re
import sublime
import sublime_plugin
from .constant import DEFAULT_TEST_FILE_NAME_SUFFIX

class UnitTestFileToggleCommand(sublime_plugin.WindowCommand):
  def run(self):
    path = self.window.active_view().file_name()

    # load settings
    test_file_name_suffix = sublime\
      .load_settings('SublimeUnitTestFileToggler.sublime-settings')\
      .get('testFileNameSuffix', DEFAULT_TEST_FILE_NAME_SUFFIX)

    # get file ext
    m = re.match('.+\.([^.]+)$', path)
    file_ext = m is not None and m.group(1)

    # is test file?
    m = re.match('.+(' + re.escape(test_file_name_suffix) + ')\.' + file_ext + '$', path)
    is_test_file = m is not None

    if is_test_file:
      # switch to source
      source_file_path = re.sub(
        r'%s\.%s$' % (test_file_name_suffix, file_ext),
        '.%s' % file_ext,
        path
      )
      if not os.path.isfile(source_file_path):
        # alert about source not fould!
        msg = 'Source file not found: %s' % source_file_path
        sublime.error_message(msg)
        return

      self.window.open_file(source_file_path, group=0)
    else:
      # switch to test
      test_file_path = re.sub(
        r'\.' + file_ext + '$',
        '%s.%s' % (test_file_name_suffix, file_ext),
        path
      )
      if not os.path.isfile(test_file_path):
        # confirmation for creating test file
        msg = 'Test file does not exist yet. Create %s now?' % \
            test_file_path
        if not sublime.ok_cancel_dialog(msg):
          return
        else:
          open(test_file_path, "a").close()

      self.window.open_file(test_file_path, group=0)
