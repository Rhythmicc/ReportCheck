const completionSpec: Fig.Spec = {
    "name": "ReportCheck",
    "description": "ReportCheck",
    "subcommands": [
        {
            "name": "--help",
            "description": "获取帮助"
        },
        {
            "name": "check",
            "description": "检查今日未上报情况\n    Check today's unreported situation",
            "args": [
                {
                    "name": "remote_url",
                    "description": "远程浏览器地址 Remote browser address"
                },
                {
                    "name": "username",
                    "description": "学号/工号 Username"
                },
                {
                    "name": "password",
                    "description": "密码 Password"
                },
                {
                    "name": "fr",
                    "description": "发件人邮箱 From email"
                },
                {
                    "name": "email_password",
                    "description": "发件人邮箱密码 From email password"
                },
                {
                    "name": "smtp",
                    "description": "SMTP 服务器 SMTP server"
                }
            ],
            "options": [
                {
                    "name": "-to",
                    "description": "收件人邮箱列表 To email list",
                    "args": {
                        "name": "to",
                        "description": "收件人邮箱列表 To email list",
                        "isVariadic": true
                    }
                },
                {
                    "name": "--press",
                    "description": "是否催报 Whether to press",
                    "isOptional": true
                }
            ]
        }
    ]
};
export default completionSpec;
