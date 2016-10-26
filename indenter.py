import sublime_plugin
import re

class Indenter(object):
	def __init__(self, view):
		self.view = view

		self.inited = False

		syntax_vars = view.meta_info('shellVariables', 0)

		if syntax_vars:
			self.inited = True

			self.comment_characters = [var['value'] for var in syntax_vars if var['name'] == 'TM_COMMENT_START'][0].strip()

			if self.comment_characters:
				view.run_command('detect_indentation')

				translate_to_spaces = view.settings().get('translate_tabs_to_spaces', False)

				if translate_to_spaces:
					self.indent_characters = u' ' * view.settings().get('tab_size', 4)
				else:
					self.indent_characters = u'	'

				self.commented = re.compile('^(%s ?)(.+)' % self.comment_characters, re.DOTALL)
				self.indented = re.compile('^(%s)(.+)' % self.indent_characters, re.DOTALL)

#				print 'indenter', self.commented.pattern, self.indented.pattern

	def indent(self, edit):
		if self.inited:
			self.process(edit, self.indent_line)
		else:
			self.view.run_command('indent')

	def unindent(self, edit):
		if self.inited:
			self.process(edit, self.unindent_line)
		else:
			self.view.run_command('unindent')

	def process(self, edit, processor):
		view = self.view

		selections = view.sel()
		new_selections = []

		for region in selections:
			whole_region = view.full_line(region)
			text = u''
			delta = 0
			offset = len(self.indent_characters)

			if not whole_region.empty():
				lines = view.lines(view.line(region))

				for line in lines:
					line_text = view.substr(view.full_line(line))
					line_text_len = len(line_text)

					if len(line_text) > len(self.comment_characters) + 1:
						line_text = processor(line_text)
						delta += len(line_text) - line_text_len

					text += line_text

				view.replace(edit, whole_region, text)

			if delta < 0:
				offset = -offset
			elif delta == 0:
				offset = 0

			begin = region.begin() + offset
			end = region.end() + delta

			if begin < whole_region.begin():
				begin = whole_region.begin()

			new_selections.append(sublime.Region(begin, end))

		selections.clear()
		for region in new_selections:
			selections.add(region)

	def indent_line(self, line):
		if line.startswith(self.comment_characters):
			line = re.sub(self.commented, u'%s%s%s' % ('\g<1>', self.indent_characters, '\g<2>'), line)
		else:
			line = u'%s%s' % (self.indent_characters, line)

		return line

	def unindent_line(self, line):
		if line.startswith(self.comment_characters):
			line_parts = re.findall(self.commented, line)

			if line_parts:
				line = line_parts[0][1]
				line = re.sub(self.indented, u'\g<2>', line)
				line = u'%s%s' % (line_parts[0][0], line)
		else:
			line = re.sub(self.indented, u'\g<2>', line)

		return line


class IndentCommand(sublime_plugin.TextCommand):
	def __init__(self, *args):
		super(IndentCommand, self).__init__(*args)

		self.indenter = Indenter(self.view)


class IndentTextCommand(IndentCommand):
	def run(self, edit):
		self.indenter.indent(edit)


class UnindentTextCommand(IndentCommand):
	def run(self, edit):
		self.indenter.unindent(edit)