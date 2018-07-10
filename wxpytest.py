import itchat
import re
from wxpy import *
from py2neo import Graph, Node, Relationship
bot = Bot(cache_path=True)

test_graph = Graph("http://localhost:7474", username="neo4j", password="08166517416reny")

def kgquery_entity(target):
   find_entity = test_graph.find_one(re.search(r".*[老师/学生/项目]", target).group(0), property_key="name",
                                     property_value=target)
   return find_entity

def kgquery_rel(start, end):
    find_relationship = test_graph.match_one(start_node=start, end_node=end, bidirectional=True)
    return find_relationship

@bot.register()
def reply_self(msg):
    input_message = msg.text
    if len(input_message) < 4:
       msg.reply(kgquery_entity(input_message))
    else:
        a = input_message.find('和')
        b = input_message.find('的')
        name1 = input_message[:a]
        name2 = input_message[a + 1:b]
        # 提取实体的类别名，在find_one中，类别名跟输入有关系
        label1 = re.search(r".*[老师/学生/项目]", name1).group(0)
        label2 = re.search(r".*[老师/学生/项目]", name2).group(0)
        # find_one函数中，类别名由输入定，属性值也由输入值定
        n1 = test_graph.find_one(label1, property_key="name", property_value=name1)
        n2 = test_graph.find_one(label2, property_key="name", property_value=name2)
        ans = kgquery_rel(n1, n2)
        ans = str(ans)
        msg.reply(name1 + '和' + name2 + '的关系是：' + ans)
embed()