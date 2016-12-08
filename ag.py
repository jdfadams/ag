#! /usr/bin/env python
"""A module for obtaining arXiv data using the ID."""
import requests
from bs4 import BeautifulSoup


def abstract_from_arxiv(arxiv_id):
    address = "http://arxiv.org/abs/" + arxiv_id
    r = requests.get(address)
    soup = BeautifulSoup(r.text, "html.parser")  # Or lxml?
    
    title_f = soup.find("meta", attrs={"name": "citation_title"})
    title = title_f["content"]
    
    author_f = soup.find_all("meta", attrs={"name": "citation_author"})
    authors = [x["content"] for x in author_f]
    
    abstract_f = soup.find("blockquote", attrs={"class": "abstract mathjax"})
    abstract = "".join(s for s in abstract_f.contents if isinstance(s, str)).strip()
    
    pdf_url_f = soup.find("meta", attrs={"name": "citation_pdf_url"})
    pdf_url = pdf_url_f["content"]
    
    return title, authors, abstract, pdf_url


def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="get data from arXiv using the ID")
    parser.add_argument("-p", "--pdf", action="store_true", help="download the PDF")
    parser.add_argument("arXivID", help="the arXiv ID")
    args = parser.parse_args()
    try:
        title, authors, abstract, pdf_url = abstract_from_arxiv(args.arXivID)
        print("Title:", title)
        print("Authors:", "; ".join(authors))
        print("Abstract:")
        print(abstract)
        print("PDF:", pdf_url)
        
        if args.pdf:
            filename = "arXiv-" + "-".join(args.arXivID.split("/")) + ".pdf"
            print("Downloading PDF as \"{}\"...".format(filename))
            pdf = requests.get(pdf_url, stream=True)
            with open(filename, "wb") as file:
                for chunk in pdf.iter_content(2000):
                    file.write(chunk)
        
    except Exception as error:
        print(error)


if __name__ == "__main__":
    main()
