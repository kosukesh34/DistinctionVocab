import Foundation

protocol VocabularyRepositoryProtocol: Sendable {
    func fetchBooks() throws -> [VocabularyBook]
}
