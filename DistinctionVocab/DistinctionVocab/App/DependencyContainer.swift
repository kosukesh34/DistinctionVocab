import SwiftUI

@MainActor
final class DependencyContainer {
    let vocabularyCatalogViewModel: VocabularyCatalogViewModel
    let searchViewModel: SearchViewModel
    let studyViewModel: StudyViewModel
    let quizViewModel: QuizViewModel
    let audioPlaybackService: AVAudioPlaybackService

    init() {
        let vocabularyDataSource = BundleVocabularyDataSource()
        let vocabularyRepository = BundleVocabularyRepository(dataSource: vocabularyDataSource)
        let audioResourceRepository = BundleAudioResourceRepository()

        let loadVocabularyUseCase = LoadVocabularyUseCase(vocabularyRepository: vocabularyRepository)
        let searchVocabularyUseCase = SearchVocabularyUseCase()
        let manageStudySessionUseCase = ManageStudySessionUseCase()
        let generateQuizQuestionsUseCase = GenerateQuizQuestionsUseCase()

        vocabularyCatalogViewModel = VocabularyCatalogViewModel(
            loadVocabularyUseCase: loadVocabularyUseCase
        )
        searchViewModel = SearchViewModel(
            searchVocabularyUseCase: searchVocabularyUseCase,
            vocabularyCatalogViewModel: vocabularyCatalogViewModel
        )
        studyViewModel = StudyViewModel(
            manageStudySessionUseCase: manageStudySessionUseCase
        )
        quizViewModel = QuizViewModel(
            generateQuizQuestionsUseCase: generateQuizQuestionsUseCase
        )
        audioPlaybackService = AVAudioPlaybackService(
            audioResourceRepository: audioResourceRepository
        )
    }

    func makeWordDetailViewModel(word: VocabularyWord, bookTitle: String) -> WordDetailViewModel {
        WordDetailViewModel(
            word: word,
            bookTitle: bookTitle
        )
    }
}
