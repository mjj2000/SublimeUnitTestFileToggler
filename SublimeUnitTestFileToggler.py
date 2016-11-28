import os
import re
import sublime
import sublime_plugin

class UnitTestFileToggleCommand(sublime_plugin.WindowCommand):
    def run(self):
        path = self.window.active_view().file_name()
        is_test_file = re.match('.+\.spec\.js$', path) is not None

        if is_test_file:
            # switch to source
            source_file_path = re.sub(r'\.spec\.js$', '.js', path)
            if not os.path.isfile(source_file_path):
                msg = 'Source file not found: %s' % source_file_path
                sublime.error_message(msg)
                return
            self.window.open_file(source_file_path, group=0)
        else:
            # switch to test
            test_file_path = re.sub(r'\.js$', '.spec.js', path)
            if not os.path.isfile(test_file_path):
                # Ask the user for confirmation
                msg = 'Test file does not exist yet. Create %s now?' % \
                      test_file_path
                if not sublime.ok_cancel_dialog(msg):
                    return
                else:
                    open(test_file_path, "a").close()

            self.window.open_file(test_file_path, group=0)
