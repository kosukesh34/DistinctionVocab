import Foundation

protocol LoadVocabularyUseCaseProtocol: Sendable {
    func execute() throws -> [VocabularyBook]
}

struct LoadVocabularyUseCase: LoadVocabularyUseCaseProtocol {
    private let vocabularyRepository: VocabularyRepositoryProtocol

    init(vocabularyRepository: VocabularyRepositoryProtocol) {
        self.vocabularyRepository = vocabularyRepository
    }

    func execute() throws -> [VocabularyBook] {
        try vocabularyRepository.fetchBooks()
    }
}
