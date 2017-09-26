from typing import List, Union


class deeptracy_plugin(object):
    def __init__(self, lang: Union[str, List[str]]):
        if not hasattr(lang, "append"):
            self.lang = [lang]
        else:
            self.lang = lang

    def __call__(self, f):
        f.deeptracy_plugin_enable = True
        f.deeptracy_plugin_lang = self.lang

        return f
