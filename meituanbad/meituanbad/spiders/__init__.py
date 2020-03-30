# # This package will contain the spiders of your Scrapy project
# #
# # Please refer to the documentation for information on how to create and manage
# # your spiders.
# class transCookie:
#     def __init__(self, cookie):
#         self.cookie = cookie
#
#     def stringToDict(self):
#         '''
#         将从浏览器上Copy来的cookie字符串转化为Scrapy能使用的Dict
#         :return:
#         '''
#         itemDict = {}
#         items = self.cookie.split(';')
#         for item in items:
#             key = item.split('=')[0].replace(' ', '')
#             value = item.split('=')[1]
#             itemDict[key] = value
#         return itemDict
#
#
# if __name__ == "__main__":
#     cookie = "uuid=efebec518ab44b67b67a.1528984059.1.0.0; _lxsdk_cuid=163fe8d4c821c-084e87f27a3e3a-601a167a-1fa400-163fe8d4c84c8; __mta=87957287.1528984063407.1528984063407.1528984069161.2; ci=42; rvct=42; _lxsdk=163fe8d4c821c-084e87f27a3e3a-601a167a-1fa400-163fe8d4c84c8; _lxsdk_s=163fe8d4c87-c4a-12a-613%7C%7C10"
#     trans = transCookie(cookie)
#     print(trans.stringToDict())
#
#     a = {'uuid': 'efebec518ab44b67b67a.1528984059.1.0.0',
#          '_lxsdk_cuid': '163fe8d4c821c-084e87f27a3e3a-601a167a-1fa400-163fe8d4c84c8',
#          '__mta': '87957287.1528984063407.1528984063407.1528984069161.2', 'ci': '42', 'rvct': '42',
#          '_lxsdk': '163fe8d4c821c-084e87f27a3e3a-601a167a-1fa400-163fe8d4c84c8',
#          '_lxsdk_s': '163fe8d4c87-c4a-12a-613%7C%7C10'}
