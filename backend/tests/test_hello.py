import io

from fastapi.testclient import TestClient


def test_hello(test_app: TestClient):
    """tests the /hello route

    Args:
        test_app (TestClient): the test client
    """

    # Given
    # test_app

    # When
    response = test_app.get("/hello")

    # Then
    assert response.status_code == 200, "Wrong status code"
    assert response.json() == {
        "Hello": "World",
        "environment": "dev",
        "testing": True,
    }


def test_hello_download_fail(test_app: TestClient):
    """checks that /hello-download fails if no file in
    upload folder

    Args:
        test_app (TestClient): the test client
    """
    response = test_app.get("/hello-download")

    assert response.status_code == 404


def test_hello_upload(test_app: TestClient):
    """tests the /hello-upload route

    Args:
        test_app (TestClient): the test client
    """
    response = test_app.post(
        "/hello-upload",
        files={"upload_file": ("myfile.pdf", io.BytesIO(b"abcdef"), "application/pdf")},
    )

    assert response.status_code == 200


def test_hello_download(test_app: TestClient):
    """tests the /hello-download route when a document is in the uploads folder

    Args:
        test_app (TestClient): the test client
    """
    response = test_app.get("/hello-download")

    assert response.status_code == 200
    assert response.content == b"abcdef"


def test_stream(test_app: TestClient):
    """tests the /hello-stream route

    Args:
        test_app (TestClient): the test client
    """
    response = test_app.post(
        "/hello-stream",
        files={"stream_file": ("myfile.pdf", io.BytesIO(b"stream"), "application/pdf")},
    )

    assert response.status_code == 200
    assert response.content == b"stream"
