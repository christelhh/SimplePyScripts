#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import logging

from collections import Counter
from pathlib import Path
from typing import List

from jsonlz4_mozLz4 import mozlz4a


def get_sessionstore(file_name_session: Path) -> dict:
    with open(file_name_session, 'rb') as f:
        return mozlz4a.loads_json(f)


def get_tab_urls_from_sessionstore(sessionstore: dict) -> List[str]:
    urls = []
    for w in sessionstore['windows']:
        for t in w['tabs']:
            i = t['index'] - 1
            tab_url = t['entries'][i]['url']
            urls.append(tab_url)

    return urls


def get_tab_urls(file_name_session: Path) -> List[str]:
    json_data = get_sessionstore(file_name_session)
    return get_tab_urls_from_sessionstore(json_data)


def close_tabs(
        file_name_session: Path,
        urls: List[str],
        log: logging.Logger,
):
    modified = False

    json_data = get_sessionstore(file_name_session)
    for w in json_data['windows']:
        for t in reversed(w['tabs']):
            i = t['index'] - 1
            tab_url = t['entries'][i]['url']

            if tab_url in urls:
                w['tabs'].remove(t)

                log.info(f'Removing tab: {tab_url}')
                modified = True

    if modified:
        log.info(f'Saved: {file_name_session}')
        with open(file_name_session, 'wb') as f:
            mozlz4a.dumps_json(f, json_data)


def close_duplicate_tabs(
        file_name_session: Path,
        log: logging.Logger,
):
    json_data = get_sessionstore(file_name_session)
    urls = get_tab_urls_from_sessionstore(json_data)

    need_to_delete = {
        url: count - 1
        for url, count in Counter(urls).items()
        if count > 1
    }

    for w in json_data['windows']:
        for t in reversed(w['tabs']):
            i = t['index'] - 1
            tab_url = t['entries'][i]['url']

            if need_to_delete.get(tab_url, 0) > 0:
                w['tabs'].remove(t)
                need_to_delete[tab_url] -= 1

                log.info(f'Removed duplicate: {tab_url}')

    if need_to_delete:
        log.info(f'Saved: {file_name_session}')
        with open(file_name_session, 'wb') as f:
            mozlz4a.dumps_json(f, json_data)
