import Foundation

final class BundleVocabularyRepository: VocabularyRepositoryProtocol, @unchecked Sendable {
    private let dataSource: BundleVocabularyDataSourceProtocol
    private let lock = NSLock()
    private var cachedBooks: [VocabularyBook]?

    init(dataSource: BundleVocabularyDataSourceProtocol) {
        self.dataSource = dataSource
    }

    func fetchBooks() throws -> [VocabularyBook] {
        lock.lock()
        defer { lock.unlock() }

        if let cachedBooks {
            return cachedBooks
        }

        let catalogDTO = try dataSource.loadCatalogDTO()
        let books = VocabularyMapper.map(catalogDTO)
        cachedBooks = books
        return books
    }
}
