import Foundation

enum QuizMode: String, CaseIterable, Identifiable, Sendable {
    case englishToJapanese
    case japaneseToEnglish
    case audioToHeadword

    var id: String { rawValue }

    var title: String {
        switch self {
        case .englishToJapanese:
            return "英語 → 日本語"
        case .japaneseToEnglish:
            return "日本語 → 英語"
        case .audioToHeadword:
            return "音声 → 英語"
        }
    }

    var promptDescription: String {
        switch self {
        case .englishToJapanese:
            return "意味に合う日本語訳を選んでください"
        case .japaneseToEnglish:
            return "意味に合う英単語を選んでください"
        case .audioToHeadword:
            return "音声を聞いて英単語を選んでください"
        }
    }
}
