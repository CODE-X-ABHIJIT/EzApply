import asyncio
from pathlib import Path

from playwright.async_api import async_playwright

from .config import BROWSER_PROFILE


async def login_to_linkedin():
    BROWSER_PROFILE.mkdir(parents=True, exist_ok=True)

    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            str(BROWSER_PROFILE),
            headless=False,
            viewport={"width": 1440, "height": 900},
        )

        page = await context.new_page()

        await page.goto(
            "https://www.linkedin.com/",
            wait_until="domcontentloaded",
        )

        print("\nLinkedIn browser opened.")
        print("Log in to your LinkedIn account normally.")
        print("After your LinkedIn feed/profile is visible,")
        input("Press ENTER here to save the session... ")

        await context.close()


async def read_linkedin_post(url):
    BROWSER_PROFILE.mkdir(
        parents=True,
        exist_ok=True,
    )

    async with async_playwright() as p:

        context = await p.chromium.launch_persistent_context(
            str(BROWSER_PROFILE),
            headless=True,
            viewport={
                "width": 1440,
                "height": 900,
            },
        )

        page = await context.new_page()

        try:
            await page.goto(
                url,
                wait_until="domcontentloaded",
                timeout=60000,
            )

            # Allow LinkedIn to render
            await page.wait_for_timeout(4000)

            # Give the post a little time to appear
            try:
                await page.wait_for_selector(
                    "main",
                    timeout=10000,
                )
            except Exception:
                pass

            post_text = await page.locator(
                "body"
            ).inner_text()

            return post_text

        finally:
            await context.close()

def login():
    asyncio.run(login_to_linkedin())

async def read_all_posts(urls):
    BROWSER_PROFILE.mkdir(
        parents=True,
        exist_ok=True,
    )

    results = []

    async with async_playwright() as p:

        context = await p.chromium.launch_persistent_context(
            str(BROWSER_PROFILE),
            headless=True,
            viewport={
                "width": 1440,
                "height": 900,
            },
        )

        page = await context.new_page()

        for index, url in enumerate(urls, start=1):

            print(
                f"[{index}/{len(urls)}] "
                f"Reading {url}"
            )

            try:
                await page.goto(
                    url,
                    wait_until="domcontentloaded",
                    timeout=60000,
                )

                await page.wait_for_timeout(4000)

                text = await page.locator(
                    "body"
                ).inner_text()

                results.append({
                    "url": url,
                    "text": text,
                    "error": None,
                })

            except Exception as exc:

                results.append({
                    "url": url,
                    "text": "",
                    "error": str(exc),
                })

        await context.close()

    return results
def read_all(urls):
    return asyncio.run(
        read_all_posts(urls)
    )

def read_post(url: str) -> str:
    return asyncio.run(read_linkedin_post(url))