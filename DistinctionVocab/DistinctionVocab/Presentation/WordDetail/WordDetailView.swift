import SwiftUI

struct WordDetailView: View {
    let viewModel: WordDetailViewModel
    @Environment(AVAudioPlaybackService.self) private var audioPlaybackService
    @State private var areDetailsVisible = true
    @State private var isBookmarked = false

    var body: some View {
        VStack(spacing: 0) {
            ScrollView {
                VStack(alignment: .leading, spacing: DistinctionTheme.Spacing.lg) {
                    Text(viewModel.bookTitle)
                        .font(.caption.weight(.semibold))
                        .foregroundStyle(DistinctionTheme.accent)
                        .padding(.horizontal, 10)
                        .padding(.vertical, 4)
                        .background(Capsule().fill(DistinctionTheme.accentSoft))

                    DistinctionWordPanel(
                        word: viewModel.word,
                        showsDetails: areDetailsVisible,
                        showsExamples: areDetailsVisible,
                        alignment: .leading
                    )
                }
                .padding(.horizontal, DistinctionTheme.Spacing.xl)
                .padding(.top, DistinctionTheme.Spacing.md)
                .padding(.bottom, DistinctionTheme.Spacing.xl)
                .frame(maxWidth: .infinity, alignment: .leading)
            }

            StudyBottomToolbar(
                areDetailsVisible: $areDetailsVisible,
                isBookmarked: $isBookmarked,
                onPlayAll: { playAllAudio() },
                isPlayingAll: audioPlaybackService.isPlaying
            )
        }
        .background(DistinctionTheme.listBackground)
        .navigationTitle(viewModel.word.headword)
        .navigationBarTitleDisplayMode(.inline)
        .onDisappear {
            audioPlaybackService.stop()
        }
    }

    private func playAllAudio() {
        if audioPlaybackService.isPlaying {
            audioPlaybackService.stop()
        } else {
            audioPlaybackService.play(resource: viewModel.word.headwordAudioResource)
        }
    }
}
