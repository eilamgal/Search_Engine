class ConfigClass:
    def __init__(self, corpus_path='', number_of_term_buckets=10, number_of_entities_buckets=2):
        self.number_of_term_buckets = number_of_term_buckets
        self.number_of_entities_buckets = number_of_entities_buckets
        self.first_entities_bucket_index = number_of_term_buckets
        self.corpusPath = corpus_path
        self.savedFileMainFolder = ''
        self.saveFilesWithStem = self.savedFileMainFolder + "/WithStem"
        self.saveFilesWithoutStem = self.savedFileMainFolder + "/WithoutStem"
        print('Project was created successfully..')

    def get_corpusPath(self):
        return self.corpusPath

    def get_saveFilesWithStem(self):
        return self.saveFilesWithStem

    def get_number_of_term_buckets(self):
        return self.number_of_term_buckets

    def get_number_of_entities_buckets(self):
        return self.number_of_entities_buckets

    def get_entities_index(self):
        return self.first_entities_bucket_index
