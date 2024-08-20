#!/usr/bin/env python3
"""
Simple Pagination Implementation
"""

import csv
import math
from typing import List, Dict, Union, Any, Optional, Callable, Tuple


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    @staticmethod
    def index_range(page: int, page_size: int) -> Tuple:
        """Return a tuple of size two containing a start index and an
        end index corresponding to the range of indexes to return in a
        list for those particular pagination parameters.
        """
        b: int = page * page_size
        a: int = b - page_size
        return (a, b)

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """Return the appropriate page of the dataset (i.e. the
        correct list of rows).
        """
        assert isinstance(page, int) and isinstance(page_size, int)
        assert page > 0 and page_size > 0
        a, b = Server.index_range(page, page_size)
        return self.dataset()[a:b]
