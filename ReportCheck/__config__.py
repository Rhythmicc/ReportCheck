import os
import json
from QuickProject import user_root, user_lang, QproDefaultConsole, QproInfoString, _ask

enable_config = True
config_path = os.path.join(user_root, ".ReportCheck_config")

questions = {
    "username": {
        "type": "input",
        "message": "Please input your username:" if user_lang != "zh" else "请输入你的用户名:",
    },
    "password": {
        "type": "password",
        "message": "Please input your password:" if user_lang != "zh" else "请输入你的密码:",
    },
    "remote_url": {
        "type": "input",
        "message": "Please input your remote url:"
        if user_lang != "zh"
        else "请输入你的远程地址:",
    },
    "email": {
        "type": "input",
        "message": "Please input your email:" if user_lang != "zh" else "请输入你的邮箱:",
    },
    "email_password": {
        "type": "password",
        "message": "Please input your email password:"
        if user_lang != "zh"
        else "请输入你的邮箱密码:",
    },
    "smtp_server": {
        "type": "input",
        "message": "Please input your smtp server:"
        if user_lang != "zh"
        else "请输入你的smtp服务器:",
    },
    "email_to": {
        "type": "input",
        "message": "Please input your email to:" if user_lang != "zh" else "请输入你的接收邮箱:",
    },
}


def init_config():
    with open(config_path, "w") as f:
        json.dump(
            {i: _ask(questions[i]) for i in questions}, f, indent=4, ensure_ascii=False
        )
    QproDefaultConsole.print(
        QproInfoString,
        f'Config file has been created at: "{config_path}"'
        if user_lang != "zh"
        else f'配置文件已创建于: "{config_path}"',
    )


class ReportCheckConfig:
    def __init__(self):
        if not os.path.exists(config_path):
            init_config()
        with open(config_path, "r") as f:
            self.config = json.load(f)

    def select(self, key):
        if key not in self.config and key in questions:
            self.update(key, _ask(questions[key]))
        return self.config[key]

    def update(self, key, value):
        self.config[key] = value
        with open(config_path, "w") as f:
            json.dump(self.config, f, indent=4, ensure_ascii=False)
