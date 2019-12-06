"""
    A property is used to define each item in an entity

"""
import re


class Property:
    def __init__(self, name, type=None, options=None):
        self.name = name
        self.type = type
        self.validatorFn = None
        self.setterFn = None
        self.derived = False
        self.defaultFn = None
        self.required = None
        if options:
            for op in options:
                val = options[op]
                if val is None:
                    continue
                if op not in ['validate', 'set', 'required', 'default']:
                    raise AttributeError(
                        'Property option %s not recognised' % op)
                field = {
                    'validate': 'validatorFn',
                    'set': 'setterFn',
                    'required': 'required',
                    'default': 'defaultFn'}[op]
                if op == 'default':
                    self.derived = callable(val)
                    if not self.derived:
                        def _derived(obj):
                            return val

                        self.defaultFn = _derived
                        continue
                self[field] = val
        if self.required is None:
            self.required = self.defaultFn is not None

    def __getitem__(self, item):
        return super().__getattribute__(item)

    def __setitem__(self, item, value):
        return super().__setattr__(item, value)

    def get_value(self, obj, value):
        if self.validate(obj, value):
            return value
        return self.defaultFn(obj)

    def set_value(self, obj, value):
        if self.setterFn and value is not None:
            value = self.setterFn(obj, value)

        self.validate(obj, value, raise_exception=True, allow_none=True)
        return value

    def type_name(self):
        return None if self.type is None else self.type.__name__

    def validate(self, obj, value, raise_exception=False, allow_none=False):
        if value is None:
            if self.required and not allow_none:
                if raise_exception:
                    raise AttributeError("%s is required" % self.name)
                return False
            return True
        if self.type is not None and type(value) != self.type:
            if raise_exception:
                raise AttributeError("%s must be a %s" %
                                     (self.name, self.type_name()))
            return False
        if self.validatorFn is not None and not self.validatorFn(obj, value):
            if raise_exception:
                raise AttributeError("%s is not valid for %s " %
                                     (str(value), self.name))
            return False
        return True

    @staticmethod
    def build(properties):
        def fn(p, i):
            if type(p) == str:
                return p if i == 0 else None
            if i < len(p):
                return p[i]
            return None
        return [
            Property(
                fn(p, 0),    # name
                fn(p, 1),    # type
                fn(p, 2))    # options
            for p in properties]

    @staticmethod
    def any(** funcs):
        def _func(obj, value):
            for f in funcs:
                if f(obj, value):
                    return True
            return False
        return _func

    @staticmethod
    def none(** funcs):
        def _func(obj, value):
            for f in funcs:
                if f(obj, value):
                    return False
            return True
        return _func

    @staticmethod
    def all(** funcs):
        def _func(obj, value):
            for f in funcs:
                if not f(obj, value):
                    return False
            return True
        return _func

    @staticmethod
    def in_range(min, max, inclusive=True):
        if inclusive:
            def _func(obj, value):
                return value >= min and value <= max
        else:
            def _func(obj, value):
                return value > min and value < max
        return _func

    @staticmethod
    def is_in(values):
        def _func(obj, value):
            return value in values
        return _func

    @staticmethod
    def in_prop(prop):
        def _func(obj, value):
            return value in obj[prop]
        return _func

    @staticmethod
    def matches(required_regexp):
        regex = re.compile(required_regexp)

        def _func(obj, value):
            return regex.match(value) is not None
        return _func
