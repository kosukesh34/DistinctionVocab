import Foundation

struct VocabularyWord: Identifiable, Hashable, Sendable {
    let entryNumber: Int
    let headword: String
    let headwordAudioResource: AudioResourceReference
    let phonetic: String?
    let japaneseMeaning: String?
    let exampleSentences: [ExampleSentence]

    var id: String { "\(headword)-\(entryNumber)" }

    var displayPhonetic: String? {
        guard let phonetic, !phonetic.isEmpty else { return nil }
        return phonetic
    }

    var displayJapaneseMeaning: String? {
        guard let japaneseMeaning, !japaneseMeaning.isEmpty else { return nil }
        return japaneseMeaning
    }
}
