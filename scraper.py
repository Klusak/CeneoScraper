import requests
from bs4 import BeautifulSoup

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
    single_opinion={
        "opinion_id": opinion["data-entry-id"],
        "author": opinion.select_one("span.user-post__author-name").text.strip(),
        "recomendation": opinion.select_one("span.user-post__author-recomendation > em").text.strip(),
        "stars": opinion.select_one("span.user-post__score-count").text.strip(),
        "purchased": opinion.select_one("div.review-pz").text.strip(),
        "opinion_date": opinion.select_one("span.user-post__published >time:nth-child(1)")["datetime"].strip(),
        "purchase_date": opinion.select_one("span.user-post__published >time:nth-child(2)")["datetime"].strip(),
        "useful": opinion.select_one("button.vote-yes")["data-total-vote"].strip(),
        "unuseful": opinion.select_one("button.vote-no")["data-total-vote"].strip(),
        "content": opinion.select_one("div.user-post__text").text.strip(),
        "cons": [ cons.text.strip() for cons in opinion.select("div.review-feature__title review-feature__title--negatives ~ div.review-feature__item")],
        "pros": [ pros.text.strip() for pros in opinion.select("div.review-feature__title review-feature__title--positives ~ div.review-feature__item")],
    }
    all_opinions.append(single_opinion)
    #print(opinion["data-entry-id"])
print((all_opinions))



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
