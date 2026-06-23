import SwiftUI

private enum StudyPage: String, CaseIterable, Identifiable {
    case flashcards
    case quiz

    var id: String { rawValue }

    var title: String {
        switch self {
        case .flashcards:
            return "学習"
        case .quiz:
            return "テスト"
        }
    }
}

struct StudyView: View {
    @Bindable var viewModel: StudyViewModel
    @Bindable var vocabularyCatalogViewModel: VocabularyCatalogViewModel
    @Bindable var quizViewModel: QuizViewModel
    @Environment(AVAudioPlaybackService.self) private var audioPlaybackService
    @State private var selectedPage = StudyPage.flashcards

    var body: some View {
        NavigationStack {
            VStack(spacing: 0) {
                Picker("モード", selection: $selectedPage) {
                    ForEach(StudyPage.allCases) { page in
                        Text(page.title).tag(page)
                    }
                }
                .pickerStyle(.segmented)
                .padding(.horizontal)
                .padding(.vertical, 8)

                TabView(selection: $selectedPage) {
                    flashcardContent
                        .tag(StudyPage.flashcards)

                    QuizView(
                        viewModel: quizViewModel,
                        availableBooks: vocabularyCatalogViewModel.availableBooks
                    )
                    .tag(StudyPage.quiz)
                }
                .tabViewStyle(.page(indexDisplayMode: .never))
            }
            .navigationTitle("学習")
            .tint(DistinctionTheme.accent)
            .onDisappear {
                audioPlaybackService.stop()
            }
        }
    }

    @ViewBuilder
    private var flashcardContent: some View {
        Group {
            if viewModel.hasSessionStarted,
               let currentWord = viewModel.currentWord,
               !viewModel.isSessionComplete {
                studyCard(for: currentWord)
            } else if viewModel.hasSessionStarted, viewModel.isSessionComplete {
                sessionCompletionView
            } else {
                sessionSetupView
            }
        }
    }

    private var sessionSetupView: some View {
        Form {
            Section("ブック") {
                Picker("ブック", selection: $viewModel.selectedBook) {
                    Text("選択してください").tag(Optional<VocabularyBook>.none)
                    ForEach(vocabularyCatalogViewModel.availableBooks) { book in
                        Text(book.title).tag(Optional(book))
                    }
                }
            }

            Section("今日の学習数") {
                Stepper("\(viewModel.dailyWordGoal) 語", value: $viewModel.dailyWordGoal, in: 5...50, step: 5)
            }

            Section {
                Button("学習を開始") {
                    viewModel.startSession()
                }
                .disabled(viewModel.selectedBook == nil)
            }
        }
    }

    private func studyCard(for word: VocabularyWord) -> some View {
        VStack(spacing: 0) {
            HStack {
                Text(viewModel.progressDescription)
                    .font(.caption.monospacedDigit())
                    .foregroundStyle(.secondary)
                Spacer()
                Text(viewModel.selectedBook?.title ?? "")
                    .font(.caption)
                    .foregroundStyle(.secondary)
            }
            .padding(.horizontal, 20)
            .padding(.top, 12)

            ScrollView {
                VStack(spacing: 16) {
                    if !viewModel.areDetailsRevealed {
                        Text("タップして意味と例文を表示")
                            .font(.caption)
                            .foregroundStyle(.tertiary)
                    }

                    DistinctionWordPanel(
                        word: word,
                        showsDetails: viewModel.areDetailsRevealed,
                        showsExamples: viewModel.areDetailsRevealed,
                        alignment: .leading
                    )
                }
                .padding(20)
                .frame(maxWidth: .infinity, alignment: .leading)
                .contentShape(Rectangle())
                .onTapGesture {
                    if !viewModel.areDetailsRevealed {
                        viewModel.revealDetails()
                    }
                }
            }

            if viewModel.areDetailsRevealed {
                ratingButtons
            }
        }
        .background(Color(.systemBackground))
        .onAppear {
            audioPlaybackService.play(resource: word.headwordAudioResource)
        }
        .onChange(of: word.id) { _, _ in
            audioPlaybackService.play(resource: word.headwordAudioResource)
        }
    }

    private var ratingButtons: some View {
        HStack(spacing: 12) {
            ratingButton(.easy, color: DistinctionTheme.easy)
            ratingButton(.good, color: DistinctionTheme.good)
            ratingButton(.hard, color: DistinctionTheme.hard)
        }
        .padding(.horizontal, 20)
        .padding(.vertical, 16)
        .background(
            Rectangle()
                .fill(.bar)
                .shadow(color: .black.opacity(0.06), radius: 8, y: -2)
                .ignoresSafeArea(edges: .bottom)
        )
    }

    private func ratingButton(_ rating: StudyRating, color: Color) -> some View {
        Button {
            viewModel.rateCurrentWord(as: rating)
        } label: {
            Text(rating.title)
                .font(.headline)
                .frame(maxWidth: .infinity)
                .padding(.vertical, 14)
        }
        .buttonStyle(.borderedProminent)
        .tint(color)
    }

    private var sessionCompletionView: some View {
        ContentUnavailableView {
            Label("お疲れさまでした", systemImage: "checkmark.seal.fill")
        } description: {
            Text("\(viewModel.reviewedWordCount) 語の学習が完了しました")
        } actions: {
            Button("もう一度") {
                viewModel.resetSession()
            }
            .buttonStyle(.borderedProminent)
            .tint(DistinctionTheme.accent)
        }
    }
}
