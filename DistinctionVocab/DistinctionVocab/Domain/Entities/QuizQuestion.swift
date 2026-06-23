import Foundation

struct QuizQuestion: Identifiable, Sendable {
    let word: VocabularyWord
    let mode: QuizMode
    let choices: [String]
    let correctChoiceIndex: Int

    var id: String { "\(word.id)-\(mode.rawValue)" }

    var promptText: String? {
        switch mode {
        case .englishToJapanese:
            return word.headword
        case .japaneseToEnglish:
            return word.displayJapaneseMeaning
        case .audioToHeadword:
            return nil
        }
    }

    var correctChoice: String {
        choices[correctChoiceIndex]
    }
}
