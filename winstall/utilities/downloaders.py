import asyncio
import os
import re
import tempfile
from tempfile import mkdtemp
from typing import List
from urllib.parse import unquote_plus

import requests
from pyppeteer import launch
from requests.exceptions import RequestException


async def _wait_for_download_completion(download_dir: str) -> str:
    while len(os.listdir(download_dir)) == 0:
        await asyncio.sleep(0.5)
    downloaded_file = None
    while not downloaded_file or downloaded_file.endswith(".crdownload"):
        downloaded_file = next(os.scandir(download_dir)).path
        await asyncio.sleep(0.5)
    return downloaded_file


def from_browser(url: str, selectors: List[str] = None) -> str:
    raise NotImplementedError


async def from_filecr(url: str) -> str:
    browser = await launch(headless=True)
    page = await browser.newPage()
    await page.goto(url)
    await asyncio.sleep(10)
    await page.evaluate("""document.querySelector("#sh_pdf_download-2 > form > input.download_submit.download_allow.button.mid.dark.spaced").click();""")
    download_dir = tempfile.mkdtemp()
    await page._client.send("Page.setDownloadBehavior", {"behavior": "allow", "downloadPath": download_dir})
    await asyncio.sleep(70)
    await page.evaluate("""document.querySelector("body > div.section-wrap.counter-section > div > section > div:nth-child(1) > div.ac-btn > a").click();""")
    archive_file = await _wait_for_download_completion(download_dir)
    await browser.close()
    return archive_file


def from_gdrive(url: str) -> str:
    raise NotImplementedError


def from_mega(url: str) -> str:
    raise NotImplementedError


def from_magnet(link: str) -> str:
    raise NotImplementedError


def from_torrent(torrent: str) -> str:
    raise NotImplementedError


def from_url(url: str) -> str:
    """
    Download the file from its url.

    :param url: The url of the file to download.
    :type url: str
    :return: The full path of the downloaded file.
    :rtype: str
    """
    try:
        with requests.get(url=url, allow_redirects=True, stream=True, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Gecko/20100101 Firefox/80.0'}) as r:
            downloaded_file = os.path.join(mkdtemp(), get_filename(url))
            with open(downloaded_file, "wb") as f:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
                        f.flush()
            return downloaded_file
    except RequestException as e:
        print(e)


def get_filename(url: str) -> str:
    """
    Retrieve the filename of the file from its url.

    :param url: The url of the file.
    :type url: str
    :return: The filename of the file.
    :rtype: str
    """
    try:
        with requests.head(url, allow_redirects=True, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Gecko/20100101 Firefox/80.0'}) as r:
            if "Content-Disposition" in r.headers.keys():
                return unquote_plus(re.findall("filename=(.+)", r.headers["Content-Disposition"])[0]).replace('"', "").replace(" ", "")
            elif is_valid_filename(r.url.split("/")[-1]):
                return unquote_plus(r.url.split("/")[-1]).replace('"', "").replace(" ", "")
            else:
                return unquote_plus(url.split("/")[-1]).replace('"', "").replace(" ", "")
    except RequestException as e:
        print(e)


def is_valid_filename(filename: str) -> bool:
    """
    Check if the filename is valid.

    :param filename: The filename to be checked.
    :type filename: str
    :return: Returns if the filename is valid.
    :rtype: bool
    """
    return bool(re.match("^.+\\.[A-Za-z]{1,6}$", filename))
