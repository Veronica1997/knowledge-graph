from py2neo import Graph, Node, Relationship
test_graph = Graph("http://127.0.0.1:7474/browser/", username="neo4j", password="08166517416reny")
test_graph.delete_all()