import Foundation

protocol BundleVocabularyDataSourceProtocol: Sendable {
    func loadCatalogDTO() throws -> VocabularyCatalogDTO
}

struct BundleVocabularyDataSource: BundleVocabularyDataSourceProtocol {
    private let bundle: Bundle
    private let catalogFileName: String

    init(bundle: Bundle = .main, catalogFileName: String = "vocabulary") {
        self.bundle = bundle
        self.catalogFileName = catalogFileName
    }

    func loadCatalogDTO() throws -> VocabularyCatalogDTO {
        guard let catalogURL = bundle.url(forResource: catalogFileName, withExtension: "json") else {
            throw VocabularyDataError.catalogFileNotFound
        }

        let catalogData = try Data(contentsOf: catalogURL)
        return try JSONDecoder().decode(VocabularyCatalogDTO.self, from: catalogData)
    }
}

enum VocabularyDataError: LocalizedError {
    case catalogFileNotFound

    var errorDescription: String? {
        switch self {
        case .catalogFileNotFound:
            return "vocabulary.json が見つかりません"
        }
    }
}
