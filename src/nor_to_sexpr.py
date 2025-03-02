import re

def convert_s_expression_to_sparql_1(s_expression):
    pattern = r"\( ASK \( AND \( (\w+) (\w+) (\w+) \) \( \1 \2 (\w+) \) \) \)"
    match = re.match(pattern, s_expression)
    
    if match:
        entity, predicate, obj1, obj2 = match.groups()
        return f"ASK WHERE {{ wd:{entity} wdt:{predicate} wd:{obj1} . wd:{entity} wdt:{predicate} wd:{obj2} }}"
    
    return None
def convert_s_expression_to_sparql_2(s_expression):
    pattern = r"\( MAX \( JOIN \( R (\w+) \) \( JOIN (\w+) (\w+) \) \) \)"
    match = re.match(pattern, s_expression)
    
    if match:
        rel2, rel1, type_entity = match.groups()
        return f"SELECT ?ent WHERE {{ ?ent wdt:{rel1} wd:{type_entity} . ?ent wdt:{rel2} ?obj }} ORDER BY DESC(?obj) LIMIT 5"
    
    return None
def convert_s_expression_to_sparql_3(s_expression):
    pattern = r"\( JOIN \( R (\w+) \) \( JOIN \( R (\w+) \) (\w+) \) \)"
    match = re.match(pattern, s_expression)
    
    if match:
        rel2, rel1, entity = match.groups()
        return f"SELECT ?answer WHERE {{ wd:{entity} wdt:{rel1} ?X . ?X wdt:{rel2} ?answer }}"
    
    return None
def convert_s_expression_to_sparql_4(s_expression):
    pattern = r"\( AND \( JOIN \( R (\w+) \) (\w+) \) \( JOIN (\w+) (\w+) \) \)"
    match = re.match(pattern, s_expression)
    
    if match:
        rel1, en1, rel2, en2 = match.groups()
        return f"SELECT DISTINCT ?obj WHERE {{ wd:{en1} wdt:{rel1} ?obj . ?obj wdt:{rel2} wd:{en2} }}"
    
    return None
def convert_s_expression_to_sparql_5(s_expression):
    pattern = r"\( MIN \( JOIN \( R (\w+) \) \( AND \( JOIN (\w+) (\w+) \) \( JOIN (\w+) (\w+) \) \) \) \)"
    match = re.match(pattern, s_expression)
    
    if match:
        rel, rel1, obj1, rel2, obj2 = match.groups()
        return f"SELECT ?ent WHERE {{ ?ent wdt:{rel1} wd:{obj1} . ?ent wdt:{rel} ?obj . ?ent wdt:{rel2} wd:{obj2} }} ORDER BY ASC(?obj) LIMIT 5"
    
    return None
def convert_s_expression_to_sparql_6(s_expression):
    pattern = r"\( MAX \( JOIN \( R (\w+) \) \( AND \( JOIN (\w+) (\w+) \) \( JOIN (\w+) (\w+) \) \) \) \)"
    match = re.match(pattern, s_expression)
    
    if match:
        rel, rel1, obj1, rel2, obj2 = match.groups()
        return f"SELECT ?ent WHERE {{ ?ent wdt:{rel1} wd:{obj1} . ?ent wdt:{rel} ?obj . ?ent wdt:{rel2} wd:{obj2} }} ORDER BY DESC(?obj) LIMIT 5"
    
    return None
def convert_s_expression_to_sparql_7(s_expression):
    pattern = r"\( JOIN (\w+) (\w+) \)"
    match = re.match(pattern, s_expression)
    
    if match:
        predicate, obj = match.groups()
        return f"SELECT DISTINCT ?answer WHERE {{ ?answer wdt:{predicate} wd:{obj} }}"
    
    return None

def convert_s_expression_to_sparql_8(s_expression):
    pattern = r"\( JOIN \( R (\w+) \) \( AND \( JOIN \( R \1 \) (\w+) \) \( JOIN (\w+) (\w+) \) \) \)"
    match = re.match(pattern, s_expression)
    
    if match:
        pred, entity, qualifier, qual_obj = match.groups()
        return f"SELECT ?obj WHERE {{ wd:{entity} p:{pred} ?s . ?s ps:{pred} ?obj . ?s pq:{qualifier} wd:{qual_obj} }}"
    
    return None

def convert_s_expression_to_sparql_9(s_expression):
    pattern = r"\( JOIN \( R (\w+) \) \( AND \( JOIN \( R (\w+) \) (\w+) \) \( JOIN \2 (\w+) \) \) \)"
    match = re.match(pattern, s_expression)
    
    if match:
        qualifier, pred, entity, obj = match.groups()
        return f"SELECT ?value WHERE {{ wd:{entity} p:{pred} ?s . ?s ps:{pred} wd:{obj} . ?s pq:{qualifier} ?value }}"
    
    return None
