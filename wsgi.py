from blog_website import create_app

app = create_app()

with app.app_context():
    app.run(debug=True)



