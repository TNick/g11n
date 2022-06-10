import pluggy

g11n_hookspec = pluggy.HookspecMarker("g11n")
g11n_hookimpl = pluggy.HookimplMarker("g11n")

g11n_pm = pluggy.PluginManager("g11n")
g11n_pm.add_hookspecs(g11n_hookspec)
g11n_pm.load_setuptools_entrypoints("g11n")
