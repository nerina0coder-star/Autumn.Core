import re
from concurrent.futures.thread import ThreadPoolExecutor
from threading import Lock
from unittest import TestCase

from Autumn.Naming.generator import Generator


class Test(TestCase):

    def setUp(self):
        self.generator: Generator = Generator()

    def test_generating_identifier(self):

        made = set()
        lock = Lock()
        pattern = re.compile(r"[a-zA-Z_][a-zA-Z0-9\-_]*")

        def test():

            for i in range(100):
                identifier = self.generator.generate_identifier()
                with lock:
                    self.assertNotIn(identifier, made)
                    self.assertRegex(identifier, pattern)
                    made.add(identifier)

        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(test) for _ in range(5)]
            for future in futures:
                future.result(timeout=5)

    def test_generating_class(self) -> None:

        made = set()
        lock = Lock()
        pattern = re.compile(r"[a-zA-Z_][a-zA-Z0-9\-_]*")

        def test():

            for i in range(100):
                cls = self.generator.generate_class()
                with lock:
                    self.assertNotIn(cls, made)
                    self.assertRegex(cls, pattern)
                    made.add(cls)

        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(test) for _ in range(5)]
            for future in futures:
                future.result(timeout=5)

    def test_instance_isolation(self) -> None:

        lock = Lock()

        generator2 = Generator()

        def test():
            for i in range(100):
                cls = self.generator.generate_identifier()
                cls2 = generator2.generate_identifier()
                with lock:
                    self.assertEqual(cls, cls2)

        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(test) for _ in range(5)]
            for future in futures:
                future.result(timeout=5)

    def test_context(self):

        with Generator.context(prefix="pre-", suffix="-fix") as gen:
            self.assertEqual(gen.generate_identifier(), "pre-a-fix")
