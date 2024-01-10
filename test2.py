import re 

parsed_tree_str = '50-3x'


pattern = re.compile(r'([+-]?\d*)[a-zA-Z]+')
matches = pattern.findall(parsed_tree_str)

print(matches)