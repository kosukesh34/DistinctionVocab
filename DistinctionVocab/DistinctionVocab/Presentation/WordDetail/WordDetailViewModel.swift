import Foundation
import Observation

@MainActor
@Observable
final class WordDetailViewModel {
    let word: VocabularyWord
    let bookTitle: String

    var exampleSentences: [ExampleSentence] { word.exampleSentences }

    init(word: VocabularyWord, bookTitle: String) {
        self.word = word
        self.bookTitle = bookTitle
    }
}
