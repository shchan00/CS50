import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    links = corpus[page]
    random = False
    # Check if the page has no links, we randomly select one from the corpus
    if not links:
        links = corpus.keys()
        random = True
    model = {}
    link_no = len(links)
    if random:
        # random distribution if no links
        for i in links:
            probability = 1 / link_no
            model.update({i: probability})
    else:
        for i in corpus.keys():
            # damping factor case + true random case for links
            if i in links:
                probability = damping_factor / link_no + (1 - damping_factor) / (len(corpus))
                model.update({i: probability})
            else:
                # true random case for pages not directly linked
                stay_prob = (1 - damping_factor) / (len(corpus))
                model.update({i: stay_prob})
    return model


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pagerank = {}
    # To make sure at least the page is recognized, even though it may not be chosen
    for page in corpus:
        pagerank[page] = 0
    # randomly choose 1 page
    page = random.choice(list(corpus.keys()))

    for _ in range(n):
        # record visiting that page once
        pagerank[page] += 1
        # Setting up the transition state, model the choices the surfer can go for this page and the probability of each choice
        prob_model = transition_model(corpus, page, damping_factor)

        links = list(prob_model.keys())
        probability = list(prob_model.values())
        # Take one of the choices based on probability
        page = random.choices(links, probability)[0]
    # Normalizing the number of visits into probability
    for i in pagerank:
        pagerank[i] = pagerank[i] / n

    return pagerank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pagerank = {}
    corpus_len = len(corpus)
    for page in corpus:
        pagerank[page] = 1 / corpus_len
    threshold = 0.001
    new_pagerank = pagerank.copy()
    while True:
        for p in corpus:
            total = (1 - damping_factor) / corpus_len
            for i in corpus:
                if p in corpus[i]:
                    total += damping_factor * (pagerank[i] / len(corpus[i]))
                if not corpus[i]:
                    total += damping_factor * (pagerank[i] / corpus_len)
            new_pagerank[p] = total
        converge = True
        for page in pagerank:
            if abs(new_pagerank[page] - pagerank[page]) >= threshold:
                converge = False
                break
        if converge == True:
            break
        else:
            pagerank = new_pagerank.copy()
    return pagerank


if __name__ == "__main__":
    main()
