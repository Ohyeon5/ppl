import json
import sys
import xml.etree.ElementTree as ET
from logging import Formatter, StreamHandler, getLogger

# from pathlib import Path
from typing import Dict, List, Tuple

import requests
from ppl.path import DATA_PATH

# from ppl.utils.index_builder import build_index

LOGGER = getLogger(__name__)
LOGGER.setLevel("INFO")
log_formatter = Formatter(
    "[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d:%(funcName)s] %(message)s"
)
for handler in LOGGER.handlers:
    LOGGER.removeHandler(handler)
handler_out = StreamHandler(sys.stdout)
handler_out.setFormatter(log_formatter)
LOGGER.addHandler(handler_out)

ESEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
ESUMMARY_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
EFETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"


def query_uids_from_terms(
    search_term: str,
    s_start: int = 1,
    n_uids: int = 15,
    relative_date: int | None = None,
) -> Tuple[List[int], int]:
    """query PubMed IDs from search terms
    if relative_date is provided, uids from the last n days will be returned
    if relative_date is not provided, latest n_uids will be returned

    Args:
        search_term (str): search term
        s_start (int, optional): start idx for querying. Defaults to 1.
        n_uids (int, optional): number of uids to query. Defaults to 15.
        relative_date (int, optional): relative dates from the search date. Defaults to None.

    Raises:
        SystemExit: abort the program if the request fails

    Returns:
        Tuple[List[int], int]: return list of uids and total counts
    """
    # Construct the PubMed API URL with the search term
    date_string = (
        f"&datetype=pdat&reldate={relative_date}" if relative_date is not None else ""
    )
    url = f"{ESEARCH_URL}?db=pubmed&term={search_term}&retmode=json&retstart={((s_start - 1) * n_uids)}\
&retmax={n_uids}{date_string}"

    try:
        # Make the request to the PubMed API to get the PubMed IDs
        response = requests.get(url)
        response.raise_for_status()
        # Extract the PubMed IDs from the API response
        data = response.json()
        pubmed_ids = data["esearchresult"]["idlist"]
        total_counts = int(data["esearchresult"]["count"])
        return pubmed_ids, total_counts
    except requests.exceptions.RequestException as e:
        LOGGER.error(e)
        raise SystemExit(e)


def query_summaries(pubmed_ids: List[int]) -> List[Dict]:
    """query article summaries from PubMed IDs

    Args:
        pubmed_ids (List[int]): a list of PubMed IDs

    Raises:
        SystemExit: abort the program if the request fails

    Returns:
        List[Dict]: a list of article details
    """
    # Construct the PubMed API URL with the PubMed IDs
    url = f"{ESUMMARY_URL}?db=pubmed&id={','.join(pubmed_ids)}&retmode=json"

    try:
        # Make the request to the PubMed API to get the article summaries
        response = requests.get(url)
        response.raise_for_status()

        summary_data = response.json()
        article_details = []
        for pubmed_id in pubmed_ids:
            article_title = summary_data["result"][pubmed_id]["title"]
            article_url = f"https://pubmed.ncbi.nlm.nih.gov/{pubmed_id}/"
            epubdate = summary_data["result"][pubmed_id]["epubdate"]

            # Get the authors' information
            author_names = [
                author["name"]
                for author in summary_data["result"][pubmed_id]["authors"]
            ]

            article_details.append(
                {
                    "pubmed_id": pubmed_id,
                    "title": article_title,
                    "url": article_url,
                    "authors": author_names,
                    "epubdate": epubdate,
                }
            )
        return article_details
    except requests.exceptions.RequestException as e:
        LOGGER.error(e)
        raise SystemExit(e)


