"""
Tests unitaires complets du framework
"""
import unittest
import asyncio
import json
from core.request import Request
from core.response import Response
from core.router import Router
from utils.parser import HTTPParser
from middleware.base import Middleware
from middleware.cors import CORSMiddleware
from middleware.logging import LoggingMiddleware


class TestHTTPParser(unittest.TestCase):
    """Tests du parser HTTP"""
    
    def test_parse_simple_get(self):
        """Test parsing d'une requête GET simple"""
        raw = "GET /test HTTP/1.1\r\nHost: localhost\r\n\r\n"
        request = HTTPParser.parse_request(raw)
        
        self.assertEqual(request.method, "GET")
        self.assertEqual(request.path, "/test")
        self.assertEqual(request.version, "HTTP/1.1")
        self.assertEqual(request.get_header("Host"), "localhost")
    
    def test_parse_post_with_body(self):
        """Test parsing d'une requête POST avec body"""
        raw = (
            "POST /api/user HTTP/1.1\r\n"
            "Content-Type: application/json\r\n"
            "Content-Length: 27\r\n"
            "\r\n"
            '{"name": "John", "age": 30}'
        )
        request = HTTPParser.parse_request(raw)
        
        self.assertEqual(request.method, "POST")
        self.assertEqual(request.path, "/api/user")
        self.assertEqual(request.content_type, "application/json")
        self.assertEqual(request.body, '{"name": "John", "age": 30}')
    
    def test_parse_query_params(self):
        """Test parsing des query parameters"""
        raw = "GET /search?q=python&page=2 HTTP/1.1\r\n\r\n"
        request = HTTPParser.parse_request(raw)
        
        self.assertEqual(request.path_without_query, "/search")
        self.assertEqual(request.query_params["q"], "python")
        self.assertEqual(request.query_params["page"], "2")


class TestRequest(unittest.IsolatedAsyncioTestCase):
    """Tests de la classe Request"""
    
    async def test_json_parsing(self):
        """Test parsing du body JSON"""
        request = Request(
            method="POST",
            path="/api/test",
            headers={"Content-Type": "application/json"},
            body='{"name": "Alice", "score": 95}'
        )
        
        data = await request.json()
        self.assertEqual(data["name"], "Alice")
        self.assertEqual(data["score"], 95)
    
    def test_get_header_case_insensitive(self):
        """Test que get_header est case-insensitive"""
        request = Request(
            method="GET",
            path="/",
            headers={"Content-Type": "text/plain", "X-Custom-Header": "value"}
        )
        
        self.assertEqual(request.get_header("content-type"), "text/plain")
        self.assertEqual(request.get_header("Content-Type"), "text/plain")
        self.assertEqual(request.get_header("x-custom-header"), "value")


class TestResponse(unittest.TestCase):
    """Tests de la classe Response"""
    
    def test_json_response(self):
        """Test création d'une réponse JSON"""
        response = Response.json({"message": "Hello", "status": "ok"})
        
        self.assertEqual(response.status, 200)
        self.assertIn("application/json", response.headers["Content-Type"])
        
        # Vérifier que le body est du JSON valide
        data = json.loads(response.body)
        self.assertEqual(data["message"], "Hello")
    
    def test_response_to_bytes(self):
        """Test conversion en bytes HTTP"""
        response = Response("Hello World", status=200)
        bytes_data = response.to_bytes()
        
        self.assertIn(b"HTTP/1.1 200 OK", bytes_data)
        self.assertIn(b"Hello World", bytes_data)
    
    def test_set_cookie(self):
        """Test définition de cookies"""
        response = Response("Test")
        response.set_cookie("session_id", "abc123", max_age=3600)
        
        self.assertIn("Set-Cookie", response.headers)
        self.assertIn("session_id=abc123", response.headers["Set-Cookie"])
        self.assertIn("Max-Age=3600", response.headers["Set-Cookie"])


