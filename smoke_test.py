from server import app


def main():
    client = app.test_client()
    health = client.get("/health")
    assert health.status_code == 200
    visualization = client.get("/visualization")
    assert visualization.status_code == 200
    spyder = client.get("/spyder/visualization")
    assert spyder.status_code == 200
    assert b"demo-user" in visualization.data


if __name__ == "__main__":
    main()
