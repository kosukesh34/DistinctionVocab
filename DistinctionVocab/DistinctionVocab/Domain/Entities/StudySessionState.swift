import Foundation

struct StudySessionState: Equatable, Sendable {
    let wordQueue: [VocabularyWord]
    let currentWordIndex: Int
    let reviewedWordCount: Int
    let areDetailsRevealed: Bool

    static let empty = StudySessionState(
        wordQueue: [],
        currentWordIndex: 0,
        reviewedWordCount: 0,
        areDetailsRevealed: false
    )

    var currentWord: VocabularyWord? {
        guard currentWordIndex < wordQueue.count else { return nil }
        return wordQueue[currentWordIndex]
    }

    var progressDescription: String {
        guard !wordQueue.isEmpty else { return "0 / 0" }
        let displayedPosition = min(currentWordIndex + 1, wordQueue.count)
        return "\(displayedPosition) / \(wordQueue.count)"
    }

    var isSessionComplete: Bool {
        !wordQueue.isEmpty
            && currentWordIndex >= wordQueue.count - 1
            && reviewedWordCount >= wordQueue.count
    }
}
