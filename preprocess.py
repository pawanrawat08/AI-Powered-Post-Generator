import json
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from llm_helper import llm


def process_posts(raw_file_path, processed_file_path="data/processed_posts.json"):
    enriched_posts = []
    with open(raw_file_path, encoding='utf-8') as file:
        posts = json.load(file)
        for post in posts:
            metadata = extract_metadata(post['text'])
            post_with_metadata = post | metadata
            enriched_posts.append(post_with_metadata)

    unified_tags = get_unified_tags(enriched_posts)

    for post in enriched_posts:
        current_tag = post['tags']
        new_tags = {unified_tags[tag] for tag in current_tag}
        post['tags'] = list(new_tags)

    with open(processed_file_path, encoding='utf-8', mode='w') as outfile:
        json.dump(enriched_posts, outfile, indent=4)


def get_unified_tags(posts_with_metadata):
    unique_tags = set()
    # Loop over each post and extract the unique tags
    for post in posts_with_metadata:
        unique_tags.update(post['tags'])

    unique_tags_list = ','.join(unique_tags)

    print(unique_tags_list)
    # "Databases, Api, ElasticSearch"

    template = '''I will give you a list of tags. You need to unify tags with the following requirements, 
    1. Tags are unified and merged to create a shorter list. 
        Example 1: "Database", "time-series databases", "Redis", "Bloom Filters" can be all merged into a single 
        tag "Database". 
        Example 2: "horizontal scaling", "partitioning", "distributed systems", "sharding", "cache" can be mapped to 
        "System Design".
        Example 3: "fuzzy string matching", "address matching", can be mapped to "String Matching Algorithm".
        Example 4: "interviews", "career" can be mapped as to "Software Engineer Career". 
    2. Each tag should be follow title case convention, it means words are separated by space and first letter 
        should be in caps. example: "database" as "Database", "system design" as  "System Design".
    3. Output should be a JSON object, No preamble.
    4. Output should have mapping of original tag and the unified tag.
        For example: {{"distributed systems": "Distributed Systems", "horizontal scaling": "Horizontal Scaling", 
        "vibe coding": "Vibe Coding"}}.
    
    Here is the list of tags: 
    {tags}
    '''

    pt = PromptTemplate.from_template(template)
    chain = pt | llm
    response = chain.invoke(input={"tags": str(unique_tags_list)})
    try:
        json_parser = JsonOutputParser()
        res = json_parser.parse(response.content)
    except OutputParserException:
        raise OutputParserException("Context too big. Unable to parse jobs.")

    return res


def extract_metadata(post):
    template = '''
    You are given a LinkedIn post. You need to extract number of lines, language of the post and tags.
    1. Return a valid Json. NO preamble.
    2. JSON object should have exactly three keys: line_count, language and tags.
    3. tags is an array of text tags. Extract maximum two tags and minimum one.
    4. Language should be English or Hinglish (Hinglish means hindi + english)
    
    Here is the actual post on which you need to perform this task:
    {post}
    '''

    pt = PromptTemplate.from_template(template)
    chain = pt | llm
    response = chain.invoke(input={'post': post})

    try:
        json_parser = JsonOutputParser()
        res = json_parser.parse(response.content)
    except OutputParserException:
        raise OutputParserException("Context too big. Unable to parse jobs.")

    return res


if __name__ == "__main__":
    process_posts("data/raw_posts.json", "data/processed_posts.json")
