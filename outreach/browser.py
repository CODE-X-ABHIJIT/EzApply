import asyncio
import os
from pathlib import Path

from playwright.async_api import async_playwright

from .config import LINKEDIN_STATE_FILE


LINKEDIN_URL = "https://www.linkedin.com/"


async def login_to_linkedin():
    print("Starting Playwright...")

    async with async_playwright() as p:

        print("Starting Chromium...")

        browser = await p.chromium.launch(
            headless=False,
            timeout=30000,
            args=[
                "--disable-gpu",
                "--no-sandbox",
                "--disable-dev-shm-usage",
            ],
        )

        print("Chromium started.")

        context = await browser.new_context()

        page = await context.new_page()

        print("Opening LinkedIn...")

        await page.goto(
            LINKEDIN_URL,
            wait_until="domcontentloaded",
            timeout=60000,
        )

        print("\n" + "=" * 72)
        print("LinkedIn login")
        print("=" * 72)

        print("\nLogin to LinkedIn manually in the browser.")

        input(
            "\nAfter successful login, press ENTER here..."
        )

        await context.storage_state(
            path=str(LINKEDIN_STATE_FILE),
        )

        print(
            f"\nLinkedIn session saved to:\n"
            f"{LINKEDIN_STATE_FILE}"
        )

        await context.close()
        await browser.close()

async def read_all_posts(urls):
    """
    Open all LinkedIn post URLs using one authenticated
    browser context.

    The browser runs headless so no browser window is shown.
    """

    if not LINKEDIN_STATE_FILE.exists():

        raise FileNotFoundError(
            "LinkedIn authentication state not found.\n"
            f"Expected: {LINKEDIN_STATE_FILE}\n\n"
            "Run:\n"
            "python -m outreach login"
        )

    results = []

    async with async_playwright() as p:

        browser = await p.chromium.launch(
            headless=True
        )

        context = await browser.new_context(
            storage_state=str(LINKEDIN_STATE_FILE),
            viewport={
                "width": 1440,
                "height": 900,
            },
        )

        page = await context.new_page()

        for index, url in enumerate(urls, start=1):

            print(
                f"[{index}/{len(urls)}] "
                f"Reading: {url}"
            )

            try:

                await page.goto(
                    url,
                    wait_until="domcontentloaded",
                    timeout=60000,
                )

                # Give LinkedIn time to render
                await page.wait_for_timeout(4000)

                # Read visible page content
                post_text = await page.locator(
                    "body"
                ).inner_text()

                results.append(
                    {
                        "url": url,
                        "text": post_text,
                        "error": None,
                    }
                )

            except Exception as exc:

                results.append(
                    {
                        "url": url,
                        "text": "",
                        "error": str(exc),
                    }
                )

        await context.close()
        await browser.close()

    return results


def login():
    asyncio.run(
        login_to_linkedin()
    )


def read_all(urls):
    return asyncio.run(
        read_all_posts(urls)
    )