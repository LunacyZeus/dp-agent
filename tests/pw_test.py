import os
import json
import anyio
import time
import asyncio
from playwright.async_api import async_playwright
from loguru import logger


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto("https://baidu.com")
        print(await page.title())

        await asyncio.sleep(3)

        logger.debug("开始获取dom树")
        async with await anyio.open_file('buildDomTree.js', 'r') as f:
            js_code = await f.read()

        args = {
            'doHighlightElements': True,
            'focusHighlightIndex': -1,
            'viewportExpansion': 0,
            'debugMode': True,
        }

        start = time.time()
        dom_tree = await page.evaluate(js_code, args)
        end = time.time()

        # print(dom_tree)
        print(f'Time: {end - start:.2f}s')

        os.makedirs('./tmp', exist_ok=True)
        async with await anyio.open_file('./tmp/dom.json', 'w') as f:
            await f.write(json.dumps(dom_tree, indent=1))

        # both of these work for immobilienscout24.de
        # await page.click('.sc-dcJsrY.ezjNCe')
        # await page.click(
        # 	'div > div:nth-of-type(2) > div > div:nth-of-type(2) > div > div:nth-of-type(2) > div > div > div > button:nth-of-type(2)'
        # )

        await asyncio.sleep(1000)


asyncio.run(main())
