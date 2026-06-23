import SwiftUI

struct WordDetailView: View {
    let viewModel: WordDetailViewModel
    @Environment(AVAudioPlaybackService.self) private var audioPlaybackService

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 20) {
                Text(viewModel.bookTitle)
                    .font(.caption.weight(.semibold))
                    .foregroundStyle(.secondary)
                    .textCase(.uppercase)

                DistinctionWordPanel(
                    word: viewModel.word,
                    showsDetails: true,
                    showsExamples: true,
                    alignment: .leading
                )
            }
            .padding(20)
            .frame(maxWidth: .infinity, alignment: .leading)
        }
        .background(Color(.systemBackground))
        .navigationTitle(viewModel.word.headword)
        .navigationBarTitleDisplayMode(.inline)
        .onDisappear {
            audioPlaybackService.stop()
        }
    }
}
