import Foundation
import Observation

@MainActor
@Observable
final class VocabularyCatalogViewModel {
    private(set) var availableBooks: [VocabularyBook] = []
    private(set) var isCatalogLoaded = false
    private(set) var loadingErrorMessage: String?

    private let loadVocabularyUseCase: LoadVocabularyUseCaseProtocol

    init(loadVocabularyUseCase: LoadVocabularyUseCaseProtocol) {
        self.loadVocabularyUseCase = loadVocabularyUseCase
    }

    func loadCatalogIfNeeded() {
        guard !isCatalogLoaded, loadingErrorMessage == nil else { return }

        do {
            availableBooks = try loadVocabularyUseCase.execute()
            isCatalogLoaded = true
        } catch {
            loadingErrorMessage = error.localizedDescription
        }
    }

    func book(withIdentifier identifier: String) -> VocabularyBook? {
        availableBooks.first { $0.identifier == identifier }
    }
}
