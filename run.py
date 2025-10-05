from app import create_app

app = create_app()

if __name__ == '__main__':
    # Running in debug mode is convenient for development
    app.run(debug=True)
