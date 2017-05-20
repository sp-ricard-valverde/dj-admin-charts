class CustomizableChart:
    pass


class CustomizableDataset:

    def _get_datasets(self):
        if hasattr(self, 'get_datasets'):
            return self.get_datasets()
        else:
            pass