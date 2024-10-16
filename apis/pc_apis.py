# encoding: utf-8
import json
import re
import asyncio
import urllib
from daili.daiLim import proxies
import requests
from xhs_utils.cookie_util import trans_cookies
from xhs_utils.xhs_util import splice_str, generate_request_params, generate_x_b3_traceid, get_common_headers

"""
    获小红书的api
    :param cookies_str: 你的cookies
"""
class XHS_Apis():
    def __init__(self):
        self.base_url = "https://edith.xiaohongshu.com"

    """
        获取笔记的id
        :param url: 你想要获取的笔记的url
        返回笔记的id
    """
    def get_noteId_and_url(self, url: str, cookies_str: str, proxies: dict = None):
        # url = "http://xhslink.com/SYdU7D"
        # url = "https://www.xiaohongshu.com/discovery/item/65f94d7b0000000012031481"
        # url = "https://www.xiaohongshu.com/explore/65f94d7b0000000012031481"
        # url = "https://www.xiaohongshu.com/explore/65f94d7b0000000012031481?a=1"
        # url = "https://www.xiaohongshu.com/explore/65f94d7b0000000012031481?a=1&b=2"
        success = True
        msg = "成功"
        note_id = None
        try:
            if "explore" in url or "discovery" in url:
                note_id = url.split("/")[-1].split("?")[0]
            else:
                cookies = trans_cookies(cookies_str)
                response = requests.get(url, verify=False, allow_redirects=False, cookies=cookies, proxies=proxies)
                note_id = response.headers['Location'].split("/")[-1].split("?")[0]
        except Exception as e:
            success = False
            msg = str(e)
        return success, msg, {
            'url': url,
            'new_url': f"https://www.xiaohongshu.com/explore/{note_id}",
            'note_id': note_id
        }


    """
        获取主页的所有频道
        返回主页的所有频道
    """
    def get_homefeed_all_channel(self, cookies_str: str, proxies: dict = None):
        res_json = None
        try:
            api = "/api/sns/web/v1/homefeed/category"
            headers, cookies, data = generate_request_params(cookies_str, api)
            response = requests.get(self.base_url + api, headers=headers, cookies=cookies, proxies=proxies)
            res_json = response.json()
            success, msg = res_json["success"], res_json["msg"]
        except Exception as e:
            success = False
            msg = str(e)
        return success, msg, res_json

    """
        获取主页推荐的笔记
        :param category: 你想要获取的频道
        :param cursor_score: 你想要获取的笔记的cursor
        :param refresh_type: 你想要获取的笔记的刷新类型
        :param note_index: 你想要获取的笔记的index
        :param cookies_str: 你的cookies
        返回主页推荐的笔记
    """
    def get_homefeed_recommend(self, category, cursor_score, refresh_type, note_index, cookies_str: str, proxies: dict = None):
        res_json = None
        try:
            api = f"/api/sns/web/v1/homefeed"
            data = {
                "cursor_score": cursor_score,
                "num": 20,
                "refresh_type": refresh_type,
                "note_index": note_index,
                "unread_begin_note_id": "",
                "unread_end_note_id": "",
                "unread_note_count": 0,
                "category": category,
                "search_key": "",
                "need_num": 10,
                "image_formats": [
                    "jpg",
                    "webp",
                    "avif"
                ],
                "need_filter_image": False
            }
            headers, cookies, trans_data = generate_request_params(cookies_str, api, data)
            response = requests.post(self.base_url + api, headers=headers, data=trans_data, cookies=cookies, proxies=proxies)
            res_json = response.json()
            success, msg = res_json["success"], res_json["msg"]
        except Exception as e:
            success = False
            msg = str(e)
        return success, msg, res_json

    """
        根据数量获取主页推荐的笔记
        :param category: 你想要获取的频道
        :param require_num: 你想要获取的笔记的数量
        :param cookies_str: 你的cookies
        根据数量返回主页推荐的笔记
    """
    def get_homefeed_recommend_by_num(self, category, require_num, cookies_str: str, proxies: dict = None):
        cursor_score, refresh_type, note_index = "", 1, 0
        note_list = []
        try:
            while True:
                success, msg, res_json = self.get_homefeed_recommend(category, cursor_score, refresh_type, note_index, cookies_str, proxies)
                if not success:
                    raise Exception(msg)
                if "items" not in res_json["data"]:
                    break
                notes = res_json["data"]["items"]
                note_list.extend(notes)
                cursor_score = res_json["data"]["cursor_score"]
                refresh_type = 3
                note_index += 20
                if len(note_list) > require_num:
                    break
        except Exception as e:
            success = False
            msg = str(e)
        if len(note_list) > require_num:
            note_list = note_list[:require_num]
        return success, msg, note_list

    """
        获取用户的信息
        :param user_id: 你想要获取的用户的id
        :param cookies_str: 你的cookies
        返回用户的信息
    """
    def get_user_info(self, user_id: str, cookies_str: str, proxies: dict = proxies):
        res_json = None
        try:
            api = f"/api/sns/web/v1/user/otherinfo"
            params = {
                "target_user_id": user_id
            }
            splice_api = splice_str(api, params)
            headers, cookies, data = generate_request_params(cookies_str, splice_api)
            response = requests.get(self.base_url + splice_api, headers=headers, cookies=cookies, proxies=proxies)
            res_json = response.json()
            success, msg = res_json["success"], res_json["msg"]
        except Exception as e:
            success = False
            msg = str(e)
        return success, msg, res_json

    """
        获取用户自己的信息
        :param cookies_str: 你的cookies
        返回用户自己的信息
    """
    def get_user_self_info(self, cookies_str: str, proxies: dict = None):
        res_json = None
        try:
            api = f"/api/sns/web/v1/user/selfinfo"
            splice_api = splice_str(api, {})
            headers, cookies, data = generate_request_params(cookies_str, splice_api)
            response = requests.get(self.base_url + splice_api, headers=headers, cookies=cookies, proxies=proxies)
            res_json = response.json()
            success, msg = res_json["success"], res_json["msg"]
        except Exception as e:
            success = False
            msg = str(e)
        return success, msg, res_json

    """
        获取用户指定位置的笔记
        :param user_id: 你想要获取的用户的id
        :param cursor: 你想要获取的笔记的cursor
        :param cookies_str: 你的cookies
        返回用户指定位置的笔记
    """
    def get_user_note_info(self, user_id: str, cursor: str, cookies_str: str, proxies: dict = None):
        res_json = None
        try:
            api = f"/api/sns/web/v1/user_posted"
            params = {
                "num": "30",
                "cursor": cursor,
                "user_id": user_id,
                "image_formats": "jpg,webp,avif"
            }
            splice_api = splice_str(api, params)
            headers, cookies, data = generate_request_params(cookies_str, splice_api)
            response = requests.get(self.base_url + splice_api, headers=headers, cookies=cookies, proxies=proxies)
            res_json = response.json()
            success, msg = res_json["success"], res_json["msg"]
        except Exception as e:
            success = False
            msg = str(e)
        return success, msg, res_json


    """
        获取用户所有笔记
        :param user_id: 你想要获取的用户的id
        :param cookies_str: 你的cookies
        返回用户的所有笔记
    """
    def get_user_all_note_info(self, user_id: str, cookies_str: str, proxies: dict = None):
        cursor = ''
        note_list = []
        try:
            while True:
                success, msg, res_json = self.get_user_note_info(user_id, cursor, cookies_str, proxies)
                if not success:
                    raise Exception(msg)
                notes = res_json["data"]["notes"]
                if 'cursor' in res_json["data"]:
                    cursor = str(res_json["data"]["cursor"])
                else:
                    break
                note_list.extend(notes)
                if len(notes) == 0 or not res_json["data"]["has_more"]:
                    break
        except Exception as e:
            success = False
            msg = str(e)
        return success, msg, note_list

    """
        获取用户指定位置收藏的笔记
        :param user_id: 你想要获取的用户的id
        :param cursor: 你想要获取的笔记的cursor
        :param cookies_str: 你的cookies
        返回用户指定位置收藏的笔记
    """
    def get_user_collect_note_info(self, user_id: str, cursor: str, cookies_str: str, proxies: dict = None):
        res_json = None
        try:
            api = f"/api/sns/web/v2/note/collect/page"
            params = {
                "num": "30",
                "cursor": cursor,
                "user_id": user_id,
                "image_formats": "jpg,webp,avif"
            }
            splice_api = splice_str(api, params)
            headers, cookies, data = generate_request_params(cookies_str, splice_api)
            response = requests.get(self.base_url + splice_api, headers=headers, cookies=cookies, proxies=proxies)
            res_json = response.json()
            success, msg = res_json["success"], res_json["msg"]
        except Exception as e:
            success = False
            msg = str(e)
        return success, msg, res_json

    """
        获取用户所有收藏笔记
        :param user_id: 你想要获取的用户的id
        :param cookies_str: 你的cookies
        返回用户的所有收藏笔记
    """
    def get_user_all_collect_note_info(self, user_id: str, cookies_str: str, proxies: dict = None):
        cursor = ''
        note_list = []
        try:
            while True:
                success, msg, res_json = self.get_user_collect_note_info(user_id, cursor, cookies_str, proxies)
                if not success:
                    raise Exception(msg)
                notes = res_json["data"]["notes"]
                if 'cursor' in res_json["data"]:
                    cursor = str(res_json["data"]["cursor"])
                else:
                    break
                note_list.extend(notes)
                if len(notes) == 0 or not res_json["data"]["has_more"]:
                    break
        except Exception as e:
            success = False
            msg = str(e)
        return success, msg, note_list

    """
        获取用户指定位置喜欢的笔记
        :param user_id: 你想要获取的用户的id
        :param cursor: 你想要获取的笔记的cursor
        :param cookies_str: 你的cookies
        返回用户指定位置喜欢的笔记
    """
    def get_user_like_note_info(self, user_id: str, cursor: str, cookies_str: str, proxies: dict = None):
        res_json = None
        try:
            api = f"/api/sns/web/v1/note/like/page"
            params = {
                "num": "30",
                "cursor": cursor,
                "user_id": user_id,
                "image_formats": "jpg,webp,avif"
            }
            splice_api = splice_str(api, params)
            headers, cookies, data = generate_request_params(cookies_str, splice_api)
            response = requests.get(self.base_url + splice_api, headers=headers, cookies=cookies, proxies=proxies)
            res_json = response.json()
            success, msg = res_json["success"], res_json["msg"]
        except Exception as e:
            success = False
            msg = str(e)
        return success, msg, res_json

    """
        获取用户所有喜欢笔记
        :param user_id: 你想要获取的用户的id
        :param cookies_str: 你的cookies
        返回用户的所有喜欢笔记
    """
    def get_user_all_like_note_info(self, user_id: str, cookies_str: str, proxies: dict = None):
        cursor = ''
        note_list = []
        try:
            while True:
                success, msg, res_json = self.get_user_collect_note_info(user_id, cursor, cookies_str, proxies)
                if not success:
                    raise Exception(msg)
                notes = res_json["data"]["notes"]
                if 'cursor' in res_json["data"]:
                    cursor = str(res_json["data"]["cursor"])
                else:
                    break
                note_list.extend(notes)
                if len(notes) == 0 or not res_json["data"]["has_more"]:
                    break
        except Exception as e:
            success = False
            msg = str(e)
        return success, msg, note_list


    """
        获取笔记的详细
        :param url: 你想要获取的笔记的url
        :param cookies_str: 你的cookies
        返回笔记的详细
    """
    def get_note_info(self, url: str, cookies_str: str, proxies: dict = None):
        if '?xsec_token' not in url:
            try:
                headers = get_common_headers()
                cookies = trans_cookies(cookies_str)
                response = requests.get(url, headers=headers, cookies=cookies)
                res_text = response.text
                res_text = re.findall(r'window\.__INITIAL_STATE__=(.*?)</script><', res_text)[0]
                res_text = res_text.replace('true', 'True').replace('false', 'False').replace('null', 'None').replace('undefined', 'None')
                res_json = eval(res_text)
                return True, "success", res_json
            except Exception as e:
                return False, str(e), None
        urlParse = urllib.parse.urlparse(url)
        note_id = urlParse.path.split("/")[-1]
        kvs = urlParse.query.split('&')
        kvDist = {kv.split('=')[0]: kv.split('=')[1] for kv in kvs}
        res_json = None
        try:
            api = f"/api/sns/web/v1/feed"
            data = {
                "source_note_id": note_id,
                "image_formats": [
                    "jpg",
                    "webp",
                    "avif"
                ],
                "extra": {
                    "need_body_topic": "1"
                },
                "xsec_source": "pc_user",
                "xsec_token": kvDist['xsec_token']
            }
            headers, cookies, data = generate_request_params(cookies_str, api, data)
            response = requests.post(self.base_url + api, headers=headers, data=data, cookies=cookies, proxies=proxies)
            res_json = response.json()
            success, msg = res_json["success"], res_json["msg"]
        except Exception as e:
            success = False
            msg = str(e)
        return success, msg, res_json

    """
        获取搜索笔记的结果
        :param query 搜索的关键词
        :param cookies_str 你的cookies
        :param page 搜索的页数
        :param sort 排序方式 general:综合排序, time_descending:时间排序, popularity_descending:热度排序
        :param note_type 笔记类型 0:全部, 1:视频, 2:图文
        返回搜索的结果
    """
    def search_note(self, query: str, cookies_str: str, page=1, sort="general", note_type=0, proxies: dict = None):
        res_json = None
        try:
            api = "/api/sns/web/v1/search/notes"
            data = {
                "keyword": query,
                "page": page,
                "page_size": 20,
                "search_id": generate_x_b3_traceid(21),
                "sort": sort,
                "note_type": note_type,
                "ext_flags": [],
                "image_formats": [
                    "jpg",
                    "webp",
                    "avif"
                ]
            }
            headers, cookies, data = generate_request_params(cookies_str, api, data)
            response = requests.post(self.base_url + api, headers=headers, data=data.encode('utf-8'), cookies=cookies, proxies=proxies)
            res_json = response.json()
            success, msg = res_json["success"], res_json["msg"]
        except Exception as e:
            success = False
            msg = str(e)
        return success, msg, res_json

    """
        指定数量搜索笔记，设置排序方式和笔记类型和笔记数量
        :param query 搜索的关键词
        :param require_num 搜索的数量
        :param cookies_str 你的cookies
        :param sort 排序方式 general:综合排序, time_descending:时间排序, popularity_descending:热度排序
        :param note_type 笔记类型 0:全部, 1:视频, 2:图文
        返回搜索的结果
    """
    def search_some_note(self, query: str, require_num: int, cookies_str: str, sort="general", note_type=0, proxies: dict = None):
        page = 1
        note_list = []
        try:
            while True:
                success, msg, res_json = self.search_note(query, cookies_str, page, sort, note_type, proxies)
                if not success:
                    raise Exception(msg)
                if "items" not in res_json["data"]:
                    break
                notes = res_json["data"]["items"]
                note_list.extend(notes)
                page += 1
                if len(note_list) >= require_num or not res_json["data"]["has_more"]:
                    break
        except Exception as e:
            success = False
            msg = str(e)
        if len(note_list) > require_num:
            note_list = note_list[:require_num]
        return success, msg, note_list
    """
        获取搜索用户的结果
        :param query 搜索的关键词
        :param cookies_str 你的cookies
        :param page 搜索的页数
        返回搜索的结果
    """
    def search_user(self, query: str, cookies_str: str, page=1, proxies: dict = None):
        res_json = None
        try:
            api = "/api/sns/web/v1/search/usersearch"
            data = {
                "search_user_request": {
                    "keyword": query,
                    "search_id": "2dn9they1jbjxwawlo4xd",
                    "page": page,
                    "page_size": 15,
                    "biz_type": "web_search_user",
                    "request_id": "22471139-1723999898524"
                }
            }
            headers, cookies, data = generate_request_params(cookies_str, api, data)
            response = requests.post(self.base_url + api, headers=headers, data=data.encode('utf-8'), cookies=cookies, proxies=proxies)
            res_json = response.json()
            success, msg = res_json["success"], res_json["msg"]
        except Exception as e:
            success = False
            msg = str(e)
        return success, msg, res_json

    """
        指定数量搜索用户
        :param query 搜索的关键词
        :param require_num 搜索的数量
        :param cookies_str 你的cookies
        返回搜索的结果
    """
    def search_some_user(self, query: str, require_num: int, cookies_str: str, proxies: dict = None):
        page = 1
        user_list = []
        try:
            while True:
                success, msg, res_json = self.search_user(query, cookies_str, page, proxies)
                if not success:
                    raise Exception(msg)
                if "users" not in res_json["data"]:
                    break
                users = res_json["data"]["users"]
                user_list.extend(users)
                page += 1
                if len(user_list) >= require_num or not res_json["data"]["has_more"]:
                    break
        except Exception as e:
            success = False
            msg = str(e)
        if len(user_list) > require_num:
            user_list = user_list[:require_num]
        return success, msg, user_list


    """
        获取指定位置的笔记一级评论
        :param note_id 笔记的id
        :param cursor 指定位置的评论的cursor
        :param cookies_str 你的cookies
        返回指定位置的笔记一级评论
    """
    def get_note_out_comment(self, note_id: str, cursor: str, cookies_str: str, proxies: dict = None):
        res_json = None
        try:
            api = "/api/sns/web/v2/comment/page"
            params = {
                "note_id": note_id,
                "cursor": cursor,
                "top_comment_id": "",
                "image_formats": "jpg,webp,avif"
            }
            splice_api = splice_str(api, params)
            headers, cookies, data = generate_request_params(cookies_str, splice_api)
            response = requests.get(self.base_url + splice_api, headers=headers, cookies=cookies, proxies=proxies)
            res_json = response.json()
            success, msg = res_json["success"], res_json["msg"]
        except Exception as e:
            success = False
            msg = str(e)
        return success, msg, res_json

    """
        获取笔记的全部一级评论
        :param note_id 笔记的id
        :param cookies_str 你的cookies
        返回笔记的全部一级评论
    """
    def get_note_all_out_comment(self, note_id: str, cookies_str: str, proxies: dict = None):
        cursor = ''
        note_out_comment_list = []
        try:
            while True:
                success, msg, res_json = self.get_note_out_comment(note_id, cursor, cookies_str, proxies)
                if not success:
                    raise Exception(msg)
                comments = res_json["data"]["comments"]
                if 'cursor' in res_json["data"]:
                    cursor = str(res_json["data"]["cursor"])
                else:
                    break
                note_out_comment_list.extend(comments)
                if len(note_out_comment_list) == 0 or not res_json["data"]["has_more"]:
                    break
        except Exception as e:
            success = False
            msg = str(e)
        return success, msg, note_out_comment_list

    """
        获取指定位置的笔记二级评论
        :param comment 笔记的一级评论
        :param cursor 指定位置的评论的cursor
        :param cookies_str 你的cookies
        返回指定位置的笔记二级评论
    """
    def get_note_inner_comment(self, comment: dict, cursor: str, cookies_str: str, proxies: dict = None):
        res_json = None
        try:
            api = "/api/sns/web/v2/comment/sub/page"
            params = {
                "note_id": comment['note_id'],
                "root_comment_id": comment['id'],
                "num": "10",
                "cursor": cursor,
                "image_formats": "jpg,webp,avif"
            }
            splice_api = splice_str(api, params)
            headers, cookies, data = generate_request_params(cookies_str, splice_api)
            response = requests.get(self.base_url + splice_api, headers=headers, cookies=cookies, proxies=proxies)
            res_json = response.json()
            success, msg = res_json["success"], res_json["msg"]
        except Exception as e:
            success = False
            msg = str(e)
        return success, msg, res_json

    """
        获取笔记的全部二级评论
        :param comment 笔记的一级评论
        :param cookies_str 你的cookies
        返回笔记的全部二级评论
    """
    def get_note_all_inner_comment(self, comment: dict, cookies_str: str, proxies: dict = None):
        try:
            if not comment['sub_comment_has_more']:
                return True, 'success', comment
            cursor = comment['sub_comment_cursor']
            inner_comment_list = []
            while True:
                success, msg, res_json = self.get_note_inner_comment(comment, cursor, cookies_str, proxies)
                if not success:
                    raise Exception(msg)
                comments = res_json["data"]["comments"]
                if 'cursor' in res_json["data"]:
                    cursor = str(res_json["data"]["cursor"])
                else:
                    break
                inner_comment_list.extend(comments)
                if not res_json["data"]["has_more"]:
                    break
            comment['sub_comments'].extend(inner_comment_list)
        except Exception as e:
            success = False
            msg = str(e)
        return success, msg, comment

    """
        获取一篇文章的所有评论
        :param note_id: 你想要获取的笔记的id
        :param cookies_str: 你的cookies
        返回一篇文章的所有评论
    """
    def get_note_all_comment(self, note_id: str, cookies_str: str, proxies: dict = None):
        out_comment_list = []
        try:
            success, msg, out_comment_list = self.get_note_all_out_comment(note_id, cookies_str, proxies)
            if not success:
                raise Exception(msg)
            for comment in out_comment_list:
                success, msg, new_comment = self.get_note_all_inner_comment(comment, cookies_str, proxies)
                if not success:
                    raise Exception(msg)
        except Exception as e:
            success = False
            msg = str(e)
        return success, msg, out_comment_list

    """
        评论笔记
        :param note_id: 你想要评论的笔记的id
        :param content: 你想要评论的内容
        :param cookies_str: 你的cookies
        返回评论的结果
    """
    def comment_note(self, note_id: str, content: str, cookies_str: str, at_users=None, proxies: dict = None):
        res_json = None
        my_content = ''
        my_at_users = []
        try:
            api = "/api/sns/web/v1/comment/post"
            if at_users is None:
                my_content = content
            else:
                for at_user in at_users:
                    my_content += f' @{at_user["nickname"]} '
                    my_at_users.append(at_user)
                my_content += content
            data = {
                "note_id": note_id,
                "content": my_content,
                "at_users": my_at_users
            }
            headers, cookies, data = generate_request_params(cookies_str, api, data)
            response = requests.post(self.base_url + api, headers=headers, data=data.encode('utf-8'), cookies=cookies, proxies=proxies)
            res_json = response.json()
            success, msg = res_json["success"], res_json["msg"]
        except Exception as e:
            success = False
            msg = str(e)
        return success, msg, res_json

    """
        评论评论
        :param note_id: 你想要评论的笔记的id
        :param content: 你想要评论的内容
        :param target_comment_id: 你想要评论的评论的id
        :param cookies_str: 你的cookies
        返回评论的结果
    """
    def comment_comment(self, note_id: str, content: str, target_comment_id: str, cookies_str: str, at_users=None, proxies: dict = None):
        res_json = None
        my_content = ''
        my_at_users = []
        try:
            api = "/api/sns/web/v1/comment/post"
            if at_users is None:
                my_content = content
            else:
                for at_user in at_users:
                    my_content += f' @{at_user["nickname"]} '
                    my_at_users.append(at_user)
                my_content += content
            data = {
                "note_id": note_id,
                "content": my_content,
                "target_comment_id": target_comment_id,
                "at_users": my_at_users
            }
            headers, cookies, data = generate_request_params(cookies_str, api, data)
            response = requests.post(self.base_url + api, headers=headers, data=data.encode('utf-8'), cookies=cookies, proxies=proxies)
            res_json = response.json()
            success, msg = res_json["success"], res_json["msg"]
        except Exception as e:
            success = False
            msg = str(e)
        return success, msg, res_json

    """
        点赞评论
        :param note_id: 你想要评论的笔记的id
        :param comment_id: 你想要点赞的评论的id
        :param cookies_str: 你的cookies
        返回评论的结果
    """
    def like_comment(self, note_id: str, comment_id: str, cookies_str: str, proxies: dict = None):
        res_json = None
        try:
            api = "/api/sns/web/v1/comment/like"
            data = {
                "note_id": note_id,
                "comment_id": comment_id
            }
            headers, cookies, data = generate_request_params(cookies_str, api, data)
            response = requests.post(self.base_url + api, headers=headers, data=data, cookies=cookies, proxies=proxies)
            res_json = response.json()
            success, msg = res_json["success"], res_json["msg"]
        except Exception as e:
            success = False
            msg = str(e)
        return success, msg, res_json

    """
        关注用户
        :param user_id: 你想要关注的用户的id
        :param cookies_str: 你的cookies
        返回关注的结果
    """
    def follow_user(self, user_id: str, cookies_str: str, proxies: dict = None):
        res_json = None
        try:
            api = "/api/sns/web/v1/user/follow"
            data = {
                "target_user_id": user_id
            }
            headers, cookies, data = generate_request_params(cookies_str, api, data)
            response = requests.post(self.base_url + api, headers=headers, data=data, cookies=cookies, proxies=proxies)
            res_json = response.json()
            success, msg = res_json["success"], res_json["msg"]
        except Exception as e:
            success = False
            msg = str(e)
        return success, msg, res_json

    """
        点赞笔记
        :param note_id: 你想要点赞的笔记的id
        :param cookies_str: 你的cookies
        返回点赞的结果
    """
    def like_note(self, note_id: str, cookies_str: str, proxies: dict = None):
        res_json = None
        try:
            api = "/api/sns/web/v1/note/like"
            data = {
                "note_oid": note_id
            }
            headers, cookies, data = generate_request_params(cookies_str, api, data)
            response = requests.post(self.base_url + api, headers=headers, data=data, cookies=cookies, proxies=proxies)
            res_json = response.json()
            success, msg = res_json["success"], res_json["msg"]
        except Exception as e:
            success = False
            msg = str(e)
        return success, msg, res_json

    """
        收藏笔记
        :param note_id: 你想要收藏的笔记的id
        :param cookies_str: 你的cookies
        返回收藏的结果
    """
    def collect_note(self, note_id: str, cookies_str: str, proxies: dict = None):
        res_json = None
        try:
            api = "/api/sns/web/v1/note/collect"
            data = {
                "note_id": note_id
            }
            headers, cookies, data = generate_request_params(cookies_str, api, data)
            response = requests.post(self.base_url + api, headers=headers, data=data, cookies=cookies, proxies=proxies)
            res_json = response.json()
            success, msg = res_json["success"], res_json["msg"]
        except Exception as e:
            success = False
            msg = str(e)
        return success, msg, res_json

    """
        获取未读消息
        :param cookies_str: 你的cookies
        返回未读消息
    """
    def get_unread_message(self, cookies_str: str, proxies: dict = None):
        res_json = None
        try:
            api = "/api/sns/web/unread_count"
            headers, cookies, data = generate_request_params(cookies_str, api)
            response = requests.get(self.base_url + api, headers=headers, cookies=cookies, proxies=proxies)
            res_json = response.json()
            success, msg = res_json["success"], res_json["msg"]
        except Exception as e:
            success = False
            msg = str(e)
        return success, msg, res_json
    """
        获取评论和@提醒
        :param cursor: 你想要获取的评论和@提醒的cursor
        :param cookies_str: 你的cookies
        返回评论和@提醒
    """
    def get_metions(self, cursor: str, cookies_str: str, proxies: dict = None):
        res_json = None
        try:
            api = "/api/sns/web/v1/you/mentions"
            params = {
                "num": "20",
                "cursor": cursor
            }
            splice_api = splice_str(api, params)
            headers, cookies, data = generate_request_params(cookies_str, splice_api)
            response = requests.get(self.base_url + splice_api, headers=headers, cookies=cookies, proxies=proxies)
            res_json = response.json()
            success, msg = res_json["success"], res_json["msg"]
        except Exception as e:
            success = False
            msg = str(e)
        return success, msg, res_json

    """
        获取全部的评论和@提醒
        :param cookies_str: 你的cookies
        返回全部的评论和@提醒
    """
    def get_all_metions(self, cookies_str: str, proxies: dict = None):
        cursor = ''
        metions_list = []
        try:
            while True:
                success, msg, res_json = self.get_metions(cursor, cookies_str, proxies)
                if not success:
                    raise Exception(msg)
                metions = res_json["data"]["message_list"]
                if 'cursor' in res_json["data"]:
                    cursor = str(res_json["data"]["cursor"])
                else:
                    break
                metions_list.extend(metions)
                if not res_json["data"]["has_more"]:
                    break
        except Exception as e:
            success = False
            msg = str(e)
        return success, msg, metions_list

    """
        获取赞和收藏
        :param cursor: 你想要获取的赞和收藏的cursor
        :param cookies_str: 你的cookies
        返回赞和收藏
    """
    def get_likesAndcollects(self, cursor: str, cookies_str: str, proxies: dict = None):
        res_json = None
        try:
            api = "/api/sns/web/v1/you/likes"
            params = {
                "num": "20",
                "cursor": cursor
            }
            splice_api = splice_str(api, params)
            headers, cookies, data = generate_request_params(cookies_str, splice_api)
            response = requests.get(self.base_url + splice_api, headers=headers, cookies=cookies, proxies=proxies)
            res_json = response.json()
            success, msg = res_json["success"], res_json["msg"]
        except Exception as e:
            success = False
            msg = str(e)
        return success, msg, res_json

    """
        获取全部的赞和收藏
        :param cookies_str: 你的cookies
        返回全部的赞和收藏
    """
    def get_all_likesAndcollects(self, cookies_str: str, proxies: dict = None):
        cursor = ''
        likesAndcollects_list = []
        try:
            while True:
                success, msg, res_json = self.get_likesAndcollects(cursor, cookies_str, proxies)
                if not success:
                    raise Exception(msg)
                likesAndcollects = res_json["data"]["message_list"]
                if 'cursor' in res_json["data"]:
                    cursor = str(res_json["data"]["cursor"])
                else:
                    break
                likesAndcollects_list.extend(likesAndcollects)
                if not res_json["data"]["has_more"]:
                    break
        except Exception as e:
            success = False
            msg = str(e)
        return success, msg, likesAndcollects_list

    """
        获取新增关注
        :param cursor: 你想要获取的新增关注的cursor
        :param cookies_str: 你的cookies
        返回新增关注
    """
    def get_new_connections(self, cursor: str, cookies_str: str, proxies: dict = None):
        res_json = None
        try:
            api = "/api/sns/web/v1/you/connections"
            params = {
                "num": "20",
                "cursor": cursor
            }
            splice_api = splice_str(api, params)
            headers, cookies, data = generate_request_params(cookies_str, splice_api)
            response = requests.get(self.base_url + splice_api, headers=headers, cookies=cookies, proxies=proxies)
            res_json = response.json()
            success, msg = res_json["success"], res_json["msg"]
        except Exception as e:
            success = False
            msg = str(e)
        return success, msg, res_json

    """
        获取全部的新增关注
        :param cookies_str: 你的cookies
        返回全部的新增关注
    """
    def get_all_new_connections(self, cookies_str: str, proxies: dict = None):
        cursor = ''
        connections_list = []
        try:
            while True:
                success, msg, res_json = self.get_new_connections(cursor, cookies_str, proxies)
                if not success:
                    raise Exception(msg)
                connections = res_json["data"]["message_list"]
                if 'cursor' in res_json["data"]:
                    cursor = str(res_json["data"]["cursor"])
                else:
                    break
                connections_list.extend(connections)
                if not res_json["data"]["has_more"]:
                    break
        except Exception as e:
            success = False
            msg = str(e)
        return success, msg, connections_list

    """
        获取通知
        :param cookies_str: 你的cookies
        返回通知
    """
    def get_all_notifications(self, cookies_str: str, proxies: dict = None):
        res_json = None
        try:
            api = "/api/sns/web/unread_count"
            headers, cookies, data = generate_request_params(cookies_str, api)
            response = requests.get(self.base_url + api, headers=headers, cookies=cookies, proxies=proxies)
            res_json = response.json()
            success, msg = res_json["success"], res_json["msg"]
        except Exception as e:
            success = False
            msg = str(e)
        return success, msg, res_json

    """
        获取笔记无水印视频
        :param note_id: 你想要获取的笔记的id
        返回笔记无水印视频
    """
    @staticmethod
    def get_note_no_water_video(note_id):
        success = True
        msg = '成功'
        video_addr = None
        try:
            headers = get_common_headers()
            url = f"https://www.xiaohongshu.com/explore/{note_id}"
            response = requests.get(url, headers=headers)
            res = response.text
            video_addr = re.findall(r'<meta name="og:video" content="(.*?)">', res)[0]
        except Exception as e:
            success = False
            msg = str(e)
        return success, msg, video_addr

    """
        获取笔记无水印图片
        :param img_url: 你想要获取的图片的url
        返回笔记无水印图片
    """
    @staticmethod
    def get_note_no_water_img(img_url):
        success = True
        msg = '成功'
        new_url = None
        try:
            # https://sns-webpic-qc.xhscdn.com/202403211626/c4fcecea4bd012a1fe8d2f1968d6aa91/110/0/01e50c1c135e8c010010000000018ab74db332_0.jpg!nd_dft_wlteh_webp_3
            if '.jpg' in img_url:
                img_id = '/'.join([split for split in img_url.split('/')[-3:]]).split('!')[0]
                # return f"http://ci.xiaohongshu.com/{img_id}?imageview2/2/w/1920/format/png"
                # return f"http://ci.xiaohongshu.com/{img_id}?imageview2/2/w/format/png"
                # return f'https://sns-img-hw.xhscdn.com/{img_id}'
                new_url = f'https://sns-img-qc.xhscdn.com/{img_id}'

            # 'https://sns-webpic-qc.xhscdn.com/202403231640/ea961053c4e0e467df1cc93afdabd630/spectrum/1000g0k0200n7mj8fq0005n7ikbllol6q50oniuo!nd_dft_wgth_webp_3'
            elif 'spectrum' in img_url:
                img_id = '/'.join(img_url.split('/')[-2:]).split('!')[0]
                # return f'http://sns-webpic.xhscdn.com/{img_id}?imageView2/2/w/1920/format/jpg'
                new_url = f'http://sns-webpic.xhscdn.com/{img_id}?imageView2/2/w/format/jpg'
            else:
                # 'http://sns-webpic-qc.xhscdn.com/202403181511/64ad2ea67ce04159170c686a941354f5/1040g008310cs1hii6g6g5ngacg208q5rlf1gld8!nd_dft_wlteh_webp_3'
                img_id = img_url.split('/')[-1].split('!')[0]
                # return f"http://ci.xiaohongshu.com/{img_id}?imageview2/2/w/1920/format/png"
                # return f"http://ci.xiaohongshu.com/{img_id}?imageview2/2/w/format/png"
                # return f'https://sns-img-hw.xhscdn.com/{img_id}'
                new_url = f'https://sns-img-qc.xhscdn.com/{img_id}'
        except Exception as e:
            success = False
            msg = str(e)
        return success, msg, new_url