def query_abstracts(pubmed_ids: List[int]) -> List[Dict]:
    """query article abstracts from PubMed IDs

    Args:
        pubmed_ids (List[int]): a list of PubMed IDs

    Raises:
        SystemExit: abort the program if the request fails

    Returns:
        List[Dict]: a list of article abstracts,
            keys are PubMed IDs and values are abstracts
    """
    # Construct the PubMed API URL with the PubMed IDs
    url = f"{EFETCH_URL}?db=pubmed&id={','.join(pubmed_ids)}&retmode=xml"

    try:
        # Make the request to the PubMed API to get the article abstracts
        response = requests.get(url)
        response.raise_for_status()
        # Extract the article abstracts from the API response
        xml_data = response.text
        root = ET.fromstring(xml_data)

        abstract_collection: List = []

        for article in root.findall("PubmedArticle"):
            uid = article.find("MedlineCitation").find("PMID").text
            abstract_elements = article.findall(".//AbstractText")
            if abstract_elements:
                abstract = "\n".join(
                    abstract_element.text.strip()
                    for abstract_element in abstract_elements
                    if abstract_element.text
                )
            else:
                abstract = ""
            abstract_collection.append({uid: abstract})

        return abstract_collection
    except requests.exceptions.RequestException as e:
        LOGGER.error(e)
        raise SystemExit(e)


def merge_article_details_and_abstracts(
    article_details: List[Dict], abstracts: List[Dict]
) -> List[Dict]:
    """merge article details and abstracts

    Args:
        article_details (List[Dict]): a list of article details
        abstracts (List[Dict]): a list of article abstracts

    Returns:
        List[Dict]: a list of article details with abstracts
    """
    merged_details = []
    for article in article_details:
        for abstract in abstracts:
            if article["pubmed_id"] in abstract:
                article["abstract"] = abstract[article["pubmed_id"]]
                merged_details.append(article)
    return merged_details


def filter_articles(keywords: List[str], article_details: List[Dict]) -> List[Dict]:
    """filter articles by keywords and existance of abstracts

    Args:
        keywords (List[str]): a list of keywords
        article_details (List[Dict]): a list of article details

    Returns:
        List[Dict]: a list of filtered article details
    """
    filtered_articles = []
    for article in article_details:
        # boolean check for the keywords in the article title or abstract
        key_check = [
            keyword.lower() in article["title"].lower()
            or keyword.lower() in article["abstract"].lower()
            for keyword in keywords
        ]
        if any(key_check):
            filtered_articles.append(article)
    return filtered_articles


def query_pubmed(
    search_term: str,
    keywords: List[str],
    n_uids: int = 20,
    relative_date: int | None = None,
) -> List[Dict]:
    """query PubMed articles by search term and page

    Args:
        search_term (str): search term
        keywords (List[str]): a list of keywords to filter articles
        n_uids (int, optional): number of uids to query. Defaults to 15.
        relative_date (int, optional): relative dates from the search date. Defaults to None.

    Returns:
        List[Dict]: a list of article details
    """
    s_start = 1
    total_counts = n_uids
    filtered_articles: List = []
    while (s_start - 1) * n_uids < total_counts:
        pubmed_ids, total_counts = query_uids_from_terms(
            search_term, s_start, n_uids, relative_date
        )
        LOGGER.info(f"Total counts: {total_counts}, returned counts: {len(pubmed_ids)}")
        article_details = query_summaries(pubmed_ids)
        abstracts = query_abstracts(pubmed_ids)
        merged_details = merge_article_details_and_abstracts(article_details, abstracts)
        filtered = filter_articles(keywords, merged_details)
        LOGGER.info(f"Filtered counts: {len(filtered)}/{len(pubmed_ids)}")
        filtered_articles.extend(filtered)
        s_start += 1
    LOGGER.info(f"Total filtered counts: {len(filtered_articles)}")
    return filtered_articles


if __name__ == "__main__":
    search_term = "cosentyx"
    keywords = [
        "consentyx",
        "psoriasis",
        "treatment outcomes",
        "Secukinumab",
        "efficacy",
        "safety",
    ]

    articles = query_pubmed(search_term, keywords, relative_date=30)

    # save articles to a json file
    with open(DATA_PATH / "articles.json", "w") as f:
        json.dump(articles, f, indent=4)

    # # TODO: build index
    # parent_dir = Path(".")
    # save_dir = Path("index")
    # build_index(parent_dir, save_dir)
