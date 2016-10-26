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
→
```
def method(arg):
#	bar = 'baz'
	return arg
```