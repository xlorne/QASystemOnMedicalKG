from neo4j import GraphDatabase

# 自定义一个类来管理连接
class Neo4jConnection:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def query(self, query, parameters=None, db=None):
        with self.driver.session(database=db) as session:
            result = session.run(query, parameters)
            return list(result)
        
    def run(self, query, parameters=None, db=None):
        return self.query(query, parameters, db)
    
    def create(self, node):
        label = node.labels[0]
        properties = {key: value for key, value in node.items()}
        property_string = ', '.join([f"{key}: ${key}" for key in properties])
        query = f"CREATE (n:{label} {{{property_string}}})"
        self.query(query, properties)
        
    def counts(self):
        records  = self.query("MATCH (n) RETURN count(n)")
        count = records[0][0]
        return count
    
    def relationship(self, start_node, end_node, edges, rel_type, rel_name):
        for edge in edges:
            p = edge[0]
            q = edge[1]
            query = f"match(p:{start_node}),(q:{end_node}) where p.name=$p and q.name=$q create (p)-[rel:{rel_type}{{name:$rel_name}}]->(q)"
            params = {'p': p, 'q': q, 'rel_name': rel_name}
            self.query(query, parameters=params) 
    
    def clear(self):
        query = "MATCH (n) DETACH DELETE n"
        self.query(query)

# 定义节点对象 
class Node:
    def __init__(self, *labels, **properties):
        self.labels = labels
        self.properties = properties

    def __getitem__(self, key):
        return self.properties[key]

    def __setitem__(self, key, value):
        self.properties[key] = value

    def __delitem__(self, key):
        del self.properties[key]

    def __iter__(self):
        return iter(self.properties)

    def __len__(self):
        return len(self.properties)

    def items(self):
        return self.properties.items()