class TestRouter(unittest.IsolatedAsyncioTestCase):
    """Tests du système de routing"""
    
    async def dummy_handler(self, request):
        return Response("OK")
    
    def test_simple_route(self):
        """Test matching d'une route simple"""
        router = Router()
        router.add_route("/test", self.dummy_handler, ["GET"])
        
        handler, params = router.match("/test", "GET")
        self.assertIsNotNone(handler)
        self.assertEqual(params, {})
    
    def test_route_with_params(self):
        """Test route avec paramètres dynamiques"""
        router = Router()
        router.add_route("/user/{id}/post/{post_id}", self.dummy_handler, ["GET"])
        
        handler, params = router.match("/user/123/post/456", "GET")
        self.assertIsNotNone(handler)
        self.assertEqual(params["id"], "123")
        self.assertEqual(params["post_id"], "456")
    
    def test_route_not_found(self):
        """Test route inexistante"""
        router = Router()
        router.add_route("/test", self.dummy_handler, ["GET"])
        
        handler, params = router.match("/notfound", "GET")
        self.assertIsNone(handler)
    
    def test_method_not_allowed(self):
        """Test méthode HTTP non autorisée"""
        router = Router()
        router.add_route("/test", self.dummy_handler, ["GET"])
        
        handler, params = router.match("/test", "POST")
        self.assertIsNone(handler)


class TestMiddleware(unittest.IsolatedAsyncioTestCase):
    """Tests des middleware"""
    
    async def test_middleware_execution_order(self):
        """Test l'ordre d'exécution des middleware"""
        execution_order = []
        
        class TestMiddleware1(Middleware):
            async def before_request(self, request):
                execution_order.append("M1_before")
                return None
            
            async def after_request(self, request, response):
                execution_order.append("M1_after")
                return response
        
        class TestMiddleware2(Middleware):
            async def before_request(self, request):
                execution_order.append("M2_before")
                return None
            
            async def after_request(self, request, response):
                execution_order.append("M2_after")
                return response
        
        m1 = TestMiddleware1()
        m2 = TestMiddleware2()
        
        request = Request("GET", "/", {})
        response = Response("OK")
        
        # Simuler l'exécution dans l'ordre
        await m1.before_request(request)
        await m2.before_request(request)
        # Handler ici
        await m2.after_request(request, response)
        await m1.after_request(request, response)
        
        self.assertEqual(
            execution_order,
            ["M1_before", "M2_before", "M2_after", "M1_after"]
        )
    
    async def test_cors_middleware(self):
        """Test du middleware CORS"""
        cors = CORSMiddleware(allow_origins=["http://example.com"])
        
        request = Request(
            "GET",
            "/api/test",
            {"Origin": "http://example.com"}
        )
        response = Response("OK")
        
        # Exécuter le middleware
        await cors.before_request(request)
        response = await cors.after_request(request, response)
        
        self.assertIn("Access-Control-Allow-Origin", response.headers)
        self.assertEqual(
            response.headers["Access-Control-Allow-Origin"],
            "http://example.com"
        )


class TestIntegration(unittest.IsolatedAsyncioTestCase):
    """Tests d'intégration"""
    
    async def test_complete_flow(self):
        """Test un flux complet requête -> réponse"""
        from core.server import App
        
        app = App("TestApp")
        
        @app.route("/hello/{name}", methods=["GET"])
        async def hello(request):
            name = request.path_params["name"]
            return Response.json({"message": f"Hello {name}!"})
        
        # Simuler une requête
        request = Request("GET", "/hello/World", {})
        response = await app.handle_request(request)
        
        self.assertEqual(response.status, 200)
        data = json.loads(response.body)
        self.assertEqual(data["message"], "Hello World!")


def run_tests():
    """Exécuter tous les tests"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestHTTPParser))
    suite.addTests(loader.loadTestsFromTestCase(TestRequest))
    suite.addTests(loader.loadTestsFromTestCase(TestResponse))
    suite.addTests(loader.loadTestsFromTestCase(TestRouter))
    suite.addTests(loader.loadTestsFromTestCase(TestMiddleware))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)