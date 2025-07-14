import json
import pandas as pd


class FewShotPosts:
    """
    Handles loading and filtering of sample social media posts
    for few-shot learning or prompt enhancement.
    """

    def __init__(self, file_path="data/processed_posts.json"):
        self.df = None
        self.unique_tags = None
        self._load_and_process_posts(file_path)

    def _load_and_process_posts(self, file_path):
        with open(file_path, encoding='utf-8') as processed_posts:
            posts = json.load(processed_posts)
            self.df = pd.json_normalize(posts)
            self.df["length"] = self.df['line_count'].apply(self.categorize_length)

            # Flatten and deduplicate all tags
            all_tags = self.df['tags'].apply(lambda x: x).sum()
            self.unique_tags = list(set(all_tags))

    def get_filtered_posts(self, tag, length, language):
        df_filtered = self.df[
            (self.df['tags'].apply(lambda tags: tag in tags)) &
            (self.df['length'] == length) &
            (self.df['language'] == language)
            ]
        return df_filtered.to_dict(orient='records')

    def categorize_length(self, line_count):
        if line_count < 5:
            return "Short"
        elif 5 <= line_count <= 10:
            return "Medium"
        else:
            return "Long"

    def get_tags(self):
        return self.unique_tags


if __name__ == "__main__":
    fs = FewShotPosts()
    posts = fs.get_filtered_posts("System Design", "Long", "English")
    print(posts)
