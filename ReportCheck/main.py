from QuickProject.Commander import Commander
from QuickProject import QproErrorString
from . import *
import time

app = Commander(name)


def email(
    fr: str = "",
    password: str = "",
    smtp: str = "",
    to: list = [],
    status: str = None,
    success: bool = True,
):
    if not (_email := fr):
        return
    if not success:
        return requirePackage(".RawSender", "Sender")(
            _email,
            password,
            smtp,
            "CUP填报检查",
        ).send(to, "【学生每日填报】发生错误", f"{status}")
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    if not status:
        requirePackage(".RawSender", "Sender")(
            _email,
            password,
            smtp,
            "CUP填报检查",
        ).send(to, "【学生每日填报】全部已上报", f"时间: {current_time}")
    else:
        requirePackage(".RawSender", "Sender")(
            _email,
            password,
            smtp,
            "CUP填报检查",
        ).send(to, "【学生每日填报】存在未上报", f"名单: {status}")


def _check(
    remote_url: str = "",
    username: str = "",
    password: str = "",
    fr: str = "",
    email_password: str = "",
    smtp: str = "",
    to: list = [],
):
    import time
    from selenium.webdriver.common.by import By

    SuccesString = "[bold green][成功][/]"

    QproDefaultConsole.record = True

    QproDefaultConsole.log(QproInfoString, "正在打开浏览器...")
    driver = driver_create(remote_url)

    QproDefaultConsole.log(SuccesString, "浏览器已打开")
    QproDefaultConsole.log(QproInfoString, "正在进入检查页面...")
    driver.get("https://eserv.cup.edu.cn/v2/fillForm/report")

    time.sleep(2)

    QproDefaultConsole.log(SuccesString, "已进入检查页面")
    QproDefaultConsole.log(QproInfoString, "正在登录...")
    driver.switch_to.frame("loginIframe")
    inputs = driver.find_elements(By.TAG_NAME, "input")
    inputs[0].send_keys(username)
    inputs[1].send_keys(password)

    driver.find_element(By.CLASS_NAME, "login_btn").click()

    QproDefaultConsole.log(SuccesString, "已登录")
    QproDefaultConsole.log(QproInfoString, "正在查找上报信息...")

    time.sleep(15)

    driver.switch_to.default_content()

    btn = driver.find_element(By.CLASS_NAME, "operation")
    if not btn:
        QproDefaultConsole.log(QproErrorString, "未找到上报信息")
        return email(fr, email_password, smtp, to, "未找到上报信息", success=False)
    btn.click()

    QproDefaultConsole.log(SuccesString, "已找到上报信息")
    QproDefaultConsole.log(QproInfoString, "正在检查今日是否已上报...")

    time.sleep(5)  # 等待加载

    driver.find_elements(By.CLASS_NAME, "el-input__inner")[2].click()
    time.sleep(1)  # CSS 动画
    driver.find_elements(By.CLASS_NAME, "el-select-dropdown__item")[3].click()
    driver.find_elements(By.CLASS_NAME, "zl-button-primary")[1].click()

    time.sleep(5)

    content = driver.find_element(By.CLASS_NAME, "report_con")

    if "暂无数据" in content.text:
        QproDefaultConsole.log(SuccesString, "全部已上报")
        driver.quit()
        return email(fr, email_password, smtp, to)

    QproDefaultConsole.log(SuccesString, "存在未上报")
    QproDefaultConsole.log(QproInfoString, "正在获取未上报名单...")

    name_lists = []

    while True:
        content = driver.find_element(By.CLASS_NAME, "report_con")
        table = content.find_element(By.TAG_NAME, "table")
        trs = table.find_elements(By.TAG_NAME, "tr")

        for tr in trs:
            tds = tr.find_elements(By.TAG_NAME, "td")
            if len(tds) <= 1:
                continue
            name_lists.append(tds[1].text)

        btn = driver.find_element(By.CLASS_NAME, "btn-next")
        if not btn.get_property("disabled"):
            btn.click()
            time.sleep(5)
        else:
            break
    QproDefaultConsole.log(SuccesString, "已获取未上报名单")
    driver_close(remote_url)
    QproDefaultConsole.log(QproInfoString, "正在发送邮件...")
    email(fr, email_password, smtp, to, "、".join(name_lists))
    QproDefaultConsole.log(SuccesString, "已发送邮件")


@app.command()
def check(
    remote_url: str,
    username: str,
    password: str,
    fr: str,
    email_password: str,
    smtp: str,
    to: list,
    name: str = "",
):
    """
    检查今日未上报情况
    Check today's unreported situation

    :param remote_url: 远程浏览器地址 Remote browser address
    :param username: 学号/工号 Username
    :param password: 密码 Password
    :param fr: 发件人邮箱 From email
    :param email_password: 发件人邮箱密码 From email password
    :param smtp: SMTP 服务器 SMTP server
    :param to: 收件人邮箱列表 To email list
    :param name: 姓名 Name
    """
    try:
        _check(remote_url, username, password, fr, email_password, smtp, to)
    except:
        driver_close(remote_url)
        QproDefaultConsole.print(
            QproErrorString, f"出现错误: {username}{f': {name}' if name else ''}"
        )
        QproDefaultConsole.print_exception()
        QproDefaultConsole.save_html("log.html")
        with open("log.html", "r", encoding="utf-8") as f:
            email(fr, email_password, smtp, [fr], f.read(), False)
        email(fr, email_password, smtp, to, "未知错误", False)
        raise SystemExit(1)


def main():
    """
    注册为全局命令时, 默认采用main函数作为命令入口, 请勿将此函数用作它途.
    When registering as a global command, default to main function as the command entry, do not use it as another way.
    """
    app()


if __name__ == "__main__":
    main()
