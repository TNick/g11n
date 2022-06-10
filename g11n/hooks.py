import pluggy

g11n_hookspec = pluggy.HookspecMarker("g11n")
g11n_hookimpl = pluggy.HookimplMarker("g11n")

g11n_pm = pluggy.PluginManager("g11n")


class Hooks:
    @g11n_hookspec
    def load_language(self, lang: str):
        """
        Invites the plugins to load all the data related to a language
        into a dictionary.
        """
        pass


g11n_pm.add_hookspecs(Hooks)
g11n_pm.load_setuptools_entrypoints("g11n")
