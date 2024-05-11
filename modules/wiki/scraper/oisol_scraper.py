import re
import requests
from lxml import etree

def oisol_infobox_data(dom) -> str|dict:

    # any panel plain text no link
    out = dom.xpath("./div[not (./a) and not (./p) and not (./abbr) and not (./span)]/text()")
    if not out == []:
        return out[0]

    # any panel with text with link
    out = dom.xpath("./div[not (./p) and not (./abbr) and not (./span) and not (./code) and not (./text())]")
    if not out == []:
        data_list = {}
        for item in out[0]:
            data_list[item.xpath("./@title")[0]] = item.xpath("./text()")[0]
        return data_list

    # cost
    out = dom.xpath("./div/p")
    if not out == []:
        data_list = {}
        chassis_name = out[0].xpath("./text()[last()]")[0]
        chassis_name = re.sub(r":\xa0", "", chassis_name)
        data_list[chassis_name] = out[0].xpath("./a/@title")[0]
        data_list["chassis_link"] = "https://foxhole.wiki.gg" + out[0].xpath("./a/@href")[0]
        items = out[0].xpath("./span")
        for item in items:
            data_list[item.xpath("./a/@title")[0]] = item.xpath("./text()")[0]
        return data_list

    # fuel capacity
    out = dom.xpath("./div[(./a) and (./span)]")
    if not out == []:
        data_list = {}
        data_list[out[0].xpath("./a/@title")[0]] = out[0].xpath("./a/text()")[0]
        items = out[0].xpath("./span")
        for item in items:
            data_list[item.xpath("./a/@title")[0]] = item.xpath("./a/@title")[0]
        return data_list

    # repair cost
    out = dom.xpath("./div[not (./a) and (./span)]/span")
    if not out == []:
        return {out[0].xpath("./a/@title")[0]: re.sub(r" ", "", out[0].xpath("./text()")[0])}

    # disable chance
    out = dom.xpath("./div[(./a) and not (./span) and (./text()) and not (./code)]")
    if not out == []:
        data_list = {}
        chance_list = out[0].xpath('./text()')
        sub_system_list = out[0].xpath('./a/@title')
        for i, chance in enumerate(chance_list):
            data_list[sub_system_list[i]] = re.sub( r" ", "", chance)
        return data_list

    # tank armor
    out = dom.xpath("./div[(./abbr) and (./text())]")
    if not out == []:
        return {re.sub( r",\xa0", "", out[0].xpath('./text()')[0]): out[0].xpath('./abbr/text()')[0]}

    # resistance
    out = dom.xpath("./div[(./a) and (./code)]")
    if not out == []:
        data_list = {}
        data_list[out[0].xpath("./a/@title")[0]] = out[0].xpath("./a/text()")[0]
        items = out[0].xpath("./code")
        for item in items:
            data_list[item.xpath("./a/@title")[0]] = item.xpath("./text()")[0]
        return data_list

    return {}

def oisol_infobox_name(dom) -> str:
    out = dom.xpath("./h3/a/text()")
    out += dom.xpath("./h3/text()")
    out += dom.xpath("./h3//abbr/text()")
    out = " ".join(out)
    out = re.sub(r"\t |\t", "", out)
    out = re.sub(r" +", " ", out)
    return out

def oisol_scraper(url:str) -> dict:
    out = {}
    info_box = {}
    page = requests.get(url)
    dom = etree.HTML(page.content)

    out["url"] = url
    out["description"] = dom.xpath("//td/i/text()")
    out["name"] = dom.xpath("//aside[contains(@class, 'portable-infobox')]/h2/text()")[0]
    out["img"] = "https://foxhole.wiki.gg" + dom.xpath("//aside[contains(@class, 'portable-infobox')]/figure//@src")[0]
    # info_box
    items = dom.xpath("//div[contains(@class, 'pi-item')]")
    for item in items:
        item_name = oisol_infobox_name(item)
        info_box[item_name] = oisol_infobox_data(item)
    out["infobox"] = info_box

    return out
