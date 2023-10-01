class PluginNotFoundError(FileNotFoundError):
    """ 插件不存在 """

class PluginExistsError(FileExistsError):
    """ 插件已安装 """

class PluginInstallFailedError(RuntimeError):
    """ 插件安装失败 """

class PluginUninstallFailedError(RuntimeError):
    """ 插件卸载失败 """