from flask import Flask, render_template,redirect,url_for
from wordcloud import WordCloud, STOPWORDS
import twint
from io import BytesIO
from flask import send_file
from flask import request
import base64

from textblob import TextBlob



app = Flask(__name__)

def WordCloud_wrapper(tweets):
    word_cloud = WordCloud(width=900, height=500,collocations = False, background_color = 'white').generate(tweets)
    img = BytesIO()
    word_cloud.to_image().save(img, 'PNG')
    img.seek(0)
    encoded_img_data = base64.b64encode(img.getvalue())
    return encoded_img_data.decode('utf-8')


def sentiment_analyzer(tweets):

    negative_tweets = []
    postive_tweets = []

    for tweet in tweets:
        analysis = TextBlob(tweet)
        if analysis.sentiment[0]<0:
            negative_tweets.append(tweet)
        else:
            postive_tweets.append(tweet)

    negative_tweets= " ".join(cat.split()[1] for cat in negative_tweets)
    postive_tweets= " ".join(cat.split()[1] for cat in postive_tweets)

    return negative_tweets,postive_tweets


@app.route('/', methods=['GET', 'POST'], endpoint='hello')
def hello():
    return render_template('homepage.html')



@app.route('/results/', methods=['GET', 'POST'], endpoint='hello2')
def hello2():

    if request.method == 'POST':
        Requested_City = request.form['City']
        Requested_State = request.form['State']

        print(Requested_City)
        print(Requested_State)

        from datetime import datetime, timedelta
        days_to_subtract = 1
        Three_days_ago = datetime.today() - timedelta(days=days_to_subtract)
        Three_days_ago = Three_days_ago.strftime("%Y-%d-%m %I:%M:%S")
        year = int(Three_days_ago[0:4])
        day = int(Three_days_ago[5:7])
        month = int(Three_days_ago[8:10])
        Three_days_ago = datetime(int(Three_days_ago[0:4]), month, day)
        print(Three_days_ago)

        c = twint.Config()
        c.Search = 'COVID-19 OR covid OR covid-19 OR covid19 OR COVID19 OR #COVID-19' #search keyword
        c.Since = str(Three_days_ago)
    #    c.Near = Requested_City + ',' +Requested_State
        c.Near = Requested_City
        c.Hide_output = True
        c.Limit = 10000
        #c.Count = True
    #    c.Stats = True
        c.Pandas = True
        twint.run.Search(c)

        Tweets_df = twint.storage.panda.Tweets_df
        print(Tweets_df)
        print(Tweets_df['tweet'])

        for cat in Tweets_df['tweet']:
            print(cat.split()[1])


        text = " ".join(cat.split()[1] for cat in Tweets_df['tweet'])
        negative_tweets,postive_tweets = sentiment_analyzer(Tweets_df['tweet'].to_list())

        all_wc= WordCloud_wrapper(text)
        n_wd= WordCloud_wrapper(negative_tweets)
        p_wd= WordCloud_wrapper(postive_tweets)


        return render_template("results.html", all_tweets_wordcloud=all_wc,plot=True,neg_tweets_wordcloud=n_wd,pos_tweets_wordcloud=p_wd,Requested_City=Requested_City,Requested_State=Requested_State)
    return render_template('homepage.html',plot=False)


if __name__ == "__main__":
    app.run(debug=True)
