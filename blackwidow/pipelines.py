# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

# import io

# class BlackwidowPipeline(object):
#     def __init__(self):
#         pass

#     def process_item(self, item, spider):

#         with io.open('output/' + item['provider'] +'/' + item.filename() + '.out', 'w', encoding='utf8') as outputfile:
#             output = item.encodeTab()
#             outputfile.write(output)
#             outputfile.close()

#         return item