from bs4 import BeautifulSoup
import requests
import csv
import time
import random

# SNES START URL url = 'https://www.mobygames.com/browse/games/playstation/list-games/'.
url = "https://www.mobygames.com/browse/games/snes/list-games/"

page = requests.get(url)
soup = BeautifulSoup(page.text, "html.parser")

pageNumbers = int(soup.find("td", class_="mobHeaderPage").text.split(" ")[4])
for bigIteration in range(pageNumbers):
    print(bigIteration)
    if bigIteration > 0:
        page = requests.get(nextPage)
        soup = BeautifulSoup(page.text, "html.parser")
    # FIND ALL GAME LINKS ON PAGE
    findTable = soup.find("table", id="mof_object_list")
    findTableBody = findTable.find("tbody")
    gameList = findTableBody.find_all("tr")
    iteration = 0

    print(gameList[0].find_all("a")[0]["href"])

    for game in gameList:
        time.sleep(random.randint(1, 4))
        print(iteration)
        iteration = iteration + 1

        link = game.find_all("a")[0]["href"]

        # NAVIGATE TO SINGLE GAME
        gamePage = requests.get(link)
        gameContent = BeautifulSoup(gamePage.text, "html.parser")

        # GET CONTENTS
        title = (
            gameContent.find("h1", class_="niceHeaderTitle")
            .find("a")
            .text.encode("utf-8")
            .decode("utf-8")
            .replace("&nbsp;", " ")
        )
        print(title)

        publishedBy = gameContent.find("div", string="Published by")
        if publishedBy is not None:
            publishedBy = (
                publishedBy.find_next("div")
                .text.encode("utf-8")
                .decode("utf-8")
                .replace("&nbsp;", " ")
            )

        developedBy = gameContent.find("div", string="Developed by")
        if developedBy is not None:
            developedBy = (
                developedBy.find_next("div")
                .text.encode("utf-8")
                .decode("utf-8")
                .replace("&nbsp;", " ")
            )

        released = gameContent.find("div", string="Released")
        if released is not None:
            released = (
                released.find_next("div")
                .text.encode("utf-8")
                .decode("utf-8")
                .replace("&nbsp;", " ")
            )

        genre = gameContent.find("div", string="Genre")
        if genre is not None:
            genre = (
                genre.find_next("div")
                .text.encode("utf-8")
                .decode("utf-8")
                .replace("&nbsp;", " ")
            )

        perspective = gameContent.find("div", string="Perspective")
        if perspective is not None:
            perspective = (
                perspective.find_next("div")
                .text.encode("utf-8")
                .decode("utf-8")
                .replace("&nbsp;", " ")
            )

        visual = gameContent.find("div", string="Visual")
        if visual is not None:
            visual = (
                visual.find_next("div")
                .text.encode("utf-8")
                .decode("utf-8")
                .replace("&nbsp;", " ")
            )

        art = gameContent.find("div", string="Art")
        if art is not None:
            art = (
                art.find_next("div")
                .text.encode("utf-8")
                .decode("utf-8")
                .replace("&nbsp;", " ")
            )

        gameplay = gameContent.find("div", string="Gameplay")
        if gameplay is not None:
            gameplay = (
                gameplay.find_next("div")
                .text.encode("utf-8")
                .decode("utf-8")
                .replace("&nbsp;", " ")
            )

        interface = gameContent.find("div", string="Interface")
        if interface is not None:
            interface = interface.find_next("div").textF

        # USER REVIEWS
        userReviews = gameContent.find("h2", string="User Reviews")
        userReviewCount = 0
        finalReviews = []
        if "no reviews" in userReviews.find_next("p").text:
            print("There are no reviews for this game.")
        else:
            userReviewsTable = userReviews.find_next("table")
            reviews = userReviewsTable.find_all("tr")
            for review in reviews:
                stars = review.find_all("td")[2]
                if stars.text == "unrated":
                    print("unrated")
                else:
                    userReviewCount = userReviewCount + 1
                    try:
                        rev = float(stars.find_next("img")["alt"].split()[0])
                    except:
                        print("Couldn't convert to float")
                    finalReviews.append(rev)
        averageReview = None
        if len(finalReviews) == 0:
            finalReviews = None
        if userReviewCount > 0:
            averageReview = sum(finalReviews) / userReviewCount

        # CRITIC REVIEWS
        criticReviews = gameContent.find("h2", string="Critic Reviews")
        criticCount = 0
        finalCritics = []
        if (
            criticReviews.find_next("p").text
            == "There are no critic reviews for this game."
        ):
            print("There are no critics for this game.")
        else:
            criticReviewsTable = criticReviews.find_next("table")
            critics = criticReviewsTable.find_all("tr")
            for critic in critics:
                score = critic.find_all("td")[3].text
                if score == "Unscored":
                    print("unscored")
                else:
                    criticCount = criticCount + 1
                    finalCritics.append(float(score))
        averageCritic = None
        if len(finalCritics) == 0:
            finalCritics = None
        if criticCount > 0:
            averageCritic = sum(finalCritics) / criticCount

        # WRITE TO CSV - 'Playstation.csv'
        with open("SNES.csv", mode="a", newline="", encoding="utf-8") as outputFile:
            platform = "SNES"
            gamereviewsCSV = csv.writer(
                outputFile, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
            )

            if bigIteration == 0 and iteration == 1:
                gamereviewsCSV.writerow(
                    [
                        "platform",
                        "title",
                        "published by",
                        "developed by",
                        "released",
                        "genre",
                        "perspective",
                        "visual",
                        "art",
                        "gameplay",
                        "interface",
                        "userReviews",
                        "userReviewCount",
                        "averageUserReview",
                        "criticReviews",
                        "criticReviewCount",
                        "averageCriticReview",
                    ]
                )

            gamereviewsCSV.writerow(
                [
                    platform,
                    title,
                    publishedBy,
                    developedBy,
                    released,
                    genre,
                    perspective,
                    visual,
                    art,
                    gameplay,
                    interface,
                    finalReviews,
                    userReviewCount,
                    averageReview,
                    finalCritics,
                    criticCount,
                    averageCritic,
                ]
            )

    # FIND NEXT BUTTON
    nextPage = soup.find("a", string="Next")["href"]
