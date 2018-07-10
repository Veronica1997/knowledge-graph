from py2neo import Graph, Node, Relationship
import re
from wxpy import *
test_graph = Graph("http://localhost:7474", username="neo4j", password="08166517416reny")
bot = Bot(cache_path=True)

def kgquery_entity(target):
   find_entity = test_graph.find_one("entity", property_key="name", property_value=target)
   return find_entity

def kgquery_rel(start, end):
    find_relationship = test_graph.match_one(start_node=start, end_node=end, bidirectional=True)
    return find_relationship

@bot.register()
def reply_self(msg):
    input_message = msg.text
    # 参加项目1的老师/学生有？
    if re.match(r'^参与[\u4e00-\u9fa5]{2,20}的..有', input_message):
        m1 = input_message.find('与')
        m2 = input_message.find('的')
        m3 = input_message.find('有')
        name3 = input_message[m1 + 1:m2]
        kind1 = input_message[m2 + 1:m3]
        progra1 = test_graph.find_one("entity", property_key="name", property_value=name3)
        for rel in test_graph.match(end_node=progra1, rel_type="成员", bidirectional=True):
            if rel.start_node()["category"] == kind1:
                msg.reply(rel.start_node()["name"])
        for rel in test_graph.match(end_node=progra1, rel_type="负责人", bidirectional=True):
            if rel.start_node()["category"] == kind1:
                msg.reply(rel.start_node()["name"])

    # 老师1/学生1参与的项目有？
    elif re.match(r'^[\u4e00-\u9fa5]{2,4}参[加与]的项目有', input_message):
        m1 = input_message.find('参')
        name3 = input_message[:m1]
        progra1 = test_graph.find_one("entity", property_key="name", property_value=name3)
        for rel in test_graph.match(start_node=progra1, rel_type="成员", bidirectional=True):
            msg.reply(rel.end_node()["name"])

    # 老师1指导的学生有？
    elif re.match(r'^[\u4e00-\u9fa5]{2,4}指导的学生有', input_message):
        m1 = input_message.find('指')
        name3 = input_message[:m1]
        progra1 = test_graph.find_one("entity", property_key="name", property_value=name3)
        for rel in test_graph.match(end_node=progra1, rel_type="师生", bidirectional=True):
            msg.reply(rel.start_node()["name"])

    # 查找属性
    elif len(input_message) < 4:
        msg.reply(kgquery_entity(input_message))

    # 查找关系
    elif re.match(r'^[\u4e00-\u9fa5]{2,20}和[\u4e00-\u9fa5]{2,20}的关系是', input_message):
        a = input_message.find('和')
        b = input_message.find('的')
        name1 = input_message[:a]
        name2 = input_message[a + 1:b]
        # find_one函数中，类别名由输入定，属性值也由输入值定
        n1 = test_graph.find_one("entity", property_key="name", property_value=name1)
        n2 = test_graph.find_one("entity", property_key="name", property_value=name2)
        ans = kgquery_rel(n1, n2)
        ans = str(ans)
        msg.reply(name1 + '和' + name2 + '的关系是：' + ans)

    else:
        msg.reply('请输入正确的查询内容')
embed()