if __name__ == '__main__':
    xhs_apis = XHS_Apis()
    # url = xhs_apis.get_note_no_water_img('https://sns-webpic-qc.xhscdn.com/202403211626/c4fcecea4bd012a1fe8d2f1968d6aa91/110/0/01e50c1c135e8c010010000000018ab74db332_0.jpg!nd_dft_wlteh_webp_3')
    # print(url)
    # # 扫描二维码登录获取cookies
    # loop = asyncio.get_event_loop()
    # cookies_str = loop.run_until_complete(xhs_apis.login_util.main())

    #cookies_str=r"abRequestId=b492d54d-9b89-5e3a-a18d-ff247fea2d00; xsecappid=xhs-pc-web; a1=191792b33095bz3cvsuycv412mbdtoc4zfqn90xmp50000848060; webId=15cbe8482d6cc941a9671871c6298420; gid=yjyWjJDq0fuWyjyWjJDqqi8C8j2DuqShM7vSA6Uh4yJ6DI28f9lS4j888Y4Y8K88qyiJd8yf; web_session=0400698e2704d9563e7cf7bcf3344bba325e39; acw_tc=5beab0324951dcfe17dd7e021360a3c2a5820562cc5aabc91fc1e2b6a1bed06d; websectiga=634d3ad75ffb42a2ade2c5e1705a73c845837578aeb31ba0e442d75c648da36a; webBuild=4.35.0; unread={%22ub%22:%2266cd42fa000000001f018c96%22%2C%22ue%22:%2266e3a3c9000000002603e74f%22%2C%22uc%22:33}; sec_poison_id=60f5cea7-ab78-4f6a-a011-484d7c9332ca"
    cookies_str=r"abRequestId=94343241-37df-5538-9cac-400314d9c573; xsecappid=xhs-pc-web; a1=191792dbc019vactw8w6ed5yr15shwgy7av56k49g50000215251; webId=75db924bb696f56bc069660da14b781a; gid=yjyWjJfSJjW8yjyWjJfDS0T48yjh0S9EYEKdhjkf2vFy2228MxEkvK888Jy2J2y84fd2YdWj; web_session=040069b7d64a897d579c2dbdf3344bda6e634c; webBuild=4.36.5; acw_tc=48b954a642f667866c97fe7e786e82c1f5777e87280de0cbab04888c31c6a7e5; websectiga=2a3d3ea002e7d92b5c9743590ebd24010cf3710ff3af8029153751e41a6af4a3; sec_poison_id=9a99c9b6-9388-4a8d-8ff7-ed87876ea69c"
    #cookies_str=r"abRequestId=1dce21a0-b7f4-5619-961a-dafccd141124; xsecappid=xhs-pc-web; a1=1920d5b8979t9fa53psues6l9d66bbbxcpcdk6zft50000190768; webId=6a637d4c7a03ae495db01cc719c344f4; gid=yjJ8f2DjqySYyjJ8f2DYjUKuWj9ji02qUM7dSi9MK1jfKf28KDDDCT888yj8WKY8YW0DfKYK; web_session=040069b7d4a8997d7187e9acd9344b71c152aa; webBuild=4.35.0; websectiga=3fff3a6f9f07284b62c0f2ebf91a3b10193175c06e4f71492b60e056edcdebb2; sec_poison_id=1141ea1b-f37d-402e-a36e-10455c9e82a6; acw_tc=67e94b27608b92b25b1e91b620d6a816ec96dad0543fdfe589c84c545870f5eb"
    # # 获取笔记id
    # url = "http://xhslink.com/6MzPJJ"
    # success, msg, note_id = xhs_apis.get_noteId_and_url(url, cookies_str)
    # print("笔记id", success, msg, note_id)
    # # 获取主页所有频道
    # success, msg, channel = xhs_apis.get_homefeed_all_channel(cookies_str)
    # print("频道", success, msg, channel)
    # # # 获取主页推荐
    # success, msg, notes = xhs_apis.get_homefeed_recommend_by_num(channel[0]['id'], 10, cookies_str)
    # print("主页推荐", success, msg, len(notes))
    # 获取用户信息
    # success, msg, user = xhs_apis.get_user_info('6253d993000000001000553e', cookies_str)
    # print("用户信息", success, msg, user)
    # # 获取用户自己的信息
    # success, msg, user = xhs_apis.get_user_self_info(cookies_str)
    # print("用户自己的信息", success, msg, user)
    # 获取用户所有笔记https://www.xiaohongshu.com/user/profile/5deaf47d0000000001000859
    # success, msg, notes = xhs_apis.get_user_all_note_info('5deaf47d0000000001000859', cookies_str)
    # print("用户所有笔记", success, msg, len(notes))
    # # 获取用户所有收藏笔记
    # success, msg, notes = xhs_apis.get_user_all_collect_note_info('632fb88d00000000230398a1', cookies_str)
    # print("用户所有收藏笔记", success, msg, len(notes))
    # # 获取用户所有喜欢笔记
    # success, msg, notes = xhs_apis.get_user_all_like_note_info('632fb88d00000000230398a1', cookies_str)
    # print("用户所有喜欢笔记", success, msg, len(notes))
    # 获取笔记信息
    #url = 'https://www.xiaohongshu.com/explore/6631e8b5000000001e02fc7b?xsec_token=ABY8VEqxFp7tzhLnmjVsiGaOTw9tzA57-etOzena24Ihk=&xsec_source=pc_user'
    url = "https://www.xiaohongshu.com/explore/66df09ff000000000c01a804"
    success, msg, note_info = xhs_apis.get_note_info(url, cookies_str)
    print("笔记信息", success, msg, json.dumps(note_info, ensure_ascii=False, separators=(',', ':')))
    # # 指定数量搜索笔记
    # success, msg, notes = xhs_apis.search_some_note('你好', 10, cookies_str)
    # print("搜索笔记", success, msg, len(notes))
    # 指定数量搜索用户
    # success, msg, users = xhs_apis.search_some_user('小红薯', 10, cookies_str)
    # print("搜索用户", success, msg, len(users))
    # # # 获取一篇文章的所有评论
    # print("获取一篇文章的所有评论")
    # success, msg, comment_list = xhs_apis.get_note_all_comment('6618e6ec000000001b00ce56', cookies_str)
    # print(success, msg, len(comment_list))
    # num = 0
    # for out_comment in comment_list:
    #     num += 1
    #     print('================================================================')
    #     print(f'{out_comment["user_info"]["nickname"]}: {out_comment["content"]}')
    #     for inner_comment in out_comment['sub_comments']:
    #         num += 1
    #         print(f'{inner_comment["user_info"]["nickname"]}: {inner_comment["content"]}')
    # print(num)
    # print(comment_list[0])
    # # 评论笔记
    # at_users = [
    #     {
    #         "user_id": "5d9b26da000000000100b059",
    #         "nickname": "mildmay"
    #     },
    #     {
    #         "user_id": "65b4d7ce000000001a00fe1a",
    #         "nickname": "小红薯65B4FDE8"
    #     },
    #     {
    #         "user_id": "65fc0d07000000000b00c752",
    #         "nickname": "木子自律"
    #     }
    # ]
    # at_users = None
    # success, msg, res = xhs_apis.comment_note('66c21e72000000001e01f2eb', '越菜越想玩┭┮﹏┭┮', cookies_str, at_users=at_users)
    # print('评论笔记', success, msg, res)
    # # 评论评论
    # success, msg, res = xhs_apis.comment_comment('66c21e72000000001e01f2eb', '友人局要四个人嘛qwq', '66c229900000000026031936', cookies_str, at_users=at_users)
    # print('评论评论', success, msg, res)
    # 点赞评论
    # success, msg, res = xhs_apis.like_comment('66c21e72000000001e01f2eb', '66c223ee000000001202f6e9', cookies_str)
    # print('点赞评论', success, msg, res)
    # # 关注用户
    # success, msg, res = xhs_apis.follow_user('65b4d7ce000000001a00fe1a', cookies_str)
    # print('关注用户', success, msg, res)
    # 点赞笔记
    # success, msg, res = xhs_apis.like_note('66c21e72000000001e01f2eb', cookies_str)
    # print('点赞笔记', success, msg, res)
    # 收藏笔记
    # success, msg, res = xhs_apis.collect_note('66c21e72000000001e01f2eb', cookies_str)
    # print('收藏笔记', success, msg, res)
    # # 获取未读消息
    # success, msg, res = xhs_apis.get_unread_message(cookies_str)
    # print('未读消息', success, msg, res)
    # # 获取评论和@提醒
    # success, msg, metions = xhs_apis.get_all_metions(cookies_str)
    # print('评论和@提醒', success, msg, len(metions))
    # # 获取赞和收藏
    # success, msg, likesAndcollects = xhs_apis.get_all_likesAndcollects(cookies_str)
    # print('赞和收藏', success, msg, len(likesAndcollects))
    # # 获取新增关注
    # success, msg, new_connections = xhs_apis.get_all_new_connections(cookies_str)
    # print('新增关注', success, msg, len(new_connections))
    # success, msg, notification = xhs_apis.get_all_notifications(cookies_str)
    # print('通知', success, msg, notification)

