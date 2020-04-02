import unittest
from starlette.testclient import TestClient
from api import routes

class BasicTests(unittest.TestCase):
    def test_generate(self):
        client = TestClient(routes.app)
        response = client.post('/generate');
        assert response.status_code == 200

    def test_generate_twosteps(self):
        client = TestClient(routes.app)
        response = client.post('/generate', json=[{"id":1,"stepId":"stepId","doc":"doc","type":"type","language":"python","position":1,"createdAt":"2020-04-02T10:11:47.805Z","updatedAt":"2020-04-02T10:11:47.805Z","workflowId":1,"inputs":[{"id":1,"doc":"doc","createdAt":"2020-04-02T10:11:47.829Z","updatedAt":"2020-04-02T10:11:47.829Z","stepId":1}],"outputs":[{"id":1,"doc":"doc","extension":"extension","createdAt":"2020-04-02T10:11:47.850Z","updatedAt":"2020-04-02T10:11:47.850Z","stepId":1}],"implementations":[{"id":1,"fileName":"hello-world.py","createdAt":"2020-04-02T10:11:47.891Z","updatedAt":"2020-04-02T10:11:47.891Z","stepId":1}]},{"id":2,"stepId":"stepId","doc":"doc","type":"type","language":"python","position":2,"createdAt":"2020-04-02T10:11:47.899Z","updatedAt":"2020-04-02T10:11:47.899Z","workflowId":1,"inputs":[{"id":2,"doc":"doc","createdAt":"2020-04-02T10:11:47.908Z","updatedAt":"2020-04-02T10:11:47.908Z","stepId":2}],"outputs":[{"id":2,"doc":"doc","extension":"extension","createdAt":"2020-04-02T10:11:47.915Z","updatedAt":"2020-04-02T10:11:47.915Z","stepId":2}],"implementations":[{"id":2,"fileName":"hello-world.py","createdAt":"2020-04-02T10:11:47.931Z","updatedAt":"2020-04-02T10:11:47.931Z","stepId":2}]}]);
        assert response.status_code == 200

if __name__ == "__main__":
    unittest.main()
