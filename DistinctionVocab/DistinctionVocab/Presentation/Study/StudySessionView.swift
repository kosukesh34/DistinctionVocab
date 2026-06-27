import SwiftUI

struct StudySessionView: View {
    @Bindable var viewModel: StudyViewModel
    @Bindable var vocabularyCatalogViewModel: VocabularyCatalogViewModel
    @Environment(AVAudioPlaybackService.self) private var audioPlaybackService
    @Environment(\.dismiss) private var dismiss
    @State private var areDetailsVisible = false
    @State private var isBookmarked = false

    var body: some View {
        Group {
            if viewModel.hasSessionStarted,
               let currentWord = viewModel.currentWord,
               !viewModel.isSessionComplete {
                activeStudyView(for: currentWord)
            } else if viewModel.hasSessionStarted, viewModel.isSessionComplete {
                completionView
            } else {
                setupView
            }
        }
        .background(DistinctionTheme.listBackground)
        .navigationTitle(viewModel.selectedBook?.title ?? "学習")
        .navigationBarTitleDisplayMode(.inline)
        .navigationBarBackButtonHidden(viewModel.hasSessionStarted && !viewModel.isSessionComplete)
        .toolbar {
            if viewModel.hasSessionStarted && !viewModel.isSessionComplete {
                ToolbarItem(placement: .topBarLeading) {
                    Button("終了") {
                        viewModel.resetSession()
                        dismiss()
                    }
                    .foregroundStyle(DistinctionTheme.accent)
                }
            }
        }
        .onDisappear {
            audioPlaybackService.stop()
        }
    }

    private var setupView: some View {
        VStack(spacing: 24) {
            if let book = viewModel.selectedBook {
                BookCoverView(book: book, size: .large)
            }

            VStack(spacing: 8) {
                Text(viewModel.selectedBook?.title ?? "")
                    .font(.title2.bold())

                Text("\(viewModel.dailyWordGoal) 語の学習を開始します")
                    .font(.subheadline)
                    .foregroundStyle(.secondary)
            }

            Button {
                viewModel.startSession()
                areDetailsVisible = false
            } label: {
                Text("学習を開始")
                    .font(.headline)
                    .foregroundStyle(.white)
                    .frame(maxWidth: .infinity)
                    .padding(.vertical, 16)
                    .background(
                        RoundedRectangle(cornerRadius: 14, style: .continuous)
                            .fill(DistinctionTheme.accent)
                    )
            }
            .padding(.horizontal, 32)
        }
        .frame(maxWidth: .infinity, maxHeight: .infinity)
    }

    private func activeStudyView(for word: VocabularyWord) -> some View {
        VStack(spacing: 0) {
            progressHeader

            ScrollView {
                VStack(spacing: DistinctionTheme.Spacing.lg) {
                    if !areDetailsVisible {
                        Label("タップして意味と例文を表示", systemImage: "hand.tap.fill")
                            .font(.caption.weight(.medium))
                            .foregroundStyle(DistinctionTheme.accent)
                            .padding(.horizontal, DistinctionTheme.Spacing.md)
                            .padding(.vertical, 6)
                            .background(Capsule().fill(DistinctionTheme.accentSoft))
                    }

                    DistinctionWordPanel(
                        word: word,
                        showsDetails: areDetailsVisible,
                        showsExamples: areDetailsVisible,
                        alignment: .leading
                    )
                }
                .padding(.horizontal, 20)
                .padding(.top, 8)
                .padding(.bottom, 20)
                .frame(maxWidth: .infinity, alignment: .leading)
                .contentShape(Rectangle())
                .onTapGesture {
                    if !areDetailsVisible {
                        withAnimation(.easeInOut(duration: 0.2)) {
                            areDetailsVisible = true
                            viewModel.revealDetails()
                        }
                    }
                }
            }

            if areDetailsVisible {
                DistinctionRatingBar { rating in
                    areDetailsVisible = false
                    isBookmarked = false
                    viewModel.rateCurrentWord(as: rating)
                }
            } else {
                StudyBottomToolbar(
                    areDetailsVisible: $areDetailsVisible,
                    isBookmarked: $isBookmarked,
                    onPlayAll: { playAllAudio(for: word) },
                    isPlayingAll: audioPlaybackService.isPlaying
                )
            }
        }
        .onAppear {
            audioPlaybackService.play(resource: word.headwordAudioResource)
        }
        .onChange(of: word.id) { _, _ in
            areDetailsVisible = false
            isBookmarked = false
            audioPlaybackService.play(resource: word.headwordAudioResource)
        }
        .onChange(of: areDetailsVisible) { _, isVisible in
            if isVisible {
                viewModel.revealDetails()
            }
        }
    }

    private var progressHeader: some View {
        VStack(spacing: 8) {
            HStack {
                Text(viewModel.progressDescription)
                    .font(.caption.monospacedDigit().weight(.semibold))
                    .foregroundStyle(.secondary)
                Spacer()
                if let book = viewModel.selectedBook {
                    Text(book.title)
                        .font(.caption)
                        .foregroundStyle(.secondary)
                }
            }

            GeometryReader { proxy in
                ZStack(alignment: .leading) {
                    Capsule()
                        .fill(Color(.systemGray5))
                    Capsule()
                        .fill(DistinctionTheme.accent)
                        .frame(width: proxy.size.width * sessionProgress)
                        .animation(.easeInOut, value: sessionProgress)
                }
            }
            .frame(height: 4)
        }
        .padding(.horizontal, DistinctionTheme.Spacing.xl)
        .padding(.vertical, DistinctionTheme.Spacing.md)
        .background(DistinctionTheme.listBackground)
        .overlay(alignment: .bottom) {
            Rectangle().fill(DistinctionTheme.hairline).frame(height: 0.5)
        }
    }

    private var sessionProgress: CGFloat {
        let goal = max(1, viewModel.dailyWordGoal)
        return min(1, CGFloat(viewModel.reviewedWordCount) / CGFloat(goal))
    }

    private var completionView: some View {
        VStack(spacing: 24) {
            Image(systemName: "checkmark.seal.fill")
                .font(.system(size: 64))
                .foregroundStyle(DistinctionTheme.accent)
                .symbolEffect(.bounce, value: viewModel.isSessionComplete)

            VStack(spacing: 8) {
                Text("お疲れさまでした")
                    .font(.title2.bold())

                Text("\(viewModel.reviewedWordCount) 語の学習が完了しました")
                    .font(.subheadline)
                    .foregroundStyle(.secondary)
            }

            Button {
                viewModel.resetSession()
                dismiss()
            } label: {
                Text("Today に戻る")
                    .font(.headline)
                    .foregroundStyle(.white)
                    .frame(maxWidth: .infinity)
                    .padding(.vertical, 16)
                    .background(
                        RoundedRectangle(cornerRadius: 14, style: .continuous)
                            .fill(DistinctionTheme.accent)
                    )
            }
            .padding(.horizontal, 32)
        }
        .frame(maxWidth: .infinity, maxHeight: .infinity)
    }

    private func playAllAudio(for word: VocabularyWord) {
        if audioPlaybackService.isPlaying {
            audioPlaybackService.stop()
        } else {
            audioPlaybackService.play(resource: word.headwordAudioResource)
        }
    }
}
