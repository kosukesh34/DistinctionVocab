import Foundation

struct VocabularyBook: Identifiable, Hashable, Sendable {
    let identifier: String
    let title: String
    let wordCount: Int
    let words: [VocabularyWord]

    var id: String { identifier }
}
