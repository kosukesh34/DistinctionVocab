import Foundation

struct ExampleSentence: Identifiable, Hashable, Sendable {
    let label: String
    let audioResource: AudioResourceReference
    let text: String?
    let japaneseTranslation: String?

    var id: String { audioResource.relativePath }

    var displayText: String {
        if let text, !text.isEmpty {
            return text
        }
        return "例文 \(label)"
    }

    var displayJapaneseTranslation: String? {
        guard let japaneseTranslation, !japaneseTranslation.isEmpty else { return nil }
        return japaneseTranslation
    }
}
