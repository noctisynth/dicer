from .const import VERSION
from ..reply.manager import manager
from ..utils.utils import (
    get_name,
    get_group_id,
    get_user_id,
    get_user_card,
    get_user_nickname,
    get_mode,
    get_status
)

def regist_all():
    regist_events()
    regist_vars()

def regist_vars():
    manager.register_method(get_name, "BotName")
    manager.register_method(get_group_id, "GroupID")
    manager.register_method(get_user_id, "UserID")
    manager.register_method(get_user_card, "SenderCard")
    manager.register_method(get_mode, "Mode")
    manager.register_method(get_status, "Status")
    manager.register_method(get_user_nickname, "SenderNickName")
    manager.register_variable(Version=VERSION)

def regist_events():
    regist_main_event()
    regist_general_event()

def regist_main_event():
    manager.register_event("PermissionDenied", "[{SenderCard}]权限不足, {BotName}拒绝执行该指令.\n请先执行`.su`开启权限鉴定.")
    manager.register_event("CommandPermissionDenied", "[{SenderCard}]权限不足, {BotName}拒绝执行指令`{Command}`.\n请先执行`.su`开启权限鉴定.")
    manager.register_event("DebugOn", "[{SenderCard}]漏洞调试模式已启动.")
    manager.register_event("DebugOff", "[{SenderCard}]漏洞调试模式已关闭.")
    manager.register_event("NotManagerYet", "[{SenderCard}]你还不是超级管理员, 无法撤销超级管理员身份.")
    manager.register_event("AlreadyManager", "[{SenderCard}]你已经是超级管理员.")
    manager.register_event("ManagerExit", "[{SenderCard}]你已撤销超级管理员身份.")
    manager.register_event("AuthenticateStarted", "[{SenderCard}]启动超级管理员鉴权, 鉴权令牌已在控制终端展示.")
    manager.register_event("AuthenticateFailed", "[{SenderCard}]鉴权失败, 请检查你的令牌是否正确复制!\n使用`.help sudo`获取帮助信息.")
    manager.register_event("AuthenticateSuccess", "[{SenderCard}]你成功取得了管理员权限.")
    manager.register_event("GroupLeaveSet", "{BotName}离开群聊, 期待与诸君的下一次见面.")
    manager.register_event("BotOn", "{BotName}已开放指令限制.")
    manager.register_event("BotOff", "{BotName}已开启指令限制.")
    manager.register_event("NameSet", "倒是好生有趣的名字, 以后我就是“{NewName}”了.")
    manager.register_event("UninstallFailed", "诶? 卸载失败?")
    manager.register_event("CommandFailed", "指令执行失败, 疑似模式[{Mode}]不存在该指令.")
    manager.register_event("UnknownMode", "未知的跑团模式[{Mode}].")
    manager.register_event("SetPermissionDenied", "仅允许主持人为其它玩家设置数据.")
    manager.register_event("DeletePermissionDenied", "仅允许主持人删除其它玩家数据.")
    manager.register_event("ModeChanged", "已切换跑团模式为[{Mode}].")
    manager.register_event("GroupApproval", "[{UserID}]邀请进入群[{GroupID}].\n处理方式: 同意.")
    manager.register_event("GroupForbidden", "[{UserID}]邀请进入群[{GroupID}].\n处理方式: 拒绝.")
    manager.register_event("BlacklistAdded", "用户[{UserID}]执行非法操作, 已列入黑名单.")
    manager.register_event("CardInit", "[{SenderCard}]角色卡已参照模板[{Mode}]初始化, 异世的诗篇或许就要开始了.")
    manager.register_event("RoleOB", "[{SenderNickName}]身份组设置为旁观者 (OB).")
    manager.register_event("RoleKP", "[{SenderNickName}]身份组设置为主持人 (KP).")
    manager.register_event("main.friend.approve", "[{UserID}]请求添加好友.\n处理方式: 同意.")
    manager.register_event("main.friend.reject", "[{UserID}]请求添加好友.\n处理方式: 拒绝.")
    manager.register_event("mian.friend.new", "[{SenderNickName}]欢迎使用 DicerGirl {Version}, 我是{BotName}. 使用`.help`查看帮助信息, 使用`.bot exit`移除群骰娘, 严禁踢出骰娘. 加入公测群[770386358]可以获得更多支持.")

def regist_general_event():
    manager.register_event("OnSet", "[{SenderCard}]录卡完成, 成功设置基础属性{AttrSetNumber}个, 技能{SkillSetNumber}个.")
    manager.register_event("OnSetWithFailure", "[{SenderCard}]录卡完成, 成功设置基础属性{AttrSetNumber}个, 技能{SkillSetNumber}个, 有{SkillSetFailed}个技能设置失败:\n{FailedDetail}")
    manager.register_event("CardInUse", "[{SenderCard}]使用中人物卡: \n{CardDetail}")
    manager.register_event("CardInCache", "[{SenderCard}]已暂存人物卡: \n{CardDetail}")
    manager.register_event("CardSaved", "[{SenderCard}]成功从缓存保存人物卡属性: \n{CardDetail}")
    manager.register_event("CardDeleted", "[{SenderCard}]已删除使用中的人物卡！")
    manager.register_event("CacheCardCleared", "[{SenderCard}]已清空暂存人物卡数据.")
    manager.register_event("BadRollString", "诶, 出错了, 请检查你的掷骰表达式.\n使用`.help roll`获得掷骰指令使用帮助.")
    manager.register_event("BadMultipleRollString", "[{SenderCard}]多轮掷骰次数过多, 指令拒绝.")
    manager.register_event("MultipleRollStringError", "参数错误, `#`提示符前应当跟随整型数.")
    manager.register_event("BadSex", "{BotName}拒绝将{CharactorName}性别将设置为[{Value}], 这是对物种的侮辱.")
    manager.register_event("AttributeCountError", "参数错误, 这是由于传输的数据数量错误, {BotName}只接受为偶数的参数数量, 这看起来不像是来源于我的错误.\n使用`.help {Command}`查看使用帮助.")
    manager.register_event("ValueError", "[{SkillName}]需要一个整型数但你传入了[{Value}].")
    manager.register_event("UnknownError", "诶, 貌似发生了未知的错误?")
    manager.register_event("SkillDeleted", "[{SenderCard}]已删除技能[{SkillName}], 唔, 真是可惜.")
    manager.register_event("ShootDocimasy", "[{SenderCard}]进行射击检定:\n{DiceDescription}\n检定命中了[{OnShoot}].")
    manager.register_event("CacheNotFound", "未找到缓存数据, 请先使用无参数的`.{ModuleName}`指令进行车卡生成角色卡, 或使用`.st`指令进行录卡.")