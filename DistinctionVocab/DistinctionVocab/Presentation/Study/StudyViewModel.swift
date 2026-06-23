import Foundation
import Observation

@MainActor
@Observable
final class StudyViewModel {
    private(set) var sessionState: StudySessionState = .empty
    private(set) var hasSessionStarted = false

    var selectedBook: VocabularyBook?
    var dailyWordGoal = 20

    private let manageStudySessionUseCase: ManageStudySessionUseCaseProtocol

    init(manageStudySessionUseCase: ManageStudySessionUseCaseProtocol) {
        self.manageStudySessionUseCase = manageStudySessionUseCase
    }

    var currentWord: VocabularyWord? {
        sessionState.currentWord
    }

    var progressDescription: String {
        sessionState.progressDescription
    }

    var isSessionComplete: Bool {
        sessionState.isSessionComplete
    }

    var areDetailsRevealed: Bool {
        sessionState.areDetailsRevealed
    }

    var reviewedWordCount: Int {
        sessionState.reviewedWordCount
    }

    func startSession() {
        guard let selectedBook else { return }

        let wordsForToday = Array(selectedBook.words.prefix(dailyWordGoal))
        sessionState = manageStudySessionUseCase.beginSession(
            with: wordsForToday,
            shouldShuffleWords: true
        )
        hasSessionStarted = true
    }

    func revealDetails() {
        sessionState = manageStudySessionUseCase.revealDetails(in: sessionState)
    }

    func rateCurrentWord(as rating: StudyRating) {
        switch rating {
        case .easy, .good:
            sessionState = manageStudySessionUseCase.markWordAsKnown(in: sessionState)
        case .hard:
            sessionState = manageStudySessionUseCase.markWordForReview(in: sessionState)
        }
    }

    func resetSession() {
        sessionState = .empty
        hasSessionStarted = false
    }
}
