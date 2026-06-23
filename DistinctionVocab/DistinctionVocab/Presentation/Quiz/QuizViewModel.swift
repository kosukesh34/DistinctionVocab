import Foundation
import Observation

@MainActor
@Observable
final class QuizViewModel {
    private(set) var questions: [QuizQuestion] = []
    private(set) var currentQuestionIndex = 0
    private(set) var correctAnswerCount = 0
    private(set) var hasSessionStarted = false
    private(set) var selectedChoiceIndex: Int?
    private(set) var hasAnsweredCurrentQuestion = false

    var selectedBook: VocabularyBook?
    var questionCount = 10
    var quizMode: QuizMode = .englishToJapanese

    private let generateQuizQuestionsUseCase: GenerateQuizQuestionsUseCaseProtocol

    init(generateQuizQuestionsUseCase: GenerateQuizQuestionsUseCaseProtocol) {
        self.generateQuizQuestionsUseCase = generateQuizQuestionsUseCase
    }

    var currentQuestion: QuizQuestion? {
        guard currentQuestionIndex < questions.count else { return nil }
        return questions[currentQuestionIndex]
    }

    var progressDescription: String {
        guard !questions.isEmpty else { return "0 / 0" }
        return "\(min(currentQuestionIndex + 1, questions.count)) / \(questions.count)"
    }

    var isSessionComplete: Bool {
        hasSessionStarted && currentQuestionIndex >= questions.count && !questions.isEmpty
    }

    var scoreDescription: String {
        "\(correctAnswerCount) / \(questions.count) 正解"
    }

    var canStartSession: Bool {
        guard let selectedBook else { return false }
        return generateQuizQuestionsUseCase.execute(
            from: selectedBook.words,
            questionCount: 1,
            mode: quizMode
        ).isEmpty == false
    }

    func startSession() {
        guard let selectedBook else { return }

        questions = generateQuizQuestionsUseCase.execute(
            from: selectedBook.words,
            questionCount: questionCount,
            mode: quizMode
        )
        currentQuestionIndex = 0
        correctAnswerCount = 0
        selectedChoiceIndex = nil
        hasAnsweredCurrentQuestion = false
        hasSessionStarted = !questions.isEmpty
    }

    func selectChoice(at index: Int) {
        guard !hasAnsweredCurrentQuestion,
              let currentQuestion,
              index < currentQuestion.choices.count else { return }

        selectedChoiceIndex = index
        hasAnsweredCurrentQuestion = true

        if index == currentQuestion.correctChoiceIndex {
            correctAnswerCount += 1
        }
    }

    func advanceToNextQuestion() {
        guard hasAnsweredCurrentQuestion else { return }

        currentQuestionIndex += 1
        selectedChoiceIndex = nil
        hasAnsweredCurrentQuestion = false
    }

    func resetSession() {
        questions = []
        currentQuestionIndex = 0
        correctAnswerCount = 0
        selectedChoiceIndex = nil
        hasAnsweredCurrentQuestion = false
        hasSessionStarted = false
    }

    func configure(book: VocabularyBook) {
        selectedBook = book
        resetSession()
    }
}
