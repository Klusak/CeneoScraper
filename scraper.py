import requests
import json
from bs4 import BeautifulSoup

def get_element(ancestor, selector=None, attribute=None, return_list=False):
    try: 
        if return_list:
            return [ tag.text.strip() for tag in ancestor.select(selector)]
        if not selector and attribute:
            return ancestor[attribute]
        if attribute:
            return ancestor.select_one(selector)[attribute].strip()
        return ancestor.select_one(selector).text.strip()
    except (AttributeError,TypeError):
        return  None

selectors={
        "opinion_id": [None,"data-entry-id"],
        "author": ["span.user-post__author-name"],
        "recomendation": ["span.user-post__author-recomendation > em"],
        "stars": ["span.user-post__score-count"],
        "purchased": ["div.review-pz"],
        "opinion_date": ["span.user-post__published >time:nth-child(1)","datetime"],
        "purchase_date": ["span.user-post__published >time:nth-child(2)","datetime"],
        "useful": ["button.vote-yes"],
        "unuseful": ["button.vote-no"],
        "content": ["div.user-post__text"],
        "cons": ["div.review-feature__title--negatives ~ div.review-feature__item", None, True],
        "pros": ["div.review-feature__title--positives ~ div.review-feature__item", None, True],
    }   


#product_code=input("Podaj kod produktu: ")
product_code="104978580"
#url="https://www.ceneo.pl/"+product_code+"#tab=reviews"
#url="https://www.ceneo.pl/{#tab=reviews".format(product_code)
url=f"https://www.ceneo.pl/{product_code}#tab=reviews"
response=requests.get(url)
page_dom= BeautifulSoup(response.text, "html.parser")
opinions=page_dom.select("div.js_product-review")
all_opinions=[]
for opinion in opinions:
    single_opinion={}
    for key, value in selectors.items():
        single_opinion[key]=get_element(opinion,*value)
    all_opinions.append(single_opinion)
    #print(opinion["data-entry-id"])

with open (f"./opinions/{product_code}.json", "w", encoding="UTF=8") as jf:
    json.dump(all_opinions, jf,  indent=4, ensure_ascii=False)



#div.js_product-review ---opinia
#["data-entry-id"] ---id opinii
#span.user-post__author-name
#span.user-post__author-recomendation > em
#span.user-post__score-count ---liczba gwiazdek
#div.review-pz ---czy opinia potwierdzona zakupem
#span.user-post__published >time:nth-child(1)["datetime"] ---data wystawienia opinii
#span.user-post__published >time:nth-child(2)["datetime"] ---data zakupu produktu
#button.vote-yes["data-total-vote"] ---ile osob zauznaje za przydatne
#button.vote-yes > span
#button.vote-no["data-total-vote"] ---ile osob zauznaje za nieprzydatne
#button.vote-no > span
#div.user-post__text ---treść opinii
#div.review-feature__title review-feature__title--negatives ~ div.review-feature__item ---lista wad
#div.review-feature__title review-feature__title--positives ~ div.review-feature__item ---lista zalet
