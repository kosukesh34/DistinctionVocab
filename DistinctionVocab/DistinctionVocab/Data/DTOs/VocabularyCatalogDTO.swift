import Foundation

struct VocabularyCatalogDTO: Decodable {
    let books: [VocabularyBookDTO]
}

struct VocabularyBookDTO: Decodable {
    let id: String
    let title: String
    let wordCount: Int
    let words: [VocabularyWordDTO]
}

struct VocabularyWordDTO: Decodable {
    let number: Int
    let headword: String
    let headwordAudio: String
    let phonetic: String?
    let nativeDefinition: String?
    let japaneseMeaning: String?
    let etymology: String?
    let examples: [ExampleSentenceDTO]
}