def convert_s_expression_to_sparql_10(s_expression):
    pattern = r"\( AND \( JOIN (\w+) (\w+) \) \( JOIN (\w+) (\w+) \) \)"
    match = re.match(pattern, s_expression)
    
    if match:
        pred, obj, p2, type_obj = match.groups()
        return f"SELECT DISTINCT ?sbj WHERE {{ ?sbj wdt:{pred} wd:{obj} . ?sbj wdt:{p2} wd:{type_obj} }}"
    
    return None

def convert_s_expression_to_sparql_11(s_expression):
    pattern = r"\( AND \( JOIN \( R (\w+) \) (\w+) \) \( JOIN (\w+) (\w+) \) \)"
    match = re.match(pattern, s_expression)
    
    if match:
        rel1, entity, rel2, obj = match.groups()
        return f"SELECT ?answer WHERE {{ wd:{entity} wdt:{rel1} ?answer . ?answer wdt:{rel2} wd:{obj} }}"
    
    return None

def convert_s_expression_to_sparql_12(s_expression):
    pattern = r"\( ASK \( (\=|>=|<=|>|<) \( JOIN \( R (\w+) \) (\w+) \) (\d+(\.\d+)?) \) \)"
    match = re.match(pattern, s_expression)
    
    if match:
        operator, predicate, entity, value, _ = match.groups()
        return f"ASK WHERE {{ wd:{entity} wdt:{predicate} ?obj filter(?obj {operator} {value}) }}"
    
    return None

def convert_s_expression_to_sparql_13(s_expression):
    pattern = r"\( JOIN \( R (\w+) \) (\w+) \) \( JOIN \( R (\w+) \) \2 \)"
    match = re.match(pattern, s_expression)
    
    if match:
        pred1, entity, pred2 = match.groups()
        return f"SELECT ?ans_1 ?ans_2 WHERE {{ wd:{entity} wdt:{pred1} ?ans_1 . wd:{entity} wdt:{pred2} ?ans_2 }}"
    
    return None

def convert_s_expression_to_sparql_14(s_expression):
    pattern = r"\( COUNT \( JOIN (\w+) (\w+) \) \)"
    match = re.match(pattern, s_expression)
    
    if match:
        predicate, obj = match.groups()
        return f"SELECT (COUNT(?sub) AS ?value ) {{ ?sub wdt:{predicate} wd:{obj} }}"
    
    return None

def convert_s_expression_to_sparql_15(s_expression):
    pattern = r"\( COUNT \( JOIN \( R (\w+) \) (\w+) \) \)"
    match = re.match(pattern, s_expression)
    
    if match:
        predicate, entity = match.groups()
        return f"SELECT (COUNT(?obj) AS ?value ) {{ wd:{entity} wdt:{predicate} ?obj }}"
    
    return None

def convert_s_expression_to_sparql_16(s_expression):
    pattern = r"\( JOIN \( R (\w+) \) (\w+) \)"
    match = re.match(pattern, s_expression)
    
    if match:
        predicate, entity = match.groups()
        return f"SELECT DISTINCT ?answer WHERE {{ wd:{entity} wdt:{predicate} ?answer }}"
    
    return None

def convert_s_expression_to_sparql_17(s_expression):
    pattern = r"\( CHAR \( AND \( JOIN (\w+) (\w+) \) \( JOIN (\w+) (\w+) \) \) ['\"](.*?)['\"] \)"
    match = re.match(pattern, s_expression)
    
    if match:
        pred1, obj1, pred2, obj2, char = match.groups()
        return f"""SELECT DISTINCT ?sbj ?sbj_label WHERE {{ 
            ?sbj wdt:{pred1} wd:{obj1} . 
            ?sbj wdt:{pred2} wd:{obj2} . 
            ?sbj rdfs:label ?sbj_label . 
            FILTER(STRSTARTS(lcase(?sbj_label), '{char}')) . 
            FILTER (lang(?sbj_label) = 'en') 
        }} LIMIT 25"""
    
    return None

def convert_s_expression_to_sparql_18(s_expression):
    pattern = r"\( ASK \( (\w+) (\w+) (\w+) \) \)"
    match = re.match(pattern, s_expression)
    
    if match:
        entity, predicate, obj = match.groups()
        return f"ASK WHERE {{ wd:{entity} wdt:{predicate} wd:{obj} }}"
    
    return None

def convert_s_expression_to_sparql_19(s_expression):
    pattern = r"\( WORD \( JOIN (\w+) (\w+) \) ['\"](.*?)['\"] \)"
    match = re.match(pattern, s_expression)
    
    if match:
        predicate, obj, word = match.groups()
        return f"""SELECT DISTINCT ?sbj ?sbj_label WHERE {{ 
            ?sbj wdt:{predicate} wd:{obj} . 
            ?sbj rdfs:label ?sbj_label . 
            FILTER(CONTAINS(lcase(?sbj_label), '{word}')) . 
            FILTER (lang(?sbj_label) = 'en') 
        }} LIMIT 25"""
    
    return None

