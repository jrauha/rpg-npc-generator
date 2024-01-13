class PaginatedResponse:
    def __init__(self, data, pagination):
        self.data = data
        self.pagination = pagination


class Pagination:
    def __init__(self, page, page_size, total_pages):
        self.page = page
        self.page_size = page_size
        self.total_pages = total_pages
