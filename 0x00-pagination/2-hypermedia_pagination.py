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

    def get_hyper(self, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        """Return a dictionary containing the following key-value
        pairs:
        - page_size: the length of the returned dataset page
        - page: the current page number
        - data: the dataset page (equivalent to return from previous
          task)
        - next_page: number of the next page, None if no next page
        - prev_page: number of the previous page, None if no previous
          page
        - total_pages: the total number of pages in the dataset as an
          integer
        """
        data: List[List] = self.get_page(page, page_size)
        total_pages: int = math.ceil(len(self.dataset()) / page_size)
        next_page: Optional[int] = page + 1 if page < total_pages else None
        prev_page: Optional[int] = page - 1 if page > 1 else None
        return {
            'page_size': len(data),
            'page': page,
            'data': data,
            'next_page': next_page,
            'prev_page': prev_page,
            'total_pages': total_pages
        }
