class ConfigClass:
    def __init__(self, corpus_path=''):
        self.corpusPath = corpus_path
        self.savedFileMainFolder = ''
        self.saveFilesWithStem = self.savedFileMainFolder + "/WithStem"
        self.saveFilesWithoutStem = self.savedFileMainFolder + "/WithoutStem"
        print('Project was created successfully..')

    def get__corpusPath(self):
        return self.corpusPath

    def get_saveFilesWithStem(self):
        return self.saveFilesWithStem
