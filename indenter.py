import sublime, sublime_plugin
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

				use_spaces = view.settings().get('translate_tabs_to_spaces', False)

				if use_spaces:
					self.indent_characters = u' ' * view.settings().get('tab_size', 4)
				else:
					self.indent_characters = u'	'

				self.commented = re.compile(u'^(?P<comment>%s+ ?)(?P<tail>.+)' % self.comment_characters, re.DOTALL)
				self.indented = re.compile(u'^(?P<first_indent>%s)(?P<tail>.+)' % self.indent_characters, re.DOTALL)

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
		processed_selections = []

		for region in selections:
			whole_region = view.full_line(region)
			text = u''
			delta = 0
			offset = 0

			if not whole_region.empty():
				lines = view.lines(whole_region)

				for line in lines:
					line_str = view.substr(view.full_line(line))
					line_str_len = len(line_str)

					if len(line_str.replace(self.comment_characters, '').strip()) > 0:
						line_str = processor(line_str)
						delta += len(line_str) - line_str_len

						if line == lines[0] and delta != 0:
							offset = len(self.indent_characters)

					text += line_str

				view.replace(edit, whole_region, text)

			if delta < 0:
				offset = -offset

			begin = region.begin() + offset
			end = region.end() + delta

			if begin < whole_region.begin():
				begin = whole_region.begin()

			processed_selections.append(sublime.Region(begin, end))

		if processed_selections:
			selections.clear()
			for region in processed_selections:
				selections.add(region)

	def indent_line(self, line):
		if line.startswith(self.comment_characters):
			line = re.sub(self.commented, u'%s%s%s' % ('\g<comment>', self.indent_characters, '\g<tail>'), line)
		else:
			line = u'%s%s' % (self.indent_characters, line)

		return line

	def unindent_line(self, line):
		if line.startswith(self.comment_characters):
			line_parts = re.search(self.commented, line)

			if line_parts:
				line = line_parts.group('tail')
				line = re.sub(self.indented, u'\g<tail>', line)
				line = u'%s%s' % (line_parts.group('comment'), line)
		else:
			line = re.sub(self.indented, u'\g<tail>', line)

		return line


class IndentCommand(sublime_plugin.TextCommand):
	def __init__(self, *args):
		super(IndentCommand, self).__init__(*args)

		self.indenter = Indenter(self.view)


class IndentLinesCommand(IndentCommand):
	def run(self, edit):
		self.indenter.indent(edit)


class UnindentLinesCommand(IndentCommand):
	def run(self, edit):
		self.indenter.unindent(edit)