import sublime, sublime_plugin
import re

# ST3 changed the way replacing views worked. Just running `self.view.replace(blah)` gives this error:
# "Edit objects may not be used after the TextCommand's run method has returned"
# The easiest way around this is to use a helper class from https://github.com/SublimeText/Tag/commit/f09952751b6a2b131d83927593b6e788afb48a9e
# Instead of this:
#
#  self.view.replace(edit, region, cleaned)
#
# download Edit.py and do this:
#
#  from .Edit import Edit as Edit 
#  with Edit(self.view) as edit:
#    edit.replace(region, cleaned)
#
# But the helper class breaks on ST2. So this now does it both ways. Which is lame.

if sublime.version().startswith('3'):
    from .Edit import Edit as Edit 

# Clean page numbers from notes exported from Skim
class CleanNumbersCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        digits = re.compile("^\\d* - ")  # Find any string that starts with "## - "
        old_page = ''
        cleaned = ''
        for region in self.view.sel():
            if not region.empty():
                # Find/replace all the Skim junk (* Text Note, page 5) with cleaner text (5 - )
                text = self.view.substr(region)

                # (p\\. *)* checks for JSTOR's p. prefix
                text = re.sub("\\* Text Note, page (p\\. *)*(\\d{1,5})\\n", "\\2 - ", text)
                text = re.sub("\\* Anchored Note, page (p\\. *)*(\\d{1,5})\\n", "\\2 - ", text)
                # text = re.sub("\\* Highlight, page (\\d{1,5})\\n", "\\1 - ", text)
                text = re.sub("\\* Highlight, page (p\\. *)*(\\d{1,5})\\n(.*)\\n", "\\2 - \"\\3\"\\n", text)

                # for line in self.view.substr(region).splitlines():
                for line in text.splitlines():
                    # line = re.sub("(\\d+ - )\\n#", "\\n\\1#", line)
                    check_for_digits = digits.match(line)

                    if check_for_digits:
                        current_page = check_for_digits.group(0)

                        if current_page == old_page:
                            line = digits.sub('', line)
                            cleaned += line + '\n'
                        else:
                            old_page = current_page
                            cleaned += line + '\n'
                    else:
                        cleaned += line + '\n'

                # Add space before Markdown H1s
                cleaned = re.sub("(\\d{1,5}) - \\n#", "\\n\\1 - #", cleaned)

                self.view.replace(edit, region, cleaned.rstrip('\n'))  # rstrip removes trailing newlines


# Convert page numbers from two-page PDFs in Skim to page ranges (1 -> 1-2; 2 -> 3-4; etc.)
# Run this after cleaning Skim's cruftiness with CleanNumbersCommand()
# TODO: Incorporate this into regular clean function
class CleanSpreadNumbersCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        def clean_spreads(input_offset):
            digits = re.compile("^\\d* - ")
            cleaned = ''
            offset = int(input_offset) * 2
            for region in self.view.sel():
                if not region.empty():
                    text = self.view.substr(region)

                    for line in text.splitlines():
                        check_for_digits = digits.match(line)

                        if check_for_digits:
                            found_number = re.search("^(\\d{1,5}) - ", line)
                            number = int(found_number.group(1))
                            page_number = number + number - offset  # number + number - offset
                            spread_numbers = '{0}-{1} - '.format(page_number, page_number+1)
                            fixed_line = re.sub("^(\\d{1,5}) - ", spread_numbers, line)
                            cleaned += fixed_line + "\n"
                        else:
                            cleaned += line + "\n"
                    
                    if sublime.version().startswith('2'):
                        self.view.replace(edit, region, cleaned)
                    else:
                        with Edit(self.view) as edit1:
                            edit1.replace(region, cleaned)

        self.view.window().show_input_panel("First absolute page number:", '', clean_spreads, None, None)     


class FixPageNumbers(sublime_plugin.TextCommand):
    def run(self, edit):
        def fix_pages(first_page):
            digits = re.compile("^\\d* - ")
            cleaned = ''
            first_page = int(first_page) - 1

            for region in self.view.sel():
                if not region.empty():
                    text = self.view.substr(region)

                    for line in text.splitlines():
                        check_for_digits = digits.match(line)

                        if check_for_digits:
                            found_number = re.search("^(\\d{1,5}) - ", line)
                            number = int(found_number.group(1))
                            page_number = number + first_page
                            spread_numbers = '{0} - '.format(page_number)
                            fixed_line = re.sub("^(\\d{1,5}) - ", spread_numbers, line)
                            cleaned += fixed_line + "\n"
                        else:
                            cleaned += line + "\n"

                    if sublime.version().startswith('2'):
                        self.view.replace(edit, region, cleaned)
                    else:
                        with Edit(self.view) as edit1:
                            edit1.replace(region, cleaned)

        self.view.window().show_input_panel("First page number in PDF:", '', fix_pages, None, None)
