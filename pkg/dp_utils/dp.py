import os
import shutil
import time
from typing import Union

import requests
from DrissionPage import Chromium
from DrissionPage._configs.chromium_options import ChromiumOptions
from DrissionPage._pages.chromium_page import ChromiumPage
from DrissionPage._pages.mix_tab import MixTab
from DrissionPage._pages.web_page import WebPage
from DrissionPage.errors import ContextLostError
from loguru import logger


def start_browser(debugger_port: int, user_agent: str = '', proxy='', browser_path=''):
    options = ChromiumOptions()
    options.set_argument(arg="--remote-allow-origins=*")
    # options.set_timeouts(pageLoad=5)
    options.set_paths(browser_path=browser_path, local_port=debugger_port)
    options.set_timeouts(base=25, page_load=15, script=15)

    if user_agent:
        options.set_user_agent(user_agent=user_agent)

    # options.set_user_agent(user_agent=user_agent)

    # page = ChromiumPage(chromium_options=options)
    debugger_address = f"127.0.0.1:{debugger_port}"
    options.set_address(address=debugger_address)

    if proxy:
        proxy = '127.0.0.1:7890'
        logger.warning(f"设置代理->{proxy}")
        options.set_proxy(proxy=proxy)

    # 启动dp
    browser = Chromium(options)

    return browser


def get_page_content(page: Union[WebPage, ChromiumPage], tag: str = ""):
    page_content = ""
    for _ in range(5):
        try:
            page_content = page.html
            return page_content
        except ContextLostError:
            logger.warning(f"页面正在刷新,获取网页源码失败")
            pass
        except TimeoutError:
            logger.warning(f"页面加载超时")
            pass
        except Exception as e:
            logger.warning(f"获取网页源码失败,错误信息:{e}")
            pass

        time.sleep(1)

    return page_content


def test_cdp_connection(local_address, count=15, is_show=True):
    logger.debug(f"测试链接到浏览器->{local_address}")
    for _ in range(count):
        try:
            ws_json = requests.get(url=f'http://{local_address}/json', timeout=2).json()
            tab_id = [i['id'] for i in ws_json if i['type'] == 'page']
            if not tab_id:
                logger.error(f"连接浏览器失败,等待1秒重试,local_address({local_address})")
                time.sleep(1)
                continue
            if is_show:
                logger.info(f"检测cdp协议正常->{ws_json}")
            else:
                logger.success(f"检测cdp协议正常")

            return True
        except Exception as e:
            logger.debug(f"cdp链接异常->{e}")
            time.sleep(1)
            continue

    return False


def connect_browser(debugger_port, count=5):  # 链接已有的浏览器
    local_address = f"127.0.0.1:{debugger_port}"
    if not test_cdp_connection(local_address, count=count, is_show=True):
        logger.error(f"多次链接浏览器端口异常,请检查浏览器是否打开")
        raise ContextLostError

    logger.debug("测试链接成功 开始cdp接管")

    options = ChromiumOptions()
    # options.set_argument(arg="--remote-allow-origins=*")
    # options.set_timeouts(pageLoad=5)
    options.set_paths(local_port=debugger_port)
    options.set_timeouts(base=25, page_load=15, script=15)

    debugger_address = f"127.0.0.1:{debugger_port}"
    options.set_address(address=debugger_address)

    # 启动dp
    browser = Chromium(options)

    return browser


def wait_for_navigation(page: Union[WebPage, MixTab, ChromiumPage], target_url, times=40):
    logger.debug(f"开始等待页面({target_url})跳转")
    for i in range(times):
        if i % 5 == 0:
            logger.debug(f"等待页面跳转到->{target_url},当前页面[{page.url}]")

        if target_url in page.url:
            return True
        logger.debug(f"等待页面跳转到->{target_url}")
        time.sleep(1)

    return False


def delete_userdata_dir():
    # 目标目录路径
    target_dir = r"C:\Users\Administrator\AppData\Local\Temp\DrissionPage\userData"

    # 遍历目标目录
    for item in os.listdir(target_dir):
        item_path = os.path.join(target_dir, item)

        # 检查是否是目录
        if os.path.isdir(item_path):
            # 删除目录及其内容
            shutil.rmtree(item_path)
            logger.debug(f"已删除目录: {item_path}")

    logger.debug("所有子目录已删除完毕。")
