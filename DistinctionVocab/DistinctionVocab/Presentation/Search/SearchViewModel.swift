import Foundation
import Observation

@MainActor
@Observable
final class SearchViewModel {
    private(set) var searchResults: [VocabularySearchResult] = []

    private let searchVocabularyUseCase: SearchVocabularyUseCaseProtocol
    private let vocabularyCatalogViewModel: VocabularyCatalogViewModel

    init(
        searchVocabularyUseCase: SearchVocabularyUseCaseProtocol,
        vocabularyCatalogViewModel: VocabularyCatalogViewModel
    ) {
        self.searchVocabularyUseCase = searchVocabularyUseCase
        self.vocabularyCatalogViewModel = vocabularyCatalogViewModel
    }

    func updateSearchQuery(_ query: String) {
        searchResults = searchVocabularyUseCase.execute(
            query: query,
            in: vocabularyCatalogViewModel.availableBooks
        )
    }
}
