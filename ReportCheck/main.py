from QuickProject.Commander import Commander
from . import *
import time

app = Commander()


def email(status: str = None, success: bool = True):
    if not (_email := global_config.select("email")):
        return
    if not success:
        return requirePackage(".RawSender", "Sender")(
            _email,
            global_config.select("email_password"),
            global_config.select("smtp_server"),
            "CUP填报检查",
        ).send([global_config.select("email_to")], "【学生每日填报】发生错误", f"{status}")
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    if not status:
        requirePackage(".RawSender", "Sender")(
            _email,
            global_config.select("email_password"),
            global_config.select("smtp_server"),
            "CUP填报检查",
        ).send(
            [global_config.select("email_to")], "【学生每日填报】全部已上报", f"时间: {current_time}"
        )
    else:
        requirePackage(".RawSender", "Sender")(
            _email,
            global_config.select("email_password"),
            global_config.select("smtp_server"),
            "CUP填报检查",
        ).send([global_config.select("email_to")], "【学生每日填报】存在未上报", f"名单: {status}")


def _check(press: bool = False):
    """
    检查今日未上报情况
    Check today's unreported situation

    :param press: 是否催报
    """
    import time
    from selenium import webdriver
    from selenium.webdriver.common.by import By

    QproDefaultConsole.record = True

    with QproDefaultConsole.status("正在打开浏览器...") as st:
        if url := global_config.select("remote_url"):
            driver = webdriver.Remote(
                command_executor=url,
                desired_capabilities=webdriver.DesiredCapabilities.CHROME,
            )
        else:
            driver = webdriver.Chrome()

        QproDefaultConsole.log(QproInfoString, "浏览器已打开")
        st.update("正在进入检查页面...")
        driver.get("https://eserv.cup.edu.cn/v2/fillForm/report")

        time.sleep(2)

        QproDefaultConsole.log(QproInfoString, "已进入检查页面")
        st.update("正在登录...")
        driver.switch_to.frame("loginIframe")
        inputs = driver.find_elements(By.TAG_NAME, "input")
        inputs[0].send_keys(global_config.select("username"))
        inputs[1].send_keys(global_config.select("password"))

        driver.find_element(By.CLASS_NAME, "login_btn").click()

        st.update("正在查找上报信息...")

        time.sleep(10)

        driver.switch_to.default_content()

        btn = driver.find_element(By.CLASS_NAME, "operation")
        if not btn:
            QproDefaultConsole.log(QproErrorString, "未找到上报信息")
            return
        btn.click()

        QproDefaultConsole.log(QproInfoString, "已找到上报信息")
        st.update("正在检查今日是否已上报...")

        time.sleep(5)  # 等待加载

        driver.find_elements(By.CLASS_NAME, "el-input__inner")[2].click()
        time.sleep(1)  # CSS 动画
        driver.find_elements(By.CLASS_NAME, "el-select-dropdown__item")[3].click()
        driver.find_elements(By.CLASS_NAME, "zl-button-primary")[1].click()

        time.sleep(3)

        content = driver.find_element(By.CLASS_NAME, "report_con")

        if "暂无数据" in content.text:
            QproDefaultConsole.log(QproInfoString, "全部已上报")
            driver.quit()
            return email()

        QproDefaultConsole.log(QproInfoString, "存在未上报")
        st.update("正在获取未上报名单...")

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
                if press:
                    tds[-1].find_elements(By.TAG_NAME, "p")[-1].click()  # 催报

            btn = driver.find_element(By.CLASS_NAME, "btn-next")
            if not btn.get_property("disabled"):
                btn.click()
                time.sleep(3.5)
            else:
                break
        QproDefaultConsole.log(QproInfoString, "已获取未上报名单")
        st.update("正在发送邮件...")
        email("、".join(name_lists))
    QproDefaultConsole.log(QproInfoString, "已发送邮件")
    QproDefaultConsole.save_html("log.html")


@app.command()
def check(press: bool = False):
    """
    检查今日未上报情况
    Check today's unreported situation

    :param press: 是否催报
    """
    try:
        _check(press)
    except:
        QproDefaultConsole.print_exception()
        QproDefaultConsole.save_html("log.html")
        with open("log.html", "r", encoding="utf-8") as f:
            email(f.read(), False)


def main():
    """
    注册为全局命令时, 默认采用main函数作为命令入口, 请勿将此函数用作它途.
    When registering as a global command, default to main function as the command entry, do not use it as another way.
    """
    app()


if __name__ == "__main__":
    main()
