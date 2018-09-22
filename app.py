from flask import Flask, render_template, redirect
import pymongo
import scrape_mars

app = Flask(__name__)

client = pymongo.MongoClient('mongodb://localhost:27017')


# @app.route('/')
# def index():
#     mars = client.db.mars.find_one()
#     return render_template('index.html', mars=mars)

# @app.route('/scrape')
# def scrape():
#     mars = client.db.mars
#     data = scrape_mars.scrape()
#     mars.update({}, data, upsert=True)
#     return redirect("http://localhost:5000/", code=302)

# if __name__ == "__main__":
#     app.run(debug=True)

db = client.mars_db
collection = db.data

@app.route('/')
def home():
    data = collection.find_one()
    return render_template('index.html', mars=data)

# Create route that will trigger scrape functions
@app.route('/scrape')
def scrape():
    mars_info = scrape_mars.scrape()

    # # Combine results into one dictionary
    # mars = {
    #     'news_title': mars_info['news_title'],
    #     'news_p': mars_info['news_p'],
    #     # 'featured_image_url': mars_info['featured_image_url'],
    #     # 'mars_weather': mars_info['mars_weather'],
    #     # 'tables': mars_info['tables'],
    #     # 'hem_img_urls': mars_info['hem_img_urls'],
        
    # }

    # # Insert forecast into database
    # collection.insert_one(mars_info)
    collection.update({}, mars_info, upsert=True)
    # Redirect back to home page
    return redirect('/', code=302)

if __name__ == '__main__':
    app.run(debug=True)



