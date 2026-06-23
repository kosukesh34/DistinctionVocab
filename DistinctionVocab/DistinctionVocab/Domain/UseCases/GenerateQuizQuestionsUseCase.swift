import Foundation

protocol GenerateQuizQuestionsUseCaseProtocol: Sendable {
    func execute(
        from words: [VocabularyWord],
        questionCount: Int,
        mode: QuizMode
    ) -> [QuizQuestion]
}

struct GenerateQuizQuestionsUseCase: GenerateQuizQuestionsUseCaseProtocol {
    private let choiceCount = 4

    func execute(
        from words: [VocabularyWord],
        questionCount: Int,
        mode: QuizMode
    ) -> [QuizQuestion] {
        let eligibleWords = words.filter { isEligible($0, for: mode) }
        guard eligibleWords.count >= choiceCount else { return [] }

        let selectedWords = Array(eligibleWords.shuffled().prefix(questionCount))
        return selectedWords.compactMap { word in
            buildQuestion(for: word, from: eligibleWords, mode: mode)
        }
    }

    private func isEligible(_ word: VocabularyWord, for mode: QuizMode) -> Bool {
        switch mode {
        case .englishToJapanese, .japaneseToEnglish:
            return word.displayJapaneseMeaning != nil
        case .audioToHeadword:
            return true
        }
    }

    private func buildQuestion(
        for word: VocabularyWord,
        from pool: [VocabularyWord],
        mode: QuizMode
    ) -> QuizQuestion? {
        guard let correctChoice = choiceText(for: word, mode: mode) else { return nil }

        var distractors = pool
            .filter { $0.id != word.id }
            .compactMap { choiceText(for: $0, mode: mode) }
            .filter { $0 != correctChoice }

        distractors = Array(Set(distractors)).shuffled()
        guard distractors.count >= choiceCount - 1 else { return nil }

        var choices = Array(distractors.prefix(choiceCount - 1))
        choices.append(correctChoice)
        choices.shuffle()

        guard let correctIndex = choices.firstIndex(of: correctChoice) else { return nil }

        return QuizQuestion(
            word: word,
            mode: mode,
            choices: choices,
            correctChoiceIndex: correctIndex
        )
    }

    private func choiceText(for word: VocabularyWord, mode: QuizMode) -> String? {
        switch mode {
        case .englishToJapanese:
            return word.displayJapaneseMeaning
        case .japaneseToEnglish, .audioToHeadword:
            return word.headword
        }
    }
}
