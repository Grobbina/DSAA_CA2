import re

parsed_tree_str = "abc 123 def 456 ghi"

match = re.search(r'\b\D+\b', parsed_tree_str)

if match:
    print("Found match:", match.group(1))
else:
    print("No match found.")
