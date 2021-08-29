import scrapy
import re
import json
from copy import deepcopy
from urllib.parse import urlencode
from scrapy.http import HtmlResponse
from instagram.items import InstagramItem


class InstagramspiderSpider(scrapy.Spider):
    name = 'instagramspider'
    allowed_domains = ['instagram.com']
    start_urls = ['https://www.instagram.com/']

    instagram_login_link = 'https://www.instagram.com/accounts/login/ajax/'
    with open('input.txt', 'r') as file:
        instagram_login = file.readline().replace('\n', '')
        instagram_password = file.readline().replace('\n', '')

    user_parse = 'kazakoff13'
    graphql_url = 'https://www.instagram.com/graphql/query/?'
    query_posts_hash = '8c2a529969ee035a5063f2fc8602a0fd'


    def parse(self, response: HtmlResponse):
        csrf = self.fetch_csrf_token(response.text)
        yield scrapy.FormRequest(self.instagram_login_link,
                                 method='POST',
                                 callback=self.login,
                                 formdata={'username': self.instagram_login,
                                           'enc_password': self.instagram_password},
                                 headers={'x-csrftoken': csrf})

    def login(self, response: HtmlResponse):
        j_data = response.json()
        if j_data['authenticated']:
            yield response.follow(f'/{self.user_parse}', callback=self.user_parsing,
                                  cb_kwargs={'username': self.user_parse})

    def user_parsing(self, response: HtmlResponse, username):
        user_id = self.fetch_user_id(response.text, username)
        variables = {'id': user_id,
                     'first': 12}
        url_posts = self.graphql_url + f'query_hash={self.query_posts_hash}&{urlencode(variables)}'
        yield response.follow(url_posts,
                              callback=self.user_data_parse,
                              cb_kwargs={'username': username,
                                         'user_id': user_id,
                                         'variables': deepcopy(variables)})

    def user_data_parse(self, response: HtmlResponse, username, user_id, variables):
        j_data = response.json()
        page_info = j_data.get('data').get('user').get('edge_owner_to_timeline_media').get('page_info')
        if page_info.get('has_next_page'):
            variables['after'] = page_info.get('end_cursor')
            url_posts = self.graphql_url + f'query_hash={self.query_posts_hash}&{urlencode(variables)}'
            yield response.follow(url_posts,
                                  callback=self.user_data_parse,
                                  cb_kwargs={'username': username,
                                             'user_id': user_id,
                                             'variables': deepcopy(variables)})

        posts = j_data.get('data').get('user').get('edge_owner_to_timeline_media').get('edges')
        for post in posts:
            item = InstagramItem(user_id=user_id,
                                   username=username,
                                   picture=post.get('node').get('display_url'),
                                   likes=post.get('node').get('edge_media_preview_like').get('count'),
                                   post_data=post.get('node'))
            yield item


    def fetch_csrf_token(self, text):
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')


    def fetch_user_id(self, text, username):
        matched = re.search(
            '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
        ).group()
        return json.loads(matched).get('id')


