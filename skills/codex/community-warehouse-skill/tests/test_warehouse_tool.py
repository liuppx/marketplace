import json
import os
import sys
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import warehouse_tool  # noqa: E402


class FakeResponse:
    def __init__(self, value):
        self.value = value

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def read(self):
        return json.dumps(self.value).encode("utf-8")


class WarehouseToolClientTest(unittest.TestCase):
    def test_put_forwards_checksum_if_match_and_trace(self):
        captured = {}

        def fake_urlopen(req, timeout):
            captured["headers"] = dict(req.headers)
            captured["body"] = json.loads(req.data.decode("utf-8"))
            captured["timeout"] = timeout
            return FakeResponse({"name": "warehouse.object.put", "result": {}})

        with mock.patch.dict(os.environ, {
            "YEYING_WAREHOUSE_URL": "http://warehouse.test",
            "YEYING_WAREHOUSE_TOOL_TOKEN": "wts_test-secret",
        }, clear=False), mock.patch("urllib.request.urlopen", fake_urlopen):
            with mock.patch("sys.argv", ["warehouse_tool.py", "put", "/personal/a.txt", "hello",
                                          "--checksum-sha256", "abc", "--if-match", "etag-1", "--overwrite",
                                          "--trace-id", "trace-1"]):
                self.assertEqual(warehouse_tool.main(), 0)

        self.assertEqual(captured["body"]["traceId"], "trace-1")
        args = captured["body"]["arguments"]
        self.assertEqual(args["checksumSha256"], "abc")
        self.assertEqual(args["ifMatch"], "etag-1")
        self.assertTrue(args["overwrite"])
        self.assertEqual(captured["headers"]["X-trace-id"], "trace-1")
        self.assertEqual(captured["timeout"], 30)

    def test_config_requires_explicit_url_and_token(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(SystemExit) as raised:
                warehouse_tool.config()
            self.assertEqual(raised.exception.code, 2)


if __name__ == "__main__":
    unittest.main()
