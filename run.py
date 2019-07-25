from app import create_app


if __name__ == '__main__':
    app = create_app()
    app.config.API_URI_FILTER = 'slash'
    app.run(**app.config['RUN_SETTING'])
