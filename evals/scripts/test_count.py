"""content-log's count.py on a real https-style download. Standard library only, no network.

    python3 evals/scripts/test_count.py

A local server stands in for Vamos's data link and answers as Cloudflare does there: Python's
default User-Agent gets a 403 (error 1010), anything else gets the rows. Before fc5222a every real
json_url failed this way while the evals, which serve file: links, passed.
"""
import json, os, subprocess, sys, threading, unittest
from http.server import BaseHTTPRequestHandler, HTTPServer

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
COUNT = os.path.join(ROOT, 'plugins', 'vamos', 'skills', 'content-log', 'scripts', 'count.py')
ROWS = os.path.join(ROOT, 'plugins', 'vamos', 'evals', 'content-log-week-opusjake', 'mocks', 'vamos', 'chat_completion_poll.md')
BODY = json.dumps(json.load(open(ROWS, encoding='utf-8'))['data']).encode()


class Cdn(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.headers.get('User-Agent', '').startswith('Python-urllib'):
            self.send_response(403)
            self.end_headers()
            self.wfile.write(b'error code: 1010')
        elif self.path.startswith('/data/rows.json'):
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(BODY)
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, *a):
        pass


class CountDownload(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = HTTPServer(('127.0.0.1', 0), Cdn)
        cls.base = f'http://127.0.0.1:{cls.server.server_address[1]}'
        threading.Thread(target=cls.server.serve_forever, daemon=True).start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()

    def run_count(self, url):
        return subprocess.run([sys.executable, '-I', COUNT, url, '--since', '2026-11-03'],
                              capture_output=True, text=True, timeout=60)

    def test_link_downloads_past_the_user_agent_check(self):
        out = self.run_count(self.base + '/data/rows.json?e=1&s=2')
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertIn('usual: 42,606 views, the median of 34 posts', out.stdout)
        self.assertRegex(out.stdout, r'14\.4\s?x')

    def test_failed_download_says_what_to_do_in_one_line(self):
        out = self.run_count(self.base + '/data/missing.json')
        self.assertNotEqual(out.returncode, 0)
        self.assertNotIn('Traceback', out.stderr)
        self.assertIn("couldn't download the rows", out.stderr)
        self.assertIn('curl -sL', out.stderr)


if __name__ == '__main__':
    unittest.main()
