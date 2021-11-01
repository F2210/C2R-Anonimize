# from .language import NER
#
# class anonimize:
#
#     id: int
#     text: str
#     placeholders: dict
#
#     def __init__(self, text):
#         # set an id for this piece of text
#         self.id = self.setid()
#
#         # detect language to choose model
#         self.language = self.detectlanguage(text)
#
#         self.entities = NER(self.text).entities
#
#         print(self.entities)
#
#         # set text in class
#         self.text = text
#
#         # perform NER
#         self.placeholders = self.performNER()
#
#         # replace data with placeholders and store them for de-anonimization
#         self.text = self.replaceNE()
#
#     def detectlanguage(self, text):
#
#         language = "NL"
#         language = "EN"
#
#         return language
#
#
#     def setid(self):
#         return 1
#
#     def performNER(self):
#         return {}
#
#     def replaceNE(self):
#         return ""
#
#
#
# def main(text):
#
#     anonimize("Tom lives in California")

