import Foundation

protocol ManageStudySessionUseCaseProtocol: Sendable {
    func beginSession(with words: [VocabularyWord], shouldShuffleWords: Bool) -> StudySessionState
    func markWordAsKnown(in sessionState: StudySessionState) -> StudySessionState
    func markWordForReview(in sessionState: StudySessionState) -> StudySessionState
    func revealDetails(in sessionState: StudySessionState) -> StudySessionState
}

struct ManageStudySessionUseCase: ManageStudySessionUseCaseProtocol {
    func beginSession(with words: [VocabularyWord], shouldShuffleWords: Bool) -> StudySessionState {
        var selectedWords = words
        if shouldShuffleWords {
            selectedWords.shuffle()
        }

        return StudySessionState(
            wordQueue: selectedWords,
            currentWordIndex: 0,
            reviewedWordCount: 0,
            areDetailsRevealed: false
        )
    }

    func markWordAsKnown(in sessionState: StudySessionState) -> StudySessionState {
        advanceToNextWord(from: sessionState)
    }

    func markWordForReview(in sessionState: StudySessionState) -> StudySessionState {
        guard let currentWord = sessionState.currentWord else { return sessionState }

        var updatedQueue = sessionState.wordQueue
        updatedQueue.append(currentWord)

        var updatedState = sessionState
        updatedState = StudySessionState(
            wordQueue: updatedQueue,
            currentWordIndex: sessionState.currentWordIndex,
            reviewedWordCount: sessionState.reviewedWordCount,
            areDetailsRevealed: sessionState.areDetailsRevealed
        )
        return advanceToNextWord(from: updatedState)
    }

    func revealDetails(in sessionState: StudySessionState) -> StudySessionState {
        StudySessionState(
            wordQueue: sessionState.wordQueue,
            currentWordIndex: sessionState.currentWordIndex,
            reviewedWordCount: sessionState.reviewedWordCount,
            areDetailsRevealed: true
        )
    }

    private func advanceToNextWord(from sessionState: StudySessionState) -> StudySessionState {
        let nextIndex = sessionState.currentWordIndex + 1 < sessionState.wordQueue.count
            ? sessionState.currentWordIndex + 1
            : sessionState.currentWordIndex

        return StudySessionState(
            wordQueue: sessionState.wordQueue,
            currentWordIndex: nextIndex,
            reviewedWordCount: sessionState.reviewedWordCount + 1,
            areDetailsRevealed: false
        )
    }
}
