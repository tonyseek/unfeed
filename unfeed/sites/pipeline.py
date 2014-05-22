import json

from brownant.pipeline.base import PipelineProperty


class DictionaryProperty(PipelineProperty):

    def prepare(self):
        self.attr_names.setdefault('text_response_attr', 'text_response')
        self.options.setdefault('decoder', json.loads)

    def provide_value(self, obj):
        text_response = self.get_attr(obj, 'text_response_attr')
        return json.loads(text_response)


class DictionaryValueProperty(PipelineProperty):

    required_attrs = {'dict_key'}
    _missing = object()

    def prepare(self):
        self.attr_names.setdefault('dict_attr', 'dict_response')
        self.options.setdefault('default', self._missing)
        self.options.setdefault('type', self._missing)

    def provide_value(self, obj):
        dict_attr = self.get_attr(obj, 'dict_attr')
        default_value = self.options['default']
        type_converter = self.options['type']

        # processes with default value
        if self.dict_key in dict_attr:
            value = dict_attr[self.dict_key]
        elif default_value is not self._missing:
            value = self.options['default']
        else:
            raise KeyError(repr(self.dict_key))

        # applies type converter
        if type_converter is not self._missing:
            if default_value is self._missing:
                raise RuntimeError(':type must be used with :default together')
            try:
                value = self.options['type'](value)
            except ValueError:
                value = default_value

        # returns the final result
        return value
