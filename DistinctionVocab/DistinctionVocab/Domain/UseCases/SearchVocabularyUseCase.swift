import Foundation

protocol SearchVocabularyUseCaseProtocol: Sendable {
    func execute(query: String, in books: [VocabularyBook]) -> [VocabularySearchResult]
}

struct SearchVocabularyUseCase: SearchVocabularyUseCaseProtocol {
    func execute(query: String, in books: [VocabularyBook]) -> [VocabularySearchResult] {
        let normalizedQuery = query
            .trimmingCharacters(in: .whitespacesAndNewlines)
            .lowercased()

        guard !normalizedQuery.isEmpty else { return [] }

        return books.flatMap { book in
            book.words
                .filter { $0.headword.lowercased().contains(normalizedQuery) }
                .map { VocabularySearchResult(book: book, word: $0) }
        }
    }
}
