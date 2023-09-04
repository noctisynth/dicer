class NoneTypeCommandError(ValueError):
    """ 预留指令槽位空错误 """
    ...

class CommandRequired(TypeError):
    """ 必须参数未传入错误 """
    ...

class TooManyAliasCommandError(TypeError):
    """ 同义参数传入多个错误 """
    ...