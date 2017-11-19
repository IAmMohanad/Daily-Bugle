from django.test import TestCase, Client

# Imports all Models for Testing
from .models import Article, Category, User
from datetime import datetime

#
# Nabil's Test Cases
#

class ArticleModelTests(TestCase):

    # Test creating an article model
    def test_create_article_model(self):
        test_user = User(full_name="Muhammad Nabil Fadhiya", email="nabil@me.com", password="NowYouSeeMe", phone_number="07478344545")
        test_user.save()
        test_category = Category(name="Racing")
        test_category.save()

        title = "Bacon Ipsum"
        text = """Bacon ipsum dolor amet sausage pig venison, pork loin cow andouille shoulder
        kevin pancetta meatloaf pastrami hamburger kielbasa salami biltong. Shank capicola tongue,
        bresaola pork chop sausage kevin short loin. Alcatra buffalo drumstick beef ribs ball tip boudin t-bone
        brisket meatball. Fatback swine salami, meatloaf sausage ball tip chicken porchetta pastrami bresaola
        biltong prosciutto boudin doner flank. Turducken cow t-bone andouille.

        Drumstick andouille buffalo swine, jowl pastrami cow chuck beef ribs. Doner short ribs andouille bacon.
        Alcatra ham pastrami, jowl fatback doner buffalo t-bone. Swine turducken pastrami ham. Shankle ribeye bacon,
        bresaola ball tip pork short loin frankfurter corned beef meatball. Turkey shoulder shankle, alcatra
        tri-tip brisket turducken chuck sausage kielbasa. Flank shankle leberkas alcatra shoulder pork."""
        pub_date = datetime.now()
        author_id = 1
        category_id = 1

        test_article = Article(title=title, text=text, pub_date=pub_date, author=test_user, category=test_category)
        test_article.save()
        # print(test_article.title, test_article.text, test_article.pub_date, test_article.author_id, test_article.category_id)
