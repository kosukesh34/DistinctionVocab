import SwiftUI

struct QuizView: View {
    @Bindable var viewModel: QuizViewModel
    var showsBookPicker = true
    var availableBooks: [VocabularyBook] = []
    @Environment(AVAudioPlaybackService.self) private var audioPlaybackService

    var body: some View {
        Group {
            if viewModel.hasSessionStarted,
               let currentQuestion = viewModel.currentQuestion,
               !viewModel.isSessionComplete {
                questionView(for: currentQuestion)
            } else if viewModel.hasSessionStarted, viewModel.isSessionComplete {
                completionView
            } else {
                setupView
            }
        }
        .onDisappear {
            audioPlaybackService.stop()
        }
    }

    private var setupView: some View {
        Form {
            if showsBookPicker {
                Section("ブック") {
                    Picker("ブック", selection: $viewModel.selectedBook) {
                        Text("選択してください").tag(Optional<VocabularyBook>.none)
                        ForEach(availableBooks) { book in
                            Text(book.title).tag(Optional(book))
                        }
                    }
                }
            }

            Section("出題形式") {
                Picker("形式", selection: $viewModel.quizMode) {
                    ForEach(QuizMode.allCases) { mode in
                        Text(mode.title).tag(mode)
                    }
                }
                .pickerStyle(.segmented)
            }

            Section("問題数") {
                Stepper("\(viewModel.questionCount) 問", value: $viewModel.questionCount, in: 5...30, step: 5)
            }

            Section {
                Text(viewModel.quizMode.promptDescription)
                    .font(.subheadline)
                    .foregroundStyle(.secondary)
            }

            Section {
                Button("テストを開始") {
                    viewModel.startSession()
                }
                .disabled(!viewModel.canStartSession)
            }
        }
    }

    private func questionView(for question: QuizQuestion) -> some View {
        VStack(spacing: 24) {
            HStack {
                Text(viewModel.progressDescription)
                    .font(.caption.monospacedDigit())
                    .foregroundStyle(.secondary)
                Spacer()
                Text(question.mode.title)
                    .font(.caption)
                    .foregroundStyle(.secondary)
            }
            .padding(.horizontal)

            Spacer()

            VStack(spacing: 20) {
                if question.mode == .audioToHeadword {
                    AudioPlayButton(
                        audioResource: question.word.headwordAudioResource,
                        iconSize: 64
                    )
                    if let phonetic = question.word.displayPhonetic {
                        PhoneticText(phonetic: phonetic)
                            .opacity(0.35)
                    }
                } else if let promptText = question.promptText {
                    Text(promptText)
                        .font(.system(.title, design: .serif, weight: .bold))
                        .multilineTextAlignment(.center)
                        .padding(.horizontal)

                    if question.mode == .japaneseToEnglish,
                       let phonetic = question.word.displayPhonetic {
                        PhoneticText(phonetic: phonetic)
                            .opacity(0.35)
                    }
                }

                VStack(spacing: 12) {
                    ForEach(Array(question.choices.enumerated()), id: \.offset) { index, choice in
                        choiceButton(choice: choice, index: index, question: question)
                    }
                }
                .padding(.horizontal)
            }
            .padding(24)
            .frame(maxWidth: .infinity)
            .background(
                RoundedRectangle(cornerRadius: 24, style: .continuous)
                    .fill(Color(.secondarySystemGroupedBackground))
            )
            .padding(.horizontal)

            Spacer()

            if viewModel.hasAnsweredCurrentQuestion {
                VStack(spacing: 12) {
                    if let selectedIndex = viewModel.selectedChoiceIndex {
                        let isCorrect = selectedIndex == question.correctChoiceIndex
                        Label(
                            isCorrect ? "正解！" : "不正解",
                            systemImage: isCorrect ? "checkmark.circle.fill" : "xmark.circle.fill"
                        )
                        .font(.headline)
                        .foregroundStyle(isCorrect ? .green : .red)

                        if !isCorrect {
                            Text("正解: \(question.correctChoice)")
                                .font(.subheadline)
                                .foregroundStyle(.secondary)
                        }
                    }

                    Button("次の問題") {
                        viewModel.advanceToNextQuestion()
                    }
                    .buttonStyle(.borderedProminent)
                }
                .padding(.horizontal)
                .padding(.bottom)
            }
        }
        .background(Color(.systemGroupedBackground))
    }

    private func choiceButton(choice: String, index: Int, question: QuizQuestion) -> some View {
        Button {
            viewModel.selectChoice(at: index)
        } label: {
            HStack {
                Text(choice)
                    .multilineTextAlignment(.leading)
                    .foregroundStyle(choiceForegroundColor(index: index, question: question))
                Spacer()
            }
            .padding()
            .frame(maxWidth: .infinity, alignment: .leading)
            .background(
                RoundedRectangle(cornerRadius: 12, style: .continuous)
                    .fill(choiceBackgroundColor(index: index, question: question))
            )
        }
        .disabled(viewModel.hasAnsweredCurrentQuestion)
    }

    private func choiceBackgroundColor(index: Int, question: QuizQuestion) -> Color {
        guard viewModel.hasAnsweredCurrentQuestion else {
            return Color(.tertiarySystemGroupedBackground)
        }

        if index == question.correctChoiceIndex {
            return Color.green.opacity(0.2)
        }
        if index == viewModel.selectedChoiceIndex {
            return Color.red.opacity(0.2)
        }
        return Color(.tertiarySystemGroupedBackground)
    }

    private func choiceForegroundColor(index: Int, question: QuizQuestion) -> Color {
        guard viewModel.hasAnsweredCurrentQuestion else {
            return Color.primary
        }

        if index == question.correctChoiceIndex {
            return .green
        }
        if index == viewModel.selectedChoiceIndex {
            return .red
        }
        return .secondary
    }

    private var completionView: some View {
        ContentUnavailableView {
            Label("テスト完了", systemImage: "flag.checkered")
        } description: {
            Text(viewModel.scoreDescription)
        } actions: {
            Button("もう一度") {
                viewModel.resetSession()
            }
            .buttonStyle(.borderedProminent)
        }
    }
}
