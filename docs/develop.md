## 插件开发
### 1. 配置
首先, 创建一个`__init__.py`, 配置以下内容, 这里以 SCP 模式为例:
```python
from .agent import Agent

__type__ = "plugin"
__charactor__ = Agent
__name__ = "scp"
__cname__ = "特工"
```
其中`__type__`声明该库为依赖于`Dicer Girl`的插件, 内容必须为`plugin`.

`__charactor__`为人物卡专有类, 详见[建立一个角色卡](#x-建立一个角色卡).

`__name__`声明该库的模式名称, 该名称必须是唯一的且为小写英文, 不应当有特殊字符.

`__cname__`为角色卡的默认称呼, 例如 SCP 模式中称呼人物为`特工`, COC 模式中称呼人物为`调查员`.

### 2. 建立一个角色卡
新建一个`charactor.py`(也可以为其它名字), 写入以下内容:
```python
class Charactor:
    def __init__(self):
        self.name = "默认人物名"
        self.age = 20 # 默认人物年龄
        # ...其它自定义内容
        self.skills = {}

    # ...其它你的自定义方法

    def __str__(self) -> str: # 也可以是__repr__, 这两者是等效的
        return str # 返回一个人物基本属性描述
    
    def output(self) -> str:
        return str # 返回一个详细的人物卡
    
    def skills_output(self) -> str:
        return str # 返回一个详细的人物技能数据

    def out_age(self) -> str: # 这里为`our_age`, 你可以使用`.show age`指令来得到它的返回值, 同样, 你可以将`age`设置为其它值
        return f"角色年龄为: {self.age}"
    
    # ...其它`.show`输出内容

    def load(self, data: dict): # 这里也可以加入特定操作, 这里是为了导入人物卡
        self.__dict__.update(data)
        return self
```