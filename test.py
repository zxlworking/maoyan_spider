#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import re

if __name__ == '__main__':
    temp_str = "Headers[('Server', 'openresty'), ('Date', 'Thu, 16 Apr 2020 04:59:28 GMT'), ('Content-Length', '0'), ('Connection', 'keep-alive'), ('M-TraceId', '3686596330078441911'), ('Location', 'https://verify.meituan.com/v2/web/general_page?action=spiderindefence&requestCode=b22688da2c044ad88b678b80e959fe75&platform=1000&adaptor=auto&succCallbackUrl=https%3A%2F%2Foptimus-mtsi.meituan.com%2Foptimus%2FverifyResult%3ForiginUrl%3Dhttp%253A%252F%252Fmaoyan.com%252Ffilms%252F1258163')]"

    result = re.findall(".*?\'Location\', \'(.*?)\'\).*?", temp_str)
    print(result)
    print(len(result))

    # temp_str = temp_str.replace(result[0], "xxx")
    # print(temp_str)

    # result_movie_id = re.findall("(\\d+)", temp_str)
    # print(result_movie_id)