Indenter – simple plugin, extending default Sublime Text `indent` and `unindent` commands.
It support commented lines and indent it content, instead of whole line.

Indent:
```
def method(arg):
#	bar = 'baz'
	return arg
```
→
```
def method(arg):
#		bar = 'baz'
		return arg
```

Unindent:
```
def method(arg):
#		bar = 'baz'
		return arg
```
←
```
def method(arg):
#	bar = 'baz'
	return arg
```

# Installation
Supports Sublime Text 2 and 3.
Use yours version number in directory path.

## OS X
```
cd ~/"Library/Application Support/Sublime Text 2/Packages"
git clone https://github.com/gzzz/sublime-indenter.git Indenter
```

## Windows
```
cd %AppData%\Sublime Text 2\Packages\
git clone https://github.com/gzzz/sublime-indenter.git Indenter
```