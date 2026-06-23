import Foundation

struct VocabularySearchResult: Identifiable, Hashable, Sendable {
    let book: VocabularyBook
    let word: VocabularyWord

    var id: String { "\(book.identifier)-\(word.id)" }
}
