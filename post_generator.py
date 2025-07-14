from llm_helper import llm
from few_shot import FewShotPosts

few_shot = FewShotPosts()


def get_length(length):
    if length == "Short":
        return "1 to 5 lines"
    if length == "Medium":
        return "6 to 10 lines"
    if length == "Long":
        return "more than 11 lines"


def generate_post(tag, length, language):
    promt = get_prompt(tag, length, language)
    post = llm.invoke(promt)
    return post.content


def get_prompt(tag, length, language):
    length_str = get_length(length)

    prompt = f'''
    Generate a LinkedIn post using the below information. No preamble.

    1) Topic: {tag}
    2) Length: {length_str}
    3) Language: {language}
    If Language is Hinglish then it means it is a mix of Hindi and English. 
    The script for the generated post should always be English.
    '''

    example_posts = few_shot.get_filtered_posts(length, language, tag)

    if len(example_posts) > 0:
        prompt += "4) Use the writing style as per the following examples."

    for i, post in enumerate(example_posts):
        post_text = post['text']
        prompt += f'\n\n Example {i + 1}: \n\n {post_text}'

        if i == 1:  # Use max two samples
            break

    return prompt


if __name__ == "__main__":
    post = generate_post("System Design", "Long", "English")
    print(post)
