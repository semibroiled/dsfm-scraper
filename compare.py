from typing import List, Dict
import matplotlib.pyplot as plt


def compare_lists(list_a: List[str], list_b: List[str]) -> Dict[str, int]:
    """
    Compare two lists of texts and count the mentions of keywords in the other text.

    Args:
        list_a (List[str]): The list of target texts.
        list_b (List[str]): The list of texts containing the keywords.

    Returns:
        Dict[str, int]: A dictionary containing the mentioned keywords as keys and their mention counts as values.
    """
    mention_counts = {keyword: list_a.count(keyword) for keyword in list_b}
    print(mention_counts)
    return mention_counts


def plot_keyword_mentions(mention_counts: Dict[str, int]) -> None:
    """
    Plot the keyword mentions.

    Args:
        mention_counts (Dict[str, int]): Dictionary with keyword mentions and their counts.
    """
    filtered_dict = {key: value for key, value in mention_counts.items() if value > 0}
    print(filtered_dict)
    keywords = list(filtered_dict.keys())
    mentions = list(filtered_dict.values())

    plt.bar(keywords, mentions)
    plt.xlabel("Keywords")
    plt.ylabel("Mentions")
    plt.title("Keyword Mentions")
    plt.show()
