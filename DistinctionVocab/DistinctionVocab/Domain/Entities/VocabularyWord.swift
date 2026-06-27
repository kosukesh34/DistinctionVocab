import Foundation

struct VocabularyWord: Identifiable, Hashable, Sendable {
    let entryNumber: Int
    let headword: String
    let headwordAudioResource: AudioResourceReference
    let phonetic: String?
    let nativeDefinition: String?
    let japaneseMeaning: String?
    let etymology: String?
    let exampleSentences: [ExampleSentence]

    var id: String { "\(headword)-\(entryNumber)" }

    var displayPhonetic: String? {
        guard let phonetic, !phonetic.isEmpty else { return nil }
        return phonetic
    }

    var displayNativeDefinition: String? {
        guard let nativeDefinition, !nativeDefinition.isEmpty else { return nil }
        return nativeDefinition
    }

    var displayJapaneseMeaning: String? {
        guard let japaneseMeaning, !japaneseMeaning.isEmpty else { return nil }
        return japaneseMeaning
    }

    var displayEtymology: String? {
        guard let etymology, !etymology.isEmpty else { return nil }
        return etymology
    }
}
