import sys
from unittest import TestCase
from threading import Thread
from memory import MemoryManager, MustGreaterThanZeroError, NotEqualObjectError, OverSizeError, NotAllocatedError


class WrongObject:
    pass


class MemoryManagerTestCase(TestCase):
    def setUp(self) -> None:
        self.obj = str()
        self.num_bytes = 5
        self.num_threads = 5

    def tearDown(self) -> None:
        del self.obj
        del self.num_bytes

    def test_initialization(self):
        """
        This test is to check initialization of memory manager.
        1) In the case that number of bytes is zero, it should raise MustGreaterThanZeroError
        2) Checking initial attributes of Memory Manager
        """
        # Checking zero bytes
        with self.assertRaises(MustGreaterThanZeroError):
            MemoryManager(self.obj, 0)

        m = MemoryManager(self.obj, self.num_bytes)
        self.assertEqual(m.num_bytes, self.num_bytes)
        self.assertEqual(m.data, [None] * self.num_bytes)
        self.assertEqual(m._none_index_list, list(range(self.num_bytes)))
        self.assertEqual(m._buffer, self.obj)

    def test_alloc(self):
        """
        This is for checking alloc function
        1) If number of bytes should be greater than zero, else it should raise MustGreaterThanZeroError
        2) If the object to be allocated isn't same as the buffer, it should raise NotEqualObjectError
        3) Checking full allocation case
        4) Checking Partial allocation case
        5) If the size of allocation is more than available size, it should raise OverSizeError
        6) Checking allocation case again
        """
        m = MemoryManager(self.obj, self.num_bytes)
        size = self.num_bytes - 1
        if size < 1:
            with self.assertRaises(MustGreaterThanZeroError):
                m.alloc(size, self.obj)
        else:
            with self.assertRaises(NotEqualObjectError):
                m.alloc(size, WrongObject)

            # Checking full allocation case
            m.alloc(self.num_bytes, self.obj)
            self.assertEqual(m.data, [self.obj] * self.num_bytes)
            del m

            m = MemoryManager(self.obj, self.num_bytes)

            # Checking partial allocation case
            test_size = 3
            m.alloc(test_size, self.obj)
            self.assertEqual(m.data[: test_size], [self.obj] * test_size)
            self.assertEqual(m._none_index_list, [3, 4])

            # oversize allocation
            over_size = 4
            with self.assertRaises(OverSizeError):
                m.alloc(over_size, self.obj)

            # Checking allocation case again
            test_size = self.num_bytes - test_size
            m.alloc(test_size, self.obj)
            self.assertEqual(m.data, [self.obj] * self.num_bytes)
            self.assertEqual(len(m._none_index_list), 0)

    def test_free(self):
        """
        This test is to check making memory manager free
        1) Checking when nothing has been allocated, it should raise NotAllocatedError
        2) Checking free after allocate 5 objects into memory manager
        3) Checking flexible allocate function
        """
        # Not Allocated
        m = MemoryManager(self.obj, self.num_bytes)
        with self.assertRaises(NotAllocatedError):
            m.free(0)

        # Checking free function
        for _ in range(self.num_bytes):
            m.alloc(1, self.obj)

        m.free(1)
        m.free(3)
        self.assertEqual(m.data[1], None)
        self.assertEqual(m.data[3], None)

        # Test alloc(2)
        m.alloc(2, self.obj)
        self.assertEqual(m.data, [self.obj] * self.num_bytes)

    def test_thread_safe(self):
        """
        This test is to check thread-safe. Just check in case of alloc for thread-safety
        """
        m = MemoryManager(self.obj, self.num_bytes)

        # Sets the thread switch interval
        sys.setswitchinterval(0.005)

        threads = []
        for _ in range(self.num_threads):
            threads.append(Thread(target=m.alloc, args=(1, self.obj,)))

        for i in range(self.num_threads):
            threads[i].start()

        for i in range(self.num_threads):
            threads[i].join()

        self.assertEqual(m.data, [self.obj] * self.num_bytes)
