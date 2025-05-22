import asyncio
import random
from typing import Union

from DrissionPage._base.chromium import Chromium
from DrissionPage._pages.chromium_page import ChromiumPage
from DrissionPage._pages.mix_tab import MixTab
from loguru import logger

from pkg.dp_utils.dp import start_browser
from pkg.utils.common.node import get_node_id


class MainProcess(object):
    def __init__(self):
        self.browser: Chromium = None
        self.page: Union[MixTab, ChromiumPage] = None

        self.node_id = get_node_id()  # 初始化节点id
        self.goods_limit = 23
        self.all_ok_count = 0

        self.ua_id = ''
        self.user_agent = ''
        self.browser_path = 'C:\Program Files\Google\Chrome\Application\chrome.exe'

    async def start_dp(self):
        debugger_port = 9222  # random.randint(10000, 40000)  # 9222
        logger.debug(f"使用调试端口->{debugger_port}")
        proxy = '127.0.0.1:7890'
        self.browser = start_browser(debugger_port=debugger_port, browser_path=self.browser_path)

    def enable_mobile(self):
        # 初始化成为手机
        # Phone(page=self.page, ua=self.user_agent).IphoneSe()
        pass

    def close(self):
        if self.browser:
            logger.debug("关闭浏览器")
            self.browser.quit()

    async def run(self, use_login=True):
        await self.start_dp()  # 启动dp

        self.page = self.browser.latest_tab  # 获取最新的tab

        logger.debug(f"开始访问目标页面")
        url = "https://baidu.com"
        self.page.get(url=url)

        js_code = open("data/scripts/buildDomTree.js", "r", encoding="utf-8").read()
        args = {
            'doHighlightElements': True,
            'focusHighlightIndex': -1,
            'viewportExpansion': 0,
            'debugMode': True,
        }
        logger.debug(f"开始执行dom树脚本")
        self.page.run_js(js_code, args)

        input('-->')


async def main():
    process = MainProcess()

    try:
        await process.run()
    except Exception as e:
        logger.error(f"执行异常->{e}")

    finally:
        logger.error("退出环境")
        process.close()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