def convert_s_expression_to_sparql_20(s_expression):
    pattern = r"\( JOIN \( R (\w+) \) \( JOIN \( R (\w+) \) (\w+) \) \)"
    match = re.match(pattern, s_expression)
    
    if match:
        rel2, rel1, entity = match.groups()
        return f"SELECT ?answer WHERE {{ wd:{entity} wdt:{rel1} ?X . ?X wdt:{rel2} ?answer }}"
    
    return None

def convert_s_expression_to_sparql_21(s_expression):
    pattern = r"\( JOIN \( R (\w+) \) \( FILTER \( JOIN \( R (\w+) \) \( JOIN \( R (\w+) \) (\w+) \) \) \( ['\"](.*?)['\"] \) \) \)"
    match = re.match(pattern, s_expression)
    
    if match:
        pred1, pred2, pred3, entity, value = match.groups()
        return f"""SELECT ?obj WHERE {{ 
            wd:{entity} p:{pred1} ?s . 
            ?s ps:{pred1} ?obj . 
            ?s pq:{pred2} ?x filter(contains(?x,'{value}')) 
        }}"""
    
    return None

def convert_s_expression_to_sparql_22(s_expression):
    pattern = r"\( JOIN \( R (\w+) \) \( FILTER \( JOIN \( R (\w+) \) (\w+) \) \( ['\"](.*?)['\"] \) \) \)"
    match = re.match(pattern, s_expression)
    
    if match:
        rel1, rel2, entity, value = match.groups()
        return f"""SELECT ?answer WHERE {{ 
            wd:{entity} wdt:{rel1} ?answer . 
            ?answer wdt:{rel2} ?x FILTER(contains(?x,'{value}')) 
        }}"""
    
    return None

def convert_s_expression_to_sparql_23(s_expression):
    pattern = r"\( JOIN \( R (\w+) \) \( FILTER \( JOIN \( R (\w+) \) \( JOIN \( R (\w+) \) (\w+) \) \) \( ['\"](.*?)['\"] \) \) \)"
    match = re.match(pattern, s_expression)
    
    if match:
        pred1, pred2, pred3, entity, value = match.groups()
        return f"""SELECT ?obj WHERE {{ 
            wd:{entity} p:{pred3} ?s . 
            ?s ps:{pred3} ?obj . 
            ?s pq:{pred2} ?x filter(contains(YEAR(?x),'{value}')) 
        }}"""
    
    return None

def convert_s_expression_to_sparql_24(s_expression):
    pattern = r"\( FILTER \( JOIN \( R (\w+) \) \( JOIN \( R (\w+) \) (\w+) \) \) \( YEAR ['\"](.*?)['\"] \) \)"
    match = re.match(pattern, s_expression)
    
    if match:
        rel2, rel1, entity, value = match.groups()
        return f"""SELECT ?answer WHERE {{ 
            wd:{entity} wdt:{rel1} ?answer . 
            ?answer wdt:{rel2} ?x FILTER(contains(YEAR(?x),'{value}')) 
        }}"""
    
    return None


def convert_s_expression_to_sparql_25(s_expression):
    pattern = r"\( WORD \( JOIN (\w+) (\w+) \) ['\"](.*?)['\"] \)"
    match = re.match(pattern, s_expression)
    
    if match:
        predicate, obj, word = match.groups()
        return f"""SELECT DISTINCT ?sbj ?sbj_label WHERE {{ 
            ?sbj wdt:{predicate} wd:{obj} . 
            ?sbj rdfs:label ?sbj_label . 
            FILTER(STRSTARTS(lcase(?sbj_label), '{word}')) . 
            FILTER (lang(?sbj_label) = 'en') 
        }} LIMIT 25"""
    
    return None

conversion_functions = [
    convert_s_expression_to_sparql_1, convert_s_expression_to_sparql_2, convert_s_expression_to_sparql_3,
    convert_s_expression_to_sparql_4, convert_s_expression_to_sparql_5, convert_s_expression_to_sparql_6,
    convert_s_expression_to_sparql_7, convert_s_expression_to_sparql_8, convert_s_expression_to_sparql_9,
    convert_s_expression_to_sparql_10, convert_s_expression_to_sparql_11, convert_s_expression_to_sparql_12,
    convert_s_expression_to_sparql_13, convert_s_expression_to_sparql_14, convert_s_expression_to_sparql_15,
    convert_s_expression_to_sparql_16, convert_s_expression_to_sparql_17, convert_s_expression_to_sparql_18,
    convert_s_expression_to_sparql_19, convert_s_expression_to_sparql_20, convert_s_expression_to_sparql_21,
    convert_s_expression_to_sparql_22, convert_s_expression_to_sparql_23, convert_s_expression_to_sparql_24,
    convert_s_expression_to_sparql_25
]

def convert_s_expression_to_sparql(s_expression):
    """
    Chuyển đổi S-expression sang SPARQL bằng cách thử từng template phù hợp.
    """
    for func in conversion_functions:
        sparql_query = func(s_expression)
        if sparql_query:
            return sparql_query  # Trả về SPARQL nếu có kết quả hợp lệ

    return "UNKNOWN"  # Trả về UNKNOWN nếu không khớp với bất kỳ mẫu nào
