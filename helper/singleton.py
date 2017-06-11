#metaclass singleton

class singleton(type):
	instance = None
	def __call__(cls, *args, **kw):
		if not cls.instance:
			cls.instance = super(singleton, cls).__call__(*args, **kw)
		return cls.instance

