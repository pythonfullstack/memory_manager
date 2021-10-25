import sys


class MustGreaterThanZeroError(Exception):
    """The number of bytes you are gonna allocate should be greater than 0"""

    def __str__(self):
        return f"MustGreaterThanZero Exception: The number of bytes you are gonna allocate should be greater than 0"


class OverSizeError(Exception):
    """The memory manager has been already fully allocated"""

    def __str__(self):
        return f"OverSize Exception: The memory manager has been already fully allocated"


class NotEqualObjectError(Exception):
    """The object you are gonna allocate into memory manager should be the same as the initialized object"""

    def __str__(self):
        return f"NotEqualObject Exception: " \
               f"The object you are gonna allocate into memory manager should be the same as the initialized object"


class NotAllocatedError(Exception):
    """No Object has been allocated"""

    def __str__(self):
        return f"NotAllocated Exception: No Object has been allocated"


class MemoryManager:
    """
    A class of Memory Manager
    attributes: public: num_bytes, data,
                protected: _none_index_list, _buffer
    methods: public methods: alloc(), free()
    """

    def __init__(self, buffer: object, num_bytes: int, *args, **kwargs) -> None:
        if num_bytes < 1:
            raise MustGreaterThanZeroError
        self.num_bytes = num_bytes
        self.data: list = [None] * num_bytes
        self._none_index_list: list = list(range(num_bytes))  # the list storing index of None in data
        self._buffer = buffer

    def alloc(self, size: int, obj: object, *args, **kwargs):

        if size < 1:
            sys.stdout.write(f"The size must be grater than zero\n")
            raise MustGreaterThanZeroError

        current = len(self._none_index_list)
        if current < size:
            sys.stdout.write(f"You are available to allocate {current} objects\n")
            raise OverSizeError
        else:
            if obj.__class__ != self._buffer.__class__:
                sys.stdout.write(
                    f"The object you are gonna allocate into memory manager "
                    f"should be the same as the initialized object\n")
                raise NotEqualObjectError
            else:
                for _ in range(size):
                    self.data[self._none_index_list[0]] = obj
                    self._none_index_list.pop(0)

    def free(self, index: int, *args, **kwargs):
        if len(self._none_index_list) == self.num_bytes:
            raise NotAllocatedError

        if index in self._none_index_list:
            sys.stdout.write(f"Index {index}, It's been already free\n")
        else:
            self._none_index_list.append(index)
            self._none_index_list = sorted(self._none_index_list)
            self.data[index] = None
