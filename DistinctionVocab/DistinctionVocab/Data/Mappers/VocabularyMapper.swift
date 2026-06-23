import Foundation

enum VocabularyMapper {
    static func map(_ catalogDTO: VocabularyCatalogDTO) -> [VocabularyBook] {
        catalogDTO.books.map(mapBook)
    }

    private static func mapBook(_ bookDTO: VocabularyBookDTO) -> VocabularyBook {
        VocabularyBook(
            identifier: bookDTO.id,
            title: bookDTO.title,
            wordCount: bookDTO.wordCount,
            words: bookDTO.words.map(mapWord)
        )
    }

    private static func mapWord(_ wordDTO: VocabularyWordDTO) -> VocabularyWord {
        VocabularyWord(
            entryNumber: wordDTO.number,
            headword: wordDTO.headword,
            headwordAudioResource: AudioResourceReference(relativePath: wordDTO.headwordAudio),
            phonetic: wordDTO.phonetic,
            japaneseMeaning: wordDTO.japaneseMeaning,
            exampleSentences: wordDTO.examples.map(mapExample)
        )
    }

    private static func mapExample(_ exampleDTO: ExampleSentenceDTO) -> ExampleSentence {
        ExampleSentence(
            label: exampleDTO.label,
            audioResource: AudioResourceReference(relativePath: exampleDTO.audio),
            text: exampleDTO.text,
            japaneseTranslation: exampleDTO.japaneseTranslation
        )
    }
}
