from pytest import fixture

from unfeed.app import create_app


@fixture
def app(request):
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'

    ctx = app.app_context()
    ctx.push()

    @request.addfinalizer
    def teardown():
        ctx.pop()

    return app
